#!/usr/bin/env python3
"""Generate YouTube upload packs for every Spring Story episode.

Mirrors java-story/v1 episode packs:
  title.txt, youtube_description.txt, tags.txt, chapters.txt,
  thumbnail.jpg, narration.md, README.md

Thumbnails are branded stills (not video frames) — no burned-in
subtitles or caption text from a recording.
"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/workspace/spring-story")
SRC = ROOT / "episodes"
OUT = ROOT / "v1" / "episodes"
WORDS_PER_MIN = 155  # spoken-lesson estimate for chapter timestamps

# Spring-ish palette (not flat purple AI default)
BG_TOP = (10, 22, 18)
BG_BOT = (16, 36, 28)
SURFACE = (22, 48, 38)
GREEN = (109, 179, 63)       # Spring leaf
GREEN_DIM = (70, 120, 50)
CREAM = (245, 247, 240)
MUTED = (170, 190, 175)
LEAF = (140, 200, 90)

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


def font(paths, size):
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def slugify(title: str) -> str:
    s = title.lower()
    s = s.replace("@", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def parse_episode(path: Path) -> dict:
    text = path.read_text()
    n = int(re.match(r"ep(\d+)_", path.name).group(1))
    title_m = re.search(r"^# Episode \d+ — (.+)$", text, re.M)
    title = title_m.group(1).strip() if title_m else path.stem
    phase_m = re.search(r"\|\s*Phase\s*\|\s*([^|]+)\|", text)
    phase = phase_m.group(1).strip() if phase_m else ""
    narr_m = re.search(
        r"## Full narration\n\n(.*?)(?:\n## Source attribution|\Z)",
        text,
        re.S,
    )
    narration = (narr_m.group(1).strip() if narr_m else text).strip()
    return {
        "n": n,
        "title": title,
        "phase": phase,
        "narration": narration,
        "source_path": path,
        "full_md": text,
    }


def sentences(text: str) -> list[str]:
    # Strip code fences for bullets/chapters
    plain = re.sub(r"```[\s\S]*?```", " ", text)
    plain = re.sub(r"`([^`]+)`", r"\1", plain)
    plain = re.sub(r"\s+", " ", plain).strip()
    parts = re.split(r"(?<=[.!?])\s+", plain)
    out = []
    for p in parts:
        p = p.strip()
        if len(p) < 28:
            continue
        if p.startswith("|"):
            continue
        out.append(p)
    return out


def fmt_ts(seconds: float) -> str:
    s = max(0, int(seconds))
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def build_chapters(narration: str) -> list[tuple[str, str]]:
    """Approximate chapter timestamps from paragraph beats."""
    paras = [p.strip() for p in re.split(r"\n\n+", narration) if p.strip()]
    # skip pure code blocks as chapter titles
    beats = []
    for p in paras:
        if p.startswith("```"):
            continue
        # first sentence-ish as label
        label = re.sub(r"\s+", " ", p.split("\n")[0]).strip()
        label = re.sub(r"[#>*_`]", "", label)
        if len(label) < 20:
            continue
        # skip code-looking lines as chapter titles
        if re.search(
            r"[{};]=|^\s*(public|private|protected|class|interface|@|"
            r"import |return |void |new |if \(|for \()",
            label,
        ):
            continue
        if len(label) > 70:
            label = label[:67].rsplit(" ", 1)[0] + "…"
        words = len(re.findall(r"\w+", p))
        beats.append((label, words))
    if not beats:
        return [("0:00", "Introduction")]

    # Merge tiny beats; target ~8–14 chapters
    merged = []
    buf_label, buf_words = beats[0][0], beats[0][1]
    for label, words in beats[1:]:
        if buf_words < 80:
            buf_words += words
        else:
            merged.append((buf_label, buf_words))
            buf_label, buf_words = label, words
    merged.append((buf_label, buf_words))
    if len(merged) > 14:
        # keep first, last, and evenly spaced middle
        idxs = sorted(set([0, len(merged) - 1] + [
            round(i * (len(merged) - 1) / 11) for i in range(1, 11)
        ]))
        merged = [merged[i] for i in idxs]

    chapters = []
    t = 0.0
    for label, words in merged:
        chapters.append((fmt_ts(t), label))
        t += (words / WORDS_PER_MIN) * 60.0
    return chapters


def yt_title(ep: dict) -> str:
    return f"The Spring Story Ep{ep['n']:02d}: {ep['title']}"


def yt_tags(ep: dict) -> str:
    base = [
        "Spring",
        "Spring Framework",
        "Spring Boot",
        "Java",
        "Spring Tutorial",
        "Learn Spring",
        "The Spring Story",
        f"Episode {ep['n']}",
        ep["title"],
        "Software Engineering",
        "Backend Development",
        "Java Enterprise",
    ]
    # phase keyword
    if ep["phase"]:
        base.append(ep["phase"].split("—")[-1].strip())
    # de-dupe preserving order
    seen = set()
    out = []
    for t in base:
        k = t.lower()
        if k not in seen and t.strip():
            seen.add(k)
            out.append(t.strip())
    return ", ".join(out[:15])


def yt_description(ep: dict, chapters: list[tuple[str, str]], next_title: str | None) -> str:
    sents = sentences(ep["narration"])
    bullets = sents[:8]
    if len(bullets) < 3:
        bullets = [ep["title"], "A spoken lesson from The Spring Story series."]
    lines = [
        f"The Spring Story — Episode {ep['n']:02d}: {ep['title']}",
        "",
        "The Spring Story is a structured series that teaches Spring Framework and Spring Boot from first principles through production practice — one clear episode at a time.",
        "",
        "In this episode:",
    ]
    for b in bullets:
        short = b if len(b) <= 110 else b[:107].rsplit(" ", 1)[0] + "…"
        lines.append(f"• {short}")
    if len(sents) > 8:
        lines.append("• …and more")
    lines += ["", "Timestamps"]
    for ts, label in chapters:
        lines.append(f"{ts} {label}")
    lines += [
        "",
        "Resources",
        "- Narration / transcript: see narration.md in this episode folder",
        "- Series index: spring-story/v1/INDEX.md",
        "",
    ]
    if next_title:
        lines.append(f"Next up: Episode {ep['n'] + 1:02d} — {next_title}")
        lines.append("")
    lines += [
        "If this helped, like the video and subscribe for the next episode.",
        "Comment with questions — I read them.",
        "",
        "#Spring #SpringBoot #Java #TheSpringStory",
    ]
    return "\n".join(lines) + "\n"


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


def make_thumbnail(ep: dict, dest: Path) -> None:
    W, H = 1920, 1080
    # Vertical gradient via a 1-wide strip, then resize (fast)
    strip = Image.new("RGB", (1, H))
    sp = strip.load()
    for y in range(H):
        t = y / (H - 1)
        sp[0, y] = tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOT))
    img = strip.resize((W, H), Image.Resampling.BILINEAR)

    draw = ImageDraw.Draw(img)
    # left accent bar
    draw.rectangle([0, 0, 28, H], fill=GREEN)
    # soft leaf orb (decorative, not text)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse([1300, -120, 2100, 680], fill=(*GREEN_DIM, 70))
    od.ellipse([-200, 700, 600, 1300], fill=(*LEAF, 40))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    f_brand = font(FONT_BOLD, 42)
    f_ep = font(FONT_SERIF, 120)
    f_title = font(FONT_BOLD, 72)
    f_phase = font(FONT_REG, 36)

    # brand
    draw.text((110, 90), "THE SPRING STORY", font=f_brand, fill=GREEN)
    # episode number
    draw.text((110, 200), f"EP {ep['n']:02d}", font=f_ep, fill=CREAM)

    # title wrapped
    title_lines = wrap_lines(draw, ep["title"], f_title, 1500)
    y = 380
    for line in title_lines[:3]:
        draw.text((110, y), line, font=f_title, fill=CREAM)
        y += 90

    if ep["phase"]:
        phase = ep["phase"]
        draw.text((110, min(y + 40, 920)), phase, font=f_phase, fill=MUTED)

    # bottom rule
    draw.rectangle([110, 1000, 700, 1008], fill=GREEN)

    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "JPEG", quality=92, optimize=True)


def write_pack(ep: dict, next_ep: dict | None) -> Path:
    folder = OUT / f"ep{ep['n']:02d}-{slugify(ep['title'])}"
    folder.mkdir(parents=True, exist_ok=True)

    chapters = build_chapters(ep["narration"])
    next_title = next_ep["title"] if next_ep else None

    (folder / "title.txt").write_text(yt_title(ep) + "\n")
    (folder / "tags.txt").write_text(yt_tags(ep) + "\n")
    (folder / "youtube_description.txt").write_text(
        yt_description(ep, chapters, next_title)
    )
    (folder / "chapters.txt").write_text(
        "\n".join(f"{ts} {label}" for ts, label in chapters) + "\n"
    )
    (folder / "narration.md").write_text(ep["full_md"])

    make_thumbnail(ep, folder / "thumbnail.jpg")

    prev_link = ""
    next_link = ""
    if ep["n"] > 1:
        prev_link = f"- Previous: see INDEX.md\n"
    if next_ep:
        next_link = f"- Next: [ep{next_ep['n']:02d}-{slugify(next_ep['title'])}](../ep{next_ep['n']:02d}-{slugify(next_ep['title'])}/)\n"

    readme = f"""# Episode {ep['n']:02d} — {ep['title']}

**Series:** The Spring Story · **YouTube upload pack**

![Episode {ep['n']:02d} thumbnail](thumbnail.jpg)

## YouTube upload checklist

| Asset | File |
|---|---|
| Title | [`title.txt`](title.txt) |
| Description + timestamps | [`youtube_description.txt`](youtube_description.txt) |
| Tags | [`tags.txt`](tags.txt) |
| Thumbnail | [`thumbnail.jpg`](thumbnail.jpg) |
| Chapters | [`chapters.txt`](chapters.txt) |
| Narration / transcript | [`narration.md`](narration.md) |

> Video (`.mp4`) and captions (`.srt`) are produced in a later video-build pass. Upload metadata and thumbnail are ready now.

## Suggested upload

1. Upload the episode video when available (clean preferred; captioned optional).
2. Set title from `title.txt`.
3. Paste `youtube_description.txt` into the YouTube description.
4. Upload `thumbnail.jpg` (branded still — not a video frame; no burned-in subtitles).
5. Add tags from `tags.txt`.
6. Upload `.srt` captions when available.

## Navigation

{prev_link}{next_link}- Index: [`../../INDEX.md`](../../INDEX.md)
"""
    (folder / "README.md").write_text(readme)
    return folder


def main() -> None:
    paths = sorted(SRC.glob("ep*.md"), key=lambda p: int(re.match(r"ep(\d+)", p.name).group(1)))
    eps = [parse_episode(p) for p in paths]
    assert len(eps) == 112, len(eps)

    OUT.mkdir(parents=True, exist_ok=True)
    for i, ep in enumerate(eps):
        nxt = eps[i + 1] if i + 1 < len(eps) else None
        folder = write_pack(ep, nxt)
        print(f"wrote {folder.name}")

    # INDEX + README for v1
    index_lines = [
        "# The Spring Story v1 — episode index (YouTube upload packs)",
        "",
        "Total episodes: **112**",
        "",
        "Each episode folder includes: **thumbnail**, **title**, **YouTube description with timestamps**, **tags**, **chapters**, and **narration**. Video/SRT land in a later production pass.",
        "",
    ]
    phase = None
    for ep in eps:
        if ep["phase"] != phase:
            phase = ep["phase"]
            index_lines += ["", f"## {phase}", ""]
        slug = slugify(ep["title"])
        index_lines.append(
            f"- ✅ [**{ep['n']:02d}. {ep['title']}**](episodes/ep{ep['n']:02d}-{slug}/)"
        )
    (ROOT / "v1" / "INDEX.md").write_text("\n".join(index_lines) + "\n")

    readme = """# The Spring Story — v1 YouTube upload packs

Episode-by-episode upload kits for **The Spring Story**, parallel to `java-story/v1`.

## Per-episode contents

| File | Purpose |
|---|---|
| `title.txt` | YouTube title |
| `youtube_description.txt` | Description + timestamps |
| `tags.txt` | Comma-separated tags |
| `chapters.txt` | Chapter list (estimated from narration pacing) |
| `thumbnail.jpg` | 1920×1080 branded thumbnail (**not** a video frame; no burned-in subtitles) |
| `narration.md` | Full spoken narration / transcript source |
| `README.md` | Upload checklist |

## Notes

- Thumbnails are designed stills for upload CTR — they intentionally do **not** use screenshots or captioned video frames.
- Chapter timestamps are estimates from narration length (~155 wpm) until final video timing is available.
- MP4 / SRT assets are added when the video-production pipeline runs per episode.
"""
    (ROOT / "v1" / "README.md").write_text(readme)
    print("done", len(eps), "packs ->", OUT)


if __name__ == "__main__":
    main()
