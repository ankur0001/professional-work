#!/usr/bin/env python3
"""
Kokoro-82M narration rebuild — open-weight TTS closest to ElevenLabs quality
that runs on CPU without an API key.

Voice default: am_michael (warm, trustworthy American English mentor).
Override with:  export KOKORO_VOICE=bm_fable
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

from humanize_audio import BEATS, ORDER, probe, generate_music_bed, write_srt

ROOT = Path("/workspace/video_build")
AUDIO = ROOT / "audio_kokoro"
CLIPS_IN = ROOT / "clips"
CLIPS_OUT = ROOT / "clips_kokoro"
OUTPUT = Path("/workspace/output")
ARTIFACTS = Path("/opt/cursor/artifacts")

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.96"))

# lang_code must match voice prefix
LANG_BY_PREFIX = {
    "a": "a",  # American
    "b": "b",  # British
    "h": "h",  # Hindi
    "e": "e",
    "f": "f",
    "i": "i",
    "j": "j",
    "p": "p",
    "z": "z",
}


def lang_for_voice(voice: str) -> str:
    return LANG_BY_PREFIX.get(voice[0], "a")


def clean_text(text: str) -> str:
    for tag in (
        '<break time="180ms"/>',
        '<break time="280ms"/>',
        '<break time="350ms"/>',
        '<break time="120ms"/>',
    ):
        text = text.replace(tag, "")
    # Kokoro handles ellipses/punctuation well; keep conversational marks
    return " ".join(text.split()).strip()


def synthesize_beat(pipeline: KPipeline, text: str, voice: str) -> np.ndarray:
    chunks = []
    for _, _, audio in pipeline(text, voice=voice, speed=SPEED):
        chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks:
        raise RuntimeError(f"No audio for: {text[:80]}")
    return np.concatenate(chunks)


def write_silence_wav(path: Path, seconds: float, sr: int = 24000):
    n = max(1, int(seconds * sr))
    sf.write(str(path), np.zeros(n, dtype=np.float32), sr)


def synthesize_scene(pipeline: KPipeline, scene_id: str, voice: str) -> Path:
    beats = BEATS[scene_id]
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []

    for i, beat in enumerate(beats):
        text = clean_text(beat)
        print(f"    beat {i+1}/{len(beats)}: {text[:72]}...")
        audio = synthesize_beat(pipeline, text, voice)
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), audio, 24000)
        parts.append(wav)

        if i < len(beats) - 1:
            gap = 0.16
            if beat.strip().endswith("?"):
                gap = 0.32
            elif any(k in beat for k in ("Watch carefully", "imagine this", "Picture this", "secret")):
                gap = 0.38
            elif beat.strip().endswith((".", "!")):
                gap = 0.20
            sil = scene_dir / f"s{i:02d}.wav"
            write_silence_wav(sil, gap)
            parts.append(sil)

    # concat wavs -> mp3
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


def remux_scene(scene_id: str) -> Path:
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
    voice = VOICE
    lang = lang_for_voice(voice)
    print(f"Kokoro voice={voice} lang={lang} speed={SPEED}")

    if "--sample-only" in sys.argv:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        pipe = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")
        text = clean_text(BEATS["hook"][0] + " " + BEATS["hook"][1] + " " + BEATS["question"][0])
        audio = synthesize_beat(pipe, text, voice)
        wav = ARTIFACTS / f"kokoro_sample_{voice}.wav"
        sf.write(str(wav), audio, 24000)
        mp3 = ARTIFACTS / f"kokoro_sample_{voice}.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav), "-c:a", "libmp3lame", "-q:a", "2", str(mp3)],
            check=True,
            capture_output=True,
        )
        print("Sample:", mp3)
        return

    if AUDIO.exists():
        shutil.rmtree(AUDIO)
    AUDIO.mkdir(parents=True)
    CLIPS_OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    print("==> Loading Kokoro pipeline...")
    pipeline = KPipeline(lang_code=lang, repo_id="hexgrad/Kokoro-82M")

    print("==> Synthesizing scenes...")
    for i, sid in enumerate(ORDER):
        print(f"  [{i+1}/{len(ORDER)}] {sid}")
        synthesize_scene(pipeline, sid, voice)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid in ORDER}
    total = sum(durations.values()) + 0.3 * len(ORDER)
    print(f"==> Narration ≈ {total/60:.1f} min")
    (ROOT / "kokoro_durations.json").write_text(json.dumps(durations, indent=2))

    shutil.copy2(AUDIO / "hook.mp3", ARTIFACTS / "narration_KOKORO_sample.mp3")
    # longer preview
    lst2 = ROOT / "kokoro_sample_list.txt"
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
            str(ARTIFACTS / "narration_KOKORO_long.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    print("==> Remux onto visuals...")
    outs = []
    for sid in ORDER:
        print(f"  remux {sid}")
        outs.append(remux_scene(sid))

    print("==> Concatenate...")
    lst = ROOT / "concat_kokoro.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep1_kokoro_narrated.mp4"
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

    print("==> Music + final mix...")
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
            "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
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

    subprocess.run(["ffprobe", "-hide_banner", str(final)])
    print("DONE — Kokoro narrated video ready")
    print(f"Voice: {voice} | Sample: {ARTIFACTS / 'narration_KOKORO_long.mp3'}")


if __name__ == "__main__":
    main()
