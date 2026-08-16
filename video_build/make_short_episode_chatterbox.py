#!/usr/bin/env python3
"""
4–5 minute condensed Java Episode 1 — local Chatterbox Turbo narration.

Same short-cut SCENES / visuals as make_short_episode.py, but TTS is free
local Chatterbox (no Kokoro / Sarvam / ElevenLabs).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

from chatterbox_tts import SAMPLE_RATE, synth_beat as cb_synth
from humanize_audio import generate_music_bed, probe
from make_short_episode import SCENES, clean, remux, write_srt

ROOT = Path("/workspace/video_build")
AUDIO = ROOT / "audio_chatterbox_short"
CLIPS_OUT = ROOT / "clips_chatterbox_short"
OUTPUT = Path("/workspace/output")
ARTIFACTS = Path("/opt/cursor/artifacts")


def silence(seconds: float, sr: int = SAMPLE_RATE) -> np.ndarray:
    return np.zeros(max(1, int(seconds * sr)), dtype=np.float32)


def synth_scene(scene_id: str, beats: list[str]) -> Path:
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    {i+1}/{len(beats)} [chatterbox]: {text[:72]}")
        audio = cb_synth(text)
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), audio, SAMPLE_RATE)
        parts.append(wav)
        if i < len(beats) - 1:
            gap = 0.26 if text.endswith("?") else 0.12
            if any(k in text for k in ("secret", "imagine", "Interview", "Watch carefully")):
                gap = 0.30
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), silence(gap), SAMPLE_RATE)
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


def main():
    if AUDIO.exists():
        shutil.rmtree(AUDIO)
    if CLIPS_OUT.exists():
        shutil.rmtree(CLIPS_OUT)
    AUDIO.mkdir(parents=True)
    CLIPS_OUT.mkdir(parents=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    # remux() writes into make_short_episode.CLIPS_OUT — redirect by patching module path
    import make_short_episode as mse

    mse.AUDIO = AUDIO
    mse.CLIPS_OUT = CLIPS_OUT

    print("==> Episode 1 short cut — Chatterbox Turbo")
    for i, (scene_id, _clip, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {scene_id}")
        synth_scene(scene_id, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.22 * len(SCENES)
    print(f"==> Spoken runtime ≈ {total/60:.2f} min ({total:.1f}s)")
    (ROOT / "chatterbox_short_durations.json").write_text(json.dumps(durations, indent=2))

    outs = []
    for scene_id, clip_id, _ in SCENES:
        print(f"  remux {scene_id} <- {clip_id}")
        outs.append(remux(scene_id, clip_id))

    lst = ROOT / "concat_chatterbox_short.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep1_chatterbox_narrated.mp4"
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

    dur = probe(narrated)
    print(f"==> Assembled {dur:.1f}s ({dur/60:.2f} min)")

    # Match series window 240–330s (same pacing approach as tip Chatterbox runner)
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 240:
        pace = max(dur / 250.0, 0.5)

    music = AUDIO / "music_bed.m4a"
    generate_music_bed((dur / pace) + 2, music)

    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep1_chatterbox_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(narrated),
                "-filter_complex",
                f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]",
                "-map",
                "[v]",
                "-map",
                "[a]",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
                str(paced),
            ],
            check=True,
        )
        base = paced
    else:
        print("==> Natural length — no heavy time-stretch")

    final = OUTPUT / "Java_Episode_01_Why_Java_Exists.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(base),
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
    if abs(pace - 1.0) > 0.015:
        srt_lines = Path(OUTPUT / "Java_Episode_01.srt").read_text().splitlines()
        out_lines = []

        def scale_ts(ts: str) -> str:
            h, m, rest = ts.split(":")
            s, ms = rest.split(",")
            total = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
            total /= pace
            h = int(total // 3600)
            m = int((total % 3600) // 60)
            s = int(total % 60)
            ms = int(round((total - int(total)) * 1000))
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        for line in srt_lines:
            if "-->" in line:
                a, b = line.split(" --> ")
                out_lines.append(f"{scale_ts(a.strip())} --> {scale_ts(b.strip())}")
            else:
                out_lines.append(line)
        Path(OUTPUT / "Java_Episode_01.srt").write_text("\n".join(out_lines) + "\n")

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

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-t",
            "40",
            "-vn",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(ARTIFACTS / "narration_CHATTERBOX_ep01_preview.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    final_dur = probe(final)
    print(f"DONE: {final_dur/60:.2f} min ({final_dur:.1f}s)")
    assert 240 <= final_dur <= 330, f"Duration {final_dur}s outside 240–330s window"
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
