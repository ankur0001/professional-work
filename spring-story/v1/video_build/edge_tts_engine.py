#!/usr/bin/env python3
"""Edge-TTS narration engine for The Spring Story (no API key, CPU-friendly).

Drop-in style API matching the Java Chatterbox helper:
  SAMPLE_RATE, synth_beat(text) -> np.ndarray float32 mono
"""
from __future__ import annotations

import asyncio
import io
import os
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

SAMPLE_RATE = 24000
VOICE = os.environ.get("SPRING_TTS_VOICE", "en-US-GuyNeural")
RATE = os.environ.get("SPRING_TTS_RATE", "+0%")


async def _synth_async(text: str) -> np.ndarray:
    import edge_tts

    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    # Write to a temp mp3 then decode with ffmpeg via soundfile-friendly wav
    with tempfile.TemporaryDirectory() as td:
        mp3 = Path(td) / "a.mp3"
        wav = Path(td) / "a.wav"
        await communicate.save(str(mp3))
        import subprocess

        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(mp3),
                "-ac", "1", "-ar", str(SAMPLE_RATE),
                str(wav),
            ],
            check=True,
            capture_output=True,
        )
        audio, sr = sf.read(str(wav), dtype="float32")
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        if sr != SAMPLE_RATE:
            # rare; ffmpeg should have resampled
            pass
        return audio.astype(np.float32)


def synth_beat(text: str) -> np.ndarray:
    text = " ".join(text.split()).strip()
    if not text:
        return np.zeros(int(0.3 * SAMPLE_RATE), dtype=np.float32)
    try:
        return asyncio.run(_synth_async(text))
    except RuntimeError:
        # Nested event loop (rare) — use a fresh loop
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(_synth_async(text))
        finally:
            loop.close()


def smoke_test(text: str = "Welcome to The Spring Story.") -> dict:
    audio = synth_beat(text)
    return {
        "ok": True,
        "samples": int(audio.shape[0]),
        "seconds": float(audio.shape[0] / SAMPLE_RATE),
        "voice": VOICE,
        "engine": "edge-tts",
    }


if __name__ == "__main__":
    print(smoke_test())
