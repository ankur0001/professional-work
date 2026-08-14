#!/usr/bin/env python3
"""Unified narrator: Sarvam (preferred when keyed) or Kokoro fallback.

Env:
  TTS_PROVIDER=sarvam|kokoro   (default: sarvam if SARVAM_API_KEY set else kokoro)
  SARVAM_API_KEY               Sarvam api-subscription-key
  SARVAM_SPEAKER               default shubh (bulbul:v3)
  SARVAM_PACE                  default 0.97
  SARVAM_LANGUAGE              default en-IN
  KOKORO_VOICE / KOKORO_SPEED  Kokoro fallback settings
"""
from __future__ import annotations

import os
from typing import Callable

import numpy as np


def provider() -> str:
    forced = (os.environ.get("TTS_PROVIDER") or "").strip().lower()
    if forced in {"sarvam", "kokoro"}:
        return forced
    from sarvam_tts import configured  # noqa: WPS433

    return "sarvam" if configured() else "kokoro"


def make_synth_beat() -> tuple[str, Callable[[str], np.ndarray], int]:
    """Return (provider_name, synth_beat(text)->float32 mono, sample_rate)."""
    name = provider()
    if name == "sarvam":
        from sarvam_tts import SAMPLE_RATE, synth_beat  # noqa: WPS433

        return "sarvam", synth_beat, SAMPLE_RATE

    # Kokoro fallback
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
