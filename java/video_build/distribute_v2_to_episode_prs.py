#!/usr/bin/env python3
"""Push java/output/v2 deliverables into each episode PR branch and retitle.

Expects v2 files already rendered under java/output/v2/.
Copies into each episode branch as java/output/v2/ (common folder name).

Usage:
  python3 java/video_build/distribute_v2_to_episode_prs.py --ep 1-5
  python3 java/video_build/distribute_v2_to_episode_prs.py --all
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path("/workspace")
V2 = ROOT / "java" / "output" / "v2"
NARR = ROOT / "java" / "narrative_review" / "episodes"

# episode -> (pr_number, branch)
PR_MAP = {
    1: (1, "cursor/java-youtube-video-production-0689"),
    2: (2, "cursor/java-ep02-jdk-jre-jvm-0689"),
    3: (3, "cursor/java-ep03-program-structure-0689"),
    4: (4, "cursor/java-ep04-variables-data-types-0689"),
    5: (5, "cursor/java-ep05-operators-0689"),
    6: (6, "cursor/java-ep06-control-flow-0689"),
    7: (7, "cursor/java-ep07-methods-0689"),
    8: (8, "cursor/java-ep08-arrays-0689"),
    9: (9, "cursor/java-ep09-strings-0689"),
    10: (10, "cursor/java-ep10-oop-0689"),
    11: (11, "cursor/java-ep11-access-modifiers-0689"),
    12: (12, "cursor/java-ep12-packages-0689"),
    13: (13, "cursor/java-ep13-enums-0689"),
    14: (14, "cursor/java-ep14-wrappers-autoboxing-0689"),
    15: (15, "cursor/java-ep15-generics-0689"),
    16: (16, "cursor/java-ep16-annotations-0689"),
    17: (17, "cursor/java-ep17-reflection-0689"),
    18: (18, "cursor/java-ep18-records-0689"),
    19: (19, "cursor/java-ep19-sealed-classes-0689"),
    20: (20, "cursor/java-ep20-modules-0689"),
    21: (21, "cursor/java-ep21-lists-0689"),
    22: (22, "cursor/java-ep22-sets-0689"),
    23: (23, "cursor/java-ep23-maps-0689"),
    24: (24, "cursor/java-ep24-queues-deques-0689"),
    25: (25, "cursor/java-ep25-sorting-comparators-0689"),
    26: (26, "cursor/java-ep26-streams-intro-0689"),
    27: (27, "cursor/java-ep27-stream-collectors-0689"),
    28: (28, "cursor/java-ep28-flatmap-0689"),
    29: (29, "cursor/java-ep29-parallel-streams-0689"),
    30: (30, "cursor/java-ep30-optional-0689"),
    31: (31, "cursor/java-ep31-java-time-0689"),
    32: (32, "cursor/java-ep32-exceptions-0689"),
    33: (33, "cursor/java-ep33-try-with-resources-0689"),
    34: (34, "cursor/java-ep34-files-nio2-0689"),
    35: (35, "cursor/java-ep35-readers-writers-0689"),
    36: (36, "cursor/java-ep36-threads-intro-0689"),
    37: (37, "cursor/java-ep37-synchronization-0689"),
    38: (38, "cursor/java-ep38-volatile-happens-before-0689"),
    39: (39, "cursor/java-ep39-explicit-locks-0689"),
    40: (40, "cursor/java-ep40-executor-service-0689"),
    41: (41, "cursor/java-ep41-callable-future-0689"),
    42: (42, "cursor/java-ep42-concurrent-collections-0689"),
    43: (43, "cursor/java-ep43-atomics-0689"),
    44: (44, "cursor/java-ep44-synchronizers-0689"),
    45: (45, "cursor/java-ep45-blocking-queue-0689"),
    46: (46, "cursor/java-ep46-completable-future-0689"),
    47: (47, "cursor/java-ep47-forkjoinpool-0689"),
    48: (48, "cursor/java-ep48-threadlocal-0689"),
    49: (49, "cursor/java-ep49-deadlocks-0689"),
    50: (50, "cursor/java-ep50-virtual-threads-0689"),
    51: (51, "cursor/java-ep51-class-loading-0689"),
    52: (52, "cursor/java-ep52-bytecode-basics-0689"),
    53: (53, "cursor/java-ep53-heap-and-stack-0689"),
    54: (54, "cursor/java-ep54-garbage-collection-0689"),
    55: (55, "cursor/java-ep55-jit-compilation-0689"),
    56: (56, "cursor/java-ep56-gc-collectors-0689"),
    57: (57, "cursor/java-ep57-memory-leaks-0689"),
    58: (58, "cursor/java-ep58-diagnostic-tools-0689"),
    59: (59, "cursor/java-ep59-escape-analysis-0689"),
    60: (60, "cursor/java-ep60-metaspace-native-0689"),
    61: (61, "cursor/java-ep61-reference-types-0689"),
    62: (62, "cursor/java-ep62-jvm-flags-0689"),
    63: (63, "cursor/java-ep63-object-layout-0689"),
    64: (64, "cursor/java-ep64-safepoints-0689"),
    65: (65, "cursor/java-ep65-jvm-startup-0689"),
    66: (66, "cursor/java-ep66-jvm-interview-wrap-0689"),
    67: (67, "cursor/java-ep67-design-patterns-intro-0689"),
    68: (68, "cursor/java-ep68-creational-patterns-0689"),
    69: (69, "cursor/java-ep69-structural-patterns-0689"),
    70: (70, "cursor/java-ep70-behavioral-patterns-0689"),
    71: (71, "cursor/java-ep71-spring-intro-0689"),
    72: (72, "cursor/java-ep72-ioc-di-0689"),
    73: (73, "cursor/java-ep73-spring-boot-0689"),
    74: (74, "cursor/java-ep74-spring-mvc-rest-0689"),
    75: (75, "cursor/java-ep75-spring-data-0689"),
    76: (76, "cursor/java-ep76-spring-security-0689"),
    77: (77, "cursor/java-ep77-spring-testing-0689"),
    78: (78, "cursor/java-ep78-microservices-0689"),
    79: (80, "cursor/java-ep79-observability-resilience-0689"),
    80: (79, "cursor/java-ep80-architecture-interview-wrap-0689"),
    81: (81, "cursor/java-ep81-caching-strategies-0689"),
    82: (82, "cursor/java-ep82-api-design-0689"),
    83: (83, "cursor/java-ep83-event-driven-0689"),
    84: (84, "cursor/java-ep84-performance-playbook-0689"),
    85: (85, "cursor/java-ep85-production-readiness-0689"),
}


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check, text=True, capture_output=True)


def title_for(ep: int) -> str:
    p = next(NARR.glob(f"ep{ep:02d}_*.md"))
    m = re.search(r"^# Episode \d+ — (.+)$", p.read_text(), re.M)
    return m.group(1).strip() if m else f"Episode {ep}"


def v2_files_for(ep: int) -> list[Path]:
    files = sorted(V2.glob(f"Java_Episode_{ep:02d}*"))
    return [f for f in files if f.is_file()]


def push_episode(ep: int) -> None:
    pr_num, branch = PR_MAP[ep]
    files = v2_files_for(ep)
    if not files:
        print(f"SKIP EP{ep:02d}: no v2 files")
        return
    print(f"==> EP{ep:02d} -> {branch} (PR #{pr_num}) files={len(files)}")
    run(["git", "fetch", "origin", branch])
    # stash-less: worktree in /tmp
    wt = Path(f"/tmp/ep-v2-{ep:02d}")
    if wt.exists():
        run(["git", "worktree", "unlock", str(wt)], check=False)
        run(["git", "worktree", "remove", "--force", str(wt)], check=False)
        shutil_rm = __import__("shutil").rmtree
        if wt.exists():
            shutil_rm(wt, ignore_errors=True)
        run(["git", "worktree", "prune"], check=False)
    run(["git", "worktree", "add", "-f", str(wt), f"origin/{branch}"])
    dest = wt / "java" / "output" / "v2"
    # some older branches use output/ at repo root
    if not (wt / "java").exists() and (wt / "output").exists():
        dest = wt / "output" / "v2"
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        target = dest / f.name
        target.write_bytes(f.read_bytes())
    # also copy narration snapshot into v2 for traceability
    narr = next(NARR.glob(f"ep{ep:02d}_*.md"))
    (dest / "narration.md").write_text(narr.read_text())
    run(["git", "-C", str(wt), "add", "-A", str(dest.relative_to(wt))])
    status = run(["git", "-C", str(wt), "status", "--porcelain"]).stdout.strip()
    if not status:
        print("    no changes")
    else:
        msg = f"Add v2 narrative video cut for Episode {ep:02d}"
        run(["git", "-C", str(wt), "commit", "-m", msg])
        run(["git", "-C", str(wt), "push", "-u", "origin", f"HEAD:{branch}"])
    # retitle / reopen via gh (read-only gh can't write - use ManagePullRequest from parent)
    meta = {
        "ep": ep,
        "pr": pr_num,
        "branch": branch,
        "title": f"Episode {ep:02d}: {title_for(ep)} — v2 narrative video",
        "files": [f.name for f in files],
    }
    (V2 / f"distribute_ep{ep:02d}.json").write_text(json.dumps(meta, indent=2))
    run(["git", "worktree", "remove", "--force", str(wt)], check=False)
    print("    pushed")


def parse_eps(spec: str) -> list[int]:
    out: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if part == "all":
            return list(range(1, 86))
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", required=True, help="1-5 or all")
    args = ap.parse_args()
    for ep in parse_eps(args.ep if args.ep != "all" else "all"):
        try:
            push_episode(ep)
        except Exception as e:
            print(f"FAIL EP{ep:02d}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
