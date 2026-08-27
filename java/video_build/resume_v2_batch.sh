#!/usr/bin/env bash
# Resume v2 video batch after VM wipe: detect remote coverage, render remaining, distribute.
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace

ROOT=/workspace
LOG_DIR=/tmp
RENDER_LOG=$LOG_DIR/render_v2_batch.log
WATCH_LOG=$LOG_DIR/watch_distribute.log

ensure_branch() {
  git fetch origin cursor/java-narrative-coherent-series-0689
  git checkout -B cursor/java-narrative-coherent-series-0689 origin/cursor/java-narrative-coherent-series-0689
}

ensure_deps() {
  python3 -c 'import torch; import chatterbox; import PIL; import soundfile' 2>/dev/null && return 0
  pip3 install --user -q torch --index-url https://download.pytorch.org/whl/cpu
  pip3 install --user -q chatterbox-tts pillow soundfile
}

mark_remote_done() {
  python3 << 'PY'
import subprocess
from pathlib import Path
PR_MAP = {
    1: "cursor/java-youtube-video-production-0689",
    2: "cursor/java-ep02-jdk-jre-jvm-0689",
    3: "cursor/java-ep03-program-structure-0689",
    4: "cursor/java-ep04-variables-data-types-0689",
    5: "cursor/java-ep05-operators-0689",
    6: "cursor/java-ep06-control-flow-0689",
    7: "cursor/java-ep07-methods-0689",
    8: "cursor/java-ep08-arrays-0689",
    9: "cursor/java-ep09-strings-0689",
    10: "cursor/java-ep10-oop-0689",
    11: "cursor/java-ep11-access-modifiers-0689",
    12: "cursor/java-ep12-packages-0689",
    13: "cursor/java-ep13-enums-0689",
    14: "cursor/java-ep14-wrappers-autoboxing-0689",
    15: "cursor/java-ep15-generics-0689",
    16: "cursor/java-ep16-annotations-0689",
    17: "cursor/java-ep17-reflection-0689",
    18: "cursor/java-ep18-records-0689",
    19: "cursor/java-ep19-sealed-classes-0689",
    20: "cursor/java-ep20-modules-0689",
    21: "cursor/java-ep21-lists-0689",
    22: "cursor/java-ep22-sets-0689",
    23: "cursor/java-ep23-maps-0689",
    24: "cursor/java-ep24-queues-deques-0689",
    25: "cursor/java-ep25-sorting-comparators-0689",
    26: "cursor/java-ep26-streams-intro-0689",
    27: "cursor/java-ep27-stream-collectors-0689",
    28: "cursor/java-ep28-flatmap-0689",
    29: "cursor/java-ep29-parallel-streams-0689",
    30: "cursor/java-ep30-optional-0689",
    31: "cursor/java-ep31-java-time-0689",
    32: "cursor/java-ep32-exceptions-0689",
    33: "cursor/java-ep33-try-with-resources-0689",
    34: "cursor/java-ep34-files-nio2-0689",
    35: "cursor/java-ep35-readers-writers-0689",
    36: "cursor/java-ep36-threads-intro-0689",
    37: "cursor/java-ep37-synchronization-0689",
    38: "cursor/java-ep38-volatile-happens-before-0689",
    39: "cursor/java-ep39-explicit-locks-0689",
    40: "cursor/java-ep40-executor-service-0689",
    41: "cursor/java-ep41-callable-future-0689",
    42: "cursor/java-ep42-concurrent-collections-0689",
    43: "cursor/java-ep43-atomics-0689",
    44: "cursor/java-ep44-synchronizers-0689",
    45: "cursor/java-ep45-blocking-queue-0689",
    46: "cursor/java-ep46-completable-future-0689",
    47: "cursor/java-ep47-forkjoinpool-0689",
    48: "cursor/java-ep48-threadlocal-0689",
    49: "cursor/java-ep49-deadlocks-0689",
    50: "cursor/java-ep50-virtual-threads-0689",
    51: "cursor/java-ep51-class-loading-0689",
    52: "cursor/java-ep52-bytecode-basics-0689",
    53: "cursor/java-ep53-heap-and-stack-0689",
    54: "cursor/java-ep54-garbage-collection-0689",
    55: "cursor/java-ep55-jit-compilation-0689",
    56: "cursor/java-ep56-gc-collectors-0689",
    57: "cursor/java-ep57-memory-leaks-0689",
    58: "cursor/java-ep58-diagnostic-tools-0689",
    59: "cursor/java-ep59-escape-analysis-0689",
    60: "cursor/java-ep60-metaspace-native-0689",
    61: "cursor/java-ep61-reference-types-0689",
    62: "cursor/java-ep62-jvm-flags-0689",
    63: "cursor/java-ep63-object-layout-0689",
    64: "cursor/java-ep64-safepoints-0689",
    65: "cursor/java-ep65-jvm-startup-0689",
    66: "cursor/java-ep66-jvm-interview-wrap-0689",
    67: "cursor/java-ep67-design-patterns-intro-0689",
    68: "cursor/java-ep68-creational-patterns-0689",
    69: "cursor/java-ep69-structural-patterns-0689",
    70: "cursor/java-ep70-behavioral-patterns-0689",
    71: "cursor/java-ep71-spring-intro-0689",
    72: "cursor/java-ep72-ioc-di-0689",
    73: "cursor/java-ep73-spring-boot-0689",
    74: "cursor/java-ep74-spring-mvc-rest-0689",
    75: "cursor/java-ep75-spring-data-0689",
    76: "cursor/java-ep76-spring-security-0689",
    77: "cursor/java-ep77-spring-testing-0689",
    78: "cursor/java-ep78-microservices-0689",
    79: "cursor/java-ep79-observability-resilience-0689",
    80: "cursor/java-ep80-architecture-interview-wrap-0689",
    81: "cursor/java-ep81-caching-strategies-0689",
    82: "cursor/java-ep82-api-design-0689",
    83: "cursor/java-ep83-event-driven-0689",
    84: "cursor/java-ep84-performance-playbook-0689",
    85: "cursor/java-ep85-production-readiness-0689",
}
done = []
for ep, br in PR_MAP.items():
    ok = False
    for path in ("output/v2", "java/output/v2"):
        r = subprocess.run(
            ["gh", "api", f"repos/ankur0001/professional-work/contents/{path}?ref={br}"],
            capture_output=True, text=True,
        )
        if r.returncode == 0 and "CAPTIONED" in r.stdout:
            ok = True
            break
    if ok:
        Path(f"/tmp/v2_distributed_ep{ep}").touch()
        done.append(ep)
print("remote_done", len(done), done[:10], "..." if len(done) > 10 else "")
resume = 1
for i in range(1, 86):
    if i not in done:
        resume = i
        break
else:
    resume = 86
print("resume_from", resume)
Path("/tmp/v2_resume_from").write_text(str(resume))
PY
}

write_watcher() {
  cat > /tmp/watch_distribute_v2.sh << 'WATCH'
#!/bin/bash
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
cd /workspace
LOG=/tmp/watch_distribute.log
echo "watcher start $(date)" >> "$LOG"
while true; do
  shopt -s nullglob
  for f in java/output/v2/Java_Episode_*_CAPTIONED.mp4; do
    [ -f "$f" ] || continue
    base=$(basename "$f")
    ep_padded=${base#Java_Episode_}
    ep_padded=${ep_padded%%_*}
    ep=$((10#$ep_padded))
    marker=/tmp/v2_distributed_ep${ep}
    if [ -f "$marker" ]; then
      continue
    fi
    clean_count=$(ls java/output/v2/Java_Episode_${ep_padded}_*.mp4 2>/dev/null | grep -v CAPTIONED | wc -l || true)
    if [ "$clean_count" -lt 1 ]; then
      continue
    fi
    s1=$(stat -c%s "$f"); sleep 3; s2=$(stat -c%s "$f")
    if [ "$s1" != "$s2" ]; then continue; fi
    echo "distributing EP${ep_padded} $(date)" >> "$LOG"
    if python3 java/video_build/distribute_v2_to_episode_prs.py --ep "$ep" >> "$LOG" 2>&1; then
      touch "$marker"; echo "ok EP$ep" >> "$LOG"
    else
      echo "fail EP$ep" >> "$LOG"
    fi
  done
  if ! pgrep -f 'render_v2_from_narrative.py --ep' >/dev/null 2>&1; then
    pending=0
    for f in java/output/v2/Java_Episode_*_CAPTIONED.mp4; do
      [ -f "$f" ] || continue
      base=$(basename "$f"); ep_padded=${base#Java_Episode_}; ep_padded=${ep_padded%%_*}; ep=$((10#$ep_padded))
      [ -f /tmp/v2_distributed_ep${ep} ] || pending=1
    done
    if [ "$pending" -eq 0 ]; then
      echo "watcher done $(date)" >> "$LOG"; break
    fi
  fi
  sleep 30
done
WATCH
  chmod +x /tmp/watch_distribute_v2.sh
}

main() {
  ensure_branch
  ensure_deps
  mkdir -p java/output/v2
  mark_remote_done
  resume=$(cat /tmp/v2_resume_from)
  if [ "$resume" -gt 85 ]; then
    echo "All 85 episodes already on remote"; exit 0
  fi
  if ! pgrep -f 'render_v2_from_narrative.py --ep' >/dev/null 2>&1; then
    echo "Starting render from EP$resume-85"
    nohup python3 -u java/video_build/render_v2_from_narrative.py --ep "${resume}-85" > "$RENDER_LOG" 2>&1 &
  fi
  write_watcher
  if ! pgrep -f 'watch_distribute_v2.sh' >/dev/null 2>&1; then
    nohup bash /tmp/watch_distribute_v2.sh >/dev/null 2>&1 &
  fi
  sleep 2
  pgrep -af 'render_v2_from_narrative|watch_distribute_v2' | grep -v pgrep || true
  head -n 5 "$RENDER_LOG" || true
}

main "$@"
