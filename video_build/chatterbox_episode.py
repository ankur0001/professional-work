#!/usr/bin/env python3
"""Shared Chatterbox render runner for The Java Story episodes.

Each make_episode_XX_chatterbox.py imports SCENES/RENDERERS from the Kokoro
episode script and calls run_episode(...).

Outputs overwrite the standard episode deliverables (mp4 / captioned / srt)
so episode PRs can ship Chatterbox narration without a paid TTS API.
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import shutil
import subprocess
from pathlib import Path
from typing import Callable

import numpy as np
import soundfile as sf

from chatterbox_tts import SAMPLE_RATE, synth_beat
from generate_java_episode import ARTIFACTS, FPS, OUTPUT
from humanize_audio import generate_music_bed, probe

ROOT = Path(__file__).resolve().parent


def _gap_for(text: str) -> float:
    keys = (
        "Interview",
        "Three common",
        "Season",
        "Capstone",
        "Production",
        "Next episode",
        "See you",
    )
    if any(k in text for k in keys):
        return 0.30
    if text.endswith("?"):
        return 0.28
    return 0.12


def synth_scene_audio(audio_root: Path, scene_id: str, beats: list[str], clean: Callable[[str], str]):
    scene_dir = audio_root / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    audio {i+1}/{len(beats)} [chatterbox]: {text[:70]}")
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), synth_beat(text), SAMPLE_RATE)
        parts.append(wav)
        if i < len(beats) - 1:
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), np.zeros(int(_gap_for(text) * SAMPLE_RATE), dtype=np.float32), SAMPLE_RATE)
            parts.append(sil)
    lst = scene_dir / "list.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    out = audio_root / f"{scene_id}.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-q:a", "2", str(out)],
        check=True,
        capture_output=True,
    )
    return out


def _frame_job(args):
    renderer_fn, i, n, scene_dir = args
    progress = i / max(n - 1, 1)
    renderer_fn(progress, i / FPS).save(Path(scene_dir) / f"f{i:05d}.jpg", quality=85)
    return i


def render_scene_clip(
    audio_root: Path,
    frames_root: Path,
    clips_root: Path,
    scene_id: str,
    renderer_fn,
    duration: float,
):
    duration = max(duration + 0.25, 2.0)
    n = int(duration * FPS)
    scene_dir = frames_root / scene_id
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)
    print(f"  frames {scene_id}: {n}")
    with mp.Pool(max(2, min(6, os.cpu_count() or 4))) as pool:
        done = 0
        jobs = [(renderer_fn, i, n, str(scene_dir)) for i in range(n)]
        for _ in pool.imap_unordered(_frame_job, jobs, chunksize=8):
            done += 1
            if done % 90 == 0 or done == n:
                print(f"    {scene_id}: {done}/{n}")
    out = clips_root / f"{scene_id}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(scene_dir / "f%05d.jpg"),
            "-i", str(audio_root / f"{scene_id}.mp3"),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(scene_dir)
    return out


def write_srt(scenes, durations, clean, path: Path):
    def fmt(ts):
        h, m = int(ts // 3600), int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int(round((ts - int(ts)) * 1000))
        if ms == 1000:
            s += 1
            ms = 0
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    t = 0.0
    idx = 1
    lines = []
    for scene_id, _, beats in scenes:
        scene_dur = durations[scene_id] + 0.25
        weights = [max(len(b), 8) for b in beats]
        tw = sum(weights)
        for beat, w in zip(beats, weights):
            slot = scene_dur * (w / tw)
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{clean(beat)}\n")
            idx += 1
            t += slot
    path.write_text("\n".join(lines))


def run_episode(
    *,
    episode: int,
    scenes,
    renderers: dict,
    clean: Callable[[str], str],
    final_name: str,
    burned_name: str,
    srt_name: str,
    verify_stills: list[tuple[str, str]] | None = None,
):
    """Render one episode with Chatterbox narration into standard output names."""
    tag = f"ep{episode:02d}_cb"
    audio_root = ROOT / f"audio_{tag}"
    frames_root = ROOT / f"frames_{tag}"
    clips_root = ROOT / f"clips_{tag}"

    for p in [audio_root, frames_root, clips_root, OUTPUT, ARTIFACTS]:
        if p in (audio_root, frames_root, clips_root) and p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True, exist_ok=True)

    print(f"==> Chatterbox Episode {episode:02d}...")
    # Warm the model once before the scene loop
    synth_beat("Warming up Chatterbox for The Java Story.")

    for i, (sid, _, beats) in enumerate(scenes):
        print(f"  [{i+1}/{len(scenes)}] {sid}")
        synth_scene_audio(audio_root, sid, beats, clean)

    durations = {sid: probe(audio_root / f"{sid}.mp3") for sid, _, _ in scenes}
    spoken = (sum(durations.values()) + 0.25 * len(scenes)) / 60.0
    print(f"==> Spoken ≈ {spoken:.2f} min")
    (ROOT / f"ep{episode:02d}_chatterbox_durations.json").write_text(json.dumps(durations, indent=2))

    outs = [
        render_scene_clip(audio_root, frames_root, clips_root, sid, renderers[r], durations[sid])
        for sid, r, _ in scenes
    ]
    lst = ROOT / f"concat_ep{episode:02d}_chatterbox.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")

    narrated = OUTPUT / f"java_ep{episode:02d}_chatterbox_narrated.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated),
        ],
        check=True,
    )
    dur = probe(narrated)
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 245:
        # Slow down enough to land near 250s (ffmpeg atempo floor is 0.5).
        pace = max(dur / 250.0, 0.5)
    music = audio_root / "music_bed.m4a"
    generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / f"java_ep{episode:02d}_chatterbox_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(narrated),
                "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced),
            ],
            check=True,
        )
        base = paced

    final = OUTPUT / final_name
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(base), "-i", str(music),
            "-filter_complex",
            "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k",
            "-movflags", "+faststart", str(final),
        ],
        check=True,
    )
    shutil.copy2(final, ARTIFACTS / final.name)

    srt = OUTPUT / srt_name
    write_srt(scenes, durations, clean, srt)
    shutil.copy2(srt, ARTIFACTS / srt.name)

    burned = OUTPUT / burned_name
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(final),
            "-vf",
            f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy",
            "-movflags", "+faststart", str(burned),
        ],
        check=True,
    )
    shutil.copy2(burned, ARTIFACTS / burned.name)

    if verify_stills:
        vdir = ARTIFACTS / f"ep{episode:02d}_chatterbox_verify"
        vdir.mkdir(exist_ok=True)
        for ts, name in verify_stills:
            subprocess.run(
                ["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")],
                capture_output=True,
            )

    final_dur = probe(final)
    print(f"DONE Episode {episode:02d} Chatterbox: {final_dur/60:.2f} min")
    print(f"  {final}")
    print(f"  {burned}")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"
    return final_dur
