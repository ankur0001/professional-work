#!/usr/bin/env python3
"""Episode 44 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_44.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 java/video_build/make_episode_44_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/workspace/java/video_build")

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_44 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=44,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_44_Synchronizers.mp4",
        burned_name="Java_Episode_44_Synchronizers_CAPTIONED.mp4",
        srt_name="Java_Episode_44.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
