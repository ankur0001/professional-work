#!/usr/bin/env python3
"""Episode 09 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_09.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 java/video_build/make_episode_09_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, "/workspace/java/video_build")

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_09 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=9,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_09_Strings.mp4",
        burned_name="Java_Episode_09_Strings_CAPTIONED.mp4",
        srt_name="Java_Episode_09.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
