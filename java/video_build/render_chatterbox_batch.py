#!/usr/bin/env python3
"""Batch-render Chatterbox episodes.

  python3 java/video_build/render_chatterbox_batch.py 81 85
  python3 java/video_build/render_chatterbox_batch.py 2 10
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: render_chatterbox_batch.py START [END]")
    start = int(sys.argv[1])
    end = int(sys.argv[2]) if len(sys.argv) > 2 else start
    failed = []
    for ep in range(start, end + 1):
        script = ROOT / f"make_episode_{ep:02d}_chatterbox.py"
        if not script.exists():
            print(f"skip missing {script.name}")
            continue
        print(f"\n######## RENDER EP {ep:02d} ########")
        rc = subprocess.call([sys.executable, str(script)])
        if rc != 0:
            failed.append(ep)
            print(f"FAILED ep {ep:02d} rc={rc}")
    if failed:
        raise SystemExit(f"failed episodes: {failed}")
    print("ALL OK")


if __name__ == "__main__":
    main()
