#!/usr/bin/env python3
"""
ElevenLabs narration rebuild for Java Episode 1.

Requires:
  export ELEVENLABS_API_KEY="sk_..."

Optional:
  export ELEVENLABS_VOICE_ID="..."   # default: warm Indian-English male-ish stock voice
  export ELEVENLABS_MODEL_ID="eleven_multilingual_v2"
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import wave
from pathlib import Path

import numpy as np
import requests

# Reuse beat script + scene order from humanize pipeline
from humanize_audio import BEATS, ORDER, remux_scene, write_srt, probe, generate_music_bed

ROOT = Path("/workspace/video_build")
AUDIO = ROOT / "audio_eleven"
CLIPS_IN = ROOT / "clips"
CLIPS_OUT = ROOT / "clips_eleven"
OUTPUT = Path("/workspace/output")
ARTIFACTS = Path("/opt/cursor/artifacts")

# Default: "Adam" is clear/professional; override with ELEVENLABS_VOICE_ID
# For Indian English mentor feel, pick a voice in ElevenLabs UI and paste its ID.
DEFAULT_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")  # Adam
MODEL_ID = os.environ.get("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
API_BASE = "https://api.elevenlabs.io/v1"


def require_key() -> str:
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        print(
            "\nERROR: ELEVENLABS_API_KEY is not set.\n\n"
            "1) Get a key from https://elevenlabs.io → Profile → API Key\n"
            "2) Run:\n"
            '   export ELEVENLABS_API_KEY="your_key_here"\n'
            "3) Optional — pick a warm Indian-English male voice in the UI and:\n"
            '   export ELEVENLABS_VOICE_ID="voice_id_here"\n'
            "4) Re-run:\n"
            "   python3 video_build/elevenlabs_narrate.py\n"
        )
        sys.exit(2)
    return key


def list_voices(api_key: str):
    r = requests.get(f"{API_BASE}/voices", headers={"xi-api-key": api_key}, timeout=60)
    r.raise_for_status()
    voices = r.json().get("voices", [])
    print(f"Available voices ({len(voices)}):")
    for v in voices[:40]:
        labels = v.get("labels") or {}
        accent = labels.get("accent", "")
        gender = labels.get("gender", "")
        print(f"  {v['voice_id']}  |  {v['name']}  |  {gender} {accent}".rstrip())
    return voices


def tts_eleven(api_key: str, text: str, out_path: Path, voice_id: str):
    url = f"{API_BASE}/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            # Conversational mentor — not flat newsreader
            "stability": 0.42,
            "similarity_boost": 0.80,
            "style": 0.35,
            "use_speaker_boost": True,
        },
    }
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    for attempt in range(5):
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        if r.status_code == 200:
            out_path.write_bytes(r.content)
            return
        if r.status_code in (429, 500, 502, 503):
            wait = 2 ** attempt
            print(f"    retry {attempt+1} after {wait}s ({r.status_code})")
            time.sleep(wait)
            continue
        raise RuntimeError(f"ElevenLabs error {r.status_code}: {r.text[:400]}")
    raise RuntimeError("ElevenLabs failed after retries")


def write_silence_mp3(path: Path, seconds: float):
    """Create short silence via ffmpeg."""
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=r=44100:cl=mono",
            "-t",
            f"{seconds:.3f}",
            "-q:a",
            "9",
            "-acodec",
            "libmp3lame",
            str(path),
        ],
        check=True,
        capture_output=True,
    )


def synthesize_scene(api_key: str, scene_id: str, voice_id: str) -> Path:
    beats = BEATS[scene_id]
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []

    for i, beat in enumerate(beats):
        # Clean text for ElevenLabs (no SSML tags)
        text = (
            beat.replace("<break time=\"180ms\"/>", "")
            .replace("<break time=\"280ms\"/>", "")
            .replace("<break time=\"350ms\"/>", "")
            .replace("<break time=\"120ms\"/>", "")
        )
        text = " ".join(text.split()).strip()
        mp3 = scene_dir / f"b{i:02d}.mp3"
        print(f"    beat {i+1}/{len(beats)}: {text[:70]}...")
        tts_eleven(api_key, text, mp3, voice_id)
        parts.append(mp3)

        if i < len(beats) - 1:
            gap = 0.18
            if beat.strip().endswith("?"):
                gap = 0.35
            elif any(k in beat for k in ("Watch carefully", "imagine this", "Picture this", "secret")):
                gap = 0.40
            elif beat.strip().endswith((".", "!")):
                gap = 0.22
            sil = scene_dir / f"s{i:02d}.mp3"
            write_silence_mp3(sil, gap)
            parts.append(sil)

    lst = scene_dir / "list.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    out = AUDIO / f"{scene_id}.mp3"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def remux_scene_eleven(scene_id: str) -> Path:
    """Same as humanize remux but paths point at eleven folders."""
    vin = CLIPS_IN / f"{scene_id}.mp4"
    ain = AUDIO / f"{scene_id}.mp3"
    vout = CLIPS_OUT / f"{scene_id}.mp4"
    if not vin.exists():
        raise FileNotFoundError(vin)

    vd = probe(vin)
    ad = probe(ain)
    target = ad + 0.30

    if target > vd:
        pad = target - vd
        filter_v = f"tpad=stop_mode=clone:stop_duration={pad:.3f}"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(vin),
            "-i",
            str(ain),
            "-filter_complex",
            f"[0:v]{filter_v}[v]",
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-shortest",
            "-movflags",
            "+faststart",
            str(vout),
        ]
    else:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(vin),
            "-i",
            str(ain),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-t",
            f"{target:.3f}",
            "-movflags",
            "+faststart",
            str(vout),
        ]
    subprocess.run(cmd, check=True, capture_output=True)
    return vout


def main():
    api_key = require_key()
    voice_id = DEFAULT_VOICE_ID

    if "--list-voices" in sys.argv:
        list_voices(api_key)
        return

    # Prefer an Indian English voice if present and user didn't override
    if "ELEVENLABS_VOICE_ID" not in os.environ:
        try:
            voices = requests.get(
                f"{API_BASE}/voices", headers={"xi-api-key": api_key}, timeout=60
            ).json().get("voices", [])
            for v in voices:
                labels = v.get("labels") or {}
                name = (v.get("name") or "").lower()
                accent = (labels.get("accent") or "").lower()
                gender = (labels.get("gender") or "").lower()
                if gender == "male" and ("indian" in accent or "india" in accent or "indian" in name):
                    voice_id = v["voice_id"]
                    print(f"Auto-selected Indian male voice: {v['name']} ({voice_id})")
                    break
        except Exception as e:
            print(f"Voice auto-select skipped: {e}")

    print(f"Using voice_id={voice_id} model={MODEL_ID}")

    if AUDIO.exists():
        shutil.rmtree(AUDIO)
    AUDIO.mkdir(parents=True)
    CLIPS_OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    print("==> ElevenLabs TTS (beat-based)...")
    for i, sid in enumerate(ORDER):
        print(f"  [{i+1}/{len(ORDER)}] {sid}")
        synthesize_scene(api_key, sid, voice_id)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid in ORDER}
    total = sum(durations.values()) + 0.3 * len(ORDER)
    print(f"==> Narration ≈ {total/60:.1f} min")
    (ROOT / "eleven_durations.json").write_text(json.dumps(durations, indent=2))

    # sample for quick listen
    shutil.copy2(AUDIO / "hook.mp3", ARTIFACTS / "narration_ELEVENLABS_sample.mp3")

    print("==> Remux onto scene videos...")
    outs = []
    for sid in ORDER:
        print(f"  remux {sid}")
        outs.append(remux_scene_eleven(sid))

    print("==> Concatenate + mix...")
    lst = ROOT / "concat_eleven.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep1_eleven_narrated.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-movflags",
            "+faststart",
            str(narrated),
        ],
        check=True,
    )

    music = AUDIO / "music_bed.m4a"
    generate_music_bed(probe(narrated) + 2, music)

    final = OUTPUT / "Java_Episode_01_Why_Java_Exists.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(narrated),
            "-i",
            str(music),
            "-filter_complex",
            "[1:a]volume=0.10[m];[0:a]volume=1.10[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map",
            "0:v",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-movflags",
            "+faststart",
            str(final),
        ],
        check=True,
    )
    shutil.copy2(final, ARTIFACTS / "Java_Episode_01_Why_Java_Exists.mp4")

    write_srt(durations, OUTPUT / "Java_Episode_01.srt")
    shutil.copy2(OUTPUT / "Java_Episode_01.srt", ARTIFACTS / "Java_Episode_01.srt")

    burned = OUTPUT / "Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-vf",
            f"subtitles={OUTPUT / 'Java_Episode_01.srt'}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "19",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(burned),
        ],
        check=True,
    )
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4")

    # longer sample
    lst2 = ROOT / "eleven_sample_list.txt"
    with open(lst2, "w") as f:
        for sid in ["hook", "question", "promise", "curiosity3", "bytecode"]:
            f.write(f"file '{AUDIO / (sid + '.mp3')}'\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst2),
            "-c",
            "copy",
            str(ARTIFACTS / "narration_ELEVENLABS_long.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    subprocess.run(["ffprobe", "-hide_banner", str(final)])
    print("DONE — ElevenLabs narrated video ready")


if __name__ == "__main__":
    main()
