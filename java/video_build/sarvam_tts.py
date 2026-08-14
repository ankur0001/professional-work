#!/usr/bin/env python3
"""Sarvam AI Text-to-Speech client for The Java Story narration.

Uses Bulbul v3 (en-IN) when SARVAM_API_KEY / SARVAM_API_SUBSCRIPTION_KEY is set.
Docs: https://docs.sarvam.ai/api-reference-docs/text-to-speech/convert
"""
from __future__ import annotations

import base64
import io
import os
import time
from typing import Optional

import numpy as np
import requests
import soundfile as sf

API_URL = "https://api.sarvam.ai/text-to-speech"
SAMPLE_RATE = 24000
MAX_CHARS = 2400  # bulbul:v3 hard limit is 2500; leave headroom


def api_key() -> Optional[str]:
    return (
        os.environ.get("SARVAM_API_KEY")
        or os.environ.get("SARVAM_API_SUBSCRIPTION_KEY")
        or os.environ.get("SARVAM_SUBSCRIPTION_KEY")
    )


def configured() -> bool:
    return bool(api_key())


def _headers() -> dict:
    key = api_key()
    if not key:
        raise RuntimeError(
            "Sarvam API key missing. Set SARVAM_API_KEY (api-subscription-key from console.sarvam.ai)."
        )
    return {
        "api-subscription-key": key,
        "Content-Type": "application/json",
    }


def _chunk_text(text: str) -> list[str]:
    text = " ".join(text.split()).strip()
    if len(text) <= MAX_CHARS:
        return [text]
    # Prefer sentence boundaries
    parts: list[str] = []
    buf = ""
    for sentence in text.replace("? ", "?|").replace(". ", ".|").replace("! ", "!|").split("|"):
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(buf) + len(sentence) + 1 <= MAX_CHARS:
            buf = f"{buf} {sentence}".strip()
        else:
            if buf:
                parts.append(buf)
            if len(sentence) <= MAX_CHARS:
                buf = sentence
            else:
                # hard wrap long sentence
                for i in range(0, len(sentence), MAX_CHARS):
                    parts.append(sentence[i : i + MAX_CHARS])
                buf = ""
    if buf:
        parts.append(buf)
    return parts


def synth_beat(
    text: str,
    *,
    speaker: Optional[str] = None,
    pace: Optional[float] = None,
    temperature: Optional[float] = None,
    language_code: Optional[str] = None,
    model: str = "bulbul:v3",
) -> np.ndarray:
    """Return mono float32 PCM at 24 kHz."""
    speaker = speaker or os.environ.get("SARVAM_SPEAKER", "shubh")
    pace = float(pace if pace is not None else os.environ.get("SARVAM_PACE", "0.97"))
    temperature = float(
        temperature if temperature is not None else os.environ.get("SARVAM_TEMPERATURE", "0.6")
    )
    language_code = language_code or os.environ.get("SARVAM_LANGUAGE", "en-IN")

    chunks: list[np.ndarray] = []
    for part in _chunk_text(text):
        payload = {
            "text": part,
            "target_language_code": language_code,  # older SDKs; REST uses language_code
            "language_code": language_code,
            "speaker": speaker,
            "pace": pace,
            "model": model,
            "speech_sample_rate": SAMPLE_RATE,
            "output_audio_codec": "wav",
            "temperature": temperature,
        }
        # Retry transient failures
        last_err: Exception | None = None
        for attempt in range(4):
            try:
                resp = requests.post(API_URL, headers=_headers(), json=payload, timeout=120)
                if resp.status_code == 429:
                    time.sleep(2 ** attempt)
                    continue
                if resp.status_code >= 400:
                    raise RuntimeError(f"Sarvam TTS {resp.status_code}: {resp.text[:500]}")
                data = resp.json()
                audios = data.get("audios") or []
                if not audios:
                    raise RuntimeError(f"Sarvam TTS empty audios: {data!r}")
                raw = base64.b64decode("".join(audios))
                audio, sr = sf.read(io.BytesIO(raw), dtype="float32")
                if audio.ndim > 1:
                    audio = audio.mean(axis=1)
                if sr != SAMPLE_RATE:
                    # Resample via linear interp if needed
                    n = int(len(audio) * SAMPLE_RATE / sr)
                    x_old = np.linspace(0.0, 1.0, num=len(audio), endpoint=False)
                    x_new = np.linspace(0.0, 1.0, num=n, endpoint=False)
                    audio = np.interp(x_new, x_old, audio).astype(np.float32)
                chunks.append(audio.astype(np.float32))
                last_err = None
                break
            except Exception as exc:  # noqa: BLE001
                last_err = exc
                time.sleep(1.5 * (attempt + 1))
        if last_err is not None:
            raise last_err
    if not chunks:
        raise RuntimeError(f"Sarvam TTS produced no audio for: {text[:80]!r}")
    return np.concatenate(chunks)


def smoke_test(text: str = "Hello from Sarvam. Welcome to The Java Story.") -> dict:
    audio = synth_beat(text)
    return {
        "ok": True,
        "samples": int(audio.shape[0]),
        "seconds": float(audio.shape[0] / SAMPLE_RATE),
        "speaker": os.environ.get("SARVAM_SPEAKER", "shubh"),
        "language": os.environ.get("SARVAM_LANGUAGE", "en-IN"),
    }


if __name__ == "__main__":
    if not configured():
        raise SystemExit("Set SARVAM_API_KEY first")
    print(smoke_test())
