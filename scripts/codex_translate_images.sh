#!/usr/bin/env bash
# Per-file codex image translation loop with configurable parallelism.
# Idempotent: codex_translate_one.sh skips images that already have a .zh.<ext>
# sibling, so this is safe to re-run after Ctrl-C or after a rebuild.
set -u
PARALLEL="${PARALLEL:-8}"
LOG="/tmp/codex-image-loop.log"
REPO="/Users/toandoan/Documents/Workspace/learning_research"
ONE="$REPO/scripts/codex_translate_one.sh"
cd "$REPO"

ALL_IMAGES=$(find docs -type f \( -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' \) ! -iname '*.zh.png' ! -iname '*.zh.jpg' ! -iname '*.zh.jpeg' | sort)
TOTAL=$(echo "$ALL_IMAGES" | wc -l | tr -d ' ')
echo "=== started $(date) — $TOTAL candidate images, parallel=$PARALLEL ===" | tee -a "$LOG"

echo "$ALL_IMAGES" | xargs -n 1 -P "$PARALLEL" "$ONE"

echo "=== finished $(date) ===" | tee -a "$LOG"
