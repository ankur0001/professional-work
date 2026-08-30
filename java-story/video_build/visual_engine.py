#!/usr/bin/env python3
"""Animated visual scenes for The Java Story v2 videos.

Turns narration beats into illustrated, motion-driven frames:
flows, stacks, comparisons, pipelines, callouts — not text walls.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Callable

from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080

# Palette — deep ink + amber (avoid purple/glow defaults)
BG_TOP = (10, 16, 28)
BG_BOT = (18, 36, 48)
PANEL = (22, 34, 48)
PANEL2 = (28, 44, 62)
AMBER = (242, 153, 41)
TEAL = (56, 189, 168)
SKY = (96, 165, 250)
CORAL = (248, 113, 113)
CREAM = (244, 240, 232)
MUTED = (148, 163, 178)
WHITE = (255, 255, 255)
LINE = (51, 65, 85)

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def ease_out(t: float) -> float:
    t = clamp(t)
    return 1 - (1 - t) ** 3


def ease_in_out(t: float) -> float:
    t = clamp(t)
    return 3 * t * t - 2 * t * t * t


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = clamp(t)
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))  # type: ignore[return-value]


_BG_CACHE: Image.Image | None = None


def gradient_bg() -> Image.Image:
    """Cached vertical gradient — rebuilt once per process."""
    global _BG_CACHE
    if _BG_CACHE is not None:
        return _BG_CACHE.copy()
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        c = mix(BG_TOP, BG_BOT, y / (H - 1))
        for x in range(W):
            px[x, y] = c
    # light amber wash band (cheap row tint)
    for y in range(160, 220):
        for x in range(W):
            px[x, y] = mix(px[x, y], AMBER, 0.04)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for i in range(28):
        a = int(3 + i * 1.4)
        d.rectangle([i, i, W - 1 - i, H - 1 - i], outline=(0, 0, 0, a))
    _BG_CACHE = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    return _BG_CACHE.copy()


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill,
    outline=None,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color=AMBER,
    width: int = 4,
    progress: float = 1.0,
) -> None:
    progress = clamp(progress)
    if progress <= 0:
        return
    x = int(lerp(x1, x2, progress))
    y = int(lerp(y1, y2, progress))
    draw.line([(x1, y1), (x, y)], fill=color, width=width)
    if progress > 0.85:
        ang = math.atan2(y2 - y1, x2 - x1)
        size = 14
        p1 = (x2, y2)
        p2 = (int(x2 - size * math.cos(ang - 0.5)), int(y2 - size * math.sin(ang - 0.5)))
        p3 = (int(x2 - size * math.cos(ang + 0.5)), int(y2 - size * math.sin(ang + 0.5)))
        draw.polygon([p1, p2, p3], fill=color)


def wrap_lines(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int, max_lines: int = 4) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


def extract_headline(beat: str, max_words: int = 7) -> str:
    """Pull a short on-screen title — never dump the full narration."""
    cleaned = re.sub(r"\s+", " ", beat).strip()
    # Prefer clause before colon / dash / question
    for sep in [": ", " — ", " - ", "? ", "! "]:
        if sep in cleaned:
            head = cleaned.split(sep)[0].strip()
            if 3 <= len(head.split()) <= 12:
                cleaned = head + ("?" if sep.startswith("?") else "")
                break
    words = cleaned.split()
    if len(words) <= max_words:
        return cleaned.rstrip(".,;")
    # Prefer starting at a capital / keyword
    return " ".join(words[:max_words]).rstrip(".,;") + "…"


def extract_tokens(beat: str, limit: int = 5) -> list[str]:
    stop = {
        "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "for", "with",
        "is", "are", "was", "were", "be", "been", "that", "this", "these", "those",
        "it", "as", "at", "by", "from", "we", "you", "they", "not", "can", "could",
        "should", "would", "will", "just", "into", "about", "when", "what", "how",
        "why", "which", "than", "then", "also", "more", "most", "some", "any", "if",
        "do", "does", "did", "have", "has", "had", "our", "your", "their", "its",
    }
    words = re.findall(r"[A-Za-z][A-Za-z0-9_/-]{2,}", beat)
    out: list[str] = []
    seen = set()
    for w in words:
        key = w.lower()
        if key in stop or key in seen:
            continue
        seen.add(key)
        out.append(w if w.isupper() or w[0].isupper() else w.capitalize())
        if len(out) >= limit:
            break
    return out


def concept_labels(kind: str, beat: str, tokens: list[str]) -> list[str]:
    """Prefer domain labels over raw narration words for diagram boxes."""
    b = beat.lower()
    if kind == "stack":
        if "jdk" in b or "jre" in b or "jvm" in b:
            return ["Your App", "JDK tools", "JRE libs", "JVM"]
        if "heap" in b or "gc" in b or "garbage" in b or "collection" in b:
            return ["Young gen", "Old gen", "Metaspace", "Native"]
        if "stack" in b:
            return ["Frames", "Locals", "Operand stack", "Return"]
        return (tokens[:4] or ["Layer 1", "Layer 2", "Layer 3"])
    if kind == "pipeline":
        return ["Source", "Map", "Filter", "Collect"]
    if kind == "lanes":
        n = 4 if any(k in b for k in ("thousand", "many", "pool", "worker")) else 3
        return [f"Worker {i}" for i in range(1, n + 1)]
    if kind == "flow":
        if "request" in b or "response" in b or "api" in b:
            return ["Client", "API", "Service", "Result"]
        if any(k in b for k in ("first", "then", "next", "finally", "step")):
            return ["Start", "Process", "Validate", "Done"]
        cleaned = [t for t in tokens if t.lower() not in {"the", "a", "is", "not", "and", "last", "another"}][:4]
        return cleaned if len(cleaned) >= 3 else ["Idea", "Build", "Ship", "Learn"]
    if kind == "nodes":
        if "event" in b:
            return ["Producer", "Bus", "Consumer", "Store"]
        if "gateway" in b or "service" in b:
            return ["Client", "Gateway", "Service", "DB"]
        return tokens[:4] or ["A", "B", "C", "D"]
    if kind == "rings":
        return ["L1 hot", "L2 warm", "Origin", "Miss path"]
    if kind == "compare":
        if len(tokens) >= 2:
            return tokens[:2]
        return ["Option A", "Option B"]
    return tokens


@dataclass
class Scene:
    kind: str
    headline: str
    tokens: list[str]
    beat: str
    idx: int
    total: int


def has_word(text: str, *words: str) -> bool:
    return any(re.search(rf"\b{re.escape(w)}\b", text) for w in words)


def plan_scene(beat: str, idx: int, total: int, title: str) -> Scene:
    b = beat.lower()
    headline = extract_headline(beat)
    tokens = extract_tokens(beat)

    if idx == 0:
        kind = "title"
        headline = title
    elif has_word(b, "stream", "streams", "map", "filter", "flatmap", "collector", "collectors") or "pipeline" in b:
        kind = "pipeline"
    elif has_word(b, "heap", "stack", "jdk", "jre", "jvm", "metaspace") or "native memory" in b or "garbage" in b:
        kind = "stack"
    elif has_word(b, "thread", "threads", "lock", "locks", "executor", "future", "futures") or any(
        k in b for k in ("synchron", "concurrent", "parallel")
    ):
        kind = "lanes"
    elif has_word(b, "cache", "cached", "ttl") or "cache hit" in b or "cache miss" in b:
        kind = "rings"
    elif has_word(b, "service", "services", "gateway", "event", "events", "queue", "topic", "api"):
        kind = "nodes"
    elif any(k in b for k in ("versus", " vs ", "instead", "rather than", "trade-off", "tradeoff", "compare")):
        kind = "compare"
    elif any(k in b for k in ("code", "method", "class", "interface", "annotation", "look at this")):
        kind = "code"
    elif any(k in b for k in ("step", "first", "then", "next", "finally", "flow", "request", "response")):
        kind = "flow"
    elif "?" in beat:
        kind = "question"
    else:
        kinds = ["callout", "flow", "tokens", "stack", "pipeline", "nodes"]
        kind = kinds[idx % len(kinds)]

    labels = concept_labels(kind, beat, tokens)
    if len(labels) < 3 and kind in {"flow", "pipeline", "tokens", "stack", "lanes", "nodes"}:
        labels = (labels + ["Idea", "Detail", "Result", "Outcome"])[:4]

    return Scene(kind=kind, headline=headline, tokens=labels[:5], beat=beat, idx=idx, total=total)


def chrome(draw: ImageDraw.ImageDraw, ep: int, title: str, idx: int, total: int, t: float) -> None:
    fb = font(FONT_BOLD, 32)
    fr = font(FONT_REG, 24)
    draw.text((72, 40), "The Java Story", font=fb, fill=AMBER)
    draw.text((72, 86), f"Episode {ep:02d}  ·  {title}", font=fr, fill=MUTED)
    # progress rail
    x0, x1, y = 72, W - 72, 130
    draw.rounded_rectangle([x0, y, x1, y + 8], radius=4, fill=PANEL)
    prog = (idx + ease_out(t)) / max(total, 1)
    draw.rounded_rectangle([x0, y, x0 + int((x1 - x0) * clamp(prog)), y + 8], radius=4, fill=TEAL)
    # episode badge
    badge = f"{idx + 1}/{total}"
    draw.text((W - 160, H - 56), badge, font=fr, fill=MUTED)


def lower_third(draw: ImageDraw.ImageDraw, text: str, appear: float) -> None:
    """Short caption strip — supports speech, does not replace visuals."""
    a = ease_out(appear)
    if a <= 0:
        return
    fr = font(FONT_REG, 30)
    lines = wrap_lines(draw, text, fr, W - 200, max_lines=2)
    box_h = 36 + 40 * len(lines)
    y0 = H - 90 - box_h
    # slide up
    y = int(lerp(H + 20, y0, a))
    rounded_rect(draw, (60, y, W - 60, y + box_h), 16, PANEL, outline=LINE, width=2)
    draw.rectangle([60, y, 72, y + box_h], fill=AMBER)
    yy = y + 18
    for line in lines:
        draw.text((92, yy), line, font=fr, fill=CREAM)
        yy += 40


# --- scene drawers (progress 0..1 within beat) ---------------------------------

def draw_title(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 72)
    fr = font(FONT_REG, 34)
    # expanding amber bar
    bar_w = int(lerp(80, 420, ease_out(p)))
    draw.rectangle([72, 220, 72 + bar_w, 228], fill=AMBER)
    lines = wrap_lines(draw, sc.headline, fb, W - 200, max_lines=3)
    y = 260
    for i, line in enumerate(lines):
        alpha = ease_out(clamp((p - i * 0.12) / 0.5))
        col = mix(BG_BOT, WHITE, alpha)
        draw.text((72, y), line, font=fb, fill=col)
        y += 88
    # orbit dots
    cx, cy = W - 320, 520
    for i in range(8):
        ang = p * math.tau + i * (math.tau / 8)
        r = 90 + 20 * math.sin(p * 4 + i)
        x = int(cx + r * math.cos(ang))
        yy = int(cy + r * 0.6 * math.sin(ang))
        rad = 8 + (i % 3) * 3
        color = [AMBER, TEAL, SKY][i % 3]
        draw.ellipse([x - rad, yy - rad, x + rad, yy + rad], fill=color)
    draw.text((72, y + 30), "Narrated walkthrough · animated cut", font=fr, fill=MUTED)


def draw_flow(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    steps = (sc.tokens or ["Start", "Work", "Result"])[:4]
    n = len(steps)
    box_w = min(360, (W - 160 - (n - 1) * 50) // n)
    gap = 50
    total_w = n * box_w + (n - 1) * gap
    x0 = (W - total_w) // 2
    y = 420
    for i, label in enumerate(steps):
        appear = ease_out(clamp((p - i * 0.15) / 0.35))
        x = x0 + i * (box_w + gap)
        yy = int(lerp(y + 40, y, appear))
        fill = mix(PANEL, PANEL2, appear)
        rounded_rect(draw, (x, yy, x + box_w, yy + 140), 20, fill, outline=TEAL if appear > 0.5 else LINE, width=3)
        # step number
        draw.ellipse([x + 18, yy + 18, x + 58, yy + 58], fill=AMBER if appear > 0.4 else PANEL)
        draw.text((x + 28, yy + 22), str(i + 1), font=font(FONT_BOLD, 28), fill=BG_TOP)
        fl = font(FONT_BOLD, 28)
        lines = wrap_lines(draw, label, fl, box_w - 36, 2)
        ly = yy + 70
        for ln in lines:
            draw.text((x + 18, ly), ln, font=fl, fill=CREAM)
            ly += 32
        if i < n - 1:
            draw_arrow(draw, x + box_w + 6, yy + 70, x + box_w + gap - 6, yy + 70, AMBER, 5, ease_out(clamp((p - 0.2 - i * 0.15) / 0.3)))
    lower_third(draw, sc.beat, clamp((p - 0.35) / 0.4))


def draw_compare(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    left = sc.tokens[0] if sc.tokens else "Approach A"
    right = sc.tokens[1] if len(sc.tokens) > 1 else "Approach B"
    a = ease_out(p)
    # left panel
    rounded_rect(draw, (100, 280, 860, 720), 24, PANEL, outline=CORAL, width=3)
    draw.text((140, 320), "A", font=font(FONT_BOLD, 40), fill=CORAL)
    draw.text((140, 400), left, font=font(FONT_BOLD, 40), fill=CREAM)
    # right panel
    rounded_rect(draw, (1060, 280, 1820, 720), 24, PANEL, outline=TEAL, width=3)
    draw.text((1100, 320), "B", font=font(FONT_BOLD, 40), fill=TEAL)
    draw.text((1100, 400), right, font=font(FONT_BOLD, 40), fill=CREAM)
    # vs badge
    cx = W // 2
    r = int(lerp(10, 48, a))
    draw.ellipse([cx - r, 460 - r, cx + r, 460 + r], fill=AMBER)
    draw.text((cx - 24, 438), "VS", font=font(FONT_BOLD, 28), fill=BG_TOP)
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


def draw_stack(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    layers = (sc.tokens or ["App", "Runtime", "OS"])[:5]
    colors = [SKY, TEAL, AMBER, CORAL, MUTED]
    base_y = 780
    box_h = 78
    for i, label in enumerate(reversed(layers)):
        appear = ease_out(clamp((p - i * 0.12) / 0.35))
        width = int(lerp(400, 980 - i * 70, appear))
        x = (W - width) // 2
        y = base_y - i * (box_h + 18)
        y = int(lerp(y + 50, y, appear))
        rounded_rect(draw, (x, y, x + width, y + box_h), 16, PANEL2, outline=colors[i % len(colors)], width=3)
        draw.text((x + 28, y + 18), label, font=font(FONT_BOLD, 32), fill=CREAM)
    lower_third(draw, sc.beat, clamp((p - 0.35) / 0.4))


def draw_pipeline(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    stages = (sc.tokens or ["Source", "Map", "Filter", "Collect"])[:5]
    y = 480
    x = 100
    stage_w = 220
    for i, label in enumerate(stages):
        appear = ease_out(clamp((p - i * 0.12) / 0.3))
        yy = int(lerp(y + 30, y, appear))
        # chevron-ish box
        rounded_rect(draw, (x, yy - 50, x + stage_w, yy + 50), 14, PANEL, outline=TEAL, width=3)
        draw.text((x + 20, yy - 18), label[:14], font=font(FONT_BOLD, 28), fill=CREAM)
        # moving particle along path
        if i < len(stages) - 1:
            draw_arrow(draw, x + stage_w + 4, yy, x + stage_w + 70, yy, AMBER, 5, appear)
            # pulse dot
            pulse = ease_in_out((p * 2 + i * 0.2) % 1.0)
            dx = int(lerp(x + stage_w + 8, x + stage_w + 66, pulse))
            draw.ellipse([dx - 8, yy - 8, dx + 8, yy + 8], fill=AMBER)
        x += stage_w + 80
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


def draw_lanes(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    lanes = min(4, max(2, len(sc.tokens) or 3))
    labels = (sc.tokens + [f"Worker {i+1}" for i in range(lanes)])[:lanes]
    for i, label in enumerate(labels):
        y = 280 + i * 140
        appear = ease_out(clamp((p - i * 0.1) / 0.35))
        rounded_rect(draw, (120, y, W - 120, y + 100), 18, PANEL, outline=SKY, width=2)
        draw.text((150, y + 30), label[:28], font=font(FONT_BOLD, 30), fill=CREAM)
        # moving task block
        tx = int(lerp(400, W - 280, ease_in_out((p + i * 0.17) % 1.0)))
        rounded_rect(draw, (tx, y + 25, tx + 120, y + 75), 10, AMBER)
        draw.text((tx + 28, y + 36), "task", font=font(FONT_BOLD, 22), fill=BG_TOP)
        # fade unused
        if appear < 1:
            pass
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


def draw_code(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 44)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    # window chrome
    rounded_rect(draw, (160, 260, W - 160, 780), 20, (15, 23, 34), outline=LINE, width=2)
    draw.ellipse([190, 290, 218, 318], fill=CORAL)
    draw.ellipse([236, 290, 264, 318], fill=AMBER)
    draw.ellipse([282, 290, 310, 318], fill=TEAL)
    mono = font(FONT_MONO, 30)
    snippets = [
        f"// {sc.tokens[0] if sc.tokens else 'concept'}",
        "public void demonstrate() {",
        f"    var focus = {sc.tokens[1] if len(sc.tokens) > 1 else 'idea'};",
        "    return apply(focus);",
        "}",
    ]
    y = 360
    for i, line in enumerate(snippets):
        appear = ease_out(clamp((p - i * 0.08) / 0.25))
        col = mix(PANEL, CREAM, appear)
        # syntax tint
        if line.strip().startswith("//"):
            col = mix(PANEL, TEAL, appear)
        elif "public" in line or "return" in line:
            col = mix(PANEL, SKY, appear)
        draw.text((220, y), line, font=mono, fill=col)
        y += 54
    # cursor blink
    if int(p * 10) % 2 == 0:
        draw.rectangle([220, y, 240, y + 36], fill=AMBER)
    lower_third(draw, sc.beat, clamp((p - 0.25) / 0.4))


def draw_rings(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    cx, cy = 620, 560
    for i, r in enumerate([80, 160, 240, 320]):
        appear = ease_out(clamp((p - i * 0.1) / 0.35))
        rr = int(r * appear)
        color = [AMBER, TEAL, SKY, MUTED][i]
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=color, width=5)
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=AMBER)
    # labels on right
    labels = (sc.tokens or ["Hot", "Warm", "Cold", "Store"])[:4]
    for i, lab in enumerate(labels):
        y = 360 + i * 80
        appear = ease_out(clamp((p - 0.15 - i * 0.1) / 0.3))
        rounded_rect(draw, (1000, y, 1700, y + 60), 12, PANEL, outline=LINE)
        draw.text((1030, y + 12), lab, font=font(FONT_BOLD, 28), fill=mix(PANEL, CREAM, appear))
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


def draw_nodes(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    labels = (sc.tokens or ["Client", "API", "Service", "Store"])[:5]
    # positions
    pts = []
    n = len(labels)
    for i, lab in enumerate(labels):
        if n == 1:
            pts.append((W // 2, 520))
        elif i == 0:
            pts.append((280, 520))
        elif i == n - 1:
            pts.append((W - 280, 520))
        else:
            pts.append((280 + i * ((W - 560) // max(n - 1, 1)), 360 + (80 if i % 2 else 200)))
    # edges first
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]
        x2, y2 = pts[i + 1]
        draw_arrow(draw, x1 + 70, y1, x2 - 70, y2, AMBER, 4, ease_out(clamp((p - 0.15 - i * 0.1) / 0.35)))
    for i, (lab, (x, y)) in enumerate(zip(labels, pts)):
        appear = ease_out(clamp((p - i * 0.12) / 0.35))
        rw, rh = 160, 90
        rounded_rect(
            draw,
            (x - rw // 2, y - rh // 2, x + rw // 2, y + rh // 2),
            18,
            PANEL2,
            outline=TEAL,
            width=3,
        )
        fl = font(FONT_BOLD, 26)
        lines = wrap_lines(draw, lab, fl, rw - 20, 2)
        ly = y - 12 * len(lines)
        for ln in lines:
            tw = draw.textlength(ln, font=fl)
            draw.text((x - tw / 2, ly), ln, font=fl, fill=mix(PANEL, CREAM, appear))
            ly += 28
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


def draw_question(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    # big question mark
    a = ease_out(p)
    qf = font(FONT_BOLD, int(lerp(80, 220, a)))
    draw.text((140, 280), "?", font=qf, fill=mix(PANEL, AMBER, a))
    fb = font(FONT_BOLD, 52)
    lines = wrap_lines(draw, sc.headline, fb, W - 520, 4)
    y = 320
    for line in lines:
        draw.text((420, y), line, font=fb, fill=WHITE)
        y += 70
    lower_third(draw, sc.beat, clamp((p - 0.25) / 0.4))


def draw_callout(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    word = sc.tokens[0] if sc.tokens else extract_headline(sc.beat, 3)
    a = ease_out(p)
    # exploding accent rings
    cx, cy = W // 2, 480
    for i in range(3):
        rr = int(lerp(40, 220 + i * 70, a))
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=mix(PANEL, AMBER, 0.4 - i * 0.1), width=3)
    fb = font(FONT_BOLD, 72)
    lines = wrap_lines(draw, word, fb, W - 240, 2)
    y = cy - 40 * len(lines)
    for line in lines:
        tw = draw.textlength(line, font=fb)
        draw.text((cx - tw / 2, y), line, font=fb, fill=WHITE)
        y += 80
    # satellite tokens
    for i, tok in enumerate(sc.tokens[1:4]):
        ang = -0.8 + i * 0.8
        r = 320
        x = int(cx + r * math.cos(ang + p * 0.4))
        yy = int(cy + 0.55 * r * math.sin(ang + p * 0.4))
        rounded_rect(draw, (x - 90, yy - 28, x + 90, yy + 28), 14, PANEL, outline=TEAL)
        fl = font(FONT_BOLD, 22)
        tw = draw.textlength(tok[:16], font=fl)
        draw.text((x - tw / 2, yy - 12), tok[:16], font=fl, fill=CREAM)
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


def draw_tokens(img: Image.Image, sc: Scene, ep: int, title: str, p: float) -> None:
    draw = ImageDraw.Draw(img)
    chrome(draw, ep, title, sc.idx, sc.total, p)
    fb = font(FONT_BOLD, 48)
    draw.text((72, 170), sc.headline, font=fb, fill=WHITE)
    toks = sc.tokens or ["Concept"]
    cols = 3
    for i, tok in enumerate(toks[:6]):
        appear = ease_out(clamp((p - i * 0.08) / 0.3))
        row, col = divmod(i, cols)
        x = 120 + col * 560
        y = 300 + row * 200
        y = int(lerp(y + 40, y, appear))
        rounded_rect(draw, (x, y, x + 500, y + 140), 22, PANEL2, outline=SKY, width=3)
        draw.rectangle([x, y, x + 12, y + 140], fill=[AMBER, TEAL, SKY, CORAL][i % 4])
        draw.text((x + 40, y + 48), tok[:28], font=font(FONT_BOLD, 36), fill=CREAM)
    lower_third(draw, sc.beat, clamp((p - 0.3) / 0.4))


DRAWERS: dict[str, Callable[..., None]] = {
    "title": draw_title,
    "flow": draw_flow,
    "compare": draw_compare,
    "stack": draw_stack,
    "pipeline": draw_pipeline,
    "lanes": draw_lanes,
    "code": draw_code,
    "rings": draw_rings,
    "nodes": draw_nodes,
    "question": draw_question,
    "callout": draw_callout,
    "tokens": draw_tokens,
}


def render_frame(ep: int, title: str, sc: Scene, progress: float) -> Image.Image:
    """progress in [0,1] across the beat duration."""
    img = gradient_bg()
    # subtle camera drift via crop-scale illusion: draw slightly offset
    drawer = DRAWERS.get(sc.kind, draw_callout)
    drawer(img, sc, ep, title, progress)
    # soft focus edge polish
    if progress < 0.08:
        # fade-in veil
        veil = Image.new("RGB", (W, H), BG_TOP)
        img = Image.blend(veil, img, ease_out(progress / 0.08))
    return img


def render_beat_frames(
    ep: int,
    title: str,
    beat: str,
    idx: int,
    total: int,
    duration: float,
    fps: float = 8.0,
    max_frames: int = 48,
) -> list[Image.Image]:
    sc = plan_scene(beat, idx, total, title)
    n = max(8, min(max_frames, int(duration * fps)))
    frames: list[Image.Image] = []
    for i in range(n):
        p = i / max(n - 1, 1)
        frames.append(render_frame(ep, title, sc, p))
    return frames
