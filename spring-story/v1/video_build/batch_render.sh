#!/usr/bin/env bash
# Batch-render Spring Story videos with resume support.
# Usage:
#   bash spring-story/v1/video_build/batch_render.sh          # all 112
#   bash spring-story/v1/video_build/batch_render.sh 1 10     # EP01-EP10
#   bash spring-story/v1/video_build/batch_render.sh 5        # EP05 only
set -euo pipefail
cd /workspace
export PATH="$HOME/.local/bin:$PATH"

START=${1:-1}
END=${2:-$START}
if [[ $# -eq 0 ]]; then
  START=1
  END=112
elif [[ $# -eq 1 ]]; then
  END=$START
fi

LOG_DIR=spring-story/v1/video_build/logs
mkdir -p "$LOG_DIR"
DONE_MARKER=$LOG_DIR/completed.txt
touch "$DONE_MARKER"

echo "Batch render Spring Story EP$(printf '%02d' "$START")–EP$(printf '%02d' "$END")"

for ep in $(seq "$START" "$END"); do
  epz=$(printf '%02d' "$ep")
  if grep -qx "$epz" "$DONE_MARKER"; then
    echo "SKIP EP$epz (already marked done)"
    continue
  fi
  # Skip if final captioned mp4 already exists in episode folder
  if ls spring-story/v1/episodes/ep${ep}-*/Spring_Episode_${epz}_*_CAPTIONED.mp4 >/dev/null 2>&1 \
     || ls spring-story/v1/episodes/ep${epz}-*/Spring_Episode_${epz}_*_CAPTIONED.mp4 >/dev/null 2>&1; then
    # ignore PREVIEW
    if ls spring-story/v1/episodes/ep*-*/Spring_Episode_${epz}_*_CAPTIONED.mp4 2>/dev/null | grep -v PREVIEW >/dev/null; then
      echo "SKIP EP$epz (captioned mp4 present)"
      echo "$epz" >> "$DONE_MARKER"
      continue
    fi
  fi
  echo "======== EP$epz $(date -Is) ========"
  if python3 -u spring-story/v1/video_build/render_spring_episode.py --ep "$ep" 2>&1 | tee -a "$LOG_DIR/ep${epz}.log"; then
    echo "$epz" >> "$DONE_MARKER"
  else
    echo "FAIL EP$epz" | tee -a "$LOG_DIR/failures.log"
  fi
done

echo "BATCH DONE $(date -Is)"
