#!/usr/bin/env python3
"""Episode 19 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_19.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 java/video_build/make_episode_19_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/workspace/java/video_build")

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_19 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=19,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_19_Sealed_Classes.mp4",
        burned_name="Java_Episode_19_Sealed_Classes_CAPTIONED.mp4",
        srt_name="Java_Episode_19.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
