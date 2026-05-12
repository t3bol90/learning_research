#!/usr/bin/env bash
# Translate a single image via codex. Idempotent: skips if .zh.<ext> exists.
# Designed for parallel invocation via `xargs -P N`.
set -u
IMG="$1"
LOG="/tmp/codex-image-loop.log"
STEM="${IMG%.*}"
EXT="${IMG##*.}"
ZH="${STEM}.zh.${EXT}"

if [ -f "$ZH" ]; then
  printf '[skip-done] %s\n' "$IMG" >> "$LOG"
  exit 0
fi

printf '[start] %s\n' "$IMG" >> "$LOG"

PROMPT="Translate Chinese text in this image to English while preserving the exact layout, colours, fonts, photos, diagrams, arrows, and any non-text content. Do not redesign.

Image: $IMG

Steps:
1. Look at the image. If it has NO Chinese text (pure photo, English-only, or a chart with no labels), reply exactly 'SKIPPED: no Chinese' and stop — do not call image_gen.
2. If it has Chinese: rename the original to '$ZH', then use your image_gen tool to produce an English version at the same dimensions and save it at $IMG.

Reply with exactly one final line:
SKIPPED: no Chinese
or
TRANSLATED: <new file size>
or
FAILED: <short reason>"

LAST=$(codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox danger-full-access --full-auto --skip-git-repo-check \
  "$PROMPT" 2>&1 | grep -E '^(TRANSLATED|SKIPPED:|FAILED)' | tail -1)

if [ -z "$LAST" ]; then LAST="FAILED: no terminal line"; fi
printf '[%s] %s\n' "$LAST" "$IMG" >> "$LOG"
