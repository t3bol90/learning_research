#!/usr/bin/env bash
# Translate a single image via codex. Idempotent: skips if .zh.<ext> exists.
# Designed for parallel invocation via `xargs -P N`.
# Truth lives on disk: .zh.<ext> appearing alongside a same-name original
# means "already translated" (or, when bit-identical, "marker for no-chinese").
# We never auto-create a no-chinese marker because rate-limit errors look
# identical to real "no chinese" judgments. Unclear cases are left alone so
# the next run can retry.
set -u
IMG="$1"
LOG="/tmp/codex-image-loop.log"
DEBUG_DIR="/tmp/codex-image-debug"
mkdir -p "$DEBUG_DIR"
STEM="${IMG%.*}"
EXT="${IMG##*.}"
ZH="${STEM}.zh.${EXT}"
SAFE=$(echo "$IMG" | tr '/' '_')
DBG="$DEBUG_DIR/${SAFE}.txt"

if [ -f "$ZH" ]; then
  printf '[skip-done] %s\n' "$IMG" >> "$LOG"
  exit 0
fi

printf '[start] %s\n' "$IMG" >> "$LOG"
PRE_MTIME=$(stat -f %m "$IMG" 2>/dev/null || echo 0)

# We use an out-of-band marker file to detect "no chinese" because codex
# echoes the prompt verbatim, so any literal token in the prompt would also
# appear in stdout regardless of what codex actually said.
MARKER="$DEBUG_DIR/$(echo "$IMG" | tr '/' '_').no-chinese"
rm -f "$MARKER"

PROMPT="Translate Chinese text in this image to English while preserving the exact layout, colours, fonts, photos, diagrams, arrows, and any non-text content. Do not redesign.

Image: $IMG

Steps:
1. Look at the image. If it has NO Chinese text (pure photo, English-only, or a chart with no labels), run the shell command 'touch $MARKER' and stop. Do NOT call image_gen.
2. If it has Chinese: rename the original to '$ZH', then use your image_gen tool to produce an English version at the same dimensions and save it at $IMG.

Then briefly summarise what you did."

codex exec -m "${CODEX_MODEL:-gpt-5.4}" \
  --config model_reasoning_effort="${CODEX_EFFORT:-medium}" \
  --sandbox danger-full-access --full-auto --skip-git-repo-check \
  "$PROMPT" >"$DBG" 2>&1

# Detect the OpenAI usage-limit error so the loop can stop cleanly.
if grep -q 'hit your usage limit' "$DBG"; then
  printf '[quota-exceeded] %s\n' "$IMG" >> "$LOG"
  exit 42  # special exit so the runner can short-circuit
fi

# Classify outcome.
if [ -f "$ZH" ] && [ -f "$IMG" ]; then
  POST_MTIME=$(stat -f %m "$IMG" 2>/dev/null || echo 0)
  if [ "$POST_MTIME" -gt "$PRE_MTIME" ]; then
    SIZE=$(stat -f %z "$IMG")
    printf '[translated %s bytes] %s\n' "$SIZE" "$IMG" >> "$LOG"
    rm -f "$DBG" "$MARKER"
    exit 0
  else
    printf '[failed-no-rewrite] %s (restoring)\n' "$IMG" >> "$LOG"
    rm -f "$IMG" && mv "$ZH" "$IMG"
    exit 0
  fi
fi

if [ -f "$ZH" ] && [ ! -f "$IMG" ]; then
  printf '[failed-stranded] %s (restoring from .zh)\n' "$IMG" >> "$LOG"
  mv "$ZH" "$IMG"
  exit 0
fi

if [ -f "$MARKER" ]; then
  printf '[no-chinese] %s\n' "$IMG" >> "$LOG"
  cp "$IMG" "$ZH"
  rm -f "$DBG" "$MARKER"
  exit 0
fi

# Failure: leave files alone so the next run can retry.
ERR_HINT=$(tail -10 "$DBG" | grep -iE 'error|429|rate|throttle|timeout' | head -1 | head -c 120)
printf '[failed-no-action] %s | %s\n' "$IMG" "${ERR_HINT:-no marker, no rename}" >> "$LOG"
