#!/usr/bin/env python3
"""
Episode 05 — Operators
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
AUDIO = ROOT / "audio_ep05"
FRAMES = ROOT / "frames_ep05"
CLIPS = ROOT / "clips_ep05"

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))


SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "hook",
        [
            "In Episode Four, we chose types carefully.",
            "Now those values meet operators — plus, equals, and, or.",
            "Small symbols. Large consequences.",
            "Overflow, equality bugs, and null crashes often start here.",
        ],
    ),
    (
        "title",
        "title",
        [
            "Episode Five.",
            "Operators — arithmetic, equality, and short-circuit logic.",
        ],
    ),
    (
        "families",
        "families",
        [
            "Three families you use every day.",
            "Arithmetic — plus, minus, multiply, divide.",
            "Relational — less than, greater than, equals-equals.",
            "Logical — and, or, not — decisions that branch your code.",
            "Java evaluates left to right. Parentheses remove guesswork.",
        ],
    ),
    (
        "equality",
        "equality",
        [
            "The classic trap — equality.",
            "For primitives, equals-equals compares values. Fine.",
            "For objects, equals-equals compares references — same object in memory?",
            "For String content — use equals. Never equals-equals for text you care about.",
            "Safer pattern — put the literal first. PAID dot equals status.",
            "That avoids a null pointer if status is null.",
        ],
    ),
    (
        "shortcircuit",
        "shortcircuit",
        [
            "Short-circuit logic protects you.",
            "Double ampersand — and. Double pipe — or.",
            "If the left side already decides the answer, the right side never runs.",
            "user not null and user is active — the second call only happens when user exists.",
            "Single ampersand does not short-circuit. That difference causes real bugs.",
            "Use short-circuit when the second check is expensive — or unsafe.",
        ],
    ),
    (
        "overflow",
        "overflow",
        [
            "Arithmetic looks innocent.",
            "int can silently wrap on overflow — no exception by default.",
            "For money limits and counters, silent wrap is dangerous.",
            "Prefer Math dot addExact when overflow must fail loudly.",
            "Or use long — and still think about the upper bound.",
            "Payment systems choose exact math for a reason.",
        ],
    ),
    (
        "ternary",
        "ternary",
        [
            "The ternary operator — question mark colon.",
            "condition question result-if-true colon result-if-false.",
            "Great for simple choices. Terrible for nested puzzles.",
            "If the expression needs a paragraph of comments — extract a method instead.",
            "Architect tip — order can be cancelled beats a pile of operators copied everywhere.",
        ],
    ),
    (
        "mistakes",
        "mistakes",
        [
            "Three common mistakes.",
            "One — equals-equals for String content.",
            "Two — ignoring integer overflow until production numbers get big.",
            "Three — side effects stuffed inside clever expressions. Hard to read. Hard to debug.",
            "Also — trusting operator precedence instead of parentheses. Be kind to the next reader.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Interview question — equals-equals versus equals?",
            "Answer cleanly.",
            "Equals-equals — references for objects. Values for primitives.",
            "Equals — logical equality defined by the type.",
            "Then add — short-circuit and protects null. That shows production sense.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "Operators decide. Next we control the path.",
            "Episode Six — control flow.",
            "if, else, switch, loops — how programs choose and repeat.",
            "See you there.",
        ],
    ),
]


def render_hook(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "Small symbols. Large consequences."
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 140), title, font=font(FONT_SERIF, 46), fill=WHITE)
    ops = [("+", ORANGE), ("==", BLUE), ("&&", GREEN), ("?:", MUTED)]
    for i, (op, col) in enumerate(ops):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.35))
        if a <= 0:
            continue
        x = 280 + i * 380
        d.rounded_rectangle([x, 420, x + 300, 700], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=4)
        d.text((x + 90, 520), op, font=font(FONT_MONO_B, 56), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 05", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Operators", font(FONT_SERIF, 72), H // 2 - 30, mix(BG, WHITE, a)),
        ("Arithmetic · equality · short-circuit", font(FONT_REG, 32), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_families(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Operator Families", font=font(FONT_SERIF, 48), fill=WHITE)
    cards = [
        ("Arithmetic", "+  -  *  /  %", "numbers & overflow risk", ORANGE, 0.1),
        ("Relational", "<  >  <=  >=  ==", "compare values / refs", BLUE, 0.35),
        ("Logical", "&&  ||  !", "short-circuit decisions", GREEN, 0.6),
    ]
    for i, (name, ops, note, col, start) in enumerate(cards):
        a = ease_out_cubic(clamp((progress - start) / 0.3))
        if a <= 0:
            continue
        y = 180 + i * 240
        d.rounded_rectangle([200, y, 1720, y + 200], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), name, font=font(FONT_BOLD, 36), fill=mix(BG, col, a))
        d.text((780, y + 45), ops, font=font(FONT_MONO, 32), fill=mix(BG, WHITE, a))
        d.text((280, y + 120), note, font=font(FONT_REG, 28), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_equality(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "==  vs  .equals()", font=font(FONT_SERIF, 48), fill=WHITE)
    rows = [
        ("primitives", "a == b", "compares values", GREEN, 0.1),
        ("objects", "o1 == o2", "same reference?", ORANGE, 0.3),
        ("String content", "s.equals(t)", "logical equality", BLUE, 0.5),
        ("null-safe", "\"PAID\".equals(status)", "literal first", GREEN, 0.7),
    ]
    for i, (label, code, note, col, start) in enumerate(rows):
        a = ease_out_cubic(clamp((progress - start) / 0.28))
        if a <= 0:
            continue
        y = 160 + i * 180
        d.rounded_rectangle([160, y, 1760, y + 150], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((220, y + 50), label, font=font(FONT_BOLD, 28), fill=mix(BG, MUTED, a))
        d.text((560, y + 45), code, font=font(FONT_MONO, 30), fill=mix(BG, WHITE, a))
        d.text((1280, y + 50), note, font=font(FONT_REG, 26), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_shortcircuit(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Short-Circuit &&", font=font(FONT_SERIF, 48), fill=WHITE)
    d.rounded_rectangle([160, 180, 1760, 360], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    d.text((220, 240), "if (user != null && user.isActive())", font=font(FONT_MONO, 34), fill=WHITE)

    steps = [
        ("1", "Check user != null", "left side first", ORANGE, 0.25),
        ("2", "If false — stop", "right side skipped", RED, 0.45),
        ("3", "If true — call isActive()", "safe to dereference", GREEN, 0.65),
    ]
    for i, (num, title, note, col, start) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - start) / 0.28))
        if a <= 0:
            continue
        x = 180 + i * 560
        d.rounded_rectangle([x, 460, x + 520, 820], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 40, 520), num, font=font(FONT_SERIF, 44), fill=mix(BG, col, a))
        d.text((x + 40, 600), title, font=font(FONT_BOLD, 28), fill=mix(BG, WHITE, a))
        d.text((x + 40, 680), note, font=font(FONT_REG, 24), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_overflow(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Overflow Reality", font=font(FONT_SERIF, 48), fill=WHITE)
    bad_a = ease_out_cubic(clamp(progress / 0.4))
    if bad_a > 0:
        d.rounded_rectangle([160, 180, 1760, 420], radius=16, fill=mix(BG, (40, 18, 18), bad_a), outline=mix(BG, RED, bad_a), width=3)
        d.text((220, 230), "Silent wrap", font=font(FONT_BOLD, 32), fill=mix(BG, RED, bad_a))
        d.text((220, 300), "int total = a + b;   // may wrap with no exception", font=font(FONT_MONO, 30), fill=mix(BG, WHITE, bad_a))
    good_a = ease_out_cubic(clamp((progress - 0.4) / 0.4))
    if good_a > 0:
        d.rounded_rectangle([160, 500, 1760, 860], radius=16, fill=mix(BG, SURFACE, good_a), outline=mix(BG, GREEN, good_a), width=3)
        d.text((220, 560), "Fail loudly", font=font(FONT_BOLD, 32), fill=mix(BG, GREEN, good_a))
        d.text((220, 650), "long total = Math.addExact(a, b);", font=font(FONT_MONO, 32), fill=mix(BG, WHITE, good_a))
        d.text((220, 740), "Throws ArithmeticException on overflow", font=font(FONT_REG, 28), fill=mix(BG, MUTED, good_a))
    return img.convert("RGB")


def render_ternary(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Ternary ?: ", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([160, 220, 1760, 520], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    d.text((240, 300), "status = paid ? \"PAID\" : \"PENDING\";", font=font(FONT_MONO, 36), fill=mix(BG, WHITE, a))
    tip_a = ease_out_cubic(clamp((progress - 0.45) / 0.35))
    if tip_a > 0:
        d.rounded_rectangle([160, 600, 1760, 820], radius=16, fill=mix(BG, SURFACE, tip_a), outline=mix(BG, ORANGE, tip_a), width=2)
        d.text((240, 680), "Keep it simple. Nested ternaries → extract a method.", font=font(FONT_REG, 32), fill=mix(BG, WHITE, tip_a))
    return img.convert("RGB")


def render_mistakes(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [
        ("01", "== for String content", "Use .equals() / Objects.equals()"),
        ("02", "Ignoring integer overflow", "Math.addExact or long + bounds"),
        ("03", "Side effects in clever expressions", "Prefer clear statements"),
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
    q = "== versus .equals() — what's the difference?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [
        ("==", "Primitives: values · Objects: references", ORANGE),
        (".equals()", "Logical equality defined by the type", BLUE),
        ("Bonus", "&& short-circuits — protects null calls", GREEN),
    ]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0:
            continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 34), fill=mix(BG, col, a))
        d.text((620, y + 50), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Control Flow"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 72))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 72), fill=WHITE)
    sub = "if · else · switch · loops"
    bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 32), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 06", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "families": render_families,
    "equality": render_equality,
    "shortcircuit": render_shortcircuit,
    "overflow": render_overflow,
    "ternary": render_ternary,
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
            if any(k in text for k in ("Three families", "classic trap", "Short-circuit", "Interview", "Three common")):
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

    print("==> Kokoro narration (Episode 05, matched to visuals)...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _r, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}")
        synth_scene_audio(pipeline, sid, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.25 * len(SCENES)
    print(f"==> Spoken ≈ {total/60:.2f} min")
    (ROOT / "ep05_durations.json").write_text(json.dumps(durations, indent=2))

    print("==> Rendering matching visuals...")
    outs = []
    for sid, renderer, _ in SCENES:
        outs.append(render_scene_clip(sid, renderer, durations[sid]))

    lst = ROOT / "concat_ep05.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep05_narrated.mp4"
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
        paced = OUTPUT / "java_ep05_paced.mp4"
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

    final = OUTPUT / "Java_Episode_05_Operators.mp4"
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
    shutil.copy2(final, ARTIFACTS / "Java_Episode_05_Operators.mp4")

    srt = OUTPUT / "Java_Episode_05.srt"
    write_srt(durations, srt)
    shutil.copy2(srt, ARTIFACTS / "Java_Episode_05.srt")

    burned = OUTPUT / "Java_Episode_05_Operators_CAPTIONED.mp4"
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
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_05_Operators_CAPTIONED.mp4")

    vdir = ARTIFACTS / "ep05_verify"
    vdir.mkdir(exist_ok=True)
    for tstamp, name in [
        ("00:00:12", "01_hook"),
        ("00:00:45", "02_families"),
        ("00:01:30", "03_equality"),
        ("00:02:20", "04_shortcircuit"),
        ("00:03:00", "05_overflow"),
        ("00:03:40", "06_interview"),
    ]:
        subprocess.run(
            ["ffmpeg", "-y", "-ss", tstamp, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")],
            capture_output=True,
        )

    final_dur = probe(final)
    print(f"DONE Episode 05: {final_dur/60:.2f} min")
    assert 195 <= final_dur <= 330, f"duration {final_dur:.1f}s outside target"
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
