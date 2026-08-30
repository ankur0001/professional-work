#!/usr/bin/env bash
# Re-render all v2 videos with FULL narration (fixes end cut-off).
# Does NOT reuse truncated mp4 audio. Uses beat wavs when complete; else TTS.
set -euo pipefail
cd /workspace
OUT=all-work/java-story/output/v2
mkdir -p "$OUT"
START=${1:-1}
END=${2:-85}
shopt -s nullglob

for ep in $(seq "$START" "$END"); do
  echo "======== EP$(printf '%02d' "$ep") FULL-AUDIO FIX ========"
  aud="all-work/java-story/video_build/v2_work/ep$(printf '%02d' "$ep")/audio"
  if [ -d "$aud" ]; then
    beats=( "$aud"/b*.wav )
    nbeats=${#beats[@]}
    if [ "$nbeats" -eq 0 ]; then
      rm -f "$aud/narration.mp3"
    fi
  fi
  python3 -u all-work/java-story/video_build/render_v2_from_narrative.py --ep "$ep"
  python3 -u all-work/java-story/video_build/distribute_v2_to_episode_prs.py --ep "$ep"
  touch "/tmp/v2_endcut_fixed_ep${ep}"
  python3 - <<PY
from pathlib import Path
import subprocess, re
ep = $ep
out = Path("all-work/java-story/output/v2")
cap = next(p for p in out.glob(f"Java_Episode_{ep:02d}_*_CAPTIONED.mp4") if "PREVIEW" not in p.name)
srt = out / f"Java_Episode_{ep:02d}.srt"

def probe(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
        text=True,
    ))

text = srt.read_text()
last = None
for block in re.split(r"\n\s*\n", text.strip()):
    lines = [ln for ln in block.splitlines() if ln.strip()]
    if not lines:
        continue
    idx = 0 if "-->" in lines[0] else 1
    if idx >= len(lines) or "-->" not in lines[idx]:
        continue
    last = lines[idx].split("-->")[1].strip()
if not last:
    raise SystemExit(f"EP{ep:02d}: could not parse srt end")
h, m, rest = last.split(":")
s, ms = rest.replace(",", ".").split(".")
end = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
vd = probe(cap)
print(f"  verify EP{ep:02d}: video={vd:.2f}s srt_end={end:.2f}s delta={vd-end:.2f}")
if vd + 0.2 < end:
    raise SystemExit(f"EP{ep:02d} still truncated")
PY
done
echo "ENDCUT FIX DONE ${START}-${END}"
