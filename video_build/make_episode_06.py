#!/usr/bin/env python3
"""
Episode 06 — Control Flow
Narration + on-screen graphics authored TOGETHER.
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
AUDIO = ROOT / "audio_ep06"
FRAMES = ROOT / "frames_ep06"
CLIPS = ROOT / "clips_ep06"

VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "hook",
        [
            "Operators decide values. Control flow decides the path.",
            "Which statements run? How often? When do we exit?",
            "In production, unclear branching becomes missed edge cases — and messy failures.",
            "Today we make the path visible — and keep it flat.",
        ],
    ),
    (
        "title",
        "title",
        [
            "Episode Six.",
            "Control Flow — if, switch, loops, and clean exits.",
        ],
    ),
    (
        "guards",
        "guards",
        [
            "Start with if — but prefer guard clauses.",
            "Validate early. Reject early. Return early.",
            "Flat code beats a pyramid of nested else blocks.",
            "If not valid — return. If not authorized — deny. Then process the happy path.",
            "Readable. Testable. Kind to the next engineer.",
        ],
    ),
    (
        "switch",
        "switch",
        [
            "When cases are finite — switch shines.",
            "Modern Java has switch expressions — they produce a value.",
            "Arrow labels. No accidental fall-through.",
            "Perfect for statuses — PENDING, PAID, CANCELLED.",
            "If you are still writing classic switch with missing breaks — upgrade the habit.",
            "Finite states belong in switch. Open-ended rules belong in methods.",
        ],
    ),
    (
        "loops",
        "loops",
        [
            "Loops repeat work.",
            "for when you know the bounds. while when you wait on a condition.",
            "for-each when you walk a collection cleanly.",
            "break exits. continue skips to the next iteration.",
            "Watch unbounded loops — they become production incidents.",
            "And avoid allocating heavy objects on every iteration in hot paths.",
        ],
    ),
    (
        "exceptions",
        "exceptions",
        [
            "Exceptions are for exceptional paths — not everyday outcomes.",
            "try, catch, finally — and try-with-resources for cleanup.",
            "Open a file or connection inside try-with-resources — Java closes it for you.",
            "Do not throw exceptions to mean not found on every request. That is control flow wearing a costume.",
            "Reserve exceptions for failures you cannot express as a normal return.",
        ],
    ),
    (
        "pipeline",
        "pipeline",
        [
            "Picture a production request.",
            "Validate. Authorize. Process. Commit. Respond.",
            "On failure — compensate or retry with clear rules.",
            "Good control flow makes normal and failure paths equally obvious.",
            "Hidden branches are where incidents hide.",
        ],
    ),
    (
        "mistakes",
        "mistakes",
        [
            "Three common mistakes.",
            "One — deeply nested branches that hide the real intent.",
            "Two — missing break in legacy switch — fall-through bugs.",
            "Three — exceptions for common outcomes. Expensive and confusing.",
            "Also — putting whole business workflows inside controllers. Extract the flow.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Interview question — when do you use a switch expression?",
            "Answer — finite, clear cases that produce a value.",
            "Then add — prefer guard clauses over nesting.",
            "And try-with-resources for deterministic cleanup.",
            "That package of answers sounds senior.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "Paths are clear. Next we package behavior.",
            "Episode Seven — methods.",
            "Parameters, return types, overloading — how code becomes reusable.",
            "See you there.",
        ],
    ),
]


def render_hook(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    title = "Which path runs?"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 52))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 52), fill=WHITE)
    nodes = [("if", ORANGE), ("switch", BLUE), ("loop", GREEN), ("return", MUTED)]
    for i, (name, col) in enumerate(nodes):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.35))
        if a <= 0:
            continue
        x = 260 + i * 400
        d.rounded_rectangle([x, 420, x + 320, 700], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=4)
        d.text((x + 90, 530), name, font=font(FONT_MONO_B, 40), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 06", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Control Flow", font(FONT_SERIF, 72), H // 2 - 30, mix(BG, WHITE, a)),
        ("if · switch · loops · clean exits", font(FONT_REG, 32), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_guards(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Guard Clauses", font=font(FONT_SERIF, 48), fill=WHITE)
    lines = [
        "if (!valid) return reject();",
        "if (!authorized) return deny();",
        "// happy path stays flat",
        "process();",
        "commit();",
        "return respond();",
    ]
    d.rounded_rectangle([300, 180, 1620, 900], radius=18, fill=SURFACE, outline=ORANGE, width=3)
    for i, line in enumerate(lines):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.3))
        col = RED if "return" in line and i < 2 else (MUTED if line.startswith("//") else WHITE)
        d.text((400, 240 + i * 100), line, font=font(FONT_MONO, 34), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_switch(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Switch Expression", font=font(FONT_SERIF, 48), fill=WHITE)
    code = [
        "String label = switch (status) {",
        "  case PAID      -> \"Ship it\";",
        "  case PENDING   -> \"Wait\";",
        "  case CANCELLED -> \"Stop\";",
        "};",
    ]
    d.rounded_rectangle([220, 180, 1700, 780], radius=18, fill=SURFACE, outline=BLUE, width=3)
    for i, line in enumerate(code):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.3))
        d.text((320, 260 + i * 90), line, font=font(FONT_MONO, 34), fill=mix(BG, WHITE if i else ORANGE, a))
    tip_a = ease_out_cubic(clamp((progress - 0.7) / 0.25))
    if tip_a > 0:
        d.text((320, 820), "Arrow labels · produces a value · no accidental fall-through", font=font(FONT_REG, 28), fill=mix(BG, MUTED, tip_a))
    return img.convert("RGB")


def render_loops(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Loops", font=font(FONT_SERIF, 48), fill=WHITE)
    cards = [
        ("for", "known bounds", ORANGE),
        ("while", "condition-driven", BLUE),
        ("for-each", "walk collections", GREEN),
        ("break / continue", "exit or skip", MUTED),
    ]
    for i, (name, note, col) in enumerate(cards):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0:
            continue
        x = 160 + (i % 2) * 880
        y = 200 + (i // 2) * 340
        d.rounded_rectangle([x, y, x + 800, y + 280], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 60, y + 80), name, font=font(FONT_MONO_B, 40), fill=mix(BG, col, a))
        d.text((x + 60, y + 160), note, font=font(FONT_REG, 30), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_exceptions(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Exceptions & Cleanup", font=font(FONT_SERIF, 46), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([160, 180, 1760, 560], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    d.text((240, 240), "try (Connection c = open()) {", font=font(FONT_MONO, 32), fill=mix(BG, WHITE, a))
    d.text((280, 320), "work(c);", font=font(FONT_MONO, 32), fill=mix(BG, GREEN, a))
    d.text((240, 400), "} // auto-closed — even on failure", font=font(FONT_MONO, 32), fill=mix(BG, MUTED, a))
    tip_a = ease_out_cubic(clamp((progress - 0.45) / 0.35))
    if tip_a > 0:
        d.rounded_rectangle([160, 620, 1760, 860], radius=16, fill=mix(BG, (40, 18, 18), tip_a), outline=mix(BG, RED, tip_a), width=3)
        d.text((240, 720), "Don't use exceptions for everyday \"not found\" control flow.", font=font(FONT_REG, 30), fill=mix(BG, WHITE, tip_a))
    return img.convert("RGB")


def render_pipeline(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 60), "Production Path", font=font(FONT_SERIF, 48), fill=WHITE)
    steps = ["Validate", "Authorize", "Process", "Commit", "Respond"]
    for i, name in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        if a <= 0:
            continue
        x = 100 + i * 360
        d.rounded_rectangle([x, 360, x + 300, 560], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE if i == 0 else BLUE, a), width=3)
        d.text((x + 40, 430), name, font=font(FONT_BOLD, 28), fill=mix(BG, WHITE, a))
        if i < len(steps) - 1 and progress > i * 0.12 + 0.15:
            d.polygon([(x + 310, 450), (x + 340, 460), (x + 310, 470)], fill=ORANGE)
    fail_a = ease_out_cubic(clamp((progress - 0.7) / 0.25))
    if fail_a > 0:
        d.text((200, 700), "On failure → compensate / retry with explicit rules", font=font(FONT_REG, 30), fill=mix(BG, RED, fail_a))
    return img.convert("RGB")


def render_mistakes(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [
        ("01", "Deep nesting pyramids", "Use guard clauses — flatten the path"),
        ("02", "Missing break in legacy switch", "Prefer switch expressions"),
        ("03", "Exceptions for common outcomes", "Reserve exceptions for exceptional paths"),
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
    q = "When do you use a switch expression?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 34))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 34), fill=WHITE)
    answers = [
        ("Finite cases", "clear statuses / enums that produce a value", ORANGE),
        ("Guard clauses", "flatten nesting — validate early", BLUE),
        ("try-with-resources", "deterministic cleanup", GREEN),
    ]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0:
            continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
        d.text((720, y + 50), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress: float, t: float) -> Image.Image:
    img = base_canvas(t)
    d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Methods"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 72))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 72), fill=WHITE)
    sub = "parameters · returns · overloading"
    bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 32), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 07", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "guards": render_guards,
    "switch": render_switch,
    "loops": render_loops,
    "exceptions": render_exceptions,
    "pipeline": render_pipeline,
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
            if any(k in text for k in ("Start with", "finite", "Loops", "Exceptions", "Picture", "Interview", "Three common")):
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

    print("==> Kokoro narration (Episode 06)...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _r, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}")
        synth_scene_audio(pipeline, sid, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.25 * len(SCENES)
    print(f"==> Spoken ≈ {total/60:.2f} min")
    (ROOT / "ep06_durations.json").write_text(json.dumps(durations, indent=2))

    outs = []
    for sid, renderer, _ in SCENES:
        outs.append(render_scene_clip(sid, renderer, durations[sid]))

    lst = ROOT / "concat_ep06.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep06_narrated.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)],
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
        paced = OUTPUT / "java_ep06_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)],
            check=True,
        )
        base = paced

    final = OUTPUT / "Java_Episode_06_Control_Flow.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)],
        check=True,
    )
    shutil.copy2(final, ARTIFACTS / "Java_Episode_06_Control_Flow.mp4")

    srt = OUTPUT / "Java_Episode_06.srt"
    write_srt(durations, srt)
    shutil.copy2(srt, ARTIFACTS / "Java_Episode_06.srt")

    burned = OUTPUT / "Java_Episode_06_Control_Flow_CAPTIONED.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)],
        check=True,
    )
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_06_Control_Flow_CAPTIONED.mp4")

    vdir = ARTIFACTS / "ep06_verify"
    vdir.mkdir(exist_ok=True)
    for tstamp, name in [("00:00:12", "01_hook"), ("00:00:50", "02_guards"), ("00:01:40", "03_switch"), ("00:02:30", "04_loops"), ("00:03:10", "05_pipeline"), ("00:03:40", "06_interview")]:
        subprocess.run(["ffmpeg", "-y", "-ss", tstamp, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)

    final_dur = probe(final)
    print(f"DONE Episode 06: {final_dur/60:.2f} min")
    assert 195 <= final_dur <= 330, f"duration {final_dur:.1f}s outside target"


if __name__ == "__main__":
    main()
