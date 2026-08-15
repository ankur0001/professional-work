#!/usr/bin/env python3
"""Shared mux/render helpers for short Java episodes."""
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
from kokoro import KPipeline

from humanize_audio import generate_music_bed, probe

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))
FPS = 30


def clean(text: str) -> str:
    return " ".join(text.split()).strip()


def synth_beat(pipeline: KPipeline, text: str) -> np.ndarray:
    chunks = []
    for _, _, audio in pipeline(text, voice=VOICE, speed=SPEED):
        chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks:
        raise RuntimeError(text)
    return np.concatenate(chunks)


def synth_scene_audio(pipeline: KPipeline, audio_root: Path, scene_id: str, beats: list[str], gap_keys: tuple[str, ...] = ()) -> Path:
    scene_dir = audio_root / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    audio {i+1}/{len(beats)}: {text[:70]}")
        audio = synth_beat(pipeline, text)
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), audio, 24000)
        parts.append(wav)
        if i < len(beats) - 1:
            gap = 0.28 if text.endswith("?") else 0.12
            if any(k in text for k in gap_keys):
                gap = 0.30
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), np.zeros(int(gap * 24000), dtype=np.float32), 24000)
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
    renderer_name, renderers, i, n, scene_dir = args
    progress = i / max(n - 1, 1)
    t = i / FPS
    frame = renderers[renderer_name](progress, t)
    from pathlib import Path as P
    frame.save(P(scene_dir) / f"f{i:05d}.jpg", quality=85)
    return i


def render_scene_clip(audio_root: Path, frames_root: Path, clips_root: Path, scene_id: str, renderer: str, renderers: dict, duration: float) -> Path:
    duration = max(duration + 0.25, 2.0)
    n = int(duration * FPS)
    scene_dir = frames_root / scene_id
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)
    print(f"  frames {scene_id}: {n}")
    args = [(renderer, renderers, i, n, str(scene_dir)) for i in range(n)]
    workers = max(2, min(6, os.cpu_count() or 4))
    with mp.Pool(workers) as pool:
        done = 0
        for _ in pool.imap_unordered(_frame_job, args, chunksize=8):
            done += 1
            if done % 90 == 0 or done == n:
                print(f"    {scene_id}: {done}/{n}")
    out = clips_root / f"{scene_id}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS), "-i", str(scene_dir / "f%05d.jpg"),
            "-i", str(audio_root / f"{scene_id}.mp3"),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(scene_dir)
    return out


def write_srt(scenes, durations: dict[str, float], path: Path):
    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
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
    ep_num: str,
    title_slug: str,
    scenes: list,
    renderers: dict,
    audio_root: Path,
    frames_root: Path,
    clips_root: Path,
    output_dir: Path,
    artifacts: Path,
    durations_name: str,
    concat_name: str,
    verify_times: list[tuple[str, str]],
    gap_keys: tuple[str, ...] = ("Interview", "Three common", "Picture"),
):
    from generate_java_episode import ARTIFACTS, OUTPUT

    output_dir = OUTPUT
    artifacts = ARTIFACTS
    for p in [audio_root, frames_root, clips_root, output_dir, artifacts]:
        if p in (audio_root, frames_root, clips_root) and p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True, exist_ok=True)

    print(f"==> Kokoro narration (Episode {ep_num})...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _r, beats) in enumerate(scenes):
        print(f"  [{i+1}/{len(scenes)}] {sid}")
        synth_scene_audio(pipeline, audio_root, sid, beats, gap_keys)

    durations = {sid: probe(audio_root / f"{sid}.mp3") for sid, _, _ in scenes}
    total = sum(durations.values()) + 0.25 * len(scenes)
    print(f"==> Spoken ≈ {total/60:.2f} min")
    (audio_root.parent / durations_name).write_text(json.dumps(durations, indent=2))

    outs = []
    for sid, renderer, _ in scenes:
        outs.append(render_scene_clip(audio_root, frames_root, clips_root, sid, renderer, renderers, durations[sid]))

    lst = audio_root.parent / concat_name
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = output_dir / f"java_ep{ep_num}_narrated.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)],
        check=True,
    )

    dur = probe(narrated)
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 255:
        pace = max(dur / 260.0, 0.88)

    music = audio_root / "music_bed.m4a"
    generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = output_dir / f"java_ep{ep_num}_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)],
            check=True,
        )
        base = paced

    final = output_dir / f"Java_Episode_{ep_num}_{title_slug}.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)],
        check=True,
    )
    shutil.copy2(final, artifacts / final.name)

    srt = output_dir / f"Java_Episode_{ep_num}.srt"
    write_srt(scenes, durations, srt)
    shutil.copy2(srt, artifacts / srt.name)

    burned = output_dir / f"Java_Episode_{ep_num}_{title_slug}_CAPTIONED.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)],
        check=True,
    )
    shutil.copy2(burned, artifacts / burned.name)

    vdir = artifacts / f"ep{ep_num}_verify"
    vdir.mkdir(exist_ok=True)
    for tstamp, name in verify_times:
        subprocess.run(["ffmpeg", "-y", "-ss", tstamp, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)

    final_dur = probe(final)
    print(f"DONE Episode {ep_num}: {final_dur/60:.2f} min")
    assert 195 <= final_dur <= 330, f"duration {final_dur:.1f}s outside target"
    return final
