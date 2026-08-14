#!/usr/bin/env python3
"""Episode 81 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_81.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 java/video_build/make_episode_81_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/workspace/java/video_build")

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_81 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=81,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_81_Caching_Strategies.mp4",
        burned_name="Java_Episode_81_Caching_Strategies_CAPTIONED.mp4",
        srt_name="Java_Episode_81.srt",
        verify_stills=[('00:00:12', '01_hook'), ('00:00:50', '02_layers'), ('00:01:40', '03_patterns'), ('00:02:30', '04_invalidation'), ('00:03:20', '05_interview')],
    )


if __name__ == "__main__":
    main()
