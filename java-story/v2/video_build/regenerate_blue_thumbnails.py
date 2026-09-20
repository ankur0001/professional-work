#!/usr/bin/env python3
"""Regenerate Java Story v2 thumbnails — Spring-style branded stills in blue.

Clean upload thumbnails only (no video frames, no burned-in subtitles).
Layout mirrors spring-story packs: brand · EP NN · title · phase · accent bar.
"""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/workspace/java-story/v2/episodes")

# Blue palette (Spring layout, Java-blue brand — not orange, not purple)
BG_TOP = (8, 16, 32)
BG_BOT = (12, 28, 52)
BLUE = (74, 158, 255)         # Java / sky accent
BLUE_DIM = (40, 90, 160)
BLUE_SOFT = (96, 165, 250)
CREAM = (245, 247, 252)
MUTED = (160, 180, 210)

FONT_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
FONT_SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]

# Episode phase bands (matches Java Story curriculum arcs)
PHASES = [
    (1, 9, "Phase 1 — Language Fundamentals"),
    (10, 20, "Phase 2 — OOP & Language Features"),
    (21, 35, "Phase 3 — Collections, Streams & I/O"),
    (36, 50, "Phase 4 — Concurrency"),
    (51, 66, "Phase 5 — JVM Internals"),
    (67, 70, "Phase 6 — Design Patterns"),
    (71, 80, "Phase 7 — Spring & Architecture"),
    (81, 85, "Phase 8 — Production Engineering"),
]


def font(paths, size):
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def phase_for(n: int) -> str:
    for a, b, label in PHASES:
        if a <= n <= b:
            return label
    return ""


def wrap_lines(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), trial, font=fnt)
        if bbox[2] - bbox[0] <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def title_from_folder(folder: Path, n: int) -> str:
    title_path = folder / "title.txt"
    if title_path.exists():
        raw = title_path.read_text().strip()
        # "The Java Story Ep50: Virtual Threads" -> "Virtual Threads"
        m = re.search(r"Ep\s*\d+\s*:\s*(.+)$", raw, re.I)
        if m:
            return m.group(1).strip()
        m = re.search(r"Episode\s*\d+\s*[:—-]\s*(.+)$", raw, re.I)
        if m:
            return m.group(1).strip()
    narr = folder / "narration.md"
    if narr.exists():
        m = re.search(r"^#\s*Episode\s+\d+\s*[—-]\s*(.+)$", narr.read_text(), re.M)
        if m:
            return m.group(1).strip()
    # fallback from folder slug
    slug = folder.name
    slug = re.sub(r"^ep\d+-", "", slug)
    return slug.replace("-", " ").title()


def make_thumbnail(n: int, title: str, phase: str, dest: Path) -> None:
    W, H = 1920, 1080
    strip = Image.new("RGB", (1, H))
    sp = strip.load()
    for y in range(H):
        t = y / (H - 1)
        sp[0, y] = tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT))
    img = strip.resize((W, H), Image.Resampling.BILINEAR)

    draw = ImageDraw.Draw(img)
    # left accent bar
    draw.rectangle([0, 0, 28, H], fill=BLUE)

    # soft blue orbs (decorative — not text / not video frame)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([1300, -120, 2100, 680], fill=(*BLUE_DIM, 70))
    od.ellipse([-200, 700, 600, 1300], fill=(*BLUE_SOFT, 40))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    f_brand = font(FONT_BOLD, 42)
    f_ep = font(FONT_SERIF, 120)
    f_title = font(FONT_BOLD, 72)
    f_phase = font(FONT_REG, 36)

    draw.text((110, 90), "THE JAVA STORY", font=f_brand, fill=BLUE)
    draw.text((110, 200), f"EP {n:02d}", font=f_ep, fill=CREAM)

    title_lines = wrap_lines(draw, title, f_title, 1500)
    y = 380
    for line in title_lines[:3]:
        draw.text((110, y), line, font=f_title, fill=CREAM)
        y += 90

    if phase:
        draw.text((110, min(y + 40, 920)), phase, font=f_phase, fill=MUTED)

    draw.rectangle([110, 1000, 700, 1008], fill=BLUE)

    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=92, optimize=True)


def main() -> None:
    folders = sorted(
        ROOT.glob("ep*"),
        key=lambda p: int(re.match(r"ep(\d+)", p.name).group(1)),
    )
    assert len(folders) == 85, len(folders)
    for folder in folders:
        n = int(re.match(r"ep(\d+)", folder.name).group(1))
        title = title_from_folder(folder, n)
        phase = phase_for(n)
        dest = folder / "thumbnail.jpg"
        make_thumbnail(n, title, phase, dest)
        print(f"wrote EP{n:02d}: {title} -> {dest}")
    print(f"done {len(folders)} blue Spring-style thumbnails")


if __name__ == "__main__":
    main()
