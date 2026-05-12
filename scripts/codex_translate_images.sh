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

# xargs -P passes a non-zero exit status from any child to its own exit. The
# per-file script exits 42 when it sees the OpenAI usage-limit error so the
# whole pool can short-circuit instead of burning iterations on doomed retries.
echo "$ALL_IMAGES" | xargs -n 1 -P "$PARALLEL" "$ONE"
RC=$?
if [ "$RC" -eq 42 ] || [ "$RC" -eq 123 ]; then
  echo "=== aborted $(date): codex usage limit reached ===" | tee -a "$LOG"
  exit 42
fi
echo "=== finished $(date) (rc=$RC) ===" | tee -a "$LOG"
