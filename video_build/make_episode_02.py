#!/usr/bin/env python3
"""
Episode 02 — JDK, JRE, and JVM (4–5 min, Kokoro).
Content adapted from Java & JVM Handbook Lesson 2.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
from kokoro import KPipeline

from humanize_audio import probe, generate_music_bed

ROOT = Path("/workspace/video_build")
AUDIO = ROOT / "audio_ep02"
CLIPS_IN = ROOT / "clips"
CLIPS_OUT = ROOT / "clips_ep02"
OUTPUT = Path("/workspace/output")
ARTIFACTS = Path("/opt/cursor/artifacts")

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))
EP = "02"

# (scene_id, visual_clip_id, beats)
SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "curiosity",
        [
            "In the last episode, we saw why Java survived.",
            "But here's where most beginners get confused.",
            "People say install Java… download the JDK… run on the JVM…",
            "Are those the same thing? No. And this tiny distinction changes everything.",
        ],
    ),
    (
        "title",
        "promise",
        [
            "Episode Two.",
            "JDK, JRE, and JVM — the three layers of the Java platform.",
        ],
    ),
    (
        "problem",
        "cpp_pain",
        [
            "Here's the real-world problem.",
            "Teams mix up development tools with the runtime.",
            "That leads to oversized containers, missing diagnostics in production,",
            "and different Java versions between build and runtime.",
            "Painful. Avoidable.",
        ],
    ),
    (
        "layers",
        "analogy",
        [
            "Think about it this way — three layers.",
            "The JVM executes bytecode. It's the engine.",
            "The JRE is the runtime — libraries and launchers to run programs.",
            "The JDK is the developer toolkit — compiler, jar, jlink, jcmd, diagnostics.",
            "JDK for develop. JRE for run. JVM is the engine inside.",
        ],
    ),
    (
        "history",
        "birth",
        [
            "Quick history note.",
            "Older Java setups shipped a separate JRE.",
            "Modern distributions usually ship a JDK.",
            "Production images can be trimmed with jlink — keep only what you need.",
        ],
    ),
    (
        "flow",
        "bytecode",
        [
            "Let's visualize what actually happens.",
            "javac compiles your .java files into .class bytecode.",
            "The launcher starts a JVM process.",
            "It creates memory areas, loads the main class, and begins execution.",
            "Watch carefully — the JVM is doing the heavy lifting.",
        ],
    ),
    (
        "hotspot",
        "bytecode",
        [
            "Most people run HotSpot — the common JVM implementation.",
            "It loads classes, interprets bytecode, then JIT-compiles hot paths.",
            "It also manages garbage collection and deep diagnostics — Flight Recorder, jmap, thread dumps.",
            "Other JVMs exist — OpenJ9, GraalVM — optimizing for startup or native images.",
            "But the bytecode contract stays the same.",
        ],
    ),
    (
        "memory",
        "memory",
        [
            "Here's a production gotcha.",
            "Runtime memory is not just the heap.",
            "You've got heap, metaspace, thread stacks, code cache, and native memory.",
            "If you set dash X m x equal to your container limit — you're already in trouble.",
            "Leave headroom. Always.",
        ],
    ),
    (
        "mistakes",
        "mistakes",
        [
            "Common mistakes.",
            "One: shipping a full JDK into every tiny container when a slim runtime would do.",
            "Two: compiling with Java twenty-one in CI… then running Java seventeen in production.",
            "Three: treating the JVM as a black box until production breaks.",
            "Don't worry — once you see the layers, these mistakes become obvious.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Interview question.",
            "What's the difference between JDK, JRE, and JVM?",
            "Answer cleanly: JVM executes bytecode.",
            "JRE provides the runtime to run Java apps.",
            "JDK adds development and diagnostic tools on top.",
            "In modern Java, you often install a JDK — and still think in these three layers.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "Now you can stop mixing the terms.",
            "JDK. JRE. JVM. Three layers. One platform.",
            "Next episode — Java program structure.",
            "public class, main, packages — what every line is actually doing.",
            "That's Episode Three. See you there.",
        ],
    ),
]


def clean(text: str) -> str:
    return " ".join(text.split()).strip()


def synth_beat(pipeline: KPipeline, text: str) -> np.ndarray:
    chunks = []
    for _, _, audio in pipeline(text, voice=VOICE, speed=SPEED):
        chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks:
        raise RuntimeError(text)
    return np.concatenate(chunks)


def silence(seconds: float, sr: int = 24000) -> np.ndarray:
    return np.zeros(max(1, int(seconds * sr)), dtype=np.float32)


def synth_scene(pipeline: KPipeline, scene_id: str, beats: list[str]) -> Path:
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    {i+1}/{len(beats)}: {text[:72]}")
        audio = synth_beat(pipeline, text)
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), audio, 24000)
        parts.append(wav)
        if i < len(beats) - 1:
            gap = 0.26 if text.endswith("?") else 0.12
            if any(k in text for k in ("Watch carefully", "Interview", "gotcha", "confused")):
                gap = 0.30
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), silence(gap), 24000)
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


def remux(scene_id: str, clip_id: str) -> Path:
    vin = CLIPS_IN / f"{clip_id}.mp4"
    if not vin.exists():
        # fallbacks for missing clip names
        fallbacks = {
            "curiosity": "curiosity3",
            "promise": "promise",
        }
        alt = CLIPS_IN / f"{fallbacks.get(clip_id, clip_id)}.mp4"
        if alt.exists():
            vin = alt
        else:
            # pick any existing
            vin = next(CLIPS_IN.glob("*.mp4"))
            print(f"    WARN missing {clip_id}, using {vin.name}")
    ain = AUDIO / f"{scene_id}.mp3"
    vout = CLIPS_OUT / f"{scene_id}.mp4"
    vd = probe(vin)
    ad = probe(ain)
    target = ad + 0.22
    if target > vd:
        pad = target - vd
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(vin),
            "-i",
            str(ain),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={pad:.3f}[v]",
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


def write_srt(durations: dict[str, float], out_path: Path):
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
    for scene_id, _, beats in SCENES:
        scene_dur = durations[scene_id] + 0.22
        weights = [max(len(b), 8) for b in beats]
        tw = sum(weights)
        for beat, w in zip(beats, weights):
            slot = scene_dur * (w / tw)
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{clean(beat)}\n")
            idx += 1
            t += slot
    out_path.write_text("\n".join(lines))


def main():
    if AUDIO.exists():
        shutil.rmtree(AUDIO)
    if CLIPS_OUT.exists():
        shutil.rmtree(CLIPS_OUT)
    AUDIO.mkdir(parents=True)
    CLIPS_OUT.mkdir(parents=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    # resolve curiosity clip alias
    if not (CLIPS_IN / "curiosity.mp4").exists() and (CLIPS_IN / "curiosity3.mp4").exists():
        shutil.copy2(CLIPS_IN / "curiosity3.mp4", CLIPS_IN / "curiosity.mp4")

    print(f"==> Episode {EP} voice={VOICE} speed={SPEED}")
    pipeline = KPipeline(lang_code="a" if VOICE.startswith("a") else "b", repo_id="hexgrad/Kokoro-82M")

    for i, (scene_id, _clip, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {scene_id}")
        synth_scene(pipeline, scene_id, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.22 * len(SCENES)
    print(f"==> Spoken ≈ {total/60:.2f} min ({total:.1f}s)")
    (ROOT / "ep02_durations.json").write_text(json.dumps(durations, indent=2))

    outs = []
    for scene_id, clip_id, _ in SCENES:
        print(f"  remux {scene_id} <- {clip_id}")
        outs.append(remux(scene_id, clip_id))

    lst = ROOT / "concat_ep02.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep02_narrated.mp4"
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
    print(f"==> Assembled {dur:.1f}s")
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 240:
        pace = max(dur / 245.0, 0.92)

    music = AUDIO / "music_bed.m4a"
    generate_music_bed((dur / pace) + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep02_paced.mp4"
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

    final = OUTPUT / "Java_Episode_02_JDK_JRE_JVM.mp4"
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
    shutil.copy2(final, ARTIFACTS / "Java_Episode_02_JDK_JRE_JVM.mp4")

    srt_path = OUTPUT / "Java_Episode_02.srt"
    write_srt(durations, srt_path)
    if abs(pace - 1.0) > 0.015:
        lines = srt_path.read_text().splitlines()
        out = []

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

        for line in lines:
            if "-->" in line:
                a, b = line.split(" --> ")
                out.append(f"{scale_ts(a.strip())} --> {scale_ts(b.strip())}")
            else:
                out.append(line)
        srt_path.write_text("\n".join(out) + "\n")
    shutil.copy2(srt_path, ARTIFACTS / "Java_Episode_02.srt")

    burned = OUTPUT / "Java_Episode_02_JDK_JRE_JVM_CAPTIONED.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-vf",
            f"subtitles={srt_path}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
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
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_02_JDK_JRE_JVM_CAPTIONED.mp4")

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
            str(ARTIFACTS / "narration_EP02_preview.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    final_dur = probe(final)
    print(f"DONE Episode 02: {final_dur/60:.2f} min ({final_dur:.1f}s)")
    assert 220 <= final_dur <= 330, f"Duration {final_dur} outside ~4–5 min"
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
