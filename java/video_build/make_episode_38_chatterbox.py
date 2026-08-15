#!/usr/bin/env python3
"""Episode 38 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_38.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 java/video_build/make_episode_38_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/workspace/java/video_build")

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_38 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=38,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_38_Volatile_Happens_Before.mp4",
        burned_name="Java_Episode_38_Volatile_Happens_Before_CAPTIONED.mp4",
        srt_name="Java_Episode_38.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
