#!/usr/bin/env python3
"""Push Chatterbox deliverables onto an episode PR branch.

Episode PRs still use repo-root video_build/ + output/ (pre java/ move).
This copies the tip java/ artifacts into that layout, commits, and pushes.

  python3 java/video_build/push_chatterbox_episode_pr.py 81
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("/workspace")
JAVA = REPO / "java"

# ep -> (branch, pr_number) — PR numbers match gh list (79/80 historically swapped)
BRANCHES = {
    2: ("cursor/java-ep02-jdk-jre-jvm-0689", 2),
    3: ("cursor/java-ep03-program-structure-0689", 3),
    4: ("cursor/java-ep04-variables-data-types-0689", 4),
    5: ("cursor/java-ep05-operators-0689", 5),
    6: ("cursor/java-ep06-control-flow-0689", 6),
    7: ("cursor/java-ep07-methods-0689", 7),
    8: ("cursor/java-ep08-arrays-0689", 8),
    9: ("cursor/java-ep09-strings-0689", 9),
    10: ("cursor/java-ep10-oop-0689", 10),
    11: ("cursor/java-ep11-access-modifiers-0689", 11),
    12: ("cursor/java-ep12-packages-0689", 12),
    13: ("cursor/java-ep13-enums-0689", 13),
    14: ("cursor/java-ep14-wrappers-autoboxing-0689", 14),
    15: ("cursor/java-ep15-generics-0689", 15),
    16: ("cursor/java-ep16-annotations-0689", 16),
    17: ("cursor/java-ep17-reflection-0689", 17),
    18: ("cursor/java-ep18-records-0689", 18),
    19: ("cursor/java-ep19-sealed-classes-0689", 19),
    20: ("cursor/java-ep20-modules-0689", 20),
    21: ("cursor/java-ep21-lists-0689", 21),
    22: ("cursor/java-ep22-sets-0689", 22),
    23: ("cursor/java-ep23-maps-0689", 23),
    24: ("cursor/java-ep24-queues-deques-0689", 24),
    25: ("cursor/java-ep25-sorting-comparators-0689", 25),
    26: ("cursor/java-ep26-streams-intro-0689", 26),
    27: ("cursor/java-ep27-stream-collectors-0689", 27),
    28: ("cursor/java-ep28-flatmap-0689", 28),
    29: ("cursor/java-ep29-parallel-streams-0689", 29),
    30: ("cursor/java-ep30-optional-0689", 30),
    31: ("cursor/java-ep31-java-time-0689", 31),
    32: ("cursor/java-ep32-exceptions-0689", 32),
    33: ("cursor/java-ep33-try-with-resources-0689", 33),
    34: ("cursor/java-ep34-files-nio2-0689", 34),
    35: ("cursor/java-ep35-readers-writers-0689", 35),
    36: ("cursor/java-ep36-threads-intro-0689", 36),
    37: ("cursor/java-ep37-synchronization-0689", 37),
    38: ("cursor/java-ep38-volatile-happens-before-0689", 38),
    39: ("cursor/java-ep39-explicit-locks-0689", 39),
    40: ("cursor/java-ep40-executor-service-0689", 40),
    41: ("cursor/java-ep41-callable-future-0689", 41),
    42: ("cursor/java-ep42-concurrent-collections-0689", 42),
    43: ("cursor/java-ep43-atomics-0689", 43),
    44: ("cursor/java-ep44-synchronizers-0689", 44),
    45: ("cursor/java-ep45-blocking-queue-0689", 45),
    46: ("cursor/java-ep46-completable-future-0689", 46),
    47: ("cursor/java-ep47-forkjoinpool-0689", 47),
    48: ("cursor/java-ep48-threadlocal-0689", 48),
    49: ("cursor/java-ep49-deadlocks-0689", 49),
    50: ("cursor/java-ep50-virtual-threads-0689", 50),
    51: ("cursor/java-ep51-class-loading-0689", 51),
    52: ("cursor/java-ep52-bytecode-basics-0689", 52),
    53: ("cursor/java-ep53-heap-and-stack-0689", 53),
    54: ("cursor/java-ep54-garbage-collection-0689", 54),
    55: ("cursor/java-ep55-jit-compilation-0689", 55),
    56: ("cursor/java-ep56-gc-collectors-0689", 56),
    57: ("cursor/java-ep57-memory-leaks-0689", 57),
    58: ("cursor/java-ep58-diagnostic-tools-0689", 58),
    59: ("cursor/java-ep59-escape-analysis-0689", 59),
    60: ("cursor/java-ep60-metaspace-native-0689", 60),
    61: ("cursor/java-ep61-reference-types-0689", 61),
    62: ("cursor/java-ep62-jvm-flags-0689", 62),
    63: ("cursor/java-ep63-object-layout-0689", 63),
    64: ("cursor/java-ep64-safepoints-0689", 64),
    65: ("cursor/java-ep65-jvm-startup-0689", 65),
    66: ("cursor/java-ep66-jvm-interview-wrap-0689", 66),
    67: ("cursor/java-ep67-design-patterns-intro-0689", 67),
    68: ("cursor/java-ep68-creational-patterns-0689", 68),
    69: ("cursor/java-ep69-structural-patterns-0689", 69),
    70: ("cursor/java-ep70-behavioral-patterns-0689", 70),
    71: ("cursor/java-ep71-spring-intro-0689", 71),
    72: ("cursor/java-ep72-ioc-di-0689", 72),
    73: ("cursor/java-ep73-spring-boot-0689", 73),
    74: ("cursor/java-ep74-spring-mvc-rest-0689", 74),
    75: ("cursor/java-ep75-spring-data-0689", 75),
    76: ("cursor/java-ep76-spring-security-0689", 76),
    77: ("cursor/java-ep77-spring-testing-0689", 77),
    78: ("cursor/java-ep78-microservices-0689", 78),
    79: ("cursor/java-ep79-observability-resilience-0689", 80),  # PR# swapped
    80: ("cursor/java-ep80-architecture-interview-wrap-0689", 79),
    81: ("cursor/java-ep81-caching-strategies-0689", 81),
    82: ("cursor/java-ep82-api-design-0689", 82),
    83: ("cursor/java-ep83-event-driven-0689", 83),
    84: ("cursor/java-ep84-performance-playbook-0689", 84),
    85: ("cursor/java-ep85-production-readiness-0689", 85),
}


def run(cmd, cwd=None, check=True):
    print("+", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, check=check)


def discover_outputs(ep: int) -> tuple[Path, Path, Path]:
    out = JAVA / "output"
    finals = sorted(out.glob(f"Java_Episode_{ep:02d}_*.mp4"))
    finals = [p for p in finals if "_CAPTIONED" not in p.name and "chatterbox" not in p.name.lower()]
    burned = sorted(out.glob(f"Java_Episode_{ep:02d}_*_CAPTIONED.mp4"))
    srt = out / f"Java_Episode_{ep:02d}.srt"
    if not finals or not burned or not srt.exists():
        raise SystemExit(f"missing chatterbox outputs for ep {ep} under {out}")
    return finals[-1], burned[-1], srt


def adapt_script(src: Path, dest: Path, ep: int):
    """Rewrite java/ paths to root video_build layout used on episode branches."""
    text = src.read_text()
    text = text.replace('sys.path.insert(0, "/workspace/java/video_build")', 'sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))')
    text = text.replace(
        f"python3 java/video_build/make_episode_{ep:02d}_chatterbox.py",
        f"python3 video_build/make_episode_{ep:02d}_chatterbox.py",
    )
    dest.write_text(text)


def adapt_shared(src: Path, dest: Path):
    """Point ROOT at this video_build/; OUTPUT still comes from generate_java_episode."""
    text = src.read_text()
    text = text.replace('Path("/workspace/java/video_build")', 'Path(__file__).resolve().parent')
    dest.write_text(text)


def push_episode(ep: int):
    if ep not in BRANCHES:
        raise SystemExit(f"unknown episode {ep}")
    branch, pr = BRANCHES[ep]
    final, burned, srt = discover_outputs(ep)
    script = JAVA / "video_build" / f"make_episode_{ep:02d}_chatterbox.py"
    shared = [
        JAVA / "video_build" / "chatterbox_tts.py",
        JAVA / "video_build" / "chatterbox_episode.py",
        JAVA / "video_build" / "narrate.py",
    ]
    for p in [script, *shared]:
        if not p.exists():
            raise SystemExit(f"missing {p}")

    run(["git", "fetch", "origin", branch], cwd=str(REPO))
    with tempfile.TemporaryDirectory(prefix=f"ep{ep:02d}_cb_") as tmp:
        wt = Path(tmp) / "wt"
        run(["git", "worktree", "add", "--force", str(wt), f"origin/{branch}"], cwd=str(REPO))
        try:
            vb = wt / "video_build"
            out = wt / "output"
            vb.mkdir(parents=True, exist_ok=True)
            out.mkdir(parents=True, exist_ok=True)

            adapt_script(script, vb / script.name, ep)
            for p in shared:
                adapt_shared(p, vb / p.name)

            shutil.copy2(final, out / final.name)
            shutil.copy2(burned, out / burned.name)
            shutil.copy2(srt, out / srt.name)

            # durations json if present
            dur = JAVA / "video_build" / f"ep{ep:02d}_chatterbox_durations.json"
            if dur.exists():
                shutil.copy2(dur, vb / dur.name)

            run(["git", "add", f"video_build/{script.name}", "video_build/chatterbox_tts.py",
                 "video_build/chatterbox_episode.py", "video_build/narrate.py",
                 f"output/{final.name}", f"output/{burned.name}", f"output/{srt.name}"], cwd=str(wt))
            if dur.exists():
                run(["git", "add", f"video_build/{dur.name}"], cwd=str(wt))

            # commit only if changes
            st = subprocess.run(["git", "status", "--porcelain"], cwd=str(wt), capture_output=True, text=True)
            if not st.stdout.strip():
                print(f"ep{ep:02d}: nothing to commit")
                return pr, branch

            msg = f"Re-narrate Episode {ep:02d} with local Chatterbox Turbo TTS"
            run(["git", "commit", "-m", msg], cwd=str(wt))
            # push to the episode branch name
            run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"], cwd=str(wt))
            print(f"ep{ep:02d}: pushed to {branch} (PR #{pr})")
            return pr, branch
        finally:
            run(["git", "worktree", "remove", "--force", str(wt)], cwd=str(REPO), check=False)


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: push_chatterbox_episode_pr.py EP [EP...]")
    results = []
    for arg in sys.argv[1:]:
        results.append(push_episode(int(arg)))
    print(json.dumps([{"pr": pr, "branch": br} for pr, br in results], indent=2))


if __name__ == "__main__":
    main()
