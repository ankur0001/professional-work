#!/usr/bin/env python3
"""Episode 48 — Chatterbox Turbo narration render.

Reuses SCENES / RENDERERS from make_episode_48.py (Kokoro script) and
writes the standard deliverables with local free Chatterbox TTS.

  python3 video_build/make_episode_48_chatterbox.py
"""
from __future__ import annotations

import sys

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from chatterbox_episode import run_episode  # noqa: E402
from make_episode_48 import RENDERERS, SCENES, clean  # noqa: E402


def main():
    run_episode(
        episode=48,
        scenes=SCENES,
        renderers=RENDERERS,
        clean=clean,
        final_name="Java_Episode_48_ThreadLocal.mp4",
        burned_name="Java_Episode_48_ThreadLocal_CAPTIONED.mp4",
        srt_name="Java_Episode_48.srt",
        verify_stills=None,
    )


if __name__ == "__main__":
    main()
