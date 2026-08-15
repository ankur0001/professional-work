#!/usr/bin/env python3
"""Episode 24 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_24.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 video_build/make_episode_24_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_24 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=24,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_24_Queues_Deques.mp4",
        burned_name="Java_Episode_24_Queues_Deques_CAPTIONED.mp4",
        srt_name="Java_Episode_24.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
