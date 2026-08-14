#!/usr/bin/env python3
"""Pilot: re-render Episode 81 narration with Sarvam (or Kokoro fallback).

Outputs distinct SARVAM-suffixed files so the Kokoro cut stays intact until approved.

  export SARVAM_API_KEY=...
  export TTS_PROVIDER=sarvam
  python3 java/video_build/make_episode_81_sarvam_pilot.py
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image  # noqa: F401 — used via imported renderers

sys.path.insert(0, "/workspace/java/video_build")
from generate_java_episode import (  # noqa: E402
    ARTIFACTS,
    FPS,
    OUTPUT,
)
from humanize_audio import generate_music_bed, probe  # noqa: E402
from narrate import make_synth_beat  # noqa: E402
from make_episode_81 import (  # noqa: E402
    RENDERERS,
    SCENES,
    clean,
)

ROOT = Path("/workspace/java/video_build")
TAG = "sarvam"
AUDIO, FRAMES, CLIPS = ROOT / f"audio_ep81_{TAG}", ROOT / f"frames_ep81_{TAG}", ROOT / f"clips_ep81_{TAG}"

PROVIDER, synth_beat, SAMPLE_RATE = make_synth_beat()


def synth_scene_audio(scene_id, beats):
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    audio {i+1}/{len(beats)} [{PROVIDER}]: {text[:70]}")
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), synth_beat(text), SAMPLE_RATE)
        parts.append(wav)
        if i < len(beats) - 1:
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Season", "Capstone", "Production")) else (0.28 if text.endswith("?") else 0.12)
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), np.zeros(int(gap * SAMPLE_RATE), dtype=np.float32), SAMPLE_RATE)
            parts.append(sil)
    lst = scene_dir / "list.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    out = AUDIO / f"{scene_id}.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-q:a", "2", str(out)],
        check=True,
        capture_output=True,
    )
    return out


def _frame_job(args):
    renderer, i, n, scene_dir = args
    progress = i / max(n - 1, 1)
    RENDERERS[renderer](progress, i / FPS).save(Path(scene_dir) / f"f{i:05d}.jpg", quality=85)
    return i


def render_scene_clip(scene_id, renderer, duration):
    duration = max(duration + 0.25, 2.0)
    n = int(duration * FPS)
    scene_dir = FRAMES / scene_id
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)
    print(f"  frames {scene_id}: {n}")
    with mp.Pool(max(2, min(6, os.cpu_count() or 4))) as pool:
        done = 0
        for _ in pool.imap_unordered(
            _frame_job, [(renderer, i, n, str(scene_dir)) for i in range(n)], chunksize=8
        ):
            done += 1
            if done % 90 == 0 or done == n:
                print(f"    {scene_id}: {done}/{n}")
    out = CLIPS / f"{scene_id}.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-framerate", str(FPS),
            "-i", str(scene_dir / "f%05d.jpg"),
            "-i", str(AUDIO / f"{scene_id}.mp3"),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(scene_dir)
    return out


def write_srt(durations, path):
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
    for scene_id, _, beats in SCENES:
        scene_dur = durations[scene_id] + 0.25
        weights = [max(len(b), 8) for b in beats]
        tw = sum(weights)
        for beat, w in zip(beats, weights):
            slot = scene_dur * (w / tw)
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{clean(beat)}\n")
            idx += 1
            t += slot
    path.write_text("\n".join(lines))


def main():
    print(f"==> Episode 81 pilot TTS provider: {PROVIDER}")
    if PROVIDER != "sarvam":
        print("WARNING: Sarvam key not set — falling back to Kokoro. Set SARVAM_API_KEY for realistic voice.")

    for p in [AUDIO, FRAMES, CLIPS, OUTPUT, ARTIFACTS]:
        if p in (AUDIO, FRAMES, CLIPS) and p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True, exist_ok=True)

    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}")
        synth_scene_audio(sid, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25 * len(SCENES)) / 60:.2f} min")
    (ROOT / f"ep81_{PROVIDER}_durations.json").write_text(json.dumps(durations, indent=2))

    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / f"concat_ep81_{PROVIDER}.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")

    narrated = OUTPUT / f"java_ep81_{PROVIDER}_narrated.mp4"
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
        pace = max(dur / 250.0, 0.85)
    music = AUDIO / "music_bed.m4a"
    generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / f"java_ep81_{PROVIDER}_paced.mp4"
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

    final = OUTPUT / f"Java_Episode_81_Caching_Strategies_{PROVIDER.upper()}.mp4"
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
    srt = OUTPUT / f"Java_Episode_81_{PROVIDER}.srt"
    write_srt(durations, srt)
    shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / f"Java_Episode_81_Caching_Strategies_{PROVIDER.upper()}_CAPTIONED.mp4"
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
    final_dur = probe(final)
    print(f"DONE Episode 81 {PROVIDER} pilot: {final_dur/60:.2f} min")
    print(f"  {final}")
    print(f"  {burned}")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
