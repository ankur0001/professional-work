#!/usr/bin/env bash
# Rebuild all v2 videos with animated visuals, reusing remote narration audio.
set -euo pipefail
cd /workspace
MAP_PY='java-story/v2/video_build/distribute_v2_to_episode_prs.py'
OUT=java-story/v2
mkdir -p "$OUT"

fetch_episode_assets() {
  local ep=$1
  python3 - <<PY
import re, subprocess
from pathlib import Path
code = open("$MAP_PY").read()
ns = {}
exec(code.split("def run")[0], ns)
ep = $ep
pr, br = ns["PR_MAP"][ep]
OUT = Path("$OUT")
srt = OUT / f"Java_Episode_{ep:02d}.srt"
caps = list(OUT.glob(f"Java_Episode_{ep:02d}_*_CAPTIONED.mp4"))
if srt.exists() and caps:
    print(f"EP{ep:02d}: local assets ok")
    raise SystemExit(0)
print(f"EP{ep:02d}: fetching from {br}")
subprocess.check_call(["git", "fetch", "-q", "origin", br])
sha = subprocess.check_output(["git", "rev-parse", f"origin/{br}"], text=True).strip()
files = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", sha], text=True).splitlines()
# prefer output/v2 then java-story/v2
candidates = [f for f in files if "/v2/" in f and f.endswith((".mp4", ".srt", ".md"))]
want_srt = [f for f in candidates if f.endswith(f"Java_Episode_{ep:02d}.srt")]
want_cap = [f for f in candidates if "CAPTIONED.mp4" in f and f"Java_Episode_{ep:02d}_" in f]
want_clean = [f for f in candidates if f.endswith(".mp4") and "CAPTIONED" not in f and f"Java_Episode_{ep:02d}_" in f]
def pull(path):
    data = subprocess.check_output(["git", "show", f"{sha}:{path}"])
    dest = OUT / Path(path).name
    dest.write_bytes(data)
    print("  pulled", dest.name, len(data))
if want_srt:
    pull(want_srt[0])
if want_cap:
    pull(want_cap[0])
elif want_clean:
    pull(want_clean[0])
else:
    raise SystemExit(f"EP{ep:02d}: no remote v2 media")
PY
}

START=${1:-1}
END=${2:-85}
for ep in $(seq "$START" "$END"); do
  echo "======== EP$(printf '%02d' "$ep") ========"
  fetch_episode_assets "$ep"
  python3 -u java-story/v2/video_build/render_v2_from_narrative.py --ep "$ep" --reuse-audio
  python3 -u java-story/v2/video_build/distribute_v2_to_episode_prs.py --ep "$ep"
  touch "/tmp/v2_anim_distributed_ep${ep}"
done
echo "ANIMATED REBUILD DONE ${START}-${END}"
