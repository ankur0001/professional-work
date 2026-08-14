#!/usr/bin/env python3
"""Unified narrator: Chatterbox (default) or Kokoro fallback.

Env:
  TTS_PROVIDER=chatterbox|kokoro   (default: chatterbox)
  CHATTERBOX_DEVICE                cpu|cuda|mps (auto)
  CHATTERBOX_VOICE_WAV             optional reference voice wav
  CHATTERBOX_EXAGGERATION          default 0.35
  CHATTERBOX_TEMPERATURE           default 0.7
  KOKORO_VOICE / KOKORO_SPEED      Kokoro fallback settings
"""
from __future__ import annotations

import os
from typing import Callable

import numpy as np


def provider() -> str:
    forced = (os.environ.get("TTS_PROVIDER") or "").strip().lower()
    if forced in {"chatterbox", "kokoro"}:
        return forced
    return "chatterbox"


def make_synth_beat() -> tuple[str, Callable[[str], np.ndarray], int]:
    """Return (provider_name, synth_beat(text)->float32 mono, sample_rate)."""
    name = provider()
    if name == "chatterbox":
        from chatterbox_tts import SAMPLE_RATE, synth_beat  # noqa: WPS433

        return "chatterbox", synth_beat, SAMPLE_RATE

    from kokoro import KPipeline  # noqa: WPS433

    voice = os.environ.get("KOKORO_VOICE", "am_michael")
    speed = float(os.environ.get("KOKORO_SPEED", "0.97"))
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")

    def synth_beat(text: str) -> np.ndarray:
        chunks = []
        for _, _, audio in pipeline(text, voice=voice, speed=speed):
            chunks.append(np.asarray(audio, dtype=np.float32))
        if not chunks:
            raise RuntimeError(text)
        return np.concatenate(chunks)

    return "kokoro", synth_beat, 24000
