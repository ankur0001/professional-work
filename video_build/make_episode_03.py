#!/usr/bin/env python3
"""
Episode 03 — Java Program Structure
Narration + on-screen graphics are authored TOGETHER (no reused story clips).
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
from kokoro import KPipeline
from PIL import Image, ImageDraw

sys.path.insert(0, "/workspace/video_build")
from generate_java_episode import (  # noqa: E402
    ARTIFACTS,
    BG,
    BLUE,
    FONT_BOLD,
    FONT_MONO,
    FONT_MONO_B,
    FONT_REG,
    FONT_SERIF,
    FPS,
    GREEN,
    H,
    MUTED,
    ORANGE,
    OUTPUT,
    RED,
    SURFACE,
    W,
    WHITE,
    base_canvas,
    clamp,
    ease_out_cubic,
    font,
    mix,
)
from humanize_audio import generate_music_bed, probe  # noqa: E402

ROOT = Path("/workspace/video_build")
AUDIO = ROOT / "audio_ep03"
FRAMES = ROOT / "frames_ep03"
CLIPS = ROOT / "clips_ep03"

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))


# ─── Scene script: narration describes exactly what appears on screen ────────
SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "hook",
        [
            "In Episode Two, we separated JDK, JRE, and JVM.",
            "Now look at a real Java file.",
            "Every line has a job — package, class, main, statements.",
            "Structure is not decoration. It decides how your code is found, loaded, and owned.",
        ],
    ),
    (
        "title",
        "title",
        [
            "Episode Three.",
            "Java Program Structure — packages, classes, and the entry point.",
        ],
    ),
    (
        "anatomy",
        "anatomy",
        [
            "Here is the shape of a Java program.",
            "A package is the folder — the namespace.",
            "Inside it — a type. Usually a class.",
            "Inside the class — fields, constructors, and methods.",
            "That hierarchy is the blueprint Java expects.",
        ],
    ),
    (
        "hello",
        "hello",
        [
            "Walk a classic Hello World — line by line.",
            "First, optional package — the fully qualified home of the class.",
            "Then public class HelloWorld — filename must match.",
            "public static void main — the JVM starts here.",
            "System.out.println — a statement that prints a line.",
            "Four jobs. Four layers. One program.",
        ],
    ),
    (
        "access",
        "access",
        [
            "Access is part of structure too.",
            "public means other packages can see it.",
            "No modifier means package-private — same package only.",
            "private fields keep state inside the class.",
            "Good structure hides what shouldn't leak.",
        ],
    ),
    (
        "packages",
        "packages",
        [
            "In real services, packages mirror ownership.",
            "api at the edge. application to orchestrate.",
            "domain for business rules. infrastructure for databases and adapters.",
            "Arrows should point inward — not dump everything into one flat folder.",
        ],
    ),
    (
        "flow",
        "flow",
        [
            "Follow runtime.",
            "Load the class. Verify bytecode. Prepare statics.",
            "Initialize. Construct objects. Invoke methods.",
            "Your package and class names become the identity the JVM loads.",
        ],
    ),
    (
        "mistakes",
        "mistakes",
        [
            "Three common mistakes.",
            "One — every class in one giant package.",
            "Two — public fields everywhere — no encapsulation.",
            "Three — Spring main class buried too deep, so component scanning misses your beans.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Interview question — why do packages matter?",
            "Answer with four words on screen.",
            "Namespacing. Access. Ownership. Framework scanning.",
            "Then add — class identity is the name plus the classloader.",
            "That answer shows you understand design and runtime.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "You can now read a Java file like a map.",
            "Next — variables and data types.",
            "int, long, boolean, String — what lives where in memory.",
            "Episode Four. See you there.",
        ],
    ),
]


def render_hook(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "A Java file is a map"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 52))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 140), title, font=font(FONT_SERIF, 52), fill=WHITE)

    lines = [
        ("package com.example;", MUTED),
        ("public class HelloWorld {", ORANGE),
        ("  public static void main(...) {", BLUE),
        ("    System.out.println(...);", GREEN),
        ("  }", MUTED),
        ("}", MUTED),
    ]
    d.rounded_rectangle([360, 260, 1560, 860], radius=18, fill=SURFACE, outline=BLUE, width=3)
    for i, (line, col) in enumerate(lines):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.35))
        d.text((440, 320 + i * 80), line, font=font(FONT_MONO, 34), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 03", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Java Program Structure", font(FONT_SERIF, 64), H // 2 - 30, mix(BG, WHITE, a)),
        ("Packages · classes · entry point", font(FONT_REG, 32), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_anatomy(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "Program Anatomy"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 70), title, font=font(FONT_SERIF, 48), fill=WHITE)

    nodes = [
        (0.10, 200, 220, 1520, 160, "package", "namespace / folder boundary", ORANGE),
        (0.30, 280, 420, 1440, 200, "class / interface / record / enum", "the type you compile", BLUE),
        (0.55, 360, 660, 560, 200, "fields", "state", GREEN),
        (0.65, 700, 660, 560, 200, "constructors", "create objects", ORANGE),
        (0.75, 1040, 660, 560, 200, "methods", "behavior", BLUE),
    ]
    for start, x, y, w, hgt, name, sub, col in nodes:
        a = ease_out_cubic(clamp((progress - start) / 0.28))
        if a <= 0:
            continue
        d.rounded_rectangle(
            [x, y, x + w, y + hgt],
            radius=16,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((x + 36, y + 40), name, font=font(FONT_BOLD, 34), fill=mix(BG, col, a))
        d.text((x + 36, y + 100), sub, font=font(FONT_REG, 26), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_hello(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((140, 60), "Hello World — Line by Line", font=font(FONT_SERIF, 44), fill=WHITE)

    steps = [
        ("01", "package", "optional home — fully qualified name", "package com.example;"),
        ("02", "public class", "filename must match class name", "public class HelloWorld {"),
        ("03", "main", "JVM entry point", "public static void main(String[] args)"),
        ("04", "statement", "work happens here", "System.out.println(\"Hello\");"),
    ]
    for i, (num, label, note, code) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.32))
        if a <= 0:
            continue
        y = 150 + i * 200
        d.rounded_rectangle(
            [140, y, 1780, y + 170],
            radius=14,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, ORANGE if i % 2 == 0 else BLUE, a),
            width=2,
        )
        d.text((180, y + 35), num, font=font(FONT_SERIF, 36), fill=mix(BG, ORANGE, a))
        d.text((280, y + 30), label, font=font(FONT_BOLD, 34), fill=mix(BG, WHITE, a))
        d.text((280, y + 80), note, font=font(FONT_REG, 26), fill=mix(BG, MUTED, a))
        d.text((980, y + 55), code, font=font(FONT_MONO, 24), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_access(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Access Is Structure", font=font(FONT_SERIF, 48), fill=WHITE)
    cards = [
        ("public", "Visible across packages", ORANGE, 0.1),
        ("(default)", "Package-private — same package only", BLUE, 0.35),
        ("private", "Hidden inside the class", GREEN, 0.6),
    ]
    for i, (name, desc, col, start) in enumerate(cards):
        a = ease_out_cubic(clamp((progress - start) / 0.3))
        if a <= 0:
            continue
        x = 180 + i * 560
        d.rounded_rectangle(
            [x, 280, x + 500, 720],
            radius=18,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=4,
        )
        d.text((x + 60, 360), name, font=font(FONT_MONO_B, 40), fill=mix(BG, col, a))
        # wrap desc
        d.text((x + 60, 480), desc, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    if progress > 0.75:
        tip = "Good structure hides what shouldn't leak."
        bbox = d.textbbox((0, 0), tip, font=font(FONT_REG, 30))
        d.text(((W - (bbox[2] - bbox[0])) // 2, 820), tip, font=font(FONT_REG, 30), fill=MUTED)
    return img.convert("RGB")


def render_packages(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Packages Mirror Ownership", font=font(FONT_SERIF, 46), fill=WHITE)
    layers = [
        ("api", "HTTP / DTOs / controllers", ORANGE),
        ("application", "use-cases / orchestration", BLUE),
        ("domain", "business rules & types", GREEN),
        ("infrastructure", "DB, messaging, adapters", MUTED),
    ]
    for i, (name, role, col) in enumerate(layers):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0:
            continue
        y = 170 + i * 180
        d.rounded_rectangle(
            [280, y, 1640, y + 150],
            radius=16,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((340, y + 45), name, font=font(FONT_MONO_B, 36), fill=mix(BG, col, a))
        d.text((780, y + 50), role, font=font(FONT_REG, 30), fill=mix(BG, WHITE, a))
        if i < 3 and progress > i * 0.15 + 0.2:
            d.polygon([(960, y + 155), (980, y + 175), (940, y + 175)], fill=ORANGE)
    return img.convert("RGB")


def render_flow(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Runtime Flow", font=font(FONT_SERIF, 48), fill=WHITE)
    steps = ["Load", "Verify", "Prepare", "Initialize", "Construct", "Invoke"]
    for i, name in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        if a <= 0:
            continue
        x = 120 + i * 300
        y = 380
        d.rounded_rectangle(
            [x, y, x + 260, y + 160],
            radius=14,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, ORANGE if i == 0 else BLUE, a),
            width=3,
        )
        d.text((x + 40, y + 55), name, font=font(FONT_BOLD, 32), fill=mix(BG, WHITE, a))
        if i < len(steps) - 1 and progress > i * 0.12 + 0.15:
            d.polygon([(x + 270, y + 70), (x + 290, y + 80), (x + 270, y + 90)], fill=ORANGE)
    note_a = ease_out_cubic(clamp((progress - 0.7) / 0.25))
    if note_a > 0:
        note = "Identity = fully qualified name + defining classloader"
        bbox = d.textbbox((0, 0), note, font=font(FONT_REG, 30))
        d.text(((W - (bbox[2] - bbox[0])) // 2, 700), note, font=font(FONT_REG, 30), fill=mix(BG, MUTED, note_a))
    return img.convert("RGB")


def render_mistakes(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [
        ("01", "One giant package for everything", "Split by ownership / capability"),
        ("02", "Public fields everywhere", "Encapsulate — private fields, clear APIs"),
        ("03", "Spring main class buried too deep", "Place it at a sensible root for scanning"),
    ]
    for i, (num, wrong, right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0:
            continue
        y = 180 + i * 240
        d.rounded_rectangle(
            [200, y, 1720, y + 200],
            radius=16,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, RED, a * 0.7),
            width=2,
        )
        d.text((260, y + 40), num, font=font(FONT_SERIF, 40), fill=mix(BG, ORANGE, a))
        d.text((360, y + 45), wrong, font=font(FONT_BOLD, 30), fill=mix(BG, RED, a))
        d.text((360, y + 110), right, font=font(FONT_REG, 28), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_interview(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Interview Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "Why do packages matter in Java?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 34))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 34), fill=WHITE)

    answers = [
        ("Namespacing", "unique fully qualified names"),
        ("Access", "package-private collaboration"),
        ("Ownership", "clear team / domain boundaries"),
        ("Scanning", "frameworks find your components"),
    ]
    for i, (k, v) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.15 - i * 0.14) / 0.28))
        if a <= 0:
            continue
        x = 180 + (i % 2) * 860
        y = 340 + (i // 2) * 220
        col = [ORANGE, BLUE, GREEN, MUTED][i]
        d.rounded_rectangle(
            [x, y, x + 780, y + 180],
            radius=14,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((x + 40, y + 40), k, font=font(FONT_BOLD, 34), fill=mix(BG, col, a))
        d.text((x + 40, y + 100), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))

    tip_a = ease_out_cubic(clamp((progress - 0.75) / 0.2))
    if tip_a > 0:
        tip = "Bonus: class identity = name + classloader"
        bbox = d.textbbox((0, 0), tip, font=font(FONT_REG, 28))
        d.text(((W - (bbox[2] - bbox[0])) // 2, 820), tip, font=font(FONT_REG, 28), fill=mix(BG, MUTED, tip_a))
    return img.convert("RGB")


def render_teaser(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Variables & Data Types"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 60))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 60), fill=WHITE)
    sub = "int · long · boolean · String · memory"
    bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 50), sub, font=font(FONT_REG, 32), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 140), "Episode 04", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "anatomy": render_anatomy,
    "hello": render_hello,
    "access": render_access,
    "packages": render_packages,
    "flow": render_flow,
    "mistakes": render_mistakes,
    "interview": render_interview,
    "teaser": render_teaser,
}


def clean(text: str) -> str:
    return " ".join(text.split()).strip()


def synth_beat(pipeline: KPipeline, text: str) -> np.ndarray:
    chunks = []
    for _, _, audio in pipeline(text, voice=VOICE, speed=SPEED):
        chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks:
        raise RuntimeError(text)
    return np.concatenate(chunks)


def synth_scene_audio(pipeline: KPipeline, scene_id: str, beats: list[str]) -> Path:
    scene_dir = AUDIO / scene_id
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
            if any(k in text for k in ("Look", "Walk", "Follow", "Interview", "Three common")):
                gap = 0.30
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), np.zeros(int(gap * 24000), dtype=np.float32), 24000)
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
    t = i / FPS
    frame = RENDERERS[renderer](progress, t)
    frame.save(Path(scene_dir) / f"f{i:05d}.jpg", quality=85)
    return i


def render_scene_clip(scene_id: str, renderer: str, duration: float) -> Path:
    duration = max(duration + 0.25, 2.0)
    n = int(duration * FPS)
    scene_dir = FRAMES / scene_id
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)
    print(f"  frames {scene_id}: {n}")
    args = [(renderer, i, n, str(scene_dir)) for i in range(n)]
    workers = max(2, min(6, os.cpu_count() or 4))
    with mp.Pool(workers) as pool:
        done = 0
        for _ in pool.imap_unordered(_frame_job, args, chunksize=8):
            done += 1
            if done % 90 == 0 or done == n:
                print(f"    {scene_id}: {done}/{n}")
    out = CLIPS / f"{scene_id}.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(scene_dir / "f%05d.jpg"),
            "-i",
            str(AUDIO / f"{scene_id}.mp3"),
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
            "-shortest",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(scene_dir)
    return out


def write_srt(durations: dict[str, float], path: Path):
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
    for p in [AUDIO, FRAMES, CLIPS, OUTPUT, ARTIFACTS]:
        if p in (AUDIO, FRAMES, CLIPS) and p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True, exist_ok=True)

    print("==> Kokoro narration (Episode 03, matched to visuals)...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _r, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}")
        synth_scene_audio(pipeline, sid, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.25 * len(SCENES)
    print(f"==> Spoken ≈ {total/60:.2f} min")
    (ROOT / "ep03_durations.json").write_text(json.dumps(durations, indent=2))

    print("==> Rendering matching visuals...")
    outs = []
    for sid, renderer, _ in SCENES:
        outs.append(render_scene_clip(sid, renderer, durations[sid]))

    lst = ROOT / "concat_ep03.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep03_narrated.mp4"
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
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 240:
        pace = max(dur / 245.0, 0.92)

    music = AUDIO / "music_bed.m4a"
    generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        paced = OUTPUT / "java_ep03_paced.mp4"
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

    final = OUTPUT / "Java_Episode_03_Program_Structure.mp4"
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
    shutil.copy2(final, ARTIFACTS / "Java_Episode_03_Program_Structure.mp4")

    srt = OUTPUT / "Java_Episode_03.srt"
    write_srt(durations, srt)
    shutil.copy2(srt, ARTIFACTS / "Java_Episode_03.srt")

    burned = OUTPUT / "Java_Episode_03_Program_Structure_CAPTIONED.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-vf",
            f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
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
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_03_Program_Structure_CAPTIONED.mp4")

    vdir = ARTIFACTS / "ep03_verify"
    vdir.mkdir(exist_ok=True)
    for tstamp, name in [
        ("00:00:12", "01_hook_map"),
        ("00:00:40", "02_anatomy"),
        ("00:01:20", "03_hello_lines"),
        ("00:02:10", "04_packages"),
        ("00:02:50", "05_flow"),
        ("00:03:30", "06_interview"),
    ]:
        subprocess.run(
            ["ffmpeg", "-y", "-ss", tstamp, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")],
            capture_output=True,
        )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-t",
            "35",
            "-vn",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(ARTIFACTS / "narration_EP03_preview.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    final_dur = probe(final)
    print(f"DONE Episode 03: {final_dur/60:.2f} min")
    assert 220 <= final_dur <= 330
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
