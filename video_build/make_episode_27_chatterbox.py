#!/usr/bin/env python3
"""Episode 27 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_27.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 video_build/make_episode_27_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_27 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=27,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_27_Stream_Collectors.mp4",
        burned_name="Java_Episode_27_Stream_Collectors_CAPTIONED.mp4",
        srt_name="Java_Episode_27.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
