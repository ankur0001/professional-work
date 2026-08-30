#!/usr/bin/env python3
"""Local Chatterbox Turbo TTS for The Java Story (free, no cloud API).

Uses Resemble AI Chatterbox Turbo on CPU by default (CUDA when available).
Sample rate: 24 kHz mono float32 — matches the existing Kokoro pipeline.
"""
from __future__ import annotations

import os
import threading
from typing import Optional

import numpy as np
import torch

SAMPLE_RATE = 24000
MAX_CHARS = 280  # keep generations stable / fast on CPU

_model = None
_lock = threading.Lock()


def device_name() -> str:
    forced = (os.environ.get("CHATTERBOX_DEVICE") or "").strip().lower()
    if forced in {"cpu", "cuda", "mps"}:
        return forced
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def get_model():
    """Lazy-load a process-wide ChatterboxTurboTTS singleton."""
    global _model
    if _model is not None:
        return _model
    with _lock:
        if _model is not None:
            return _model
        from chatterbox.tts_turbo import ChatterboxTurboTTS  # noqa: WPS433

        dev = device_name()
        print(f"==> Loading Chatterbox Turbo on {dev}...")
        _model = ChatterboxTurboTTS.from_pretrained(device=dev)
        return _model


def _chunk_text(text: str) -> list[str]:
    text = " ".join(text.split()).strip()
    if not text:
        return []
    if len(text) <= MAX_CHARS:
        return [text]
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
                for i in range(0, len(sentence), MAX_CHARS):
                    parts.append(sentence[i : i + MAX_CHARS])
                buf = ""
    if buf:
        parts.append(buf)
    return parts


def synth_beat(
    text: str,
    *,
    audio_prompt_path: Optional[str] = None,
    exaggeration: Optional[float] = None,
    temperature: Optional[float] = None,
    cfg_weight: Optional[float] = None,
) -> np.ndarray:
    """Return mono float32 PCM at 24 kHz."""
    model = get_model()
    prompt = audio_prompt_path or os.environ.get("CHATTERBOX_VOICE_WAV") or None
    exaggeration = float(
        exaggeration if exaggeration is not None else os.environ.get("CHATTERBOX_EXAGGERATION", "0.35")
    )
    temperature = float(
        temperature if temperature is not None else os.environ.get("CHATTERBOX_TEMPERATURE", "0.7")
    )
    cfg_weight = float(
        cfg_weight if cfg_weight is not None else os.environ.get("CHATTERBOX_CFG_WEIGHT", "0.0")
    )

    chunks: list[np.ndarray] = []
    for part in _chunk_text(text):
        kwargs: dict = {
            "text": part,
            "exaggeration": exaggeration,
            "temperature": temperature,
            "cfg_weight": cfg_weight,
            "norm_loudness": True,
        }
        if prompt:
            kwargs["audio_prompt_path"] = prompt
        with torch.inference_mode():
            wav = model.generate(**kwargs)
        if isinstance(wav, torch.Tensor):
            audio = wav.detach().cpu().float().numpy()
        else:
            audio = np.asarray(wav, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.reshape(-1)
        chunks.append(audio.astype(np.float32))
    if not chunks:
        raise RuntimeError(f"Chatterbox produced no audio for: {text[:80]!r}")
    return np.concatenate(chunks)


def smoke_test(text: str = "Hello from Chatterbox. Welcome to The Java Story.") -> dict:
    audio = synth_beat(text)
    return {
        "ok": True,
        "samples": int(audio.shape[0]),
        "seconds": float(audio.shape[0] / SAMPLE_RATE),
        "device": device_name(),
        "engine": "chatterbox-turbo",
    }


if __name__ == "__main__":
    print(smoke_test())
