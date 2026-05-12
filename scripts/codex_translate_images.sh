#!/usr/bin/env bash
# Per-file codex image translation loop. Idempotent: skips any image that
# already has a sibling .zh.<ext> (so it's safe to re-run after Ctrl-C).
set -u
LOG="/tmp/codex-image-loop.log"
REPO="/Users/toandoan/Documents/Workspace/learning_research"
cd "$REPO"

ALL_IMAGES=$(find docs -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) ! -iname '*.zh.png' ! -iname '*.zh.jpg' ! -iname '*.zh.jpeg' | sort)
TOTAL=$(echo "$ALL_IMAGES" | wc -l | tr -d ' ')
COUNT=0

echo "=== started $(date) — $TOTAL candidate images ===" | tee -a "$LOG"

for IMG in $ALL_IMAGES; do
  COUNT=$((COUNT+1))
  STEM="${IMG%.*}"
  EXT="${IMG##*.}"
  ZH="${STEM}.zh.${EXT}"

  if [ -f "$ZH" ]; then
    echo "[$COUNT/$TOTAL] SKIP-DONE $IMG" | tee -a "$LOG"
    continue
  fi

  echo "[$COUNT/$TOTAL] PROCESSING $IMG" | tee -a "$LOG"

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

  RESULT=$(codex exec -m gpt-5.4 \
    --config model_reasoning_effort="high" \
    --sandbox danger-full-access --full-auto --skip-git-repo-check \
    "$PROMPT" 2>&1 | tail -8)

  echo "$RESULT" | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

echo "=== finished $(date) ===" | tee -a "$LOG"
