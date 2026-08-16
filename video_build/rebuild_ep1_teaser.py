#!/usr/bin/env python3
"""Rebuild only Episode 1 teaser (audio + visual), then remux final short cut."""

from __future__ import annotations

import json
import math
import multiprocessing as mp
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline
from PIL import Image

from generate_java_episode import FPS, FRAMES, Scene, render_teaser
from humanize_audio import generate_music_bed, probe
from make_short_episode import (
    ARTIFACTS,
    AUDIO,
    CLIPS_IN,
    CLIPS_OUT,
    OUTPUT,
    ROOT,
    SCENES,
    SPEED,
    VOICE,
    clean,
    remux,
    silence,
    synth_beat,
    write_srt,
)

TEASER_BEATS = next(beats for sid, _, beats in SCENES if sid == "teaser")


def synth_teaser(pipeline: KPipeline) -> Path:
    scene_dir = AUDIO / "teaser"
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    for i, beat in enumerate(TEASER_BEATS):
        text = clean(beat)
        print(f"  synth teaser beat {i}: {text[:60]}…")
        audio = synth_beat(pipeline, text)
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(wav, audio, 24000)
        parts.append(wav)
        if i < len(TEASER_BEATS) - 1:
            gap = silence(0.18)
            gpath = scene_dir / f"s{i:02d}.wav"
            sf.write(gpath, gap, 24000)
            parts.append(gpath)
    lst = scene_dir / "list.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    out = AUDIO / "teaser.mp3"
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


def _frame_job(args):
    i, n_frames, scene_dir = args
    progress = i / max(n_frames - 1, 1)
    t = i / FPS
    frame = render_teaser(progress, t)
    path = Path(scene_dir) / f"f{i:05d}.jpg"
    frame.save(path, quality=85)
    return i


def render_teaser_visual(duration: float) -> Path:
    duration = max(duration + 0.5, 4.0)
    n_frames = int(math.ceil(duration * FPS))
    scene_dir = FRAMES / "teaser_rebuild"
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)
    print(f"  Rendering teaser visual: {n_frames} frames ({duration:.1f}s)")
    args = [(i, n_frames, str(scene_dir)) for i in range(n_frames)]
    workers = max(2, min(8, os.cpu_count() or 4))
    with mp.Pool(workers) as pool:
        done = 0
        for _ in pool.imap_unordered(_frame_job, args, chunksize=8):
            done += 1
            if done % 60 == 0 or done == n_frames:
                print(f"    frames {done}/{n_frames}")
    out = CLIPS_IN / "teaser.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(scene_dir / "f%05d.jpg"),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(scene_dir)
    return out


def assemble_final(durations: dict[str, float]) -> Path:
    outs = []
    for scene_id, clip_id, _ in SCENES:
        if scene_id == "teaser":
            print(f"  remux teaser <- teaser")
            outs.append(remux("teaser", "teaser"))
        else:
            existing = CLIPS_OUT / f"{scene_id}.mp4"
            if not existing.exists():
                raise FileNotFoundError(existing)
            outs.append(existing)

    lst = ROOT / "concat_short_teaser.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep1_short_narrated.mp4"
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

    music = AUDIO / "music_bed.m4a"
    generate_music_bed(dur + 2, music)

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
            "192k",
            "-ar",
            "48000",
            "-shortest",
            "-movflags",
            "+faststart",
            str(final),
        ],
        check=True,
    )
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(final, ARTIFACTS / "Java_Episode_01_Why_Java_Exists.mp4")

    write_srt(durations, OUTPUT / "Java_Episode_01.srt")
    # trim SRT end to match video
    srt_lines = Path(OUTPUT / "Java_Episode_01.srt").read_text().splitlines()
    # keep as-is from write_srt
    Path(OUTPUT / "Java_Episode_01.srt").write_text("\n".join(srt_lines) + "\n")
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
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(burned),
        ],
        check=True,
    )
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4")
    return final


def main():
    AUDIO.mkdir(parents=True, exist_ok=True)
    CLIPS_OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)

    print(f"==> Rebuild Ep1 teaser only voice={VOICE} speed={SPEED}")
    pipeline = KPipeline(lang_code="a" if VOICE.startswith("a") else "b", repo_id="hexgrad/Kokoro-82M")
    synth_teaser(pipeline)
    teaser_dur = probe(AUDIO / "teaser.mp3")
    print(f"==> Teaser audio {teaser_dur:.2f}s")
    render_teaser_visual(teaser_dur)

    # refresh durations map
    durations_path = ROOT / "short_durations.json"
    if durations_path.exists():
        durations = json.loads(durations_path.read_text())
    else:
        durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES if sid != "teaser"}
    durations["teaser"] = teaser_dur
    durations_path.write_text(json.dumps(durations, indent=2))

    final = assemble_final(durations)
    print(f"==> Done: {final} ({probe(final):.1f}s)")

    # verify frame text
    verify = ARTIFACTS / "ep01_teaser_verify.png"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            str(max(0, probe(final) - 8)),
            "-i",
            str(final),
            "-frames:v",
            "1",
            str(verify),
        ],
        check=True,
        capture_output=True,
    )
    print(f"==> Verify frame: {verify}")


if __name__ == "__main__":
    main()
