#!/usr/bin/env python3
"""
Episode 04 — Variables and Data Types
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

sys.path.insert(0, "/workspace/java/video_build")
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

ROOT = Path("/workspace/java/video_build")
AUDIO = ROOT / "audio_ep04"
FRAMES = ROOT / "frames_ep04"
CLIPS = ROOT / "clips_ep04"

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))


SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "hook",
        [
            "In Episode Three, we mapped packages and classes.",
            "Now — what actually lives inside those fields and methods?",
            "Variables name values. Types decide what is valid.",
            "Pick the wrong type… and production pays for it — overflow, nulls, money bugs.",
        ],
    ),
    (
        "title",
        "title",
        [
            "Episode Four.",
            "Variables and Data Types — primitives, references, and real choices.",
        ],
    ),
    (
        "families",
        "families",
        [
            "Java has two families of types. Keep this picture.",
            "On the left — primitives. Raw values. Fast. Never null.",
            "On the right — references. They point to objects on the heap.",
            "Assignment behaves differently in each family — that is why this split matters.",
            "That mental model everything else builds on.",
        ],
    ),
    (
        "primitives",
        "primitives",
        [
            "Eight primitives — memorize the common ones first.",
            "int for whole numbers. long for bigger IDs and timestamps.",
            "boolean for true or false. double for binary floating point.",
            "byte, short, char, float exist too — useful, but rarer in day-to-day code.",
            "Primitives hold the value itself — not a pointer.",
            "And they cannot be null. That alone prevents a whole class of bugs.",
        ],
    ),
    (
        "memory",
        "memory",
        [
            "Picture memory.",
            "int count equals ten — the value sits in the local frame.",
            "Order order equals new Order — the variable holds a reference.",
            "The real object lives on the heap.",
            "Assignment copies the primitive… or copies the reference — not the whole object.",
            "final blocks reassignment of that variable — it does not freeze the object inside.",
        ],
    ),
    (
        "money",
        "money",
        [
            "Production gotcha — money.",
            "Never store currency in double.",
            "Binary floating point cannot represent many decimals exactly.",
            "Prefer long minor units — cents — or a Money value type.",
            "Use BigDecimal when you need precise decimal math and rounding rules.",
            "Architects standardize this early — because fixing money types later is expensive.",
        ],
    ),
    (
        "wrappers",
        "wrappers",
        [
            "Wrappers look similar — Integer, Long, Boolean.",
            "They are objects. They can be null. They cost more memory.",
            "Autoboxing hides conversions — and can hide NullPointerExceptions too.",
            "A List of Integer can thrash the heap versus an int array.",
            "Prefer primitives in hot paths. Use wrappers when null is a real signal.",
        ],
    ),
    (
        "mistakes",
        "mistakes",
        [
            "Three common mistakes.",
            "One — double for money. Rounding bugs wait quietly.",
            "Two — ignoring integer overflow on big counters.",
            "Three — assuming final means deep immutability. It only blocks reassignment.",
            "Bonus trap — overusing String for every domain idea. Prefer typed values when meaning matters.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Interview question — primitive versus wrapper?",
            "Answer on screen.",
            "Primitive — value, non-null, compact.",
            "Wrapper — object, nullable, overhead, autoboxing risk.",
            "Then mention — why avoid double for money. That lands the offer-level detail.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "You now know how Java stores meaning.",
            "Next — operators.",
            "Plus, compare, and, or — and the traps that break equality checks.",
            "Episode Five. See you there.",
        ],
    ),
]


def render_hook(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "Types decide what is valid"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 140), title, font=font(FONT_SERIF, 50), fill=WHITE)

    cards = [
        ("int count = 10;", "primitive value", ORANGE),
        ("Order o = new Order();", "reference → heap", BLUE),
        ("double money = 10.1;", "dangerous for currency", RED),
    ]
    for i, (code, note, col) in enumerate(cards):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0:
            continue
        y = 280 + i * 200
        d.rounded_rectangle(
            [300, y, 1620, y + 160],
            radius=16,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((360, y + 35), code, font=font(FONT_MONO, 34), fill=mix(BG, WHITE, a))
        d.text((360, y + 95), note, font=font(FONT_REG, 26), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_title(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 04", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Variables & Data Types", font(FONT_SERIF, 64), H // 2 - 30, mix(BG, WHITE, a)),
        ("Primitives · references · real choices", font(FONT_REG, 32), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_families(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "Two Families"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), title, font=font(FONT_SERIF, 48), fill=WHITE)

    left_a = ease_out_cubic(clamp(progress / 0.4))
    right_a = ease_out_cubic(clamp((progress - 0.25) / 0.4))
    if left_a > 0:
        d.rounded_rectangle([140, 220, 900, 880], radius=20, fill=mix(BG, SURFACE, left_a), outline=mix(BG, ORANGE, left_a), width=4)
        d.text((220, 280), "Primitives", font=font(FONT_BOLD, 44), fill=mix(BG, ORANGE, left_a))
        for i, line in enumerate(["Raw values", "Fast", "Never null", "int · long · boolean…"]):
            d.text((220, 400 + i * 80), f"•  {line}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, left_a))
    if right_a > 0:
        d.rounded_rectangle([1020, 220, 1780, 880], radius=20, fill=mix(BG, SURFACE, right_a), outline=mix(BG, BLUE, right_a), width=4)
        d.text((1100, 280), "References", font=font(FONT_BOLD, 44), fill=mix(BG, BLUE, right_a))
        for i, line in enumerate(["Point to objects", "Live on the heap", "Can be null", "String · Order · List…"]):
            d.text((1100, 400 + i * 80), f"•  {line}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, right_a))
    return img.convert("RGB")


def render_primitives(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Eight Primitives", font=font(FONT_SERIF, 46), fill=WHITE)
    items = [
        ("int", "whole numbers", ORANGE),
        ("long", "IDs · timestamps", ORANGE),
        ("boolean", "true / false", GREEN),
        ("double", "binary float", BLUE),
        ("byte", "8-bit", MUTED),
        ("short", "16-bit", MUTED),
        ("char", "Unicode", MUTED),
        ("float", "32-bit float", MUTED),
    ]
    for i, (name, desc, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.08) / 0.3))
        if a <= 0:
            continue
        x = 160 + (i % 4) * 430
        y = 200 + (i // 4) * 340
        d.rounded_rectangle(
            [x, y, x + 390, y + 280],
            radius=16,
            fill=mix(BG, SURFACE, a),
            outline=mix(BG, col, a),
            width=3,
        )
        d.text((x + 40, y + 80), name, font=font(FONT_MONO_B, 42), fill=mix(BG, col, a))
        d.text((x + 40, y + 160), desc, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_memory(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Value vs Reference", font=font(FONT_SERIF, 46), fill=WHITE)

    # stack box
    a1 = ease_out_cubic(clamp(progress / 0.35))
    if a1 > 0:
        d.rounded_rectangle([140, 180, 900, 900], radius=18, fill=mix(BG, SURFACE, a1), outline=mix(BG, ORANGE, a1), width=3)
        d.text((200, 220), "Local frame", font=font(FONT_BOLD, 34), fill=mix(BG, ORANGE, a1))
        d.text((200, 320), "int count = 10", font=font(FONT_MONO, 30), fill=mix(BG, WHITE, a1))
        d.text((200, 390), "→ value 10 lives here", font=font(FONT_REG, 26), fill=mix(BG, MUTED, a1))
        d.text((200, 520), "Order order = …", font=font(FONT_MONO, 30), fill=mix(BG, WHITE, a1))
        d.text((200, 590), "→ holds a reference", font=font(FONT_REG, 26), fill=mix(BG, MUTED, a1))

    a2 = ease_out_cubic(clamp((progress - 0.35) / 0.35))
    if a2 > 0:
        d.rounded_rectangle([1020, 180, 1780, 900], radius=18, fill=mix(BG, SURFACE, a2), outline=mix(BG, BLUE, a2), width=3)
        d.text((1100, 220), "Heap", font=font(FONT_BOLD, 34), fill=mix(BG, BLUE, a2))
        d.rounded_rectangle([1120, 340, 1680, 620], radius=14, fill=mix(SURFACE, BG, 0.15), outline=mix(BG, GREEN, a2), width=2)
        d.text((1180, 400), "Order object", font=font(FONT_BOLD, 32), fill=mix(BG, GREEN, a2))
        d.text((1180, 480), "fields · identity", font=font(FONT_REG, 26), fill=mix(BG, MUTED, a2))
        if progress > 0.55:
            # arrow hint
            d.text((920, 480), "→", font=font(FONT_BOLD, 48), fill=ORANGE)
    return img.convert("RGB")


def render_money(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Money Types", font=font(FONT_SERIF, 48), fill=WHITE)

    bad_a = ease_out_cubic(clamp(progress / 0.35))
    if bad_a > 0:
        d.rounded_rectangle([160, 180, 1760, 360], radius=16, fill=mix(BG, (40, 18, 18), bad_a), outline=mix(BG, RED, bad_a), width=3)
        d.text((220, 220), "AVOID", font=font(FONT_BOLD, 28), fill=mix(BG, RED, bad_a))
        d.text((220, 270), "double amount = 10.10;   // binary precision lies", font=font(FONT_MONO, 30), fill=mix(BG, WHITE, bad_a))

    goods = [
        ("long minorUnits = 1010L;", "cents / paise — exact integers", ORANGE, 0.35),
        ("record Money(String currency, long minorUnits) {}", "domain meaning + safety", GREEN, 0.55),
        ("BigDecimal tax = new BigDecimal(\"0.18\");", "precise decimal math", BLUE, 0.75),
    ]
    for i, (code, note, col, start) in enumerate(goods):
        a = ease_out_cubic(clamp((progress - start) / 0.28))
        if a <= 0:
            continue
        y = 420 + i * 160
        d.rounded_rectangle([160, y, 1760, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((220, y + 30), code, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, a))
        d.text((220, y + 80), note, font=font(FONT_REG, 26), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_wrappers(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Primitives vs Wrappers", font=font(FONT_SERIF, 46), fill=WHITE)
    rows = [
        ("int", "Integer", "null? No / Yes", ORANGE),
        ("long", "Long", "overhead? Low / Object header", BLUE),
        ("boolean", "Boolean", "autoboxing can NPE", GREEN),
    ]
    d.text((280, 180), "Primitive", font=font(FONT_BOLD, 28), fill=MUTED)
    d.text((720, 180), "Wrapper", font=font(FONT_BOLD, 28), fill=MUTED)
    d.text((1160, 180), "Watch out", font=font(FONT_BOLD, 28), fill=MUTED)
    for i, (p, w, note, col) in enumerate(rows):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0:
            continue
        y = 260 + i * 200
        d.rounded_rectangle([160, y, 1760, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 55), p, font=font(FONT_MONO_B, 40), fill=mix(BG, ORANGE, a))
        d.text((720, y + 55), w, font=font(FONT_MONO_B, 40), fill=mix(BG, BLUE, a))
        d.text((1160, y + 60), note, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [
        ("01", "double for money", "Use long minor units or BigDecimal"),
        ("02", "Ignoring integer overflow", "Use long / checked math for big counters"),
        ("03", "final = deep immutability", "final only blocks reassignment"),
    ]
    for i, (num, wrong, right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0:
            continue
        y = 180 + i * 240
        d.rounded_rectangle([200, y, 1720, y + 200], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a * 0.7), width=2)
        d.text((260, y + 40), num, font=font(FONT_SERIF, 40), fill=mix(BG, ORANGE, a))
        d.text((360, y + 45), wrong, font=font(FONT_BOLD, 30), fill=mix(BG, RED, a))
        d.text((360, y + 110), right, font=font(FONT_REG, 28), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_interview(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Interview Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "Primitive vs wrapper — what's the difference?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)

    answers = [
        ("Primitive", "Value · non-null · compact", ORANGE),
        ("Wrapper", "Object · nullable · overhead", BLUE),
        ("Bonus", "Avoid double for money", GREEN),
    ]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0:
            continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 34), fill=mix(BG, col, a))
        d.text((620, y + 50), v, font=font(FONT_REG, 30), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Operators"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 72))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 72), fill=WHITE)
    sub = "+  ·  ==  ·  &&  ·  equality traps"
    bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 32), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 05", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "families": render_families,
    "primitives": render_primitives,
    "memory": render_memory,
    "money": render_money,
    "wrappers": render_wrappers,
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
            if any(k in text for k in ("Picture", "Eight", "Production", "Interview", "Three common")):
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

    print("==> Kokoro narration (Episode 04, matched to visuals)...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _r, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}")
        synth_scene_audio(pipeline, sid, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.25 * len(SCENES)
    print(f"==> Spoken ≈ {total/60:.2f} min")
    (ROOT / "ep04_durations.json").write_text(json.dumps(durations, indent=2))

    print("==> Rendering matching visuals...")
    outs = []
    for sid, renderer, _ in SCENES:
        outs.append(render_scene_clip(sid, renderer, durations[sid]))

    lst = ROOT / "concat_ep04.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep04_narrated.mp4"
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
    elif dur < 255:
        pace = max(dur / 260.0, 0.88)

    music = AUDIO / "music_bed.m4a"
    generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep04_paced.mp4"
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

    final = OUTPUT / "Java_Episode_04_Variables_Data_Types.mp4"
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
    shutil.copy2(final, ARTIFACTS / "Java_Episode_04_Variables_Data_Types.mp4")

    srt = OUTPUT / "Java_Episode_04.srt"
    write_srt(durations, srt)
    shutil.copy2(srt, ARTIFACTS / "Java_Episode_04.srt")

    burned = OUTPUT / "Java_Episode_04_Variables_Data_Types_CAPTIONED.mp4"
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
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_04_Variables_Data_Types_CAPTIONED.mp4")

    vdir = ARTIFACTS / "ep04_verify"
    vdir.mkdir(exist_ok=True)
    for tstamp, name in [
        ("00:00:12", "01_hook"),
        ("00:00:45", "02_families"),
        ("00:01:20", "03_primitives"),
        ("00:02:00", "04_memory"),
        ("00:02:40", "05_money"),
        ("00:03:30", "06_interview"),
    ]:
        subprocess.run(
            ["ffmpeg", "-y", "-ss", tstamp, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")],
            capture_output=True,
        )

    final_dur = probe(final)
    print(f"DONE Episode 04: {final_dur/60:.2f} min")
    assert 195 <= final_dur <= 330, f"duration {final_dur:.1f}s outside target"
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
