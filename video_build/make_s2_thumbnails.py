#!/usr/bin/env python3
"""Generate YouTube thumbnails for Season 2 episodes missing them (81, 83, 84, 85)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/workspace")
OUTPUT = ROOT / "output"
ARTIFACTS = Path("/opt/cursor/artifacts")

W, H = 1920, 1080
BG = (12, 16, 28)
SURFACE = (24, 32, 52)
WHITE = (245, 247, 250)
MUTED = (150, 160, 180)
ORANGE = (232, 119, 34)
BLUE = (80, 160, 230)
GREEN = (90, 200, 140)
RED = (220, 90, 90)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_REG_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
FONT_SERIF_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
]


def pick_font(paths, size):
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def font_bold(size):
    return pick_font(FONT_CANDIDATES, size)


def font_reg(size):
    return pick_font(FONT_REG_CANDIDATES, size)


def font_serif(size):
    return pick_font(FONT_SERIF_CANDIDATES, size)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def gradient_bg():
    img = Image.new("RGB", (W, H), BG)
    px = img.load()
    for y in range(H):
        for x in range(0, W, 4):
            t = (x / W) * 0.35 + (y / H) * 0.45
            c = mix(BG, (18, 28, 48), t)
            for dx in range(4):
                if x + dx < W:
                    px[x + dx, y] = c
    # soft orange glow top-left, blue bottom-right
    overlay = Image.new("RGB", (W, H), BG)
    od = ImageDraw.Draw(overlay)
    od.ellipse([-200, -200, 900, 700], fill=(40, 24, 12))
    od.ellipse([1100, 400, 2200, 1400], fill=(12, 28, 48))
    img = Image.blend(img, overlay, 0.35)
    return img


EPISODES = [
    {
        "ep": 81,
        "title": "Caching Strategies",
        "subtitle": "layers · invalidation · stampede control",
        "accent": ORANGE,
        "pills": [("CDN", BLUE), ("Redis", ORANGE), ("TTL", GREEN)],
        "stem": "Caching_Strategies",
    },
    {
        "ep": 83,
        "title": "Event-Driven Architecture",
        "subtitle": "facts · outbox · idempotent consumers",
        "accent": BLUE,
        "pills": [("Events", ORANGE), ("Outbox", BLUE), ("Kafka", GREEN)],
        "stem": "Event_Driven_Architecture",
    },
    {
        "ep": 84,
        "title": "Performance Playbook",
        "subtitle": "measure · bottleneck · hottest path",
        "accent": GREEN,
        "pills": [("SLO", ORANGE), ("Profile", BLUE), ("p99", GREEN)],
        "stem": "Performance_Playbook",
    },
    {
        "ep": 85,
        "title": "Production Readiness",
        "subtitle": "checklist · release · staff lens",
        "accent": RED,
        "pills": [("SLOs", ORANGE), ("Rollback", BLUE), ("On-call", GREEN)],
        "stem": "Production_Readiness_Capstone",
    },
]


def draw_centered(d, text, y, fnt, fill):
    bbox = d.textbbox((0, 0), text, font=fnt)
    x = (W - (bbox[2] - bbox[0])) // 2
    d.text((x, y), text, font=fnt, fill=fill)
    return bbox[3] - bbox[1]


def make_thumbnail(epdef: dict) -> Image.Image:
    img = gradient_bg()
    d = ImageDraw.Draw(img)

    # brand bar
    d.rounded_rectangle([80, 70, 520, 140], radius=18, fill=SURFACE, outline=ORANGE, width=3)
    d.text((110, 88), "THE JAVA STORY", font=font_bold(28), fill=ORANGE)

    d.rounded_rectangle([540, 70, 780, 140], radius=18, fill=mix(BG, SURFACE, 0.8), outline=BLUE, width=2)
    d.text((575, 92), "SEASON 2", font=font_bold(26), fill=BLUE)

    # episode badge
    d.rounded_rectangle([1480, 70, 1840, 140], radius=18, fill=SURFACE, outline=epdef["accent"], width=3)
    d.text((1520, 88), f"EPISODE {epdef['ep']}", font=font_bold(28), fill=WHITE)

    # accent rule
    d.rectangle([200, 320, 1720, 328], fill=epdef["accent"])

    # title
    draw_centered(d, epdef["title"], 380, font_serif(72), WHITE)
    draw_centered(d, epdef["subtitle"], 490, font_reg(34), MUTED)

    # pills
    pills = epdef["pills"]
    total_w = len(pills) * 360 + (len(pills) - 1) * 40
    x0 = (W - total_w) // 2
    for i, (lab, col) in enumerate(pills):
        x = x0 + i * 400
        d.rounded_rectangle([x, 620, x + 360, 740], radius=20, fill=SURFACE, outline=col, width=4)
        bbox = d.textbbox((0, 0), lab, font=font_bold(36))
        tw = bbox[2] - bbox[0]
        d.text((x + (360 - tw) // 2, 655), lab, font=font_bold(36), fill=col)

    # footer
    d.text((120, 960), "Premium Java · Production Systems", font=font_reg(28), fill=MUTED)
    d.text((1380, 960), "YouTube · 4–5 min", font=font_reg(28), fill=MUTED)
    return img


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    for epdef in EPISODES:
        img = make_thumbnail(epdef)
        # canonical names
        slug = {
            81: "81-caching-strategies",
            83: "83-event-driven-architecture",
            84: "84-performance-playbook",
            85: "85-production-readiness-capstone",
        }[epdef["ep"]]
        ep_dir = ROOT / "episodes" / slug
        ep_dir.mkdir(parents=True, exist_ok=True)
        paths = [
            OUTPUT / f"Java_Episode_{epdef['ep']}_thumbnail.jpg",
            ep_dir / "thumbnail.jpg",
        ]

        for p in paths:
            img.save(p, quality=95)
            print("wrote", p)
        art = ARTIFACTS / f"Java_Episode_{epdef['ep']}_thumbnail.jpg"
        img.save(art, quality=95)
        print("wrote", art)


if __name__ == "__main__":
    main()
