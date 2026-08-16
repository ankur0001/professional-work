#!/usr/bin/env python3
"""
Java Episode 1 — Why Java Exists
Premium motion-graphics documentary renderer (1080p / 30fps).
"""

from __future__ import annotations

import asyncio
import json
import math
import multiprocessing as mp
import os
import random
import shutil
import subprocess
import wave
from dataclasses import dataclass
from pathlib import Path

import edge_tts
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ─── Paths & constants ───────────────────────────────────────────────────────
ROOT = Path("/workspace/video_build")
ASSETS = ROOT / "assets"
FRAMES = ROOT / "frames"
AUDIO = ROOT / "audio"
CLIPS = ROOT / "clips"
OUTPUT = Path("/workspace/output")
ARTIFACTS = Path("/opt/cursor/artifacts")

W, H = 1920, 1080
FPS = 30
BG = (13, 17, 23)
SURFACE = (22, 27, 34)
ORANGE = (248, 152, 32)
BLUE = (74, 158, 255)
WHITE = (255, 255, 255)
MUTED = (139, 148, 158)
GREEN = (63, 185, 80)
RED = (248, 81, 73)
DARKER = (8, 10, 14)

FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
FONT_SERIF_R = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
FONT_MONO = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"
FONT_MONO_B = "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"

VOICE = "en-IN-PrabhatNeural"
random.seed(42)
np.random.seed(42)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def ease_in_out(t: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * t)


def clamp(v: float, a: float = 0.0, b: float = 1.0) -> float:
    return max(a, min(b, v))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def mix(c1, c2, t: float):
    t = clamp(t)
    return tuple(int(lerp(c1[i], c2[i], t)) for i in range(3))


_GRAD_CACHE = None


def draw_gradient(img: Image.Image, top=None, bottom=None):
    global _GRAD_CACHE
    top = top or BG
    bottom = bottom or DARKER
    if _GRAD_CACHE is None:
        arr = np.zeros((H, W, 3), dtype=np.uint8)
        for y in range(H):
            t = y / (H - 1)
            arr[y, :] = mix(top, bottom, t)
        _GRAD_CACHE = Image.fromarray(arr, "RGB")
    img.paste(_GRAD_CACHE)


def draw_grid(draw: ImageDraw.ImageDraw, alpha_boost: float = 0.0, offset: float = 0.0):
    spacing = 80
    color = mix(BG, (40, 48, 60), 0.35 + alpha_boost * 0.2)
    ox = int(offset) % spacing
    for x in range(-spacing + ox, W + spacing, spacing):
        draw.line([(x, 0), (x, H)], fill=color, width=1)
    for y in range(0, H, spacing):
        draw.line([(0, y), (W, y)], fill=color, width=1)


def draw_glow_circle(base: Image.Image, xy, r: int, color, strength: float = 0.55):
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i in range(6, 0, -1):
        rr = int(r * (1 + i * 0.35))
        a = int(28 * strength * (i / 6))
        d.ellipse([xy[0] - rr, xy[1] - rr, xy[0] + rr, xy[1] + rr], fill=(*color, a))
    d.ellipse([xy[0] - r, xy[1] - r, xy[0] + r, xy[1] + r], fill=(*color, int(180 * strength)))
    base.alpha_composite(overlay)


def wrapped_text(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=fnt) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered_lines(draw, lines, y, fnt, fill=WHITE, spacing=12):
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=fnt)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        draw.text(((W - tw) // 2, y), line, font=fnt, fill=fill)
        y += th + spacing
    return y


def pill(draw, text, xy, fnt, fg=WHITE, bg=ORANGE, pad_x=22, pad_y=12):
    bbox = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x, y = xy
    draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + th + pad_y * 2], radius=10, fill=bg)
    draw.text((x + pad_x, y + pad_y - 2), text, font=fnt, fill=fg)


# ─── Scene definitions ───────────────────────────────────────────────────────
@dataclass
class Scene:
    id: str
    narration: str
    renderer: str
    title: str = ""
    subtitle: str = ""
    on_screen: str = ""


SCENES: list[Scene] = [
    Scene(
        "hook",
        "Nearly every bank, airline, stock exchange, Android app, and enterprise software company depends on one programming language.",
        "hook",
        "THE LANGUAGE BEHIND EVERYTHING",
    ),
    Scene(
        "question",
        "That language is Java. But why has a language created almost thirty years ago survived — while hundreds of others disappeared?",
        "question",
        "JAVA",
        "Why is it still everywhere?",
    ),
    Scene(
        "promise",
        "Today we're going to find out. Not by reading a textbook. Not by memorising syntax. We're going to tell the story — of how Java was born, what problem it solved, and why it's still running the world.",
        "title_card",
        "Episode 1",
        "Why Java Exists",
    ),
    Scene(
        "curiosity1",
        "But first — a question. If C++ was already powerful… why did the industry need another language at all? Let's go back to the nineteen nineties.",
        "timeline",
        "1990s",
        "The industry needed something new",
    ),
    Scene(
        "nineties",
        "Picture this. It's the early nineties. The internet is about to explode. And at Sun Microsystems, a team led by James Gosling is building software for consumer electronics — interactive TVs, set-top boxes, handheld devices. They started with C++.",
        "history",
        "Sun Microsystems",
        "James Gosling · Project Oak",
    ),
    Scene(
        "cpp_pain",
        "And very quickly, they hit a wall. C++ gave them power — but it came with a price. Manual memory management. One mistake, and your program leaks memory… or crashes. Platform dependency. Code that compiled on one operating system could break completely on another. And for a team trying to write software for many different devices? That was a nightmare.",
        "cpp_pain",
        "The C++ Problem",
        "Memory leaks · Platform lock-in",
    ),
    Scene(
        "curiosity2",
        "So here's the real-world problem. How do you write software once… and run it on Windows, Mac, Unix, and embedded devices — without rewriting everything?",
        "curiosity",
        "Write once… run everywhere?",
    ),
    Scene(
        "birth",
        "Gosling's team made a bold decision. They would build something new. Originally called Oak — later renamed Java — inspired by the coffee that fuelled those late-night coding sessions. The goal was simple to say… but incredibly hard to build. Safer than C++. Simpler to learn. And most importantly — portable across platforms.",
        "birth",
        "1995",
        "Safer · Simpler · Portable",
    ),
    Scene(
        "wora_intro",
        "When Java launched in nineteen ninety-five, it arrived with a promise that sounded almost too good to be true. Write Once. Run Anywhere. And for an industry tired of porting code across platforms? That promise was everything.",
        "wora",
        "Write Once. Run Anywhere.",
    ),
    Scene(
        "wora_explain",
        "So what does Write Once, Run Anywhere actually mean? Imagine you write one instruction manual — and every machine on Earth can follow it. Not because every machine speaks the same language… but because every machine has the same translator.",
        "devices",
        "One codebase. Every platform.",
    ),
    Scene(
        "curiosity3",
        "But wait — Windows and Mac don't run the same programs natively. So how does Java actually run on every operating system? Watch carefully. This is the secret.",
        "curiosity",
        "What's the secret?",
    ),
    Scene(
        "bytecode",
        "When you write Java code, you don't give your program directly to Windows or Mac. First, the compiler converts your Java source code into bytecode — an intermediate format. Think of bytecode like an international language. Not tied to any one operating system. Then, the JVM — the Java Virtual Machine — takes that bytecode and translates it for whatever system you're on. The JVM is like Google Translate for computers. Windows has a JVM. Mac has a JVM. Linux has a JVM. Same bytecode. Different translator. Same result.",
        "pipeline",
        "Bytecode + JVM",
        "The secret to platform independence",
    ),
    Scene(
        "analogy",
        "Think about it this way. Your Java source code is like handwritten notes. The compiler turns those notes into a professional blueprint — the bytecode. The JVM is the construction crew that reads the blueprint and builds the house — whether the site is Windows, Mac, or Linux. You don't rebuild the blueprint for every site. You send the same blueprint. The crew adapts.",
        "analogy",
        "Blueprint Analogy",
    ),
    Scene(
        "curiosity4",
        "Okay, so Java solved the portability problem beautifully. But is that really enough to explain why it's still dominant thirty years later? Let's look at where Java actually lives today.",
        "curiosity",
        "Why is it still dominant?",
    ),
    Scene(
        "industry",
        "Java didn't survive because of a slogan. It survived because it became infrastructure. When a bank processes millions of transactions a day — it needs stability, not hype. When Android needed a language millions of developers already knew — Java was there. When companies like Netflix, Uber, and Amazon built backend systems that had to scale globally — Java's ecosystem was already battle-tested. Enterprise teams don't switch languages because something is trendy. They switch when the cost of failure is too high. And Java earned trust — one production deployment at a time.",
        "industry",
        "Java in the Real World",
        "Stability · Scale · Ecosystem",
    ),
    Scene(
        "others",
        "Now, you might ask — what about Python? JavaScript? Go? They're all excellent. But Java carved out a lane that still matters: large-scale backend systems, Android, financial platforms, and enterprise software where performance, strong typing, and decades of tooling create real business value. Not the only choice. But still one of the most important.",
        "compare",
        "Still one of the most important",
    ),
    Scene(
        "code_intro",
        "Alright — enough history. Let's write Java. Your first program. And I want you to watch every keyword — because each one is doing something deliberate.",
        "ide_intro",
        "Your First Java Program",
    ),
    Scene(
        "code_public",
        "Public — this means our class is accessible from outside. Think of it as: this code is open for business.",
        "code",
        "public",
        "Accessible from outside",
    ),
    Scene(
        "code_class",
        "Class Hello World — a class is a blueprint. Hello World is the name we chose. The filename must match: HelloWorld.java.",
        "code",
        "class HelloWorld",
        "Blueprint name = filename",
    ),
    Scene(
        "code_main",
        "Public static void main, String args — this is the entry point. When you run the program, the JVM looks for this exact method. It's where execution begins.",
        "code",
        "main()",
        "JVM starts here",
    ),
    Scene(
        "code_print",
        "System.out.println — this prints text to the console. Println means print line — add text, then move to the next line. Now… let's run it.",
        "code",
        "System.out.println",
        "Print to console",
    ),
    Scene(
        "run",
        "Watch what happens behind the scenes. You hit Run. The compiler reads HelloWorld.java… converts it to bytecode… the JVM loads it… finds the main method… and executes println. Hello, World!",
        "run",
        "Hello, World!",
    ),
    Scene(
        "memory",
        "Here's where most beginners get confused. They think Java runs directly on Windows. It doesn't. Your source code goes to the compiler… becomes bytecode… the JVM loads it into memory… the CPU executes machine instructions through the JVM. Every step matters. This tiny detail changes everything.",
        "memory",
        "Source → Compiler → Bytecode → JVM → Memory → CPU",
    ),
    Scene(
        "mistakes",
        "Many beginners think Java runs directly on Windows. It doesn't. The JVM is doing the heavy lifting. Mistake two: confusing JDK, JRE, and JVM. Quick version — JDK means develop. JRE means run. JVM is the engine inside. Mistake three: naming your file helloworld.java when the class is HelloWorld. Java is case-sensitive. The filename must match the public class name. Don't worry if this feels like a lot. We'll unpack JDK versus JRE versus JVM properly in Episode Two.",
        "mistakes",
        "Common Beginner Mistakes",
    ),
    Scene(
        "interview",
        "Here's an interview question. Why is Java platform independent? Here's how you answer — like someone who's actually shipped code. Java achieves platform independence through bytecode and the JVM. When we compile Java source code, we don't get machine-specific code. We get bytecode — a platform-neutral intermediate format. The JVM on each operating system interprets or JIT-compiles that bytecode into native machine code. So the same class files can run on Windows, Mac, or Linux — as long as a compatible JVM is installed. If you can explain that calmly in an interview? You've already beaten half the candidates.",
        "interview",
        "Interview Question",
        "Why is Java platform independent?",
    ),
    Scene(
        "summary",
        "Let's land the plane. Java exists because the nineties needed a safer, portable alternative to C++. Write Once, Run Anywhere works because of bytecode and the JVM. Industry adopted it because stability at scale beats hype. And your first program? Public class… main… println. You now understand why Java became one of the most successful programming languages ever created.",
        "summary",
        "What You Learned",
    ),
    Scene(
        "teaser",
        "But one mystery remains. When people say install Java… what are they actually installing? JDK. JRE. JVM — three names beginners mix up every day. That's what we'll unpack in Episode Two.",
        "teaser",
        "Next Episode",
        "JDK, JRE & JVM — Develop, Run, Engine",
    ),
]


# ─── Audio: TTS + music bed ──────────────────────────────────────────────────
async def synthesize_scene(scene: Scene, out_path: Path):
    communicate = edge_tts.Communicate(scene.narration, VOICE, rate="-5%", pitch="-2Hz")
    await communicate.save(str(out_path))


async def synthesize_all():
    AUDIO.mkdir(parents=True, exist_ok=True)
    tasks = []
    for sc in SCENES:
        out = AUDIO / f"{sc.id}.mp3"
        if out.exists() and out.stat().st_size > 1000:
            continue
        tasks.append(synthesize_scene(sc, out))
    # batch to avoid rate limits
    for i in range(0, len(tasks), 4):
        await asyncio.gather(*tasks[i : i + 4])
        print(f"  TTS batch {i // 4 + 1}/{(len(tasks) + 3) // 4}")


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def generate_music_bed(duration: float, out_path: Path):
    """Procedural cinematic ambient bed (no external samples)."""
    sr = 44100
    n = int(duration * sr)
    t = np.linspace(0, duration, n, endpoint=False)

    # layered soft pads + pulse
    pad1 = 0.08 * np.sin(2 * np.pi * 110 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t))
    pad2 = 0.06 * np.sin(2 * np.pi * 164.81 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t + 1))
    pad3 = 0.05 * np.sin(2 * np.pi * 220 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.03 * t + 2))
    pulse = 0.03 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.5 * t))
    noise = 0.008 * np.random.randn(n)
    # soft lowpass-ish via cumulative moving average
    sig = pad1 + pad2 + pad3 + pulse + noise
    kernel = np.ones(64) / 64
    sig = np.convolve(sig, kernel, mode="same")
    # envelope fade in/out
    fade = int(2.5 * sr)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    sig = sig * env * 0.55
    # peak normalize gently
    peak = np.max(np.abs(sig)) + 1e-9
    sig = (sig / peak * 0.35).astype(np.float32)

    # write wav then convert
    wav_path = out_path.with_suffix(".wav")
    with wave.open(str(wav_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        pcm = (sig * 32767).astype(np.int16)
        wf.writeframes(pcm.tobytes())
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "aac", "-b:a", "192k", str(out_path)],
        check=True,
        capture_output=True,
    )


# ─── Visual renderers ────────────────────────────────────────────────────────
def base_canvas(t: float = 0.0) -> Image.Image:
    img = Image.new("RGBA", (W, H), (*BG, 255))
    draw_gradient(img)
    d = ImageDraw.Draw(img)
    draw_grid(d, offset=t * 12)
    # ambient orbs
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glow_circle(glow, (int(280 + 40 * math.sin(t * 0.4)), 220), 160, ORANGE, 0.35)
    draw_glow_circle(glow, (int(1600 + 30 * math.cos(t * 0.3)), 780), 200, BLUE, 0.3)
    img = Image.alpha_composite(img, glow)
    return img


def render_hook(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # expanding network
    cx, cy = W // 2, H // 2 - 40
    nodes = [
        (cx, cy),
        (cx - 320, cy - 160),
        (cx + 340, cy - 120),
        (cx - 280, cy + 180),
        (cx + 300, cy + 200),
        (cx - 480, cy + 20),
        (cx + 500, cy - 20),
        (cx, cy - 260),
    ]
    labels = ["Bank", "Airline", "Android", "Enterprise", "Stock", "Cloud", "Server", "App"]
    appear = ease_out_cubic(clamp(progress * 1.4))
    for i, (x, y) in enumerate(nodes):
        if i / len(nodes) > appear:
            continue
        # edges to center
        if i > 0:
            d.line([(cx, cy), (x, y)], fill=mix(BG, BLUE, 0.55), width=2)
        pulse = 10 + 4 * math.sin(t * 3 + i)
        color = ORANGE if i == 0 else BLUE
        d.ellipse([x - pulse, y - pulse, x + pulse, y + pulse], fill=color)
        if i > 0:
            f = font(FONT_BOLD, 22)
            bbox = d.textbbox((0, 0), labels[i - 1], font=f)
            tw = bbox[2] - bbox[0]
            d.text((x - tw // 2, y + 22), labels[i - 1], font=f, fill=MUTED)
    # title
    title_a = ease_out_cubic(clamp((progress - 0.35) / 0.4))
    if title_a > 0:
        f = font(FONT_SERIF, 54)
        text = "THE LANGUAGE BEHIND EVERYTHING"
        bbox = d.textbbox((0, 0), text, font=f)
        tw = bbox[2] - bbox[0]
        col = mix(BG, WHITE, title_a)
        d.text(((W - tw) // 2, H - 160), text, font=f, fill=col)
    return img.convert("RGB")


def render_question(progress: float, t: float) -> Image.Image:
    scale = ease_out_cubic(clamp(progress * 1.5))
    cx, cy = W // 2, H // 2 - 60
    r = int(120 * scale)
    img = base_canvas(t)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glow_circle(overlay, (cx, cy), r, ORANGE, 0.7)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    # cup body
    d.rounded_rectangle([cx - 70, cy - 50, cx + 50, cy + 70], radius=18, fill=ORANGE)
    d.arc([cx + 40, cy - 20, cx + 95, cy + 40], 270, 90, fill=ORANGE, width=10)
    # steam
    for i in range(3):
        sx = cx - 30 + i * 28
        sy = cy - 70 - int(20 * math.sin(t * 2 + i))
        d.arc([sx, sy, sx + 16, sy + 40], 200, 340, fill=mix(ORANGE, WHITE, 0.5), width=3)
    f = font(FONT_SERIF, 96)
    text = "JAVA"
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, cy + 140), text, font=f, fill=WHITE)
    if progress > 0.45:
        f2 = font(FONT_REG, 36)
        q = "Why is it still everywhere?"
        bbox = d.textbbox((0, 0), q, font=f2)
        tw = bbox[2] - bbox[0]
        d.text(((W - tw) // 2, cy + 250), q, font=f2, fill=MUTED)
    return img.convert("RGB")


def render_title_card(progress: float, t: float, title: str, subtitle: str) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.2))
    # thin orange line
    lw = int(lerp(0, 220, a))
    d.rectangle([(W - lw) // 2, H // 2 - 40, (W + lw) // 2, H // 2 - 36], fill=ORANGE)
    f1 = font(FONT_BOLD, 28)
    f2 = font(FONT_SERIF, 72)
    c1 = mix(BG, MUTED, a)
    c2 = mix(BG, WHITE, a)
    for txt, fnt, y, col in [
        (title.upper(), f1, H // 2 - 120, c1),
        (subtitle, f2, H // 2 - 20, c2),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        tw = bbox[2] - bbox[0]
        d.text(((W - tw) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_timeline(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    years = [2026, 2015, 2005, 1995, 1991]
    # scrubber
    y = H // 2
    d.line([(200, y), (W - 200, y)], fill=mix(BG, MUTED, 0.5), width=4)
    idx = int(clamp(progress) * (len(years) - 1) + 0.001)
    for i, year in enumerate(years):
        x = 200 + i * ((W - 400) // (len(years) - 1))
        active = i <= idx
        col = ORANGE if active else MUTED
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=col)
        f = font(FONT_BOLD, 28 if active else 22)
        bbox = d.textbbox((0, 0), str(year), font=f)
        tw = bbox[2] - bbox[0]
        d.text((x - tw // 2, y + 30), str(year), font=f, fill=col)
    # focus year
    focus = years[idx]
    fbig = font(FONT_SERIF, 96)
    text = str(focus)
    bbox = d.textbbox((0, 0), text, font=fbig)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, 220), text, font=fbig, fill=WHITE)
    fsub = font(FONT_REG, 32)
    sub = "The industry needed something new"
    bbox = d.textbbox((0, 0), sub, font=fsub)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, 340), sub, font=fsub, fill=MUTED)
    return img.convert("RGB")


def render_history(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # CRT-ish panels
    panels = [
        (180, 220, 520, 480, "C++"),
        (700, 220, 1040, 480, "Devices"),
        (1220, 220, 1560, 480, "Sun"),
    ]
    for i, (x1, y1, x2, y2, label) in enumerate(panels):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.4))
        if a <= 0:
            continue
        col = mix(BG, SURFACE, a)
        d.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=col, outline=mix(BG, MUTED, a), width=2)
        # scanlines
        for yy in range(y1 + 10, y2 - 10, 6):
            d.line([(x1 + 10, yy), (x2 - 10, yy)], fill=mix(col, BG, 0.3), width=1)
        f = font(FONT_BOLD, 36)
        bbox = d.textbbox((0, 0), label, font=f)
        tw = bbox[2] - bbox[0]
        d.text(((x1 + x2 - tw) // 2, (y1 + y2) // 2 - 20), label, font=f, fill=mix(BG, WHITE, a))
    f = font(FONT_SERIF, 48)
    title = "Sun Microsystems · James Gosling"
    bbox = d.textbbox((0, 0), title, font=f)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, 120), title, font=f, fill=WHITE)
    pill(d, "1991", (W // 2 - 50, H - 180), font(FONT_BOLD, 22), fg=BG, bg=ORANGE)
    return img.convert("RGB")


def render_cpp_pain(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # split screens
    d.rounded_rectangle([80, 180, 900, 820], radius=18, fill=SURFACE, outline=RED, width=3)
    d.rounded_rectangle([1020, 180, 1840, 820], radius=18, fill=SURFACE, outline=GREEN, width=3)
    f = font(FONT_BOLD, 32)
    d.text((120, 210), "Windows build", font=f, fill=GREEN)
    d.text((1060, 210), "Unix build", font=f, fill=RED)
    # fake code / errors
    mono = font(FONT_MONO, 22)
    ok_lines = ["g++ main.cpp -o app", "Linking...", "SUCCESS", "./app", "Hello from Windows"]
    err_lines = [
        "g++ main.cpp -o app",
        "error: undefined reference",
        "segfault at 0x0",
        "memory leak detected",
        "BUILD FAILED",
    ]
    for i, line in enumerate(ok_lines):
        if progress > i * 0.12:
            d.text((120, 300 + i * 50), line, font=mono, fill=GREEN if i >= 2 else MUTED)
    for i, line in enumerate(err_lines):
        if progress > 0.2 + i * 0.12:
            d.text((1060, 300 + i * 50), line, font=mono, fill=RED if i >= 1 else MUTED)
    # memory leak bars
    for i in range(8):
        h = int(40 + 60 * abs(math.sin(t + i)))
        x = 120 + i * 90
        d.rectangle([x, 720 - h, x + 50, 720], fill=mix(ORANGE, RED, i / 8))
    f2 = font(FONT_SERIF, 44)
    title = "The C++ Problem"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=f2, fill=WHITE)
    return img.convert("RGB")


def render_curiosity(progress: float, t: float, title: str) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # pulsing question
    r = 90 + 10 * math.sin(t * 3)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glow_circle(overlay, (W // 2, H // 2 - 40), int(r), BLUE, 0.6)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    f = font(FONT_SERIF, 120)
    bbox = d.textbbox((0, 0), "?", font=f)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, H // 2 - 120), "?", font=f, fill=WHITE)
    f2 = font(FONT_REG, 40)
    lines = wrapped_text(d, title, f2, 1400)
    draw_centered_lines(d, lines, H // 2 + 80, f2, MUTED, 16)
    return img.convert("RGB")


def render_birth(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # Oak -> Java morph text
    phase = ease_in_out(clamp(progress))
    word = "Oak" if phase < 0.45 else "Java"
    f = font(FONT_SERIF, 110)
    bbox = d.textbbox((0, 0), word, font=f)
    tw = bbox[2] - bbox[0]
    col = mix(MUTED, ORANGE, clamp((phase - 0.35) / 0.3))
    d.text(((W - tw) // 2, H // 2 - 140), word, font=f, fill=col)
    if phase > 0.5:
        # coffee cup
        cx, cy = W // 2, H // 2 + 40
        d.rounded_rectangle([cx - 55, cy - 40, cx + 40, cy + 55], radius=14, fill=ORANGE)
        d.arc([cx + 30, cy - 15, cx + 75, cy + 30], 270, 90, fill=ORANGE, width=8)
    pills = ["Safer", "Simpler", "Portable"]
    for i, p in enumerate(pills):
        if progress > 0.55 + i * 0.1:
            x = W // 2 - 280 + i * 200
            pill(d, p, (x, H - 220), font(FONT_BOLD, 24), fg=BG, bg=ORANGE if i == 2 else BLUE)
    f2 = font(FONT_BOLD, 28)
    d.text((W // 2 - 40, 160), "1995", font=f2, fill=MUTED)
    return img.convert("RGB")


def render_wora(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    words = ["Write", "Once.", "Run", "Anywhere."]
    f = font(FONT_SERIF, 72)
    x = 280
    for i, w in enumerate(words):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.3))
        if a <= 0:
            continue
        col = ORANGE if i in (1, 3) else mix(BG, WHITE, a)
        d.text((x, H // 2 - 40), w, font=f, fill=col)
        x += int(d.textlength(w + "  ", font=f))
    return img.convert("RGB")


def render_devices(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # center java file
    cx, cy = W // 2, H // 2
    d.rounded_rectangle([cx - 90, cy - 110, cx + 90, cy + 110], radius=12, fill=SURFACE, outline=ORANGE, width=3)
    fm = font(FONT_MONO_B, 28)
    d.text((cx - 55, cy - 20), ".java", font=fm, fill=ORANGE)
    devices = [
        (-520, -220, "Windows"),
        (520, -220, "Mac"),
        (-520, 220, "Linux"),
        (520, 220, "Android"),
        (0, -300, "Cloud"),
        (0, 300, "Server"),
    ]
    for i, (dx, dy, name) in enumerate(devices):
        a = ease_out_cubic(clamp((progress - i * 0.08) / 0.35))
        if a <= 0:
            continue
        x, y = cx + dx, cy + dy
        # traveling packet
        px = int(lerp(cx, x, a))
        py = int(lerp(cy, y, a))
        d.line([(cx, cy), (x, y)], fill=mix(BG, BLUE, a * 0.7), width=2)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=BLUE)
        d.rounded_rectangle([x - 90, y - 40, x + 90, y + 40], radius=12, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=2)
        f = font(FONT_BOLD, 26)
        bbox = d.textbbox((0, 0), name, font=f)
        tw = bbox[2] - bbox[0]
        d.text((x - tw // 2, y - 14), name, font=f, fill=mix(BG, WHITE, a))
    f2 = font(FONT_REG, 34)
    title = "One codebase. Every platform."
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=f2, fill=WHITE)
    return img.convert("RGB")


def render_pipeline(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    stages = [
        ("Source", ".java", ORANGE),
        ("Compiler", "javac", MUTED),
        ("Bytecode", ".class", BLUE),
        ("JVM", "translator", ORANGE),
        ("Native", "CPU", GREEN),
        ("Output", "result", WHITE),
    ]
    n = len(stages)
    packet = clamp(progress) * (n - 1)
    for i, (name, sub, col) in enumerate(stages):
        x = 140 + i * 290
        y = H // 2 - 40
        active = packet >= i - 0.2
        box_col = mix(BG, SURFACE, 1 if active else 0.4)
        border = col if active else mix(BG, MUTED, 0.4)
        d.rounded_rectangle([x, y, x + 220, y + 160], radius=16, fill=box_col, outline=border, width=3)
        f = font(FONT_BOLD, 28)
        fs = font(FONT_MONO, 20)
        bbox = d.textbbox((0, 0), name, font=f)
        d.text((x + (220 - (bbox[2] - bbox[0])) // 2, y + 45), name, font=f, fill=col if active else MUTED)
        bbox = d.textbbox((0, 0), sub, font=fs)
        d.text((x + (220 - (bbox[2] - bbox[0])) // 2, y + 95), sub, font=fs, fill=MUTED)
        if i < n - 1:
            ax = x + 230
            d.polygon([(ax, y + 70), (ax + 40, y + 80), (ax, y + 90)], fill=BLUE if packet > i else mix(BG, MUTED, 0.4))
    # traveling highlight
    pi = int(packet)
    pf = packet - pi
    if pi < n - 1:
        x1 = 140 + pi * 290 + 110
        x2 = 140 + (pi + 1) * 290 + 110
        px = int(lerp(x1, x2, ease_in_out(pf)))
        d.ellipse([px - 14, H // 2 + 40, px + 14, H // 2 + 68], fill=ORANGE)
    f2 = font(FONT_SERIF, 44)
    title = "Bytecode + JVM"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 100), title, font=f2, fill=WHITE)
    f3 = font(FONT_REG, 28)
    sub = "The secret to platform independence"
    bbox = d.textbbox((0, 0), sub, font=f3)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 165), sub, font=f3, fill=MUTED)
    return img.convert("RGB")


def render_analogy(progress: float, t: float, heading: str = "Blueprint Analogy") -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    if "JDK" in heading:
        cards = [
            (200, 280, "JDK", "Develop & compile", ORANGE),
            (760, 280, "JRE", "Run programs", BLUE),
            (1320, 280, "JVM", "Execute bytecode", GREEN),
        ]
    else:
        cards = [
            (200, 280, "Handwritten notes", "Source code", ORANGE),
            (760, 280, "Blueprint", "Bytecode", BLUE),
            (1320, 280, "Construction crew", "JVM", GREEN),
        ]
    for i, (x, y, title, sub, col) in enumerate(cards):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.4))
        if a <= 0:
            continue
        d.rounded_rectangle([x, y, x + 400, y + 320], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        f = font(FONT_BOLD, 30)
        fs = font(FONT_REG, 24)
        bbox = d.textbbox((0, 0), title, font=f)
        d.text((x + (400 - (bbox[2] - bbox[0])) // 2, y + 110), title, font=f, fill=mix(BG, WHITE, a))
        bbox = d.textbbox((0, 0), sub, font=fs)
        d.text((x + (400 - (bbox[2] - bbox[0])) // 2, y + 170), sub, font=fs, fill=mix(BG, col, a))
        if i < 2 and progress > 0.35 + i * 0.18:
            d.polygon([(x + 410, y + 150), (x + 450, y + 160), (x + 410, y + 170)], fill=ORANGE)
    f2 = font(FONT_SERIF, 48)
    bbox = d.textbbox((0, 0), heading, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), heading, font=f2, fill=WHITE)
    return img.convert("RGB")


def render_industry(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # world-ish dots map
    hotspots = [
        (480, 360, "Banking"),
        (980, 300, "Android"),
        (1300, 420, "Cloud backends"),
        (700, 560, "Enterprise"),
        (1150, 620, "Finance"),
    ]
    for i, (x, y, name) in enumerate(hotspots):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.35))
        if a <= 0:
            continue
        pulse = 18 + 6 * math.sin(t * 3 + i)
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_glow_circle(overlay, (x, y), int(pulse), ORANGE if i % 2 == 0 else BLUE, a * 0.7)
        img = Image.alpha_composite(img.convert("RGBA"), overlay)
        d = ImageDraw.Draw(img)
        f = font(FONT_BOLD, 24)
        d.text((x + 28, y - 12), name, font=f, fill=mix(BG, WHITE, a))
    f2 = font(FONT_SERIF, 48)
    title = "Java in the Real World"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 100), title, font=f2, fill=WHITE)
    pills = ["Stability", "Scale", "Ecosystem"]
    for i, p in enumerate(pills):
        if progress > 0.55:
            pill(d, p, (W // 2 - 300 + i * 220, H - 160), font(FONT_BOLD, 22), fg=BG, bg=ORANGE if i == 0 else BLUE)
    return img.convert("RGB")


def render_compare(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    langs = [("Python", 420), ("JavaScript", 720), ("Go", 1020), ("Java", 1320)]
    for i, (name, x) in enumerate(langs):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.35))
        highlight = name == "Java"
        col = ORANGE if highlight else BLUE
        size = 140 if highlight else 100
        y = H // 2 - size // 2
        d.rounded_rectangle([x - size // 2, y, x + size // 2, y + size], radius=20, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3 if highlight else 2)
        f = font(FONT_BOLD, 28 if highlight else 22)
        bbox = d.textbbox((0, 0), name, font=f)
        d.text((x - (bbox[2] - bbox[0]) // 2, y + size // 2 - 14), name, font=f, fill=mix(BG, WHITE, a))
    f2 = font(FONT_REG, 34)
    title = "Still one of the most important"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 160), title, font=f2, fill=WHITE)
    return img.convert("RGB")


CODE_LINES = [
    "public class HelloWorld {",
    "    public static void main(String[] args) {",
    "        System.out.println(\"Hello, World!\");",
    "    }",
    "}",
]


def render_ide_intro(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    # window chrome
    d.rounded_rectangle([220, 140, 1700, 900], radius=16, fill=SURFACE, outline=mix(BG, MUTED, 0.5), width=2)
    d.rounded_rectangle([220, 140, 1700, 200], radius=16, fill=(30, 36, 44))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([250 + i * 28, 162, 268 + i * 28, 180], fill=c)
    f = font(FONT_BOLD, 24)
    d.text((320, 160), "HelloWorld.java — IntelliJ IDEA", font=f, fill=MUTED)
    # blinking cursor
    if int(t * 2) % 2 == 0:
        d.rectangle([280, 280, 286, 320], fill=ORANGE)
    f2 = font(FONT_SERIF, 48)
    title = "Your First Java Program"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 40), title, font=f2, fill=WHITE)
    return img.convert("RGB")


def render_code(progress: float, t: float, highlight_key: str, label: str) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([160, 120, 1760, 860], radius=16, fill=SURFACE, outline=mix(BG, MUTED, 0.4), width=2)
    d.rounded_rectangle([160, 120, 1760, 180], radius=16, fill=(30, 36, 44))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([190 + i * 28, 142, 208 + i * 28, 160], fill=c)
    ftitle = font(FONT_BOLD, 22)
    d.text((280, 140), "HelloWorld.java", font=ftitle, fill=MUTED)

    mono = font(FONT_MONO, 34)
    # reveal lines based on which keyword
    reveal = {
        "public": 1,
        "class HelloWorld": 1,
        "main()": 2,
        "System.out.println": 5,
    }.get(highlight_key, 5)
    y = 240
    for i, line in enumerate(CODE_LINES[:reveal]):
        # line number
        d.text((200, y), f"{i+1}", font=font(FONT_MONO, 24), fill=mix(BG, MUTED, 0.5))
        # syntax-ish coloring
        color = WHITE
        if "public" in line or "class" in line or "static" in line or "void" in line:
            color = ORANGE
        if "Hello" in line and '"' in line:
            # draw with string highlight separately
            pass
        # highlight active keyword line
        active = False
        if highlight_key == "public" and i == 0:
            active = True
        if highlight_key == "class HelloWorld" and i == 0:
            active = True
        if highlight_key == "main()" and i == 1:
            active = True
        if highlight_key == "System.out.println" and i == 2:
            active = True
        if active:
            d.rounded_rectangle([250, y - 8, 1680, y + 48], radius=8, fill=(40, 30, 18))
        d.text((280, y), line, font=mono, fill=ORANGE if ("public" in line or "class" in line) else WHITE)
        # refine string color for println line
        if i == 2:
            d.text((280, y), line, font=mono, fill=WHITE)
            # overlay green string
            prefix = '        System.out.println('
            px = 280 + d.textlength(prefix, font=mono)
            d.text((280, y), prefix, font=mono, fill=BLUE)
            d.text((px, y), '"Hello, World!"', font=mono, fill=GREEN)
            d.text((px + d.textlength('"Hello, World!"', font=mono), y), ");", font=mono, fill=WHITE)
        y += 70

    # floating label
    a = ease_out_cubic(clamp(progress * 2))
    if a > 0:
        f = font(FONT_BOLD, 36)
        bbox = d.textbbox((0, 0), highlight_key, font=f)
        d.text((200, H - 160), highlight_key, font=f, fill=mix(BG, ORANGE, a))
        fs = font(FONT_REG, 28)
        d.text((200, H - 110), label, font=fs, fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_run(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([160, 100, 1760, 560], radius=16, fill=SURFACE, outline=mix(BG, MUTED, 0.4), width=2)
    mono = font(FONT_MONO, 30)
    y = 160
    for i, line in enumerate(CODE_LINES):
        # execution highlight
        exec_line = int(clamp(progress) * 4)
        if i == exec_line:
            d.rounded_rectangle([200, y - 6, 1700, y + 42], radius=8, fill=(20, 40, 28))
        d.text((240, y), line, font=mono, fill=WHITE)
        y += 60
    # Run button
    pill(d, "▶  Run", (1600, 120), font(FONT_BOLD, 22), fg=WHITE, bg=GREEN)
    # console
    d.rounded_rectangle([160, 600, 1760, 980], radius=16, fill=(10, 12, 16), outline=mix(BG, MUTED, 0.4), width=2)
    d.text((200, 630), "Console", font=font(FONT_BOLD, 22), fill=MUTED)
    out = "Hello, World!"
    chars = int(clamp((progress - 0.35) / 0.5) * len(out))
    if chars > 0:
        d.text((200, 720), out[:chars] + ("▍" if int(t * 2) % 2 == 0 else ""), font=font(FONT_MONO_B, 40), fill=GREEN)
    return img.convert("RGB")


def render_memory(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    stages = ["Source", "Compiler", "Bytecode", "JVM", "Memory", "CPU", "Output"]
    packet = clamp(progress) * (len(stages) - 1)
    for i, name in enumerate(stages):
        y = 160 + i * 110
        active = packet >= i - 0.15
        col = ORANGE if i in (0, 3) else BLUE if i in (2, 4) else GREEN if i == 6 else MUTED
        d.rounded_rectangle([W // 2 - 220, y, W // 2 + 220, y + 80], radius=14, fill=SURFACE if active else mix(BG, SURFACE, 0.4), outline=col if active else mix(BG, MUTED, 0.3), width=3)
        f = font(FONT_BOLD, 30)
        bbox = d.textbbox((0, 0), name, font=f)
        d.text((W // 2 - (bbox[2] - bbox[0]) // 2, y + 22), name, font=f, fill=col if active else MUTED)
        if i < len(stages) - 1:
            d.polygon([(W // 2 - 12, y + 88), (W // 2 + 12, y + 88), (W // 2, y + 104)], fill=ORANGE if packet > i else mix(BG, MUTED, 0.4))
    return img.convert("RGB")


def render_mistakes(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    items = [
        ("01", "Java runs directly on Windows", "No — the JVM does the heavy lifting"),
        ("02", "JDK, JRE, and JVM are the same", "JDK = develop · JRE = run · JVM = engine"),
        ("03", "Filename case doesn't matter", "HelloWorld.java must match the class"),
    ]
    f2 = font(FONT_SERIF, 48)
    title = "Common Beginner Mistakes"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=f2, fill=WHITE)
    for i, (num, wrong, right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0:
            continue
        y = 200 + i * 220
        d.rounded_rectangle([220, y, 1700, y + 180], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a * 0.6), width=2)
        d.text((260, y + 30), num, font=font(FONT_SERIF, 40), fill=mix(BG, ORANGE, a))
        d.text((360, y + 40), wrong, font=font(FONT_BOLD, 30), fill=mix(BG, RED, a))
        d.text((360, y + 100), right, font=font(FONT_REG, 28), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_interview(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    f2 = font(FONT_SERIF, 44)
    title = "Interview Question"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=f2, fill=WHITE)
    d.rounded_rectangle([160, 200, 1760, 360], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "Why is Java platform independent?"
    fq = font(FONT_BOLD, 36)
    bbox = d.textbbox((0, 0), q, font=fq)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 250), q, font=fq, fill=WHITE)
    answers = [
        "Compile to bytecode — not machine code",
        "Bytecode is platform-neutral",
        "JVM translates per operating system",
        "Same .class files → Windows / Mac / Linux",
    ]
    for i, atext in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.15) / 0.3))
        if a <= 0:
            continue
        y = 420 + i * 100
        d.rounded_rectangle([260, y, 1660, y + 80], radius=12, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=2)
        d.text((300, y + 22), f"{i+1}.  {atext}", font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_summary(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    items = [
        ("1990s", "Born to solve C++ pain"),
        ("WORA", "Write Once, Run Anywhere"),
        ("Bytecode", "Platform-neutral code"),
        ("JVM", "Translator on every OS"),
        ("Industry", "Banks, Android, backends"),
        ("main()", "Every program starts here"),
    ]
    f2 = font(FONT_SERIF, 48)
    title = "What You Learned"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=f2, fill=WHITE)
    for i, (k, v) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.3))
        if a <= 0:
            continue
        col = i % 2
        x = 200 + (i % 3) * 540
        y = 220 + (i // 3) * 280
        d.rounded_rectangle([x, y, x + 480, y + 220], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE if col == 0 else BLUE, a), width=2)
        d.text((x + 40, y + 50), k, font=font(FONT_BOLD, 34), fill=mix(BG, ORANGE if col == 0 else BLUE, a))
        d.text((x + 40, y + 120), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_glow_circle(overlay, (W // 2, H // 2 - 20), 160 + int(20 * math.sin(t * 2)), BLUE, 0.75)
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    f = font(FONT_BOLD, 28)
    d.text((W // 2 - 80, 200), "NEXT EPISODE", font=f, fill=MUTED)
    f2 = font(FONT_SERIF, 64)
    title = "JDK, JRE & JVM"
    bbox = d.textbbox((0, 0), title, font=f2)
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=f2, fill=WHITE)
    f3 = font(FONT_REG, 32)
    sub = "Develop · Run · The Engine Inside"
    bbox = d.textbbox((0, 0), sub, font=f3)
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=f3, fill=BLUE)
    # question mark
    f4 = font(FONT_SERIF, 80)
    d.text((W // 2 - 20, H // 2 - 200), "?", font=f4, fill=ORANGE)
    return img.convert("RGB")


def render_frame(scene: Scene, progress: float, t: float) -> Image.Image:
    r = scene.renderer
    if r == "hook":
        return render_hook(progress, t)
    if r == "question":
        return render_question(progress, t)
    if r == "title_card":
        return render_title_card(progress, t, scene.title, scene.subtitle)
    if r == "timeline":
        return render_timeline(progress, t)
    if r == "history":
        return render_history(progress, t)
    if r == "cpp_pain":
        return render_cpp_pain(progress, t)
    if r == "curiosity":
        return render_curiosity(progress, t, scene.title)
    if r == "birth":
        return render_birth(progress, t)
    if r == "wora":
        return render_wora(progress, t)
    if r == "devices":
        return render_devices(progress, t)
    if r == "pipeline":
        return render_pipeline(progress, t)
    if r == "analogy":
        return render_analogy(progress, t, scene.title or "Blueprint Analogy")
    if r == "industry":
        return render_industry(progress, t)
    if r == "compare":
        return render_compare(progress, t)
    if r == "ide_intro":
        return render_ide_intro(progress, t)
    if r == "code":
        return render_code(progress, t, scene.title, scene.subtitle)
    if r == "run":
        return render_run(progress, t)
    if r == "memory":
        return render_memory(progress, t)
    if r == "mistakes":
        return render_mistakes(progress, t)
    if r == "interview":
        return render_interview(progress, t)
    if r == "summary":
        return render_summary(progress, t)
    if r == "teaser":
        return render_teaser(progress, t)
    return render_title_card(progress, t, scene.title or scene.id, scene.subtitle)


# ─── Encode scenes ───────────────────────────────────────────────────────────
def _render_one_frame(args):
    scene_id, renderer, title, subtitle, i, n_frames, scene_dir = args
    progress = i / max(n_frames - 1, 1)
    t = i / FPS
    # reconstruct minimal scene-like object
    sc = Scene(id=scene_id, narration="", renderer=renderer, title=title, subtitle=subtitle)
    frame = render_frame(sc, progress, t)
    path = Path(scene_dir) / f"f{i:05d}.jpg"
    frame.save(path, quality=85)
    return i


def render_scene_clip(scene: Scene, duration: float, out_mp4: Path):
    # pad a little silence visual hold
    duration = max(duration + 0.35, 2.0)
    n_frames = int(duration * FPS)
    scene_dir = FRAMES / scene.id
    if scene_dir.exists():
        shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)

    print(f"  Rendering {scene.id}: {n_frames} frames ({duration:.1f}s)")
    args = [
        (scene.id, scene.renderer, scene.title, scene.subtitle, i, n_frames, str(scene_dir))
        for i in range(n_frames)
    ]
    workers = max(2, min(8, os.cpu_count() or 4))
    with mp.Pool(workers) as pool:
        done = 0
        for _ in pool.imap_unordered(_render_one_frame, args, chunksize=8):
            done += 1
            if done % 90 == 0 or done == n_frames:
                print(f"    {scene.id}: {done}/{n_frames}")

    # encode video from frames
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(scene_dir / "f%05d.jpg"),
            "-i",
            str(AUDIO / f"{scene.id}.mp3"),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "20",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(out_mp4),
        ],
        check=True,
        capture_output=True,
    )
    # free disk
    shutil.rmtree(scene_dir)


def concat_clips(clip_paths: list[Path], out_path: Path):
    lst = ROOT / "concat.txt"
    with open(lst, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p}'\n")
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
            "-c",
            "copy",
            str(out_path),
        ],
        check=True,
        capture_output=True,
    )


def mix_music(video_path: Path, music_path: Path, out_path: Path):
    # lower music under narration
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(music_path),
            "-filter_complex",
            "[1:a]volume=0.14[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
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
            "-movflags",
            "+faststart",
            str(out_path),
        ],
        check=True,
        capture_output=True,
    )


def write_srt(durations: dict[str, float], out_path: Path):
    t = 0.0
    idx = 1
    lines = []

    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    for sc in SCENES:
        dur = durations[sc.id] + 0.35
        # chunk narration into ~2 caption lines
        words = sc.narration.split()
        chunk_size = 12
        chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
        if not chunks:
            continue
        slot = dur / len(chunks)
        for ch in chunks:
            start = t
            end = t + slot
            lines.append(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{ch}\n")
            idx += 1
            t = end
    out_path.write_text("\n".join(lines))


def main():
    for p in [ASSETS, FRAMES, AUDIO, CLIPS, OUTPUT, ARTIFACTS]:
        p.mkdir(parents=True, exist_ok=True)

    print("==> Synthesizing narration (Indian English TTS)...")
    asyncio.run(synthesize_all())

    durations = {}
    total = 0.0
    for sc in SCENES:
        d = probe_duration(AUDIO / f"{sc.id}.mp3")
        durations[sc.id] = d
        total += d + 0.35
    print(f"==> Total narration runtime ≈ {total/60:.1f} min ({total:.1f}s)")
    (ROOT / "durations.json").write_text(json.dumps(durations, indent=2))

    print("==> Generating ambient music bed...")
    music = AUDIO / "music_bed.m4a"
    if not music.exists():
        generate_music_bed(total + 5, music)

    print("==> Rendering scene clips...")
    clip_paths = []
    for sc in SCENES:
        clip = CLIPS / f"{sc.id}.mp4"
        if not clip.exists():
            render_scene_clip(sc, durations[sc.id], clip)
        else:
            print(f"  skip existing {sc.id}")
        clip_paths.append(clip)

    print("==> Concatenating...")
    silent_mix = OUTPUT / "java_ep1_narrated.mp4"
    concat_clips(clip_paths, silent_mix)

    print("==> Mixing music...")
    final = OUTPUT / "Java_Episode_01_Why_Java_Exists.mp4"
    mix_music(silent_mix, music, final)

    # also copy to artifacts
    art = ARTIFACTS / "Java_Episode_01_Why_Java_Exists.mp4"
    shutil.copy2(final, art)

    print("==> Writing captions...")
    write_srt(durations, OUTPUT / "Java_Episode_01.srt")
    shutil.copy2(OUTPUT / "Java_Episode_01.srt", ARTIFACTS / "Java_Episode_01.srt")

    # thumbnail from last teaser / question frame
    thumb = render_question(1.0, 1.0)
    d = ImageDraw.Draw(thumb)
    f = font(FONT_SERIF, 72)
    text = "WHY JAVA?"
    bbox = d.textbbox((0, 0), text, font=f)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), text, font=f, fill=WHITE)
    f2 = font(FONT_BOLD, 36)
    d.text((W // 2 - 90, H - 120), "Episode 1", font=f2, fill=ORANGE)
    thumb_path = OUTPUT / "thumbnail.jpg"
    thumb.save(thumb_path, quality=95)
    shutil.copy2(thumb_path, ARTIFACTS / "thumbnail.jpg")

    print(f"DONE: {final}")
    print(f"Artifact: {art}")
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
