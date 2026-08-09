#!/usr/bin/env python3
"""
Episode 02 — JDK, JRE, JVM
Narration + on-screen graphics are authored TOGETHER (no reused Ep1 story clips).
"""

from __future__ import annotations

import json
import math
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

sys.path.insert(0, "/workspace/java/video_build")
from generate_java_episode import (  # noqa: E402
    ARTIFACTS,
    BG,
    BLUE,
    DARKER,
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
    draw_glow_circle,
    ease_out_cubic,
    font,
    mix,
    pill,
)
from humanize_audio import generate_music_bed, probe  # noqa: E402

ROOT = Path("/workspace/java/video_build")
AUDIO = ROOT / "audio_ep02m"
FRAMES = ROOT / "frames_ep02m"
CLIPS = ROOT / "clips_ep02m"

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))


# ─── Scene script: narration describes exactly what appears on screen ────────
# (id, renderer, beats)
SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "hook",
        [
            "In Episode One, we learned why Java survived.",
            "But beginners still mix three names — JDK, JRE, and JVM.",
            "They are not the same thing.",
            "Today we separate them — clearly — on screen.",
        ],
    ),
    (
        "title",
        "title",
        [
            "Episode Two.",
            "JDK, JRE, and JVM — the three layers of the Java platform.",
        ],
    ),
    (
        "layers",
        "layers",
        [
            "Look at these three boxes.",
            "At the top — the JDK. Your developer toolkit.",
            "In the middle — the JRE. What you need to run Java apps.",
            "At the bottom — the JVM. The engine that executes bytecode.",
            "JDK for develop. JRE for run. JVM is the engine inside.",
        ],
    ),
    (
        "jdk_tools",
        "jdk_tools",
        [
            "Zoom into the JDK.",
            "This is where javac lives — the compiler.",
            "Also jar, jlink, jcmd, jmap, and Java Flight Recorder tools.",
            "If you write code or debug production issues — you want the JDK.",
        ],
    ),
    (
        "jre_run",
        "jre_run",
        [
            "The JRE is the runtime layer.",
            "Libraries, launchers, and everything needed to start a Java process.",
            "It does not include the compiler.",
            "Modern installs often ship a JDK — but the runtime idea still matters.",
        ],
    ),
    (
        "jvm_engine",
        "jvm_engine",
        [
            "And here is the JVM.",
            "It loads class files, verifies bytecode, and runs your program.",
            "HotSpot is the common implementation — interpreter, JIT, garbage collection.",
            "Same bytecode contract. Different machines. Same result.",
        ],
    ),
    (
        "flow",
        "flow",
        [
            "Follow the arrows.",
            "Your .java file goes into javac — that tool comes from the JDK.",
            "Out comes a .class file — bytecode.",
            "The java launcher starts a JVM process.",
            "The JVM reads bytecode and runs it.",
            "That is the full path — develop, package, execute.",
        ],
    ),
    (
        "memory",
        "memory",
        [
            "Now the production gotcha.",
            "On screen — heap is only one slice of memory.",
            "Also metaspace, thread stacks, code cache, and native memory.",
            "If dash X m x equals your container limit — you leave no headroom.",
            "Always leave room beyond the heap.",
        ],
    ),
    (
        "mistakes",
        "mistakes",
        [
            "Three common mistakes.",
            "One — shipping a full JDK into every tiny container when a slim runtime would do.",
            "Two — compiling with Java twenty-one in CI, then running Java seventeen in production.",
            "Three — treating the JVM as a black box until something breaks.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Interview question — what's the difference between JDK, JRE, and JVM?",
            "Point to the diagram.",
            "JVM executes bytecode.",
            "JRE provides the runtime to launch apps.",
            "JDK adds compilers and diagnostics on top.",
            "Answer that calmly — and you sound like you've shipped Java.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "Now the three names finally line up with the picture.",
            "Next episode — Java program structure.",
            "public class, main, packages — what every line is doing.",
            "Episode Three. See you there.",
        ],
    ),
]


# ─── Visual renderers (must match narration) ─────────────────────────────────
def render_hook(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    f = font(FONT_SERIF, 54)
    title = "JDK  ·  JRE  ·  JVM"
    bbox = d.textbbox((0, 0), title, font=f)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 180), title, font=f, fill=WHITE)
    # three confused chips
    labels = [("JDK", ORANGE), ("JRE", BLUE), ("JVM", GREEN)]
    for i, (lab, col) in enumerate(labels):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.35))
        x = 420 + i * 360
        y = 420
        d.rounded_rectangle(
            [x, y, x + 280, y + 160],
            radius=18,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((x + 90, y + 55), lab, font=font(FONT_BOLD, 48), fill=mix(BG, col, a))
    if progress > 0.55:
        q = "Same thing?  No."
        bbox = d.textbbox((0, 0), q, font=font(FONT_REG, 36))
        d.text(((W - (bbox[2] - bbox[0])) // 2, 680), q, font=font(FONT_REG, 36), fill=MUTED)
    return img.convert("RGB")


def render_title(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(220 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 02", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("JDK, JRE & JVM", font(FONT_SERIF, 72), H // 2 - 30, mix(BG, WHITE, a)),
        ("Three layers of the Java platform", font(FONT_REG, 32), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_layers(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "Three Layers"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=font(FONT_SERIF, 48), fill=WHITE)

    layers = [
        ("JDK", "Develop & diagnose", "javac · jar · jlink · jcmd", ORANGE, 0.15),
        ("JRE", "Run applications", "libraries · launchers", BLUE, 0.35),
        ("JVM", "Execute bytecode", "engine inside the runtime", GREEN, 0.55),
    ]
    for i, (name, role, tools, col, start) in enumerate(layers):
        a = ease_out_cubic(clamp((progress - start) / 0.3))
        if a <= 0:
            continue
        y = 200 + i * 220
        d.rounded_rectangle(
            [360, y, 1560, y + 180],
            radius=20,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=4,
        )
        d.text((420, y + 40), name, font=font(FONT_BOLD, 48), fill=mix(BG, col, a))
        d.text((420, y + 105), role, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
        d.text((980, y + 70), tools, font=font(FONT_MONO, 24), fill=mix(BG, MUTED, a))
        if i < 2 and progress > start + 0.25:
            d.polygon([(960, y + 190), (980, y + 210), (940, y + 210)], fill=ORANGE)
    return img.convert("RGB")


def render_jdk_tools(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 80), "Inside the JDK", font=font(FONT_SERIF, 48), fill=WHITE)
    d.rounded_rectangle([160, 180, 1760, 900], radius=20, fill=SURFACE, outline=ORANGE, width=4)
    d.text((220, 220), "JDK", font=font(FONT_BOLD, 56), fill=ORANGE)
    tools = [
        ("javac", "compiler"),
        ("jar", "packaging"),
        ("jlink", "custom runtime"),
        ("jcmd", "diagnostics"),
        ("jmap", "heap tools"),
        ("jfr", "flight recorder"),
    ]
    for i, (name, desc) in enumerate(tools):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.3))
        if a <= 0:
            continue
        col = i % 3
        x = 260 + (i % 3) * 480
        y = 340 + (i // 3) * 220
        d.rounded_rectangle(
            [x, y, x + 400, y + 160],
            radius=16,
            fill=mix(SURFACE, BG, 0.2),
            outline=mix(BG, ORANGE if col == 0 else BLUE, a),
            width=2,
        )
        d.text((x + 40, y + 40), name, font=font(FONT_MONO_B, 36), fill=mix(BG, ORANGE, a))
        d.text((x + 40, y + 95), desc, font=font(FONT_REG, 26), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_jre_run(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 80), "JRE — Runtime Layer", font=font(FONT_SERIF, 48), fill=WHITE)
    d.rounded_rectangle([200, 220, 900, 820], radius=20, fill=SURFACE, outline=BLUE, width=4)
    d.text((280, 280), "Includes", font=font(FONT_BOLD, 32), fill=BLUE)
    for i, item in enumerate(["Core libraries", "java launcher", "Runtime classes"]):
        a = ease_out_cubic(clamp((progress - 0.1 - i * 0.15) / 0.3))
        d.text((280, 380 + i * 80), f"•  {item}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, a))
    d.rounded_rectangle([1020, 220, 1720, 820], radius=20, fill=SURFACE, outline=RED, width=3)
    d.text((1100, 280), "Does NOT include", font=font(FONT_BOLD, 32), fill=RED)
    for i, item in enumerate(["javac compiler", "Many JDK debug tools"]):
        a = ease_out_cubic(clamp((progress - 0.35 - i * 0.15) / 0.3))
        d.text((1100, 400 + i * 80), f"•  {item}", font=font(FONT_REG, 30), fill=mix(BG, MUTED, a))
    if progress > 0.7:
        note = "Modern installs often ship a JDK — the runtime idea still matters."
        bbox = d.textbbox((0, 0), note, font=font(FONT_REG, 28))
        d.text(((W - (bbox[2] - bbox[0])) // 2, 880), note, font=font(FONT_REG, 28), fill=MUTED)
    return img.convert("RGB")


def render_jvm_engine(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glow_circle(overlay, (W // 2, 380), 140 + int(12 * math.sin(t * 2)), GREEN, 0.7)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    d.text((W // 2 - 80, 120), "JVM", font=font(FONT_SERIF, 64), fill=WHITE)
    d.text((W // 2 - 200, 200), "The execution engine", font=font(FONT_REG, 30), fill=MUTED)
    features = [
        ("Class loading", BLUE),
        ("Bytecode verify", ORANGE),
        ("Interpreter", MUTED),
        ("JIT (C1/C2)", GREEN),
        ("Garbage collection", BLUE),
        ("HotSpot runtime", ORANGE),
    ]
    for i, (name, col) in enumerate(features):
        a = ease_out_cubic(clamp((progress - i * 0.08) / 0.3))
        if a <= 0:
            continue
        x = 220 + (i % 3) * 520
        y = 520 + (i // 3) * 180
        d.rounded_rectangle(
            [x, y, x + 440, y + 120],
            radius=16,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((x + 40, y + 40), name, font=font(FONT_BOLD, 30), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_flow(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Develop → Package → Execute", font=font(FONT_SERIF, 44), fill=WHITE)
    stages = [
        (".java", "Source", ORANGE, "you write"),
        ("javac", "JDK tool", BLUE, "compiler"),
        (".class", "Bytecode", GREEN, "portable"),
        ("java", "Launcher", ORANGE, "starts JVM"),
        ("JVM", "Engine", BLUE, "runs it"),
    ]
    packet = clamp(progress) * (len(stages) - 1)
    for i, (top, mid, col, bot) in enumerate(stages):
        x = 80 + i * 370
        y = 320
        active = packet >= i - 0.15
        d.rounded_rectangle(
            [x, y, x + 300, y + 280],
            radius=18,
            fill=SURFACE if active else mix(BG, SURFACE, 0.4),
            outline=col if active else mix(BG, MUTED, 0.35),
            width=3,
        )
        d.text((x + 70, y + 50), top, font=font(FONT_MONO_B, 36), fill=col if active else MUTED)
        d.text((x + 70, y + 120), mid, font=font(FONT_BOLD, 28), fill=WHITE if active else MUTED)
        d.text((x + 70, y + 180), bot, font=font(FONT_REG, 24), fill=MUTED)
        if i < len(stages) - 1:
            ax = x + 310
            d.polygon(
                [(ax, y + 130), (ax + 40, y + 145), (ax, y + 160)],
                fill=ORANGE if packet > i else mix(BG, MUTED, 0.4),
            )
    # layer tags under path
    tags = [(200, "JDK"), (900, "Runtime"), (1500, "JVM")]
    for x, lab in tags:
        if progress > 0.4:
            pill(d, lab, (x, 720), font(FONT_BOLD, 22), fg=BG, bg=ORANGE if lab == "JDK" else BLUE)
    return img.convert("RGB")


def render_memory(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "JVM Memory ≠ only Heap", font=font(FONT_SERIF, 44), fill=WHITE)
    # container box
    d.rounded_rectangle([200, 180, 1720, 780], radius=18, fill=SURFACE, outline=MUTED, width=2)
    d.text((240, 210), "Container / Process memory limit", font=font(FONT_BOLD, 28), fill=MUTED)
    slices = [
        ("Heap (-Xmx)", 0.42, ORANGE),
        ("Metaspace", 0.14, BLUE),
        ("Thread stacks", 0.12, GREEN),
        ("Code cache", 0.10, MUTED),
        ("Native / other", 0.22, RED),
    ]
    x0, y0, x1, y1 = 260, 300, 1660, 520
    total_w = x1 - x0
    x = x0
    shown = 0.0
    for name, frac, col in slices:
        shown += frac
        a = ease_out_cubic(clamp((progress - shown * 0.5) / 0.35))
        w = int(total_w * frac)
        if a > 0:
            d.rectangle([x, y0, x + w - 6, y1], fill=mix(BG, col, 0.55 + 0.35 * a))
            d.text((x + 12, y0 + 70), name, font=font(FONT_BOLD, 22), fill=WHITE)
        x += w
    # warning
    warn_a = ease_out_cubic(clamp((progress - 0.55) / 0.3))
    if warn_a > 0:
        d.rounded_rectangle(
            [260, 580, 1660, 720],
            radius=14,
            fill=mix(BG, (40, 20, 20), warn_a),
            outline=mix(BG, RED, warn_a),
            width=3,
        )
        msg = "Wrong: -Xmx == container limit     Right: leave headroom for non-heap"
        d.text((320, 630), msg, font=font(FONT_REG, 30), fill=mix(BG, WHITE, warn_a))
    return img.convert("RGB")


def render_mistakes(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [
        ("01", "Full JDK in every tiny container", "Use a slim runtime / jlink image when possible"),
        ("02", "CI = Java 21, Prod = Java 17", "Keep build and runtime versions aligned"),
        ("03", "JVM as a black box", "Learn flags, GC, and diagnostics before incidents"),
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
    d.rounded_rectangle([160, 160, 1760, 300], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "What's the difference between JDK, JRE, and JVM?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 210), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [
        ("JVM", "Executes bytecode — the engine"),
        ("JRE", "Runtime libraries + launcher to run apps"),
        ("JDK", "Compiler + diagnostics on top of the runtime"),
    ]
    for i, (k, v) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0:
            continue
        y = 360 + i * 160
        col = [GREEN, BLUE, ORANGE][i]
        d.rounded_rectangle(
            [260, y, 1660, y + 130],
            radius=14,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((320, y + 40), k, font=font(FONT_BOLD, 36), fill=mix(BG, col, a))
        d.text((520, y + 45), v, font=font(FONT_REG, 30), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Java Program Structure"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 60))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 60), fill=WHITE)
    sub = "public class · main · packages"
    bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 50), sub, font=font(FONT_REG, 32), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 140), "Episode 03", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "layers": render_layers,
    "jdk_tools": render_jdk_tools,
    "jre_run": render_jre_run,
    "jvm_engine": render_jvm_engine,
    "flow": render_flow,
    "memory": render_memory,
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
            if any(k in text for k in ("Look at", "Follow", "Interview", "gotcha", "Zoom")):
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

    print("==> Kokoro narration (matched to visuals)...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _r, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}")
        synth_scene_audio(pipeline, sid, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.25 * len(SCENES)
    print(f"==> Spoken ≈ {total/60:.2f} min")
    (ROOT / "ep02_matched_durations.json").write_text(json.dumps(durations, indent=2))

    print("==> Rendering matching visuals...")
    outs = []
    for sid, renderer, _ in SCENES:
        outs.append(render_scene_clip(sid, renderer, durations[sid]))

    lst = ROOT / "concat_ep02m.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep02_matched_narrated.mp4"
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
        paced = OUTPUT / "java_ep02_matched_paced.mp4"
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

    srt = OUTPUT / "Java_Episode_02.srt"
    write_srt(durations, srt)
    shutil.copy2(srt, ARTIFACTS / "Java_Episode_02.srt")

    burned = OUTPUT / "Java_Episode_02_JDK_JRE_JVM_CAPTIONED.mp4"
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
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_02_JDK_JRE_JVM_CAPTIONED.mp4")

    # verification stills
    vdir = ARTIFACTS / "ep02_verify"
    vdir.mkdir(exist_ok=True)
    for tstamp, name in [
        ("00:00:10", "01_hook_names"),
        ("00:00:45", "02_three_layers"),
        ("00:01:30", "03_jdk_tools"),
        ("00:02:20", "04_flow"),
        ("00:03:10", "05_memory"),
        ("00:03:40", "06_interview"),
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
            str(ARTIFACTS / "narration_EP02_preview.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    final_dur = probe(final)
    print(f"DONE matched Episode 02: {final_dur/60:.2f} min")
    assert 220 <= final_dur <= 330
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
