#!/usr/bin/env python3
"""Episode 48 — ThreadLocal. Narration + visuals authored together."""
from __future__ import annotations

import json, multiprocessing as mp, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro import KPipeline
from PIL import Image, ImageDraw

sys.path.insert(0, "/workspace/java/video_build")
from generate_java_episode import (  # noqa: E402
    ARTIFACTS, BG, BLUE, FONT_BOLD, FONT_MONO, FONT_MONO_B, FONT_REG, FONT_SERIF,
    FPS, GREEN, H, MUTED, ORANGE, OUTPUT, RED, SURFACE, W, WHITE,
    base_canvas, clamp, ease_out_cubic, font, mix,
)
from humanize_audio import generate_music_bed, probe  # noqa: E402

ROOT = Path("/workspace/java/video_build")
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep48", ROOT / "frames_ep48", ROOT / "clips_ep48"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Forty-Seven split work across a ForkJoinPool.',
        'Each thread needs its own context — request ID, formatter, database connection.',
        'Passing context through every method signature gets noisy fast.',
        'ThreadLocal gives each thread a private copy of a variable.',
        'SimpleLocal.get on thread A never sees thread B value.',
        'Today — ThreadLocal, inheritance, common patterns, and leak traps.',
    ]),
    ("title", "title", [
        'Episode Forty-Eight.',
        'ThreadLocal — Per-Thread State.',
    ]),
    ("per_thread_state", "per_thread_state", [
        'ThreadLocal of T stores a value per calling thread.',
        'Internally a map from Thread to T — invisible to your code.',
        'set assigns the value for the current thread.',
        'get returns the current thread value — or the initial value.',
        'remove clears the entry for the current thread.',
        'No synchronization needed for reads and writes on the same thread.',
    ]),
    ("get_set", "get_set", [
        'Typical usage — static final ThreadLocal of DateFormat.',
        'withInitial supplies a factory — lazy per-thread creation.',
        'First get on a thread calls the supplier once.',
        'Subsequent gets return the same instance for that thread.',
        'DateFormat is not thread-safe — ThreadLocal avoids locking.',
        'Same pattern for SimpleDateFormat, Random, StringBuilder scratch buffers.',
    ]),
    ("inheritance", "inheritance", [
        'InheritableThreadLocal propagates values to child threads.',
        'When you new Thread or pool creates a worker, child inherits parent value.',
        'Useful for tracing context — correlation IDs across async handoffs.',
        'Child gets a copy at creation time — not live updates from parent.',
        'ThreadLocal does not inherit — child starts with initial value only.',
        'Modern alternative — pass context explicitly or use scoped values in newer JDKs.',
    ]),
    ("common_patterns", "common_patterns", [
        'Common ThreadLocal uses in production.',
        'Per-request user or tenant context in servlet containers.',
        'Security principal or locale without method parameter drilling.',
        'Transaction or connection context in older frameworks.',
        'Diagnostic MDC in logging — map diagnostic context per thread.',
        'Keep the scope narrow — set at entry, remove at exit.',
    ]),
    ("leaks", "leaks", [
        'ThreadLocal leak risk — the classic thread-pool trap.',
        'Pool threads live forever — their ThreadLocal map never garbage-collected.',
        'If the value references a large object graph, memory grows each request.',
        'Always remove in a finally block when borrowing from a pool.',
        'Weak references in some implementations help — but do not rely on them.',
        'Prefer try-finally or try-with-resources wrappers around ThreadLocal scope.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — forgetting remove on pooled threads — slow memory leak.',
        'Two — storing heavy mutable singletons — defeats per-thread isolation.',
        'Three — assuming InheritableThreadLocal updates propagate — they do not.',
        'Also — using ThreadLocal where explicit parameters are clearer.',
        'ThreadLocal is convenience — not a substitute for good API design.',
    ]),
    ("interview", "interview", [
        'Interview question — what is ThreadLocal and when is it dangerous?',
        'Per-thread variable — each thread has its own copy via get and set.',
        'Use for non-thread-safe helpers — formatters, buffers, request context.',
        'Danger — thread pools reuse threads — stale values and memory leaks.',
        'Always remove after use on pooled threads.',
        'Mention InheritableThreadLocal for child-thread propagation at creation.',
    ]),
    ("teaser", "teaser", [
        'Per-thread state avoids sharing. What when threads block each other forever?',
        'Episode Forty-Nine — Deadlocks.',
        'Four conditions, detection, avoidance, and lock ordering.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Private per thread"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("Thread A", ORANGE), ("Thread B", BLUE), ("Thread C", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 80, 500), lab, font=font(FONT_BOLD, 26), fill=mix(BG, col, a))
        d.text((x + 100, 560), "own value", font=font(FONT_REG, 22), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 48", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("ThreadLocal", font(FONT_SERIF, 56), H // 2 - 30, mix(BG, WHITE, a)),
        ("per-thread state · inheritance · leaks", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_per_thread_state(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "ThreadLocal<T>", font=font(FONT_SERIF, 46), fill=WHITE)
    items = [("set(value)", "store for current thread", ORANGE), ("get()", "read current thread copy", BLUE), ("remove()", "clear on exit", GREEN)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 220
        d.rounded_rectangle([200, y, 1720, y + 180], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), k, font=font(FONT_MONO, 32), fill=mix(BG, col, a))
        d.text((620, y + 50), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_get_set(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "withInitial", font=font(FONT_SERIF, 46), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    lines = [
        "private static final ThreadLocal<DateFormat> FMT =",
        "  ThreadLocal.withInitial(() -> new SimpleDateFormat(\"yyyy\"));",
        "DateFormat fmt = FMT.get(); // one per thread",
        "FMT.remove(); // in finally on pooled threads",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 300 + i * 120), line, font=font(FONT_MONO, 24), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_inheritance(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "InheritableThreadLocal", font=font(FONT_SERIF, 40), fill=WHITE)
    items = [("parent sets value", "visible to child at spawn", ORANGE), ("child thread", "gets copy at creation", BLUE), ("no live sync", "parent updates invisible", RED)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_common_patterns(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Common Patterns", font=font(FONT_SERIF, 44), fill=WHITE)
    patterns = [("request context", "user, tenant, locale", ORANGE), ("MDC logging", "correlation ID per thread", BLUE), ("non-thread-safe helpers", "formatters, buffers", GREEN)]
    for i, (k, v, col) in enumerate(patterns):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_leaks(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Leak Hazard", font=font(FONT_SERIF, 46), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=3)
    lines = [
        "Thread pool → threads live forever",
        "ThreadLocal map holds references",
        "Forgotten remove → memory grows",
        "try { ... } finally { TL.remove(); }",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        col = RED if i == 2 else WHITE
        d.text((280, 300 + i * 120), line, font=font(FONT_MONO, 28), fill=mix(BG, col, aa))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "no remove on pool exit", "memory leak"), ("02", "heavy shared refs", "defeats isolation"), ("03", "inheritance assumptions", "stale child copies")]
    for i, (num, wrong, right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        y = 180 + i * 240
        d.rounded_rectangle([200, y, 1720, y + 200], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a * 0.7), width=2)
        d.text((260, y + 40), num, font=font(FONT_SERIF, 40), fill=mix(BG, ORANGE, a))
        d.text((360, y + 45), wrong, font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
        d.text((360, y + 110), right, font=font(FONT_REG, 28), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_interview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Interview Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "ThreadLocal dangers in thread pools?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [("per-thread copy", "no locks for same thread", ORANGE), ("pool reuse", "stale values linger", RED), ("always remove", "finally block cleanup", GREEN)]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Deadlocks"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "detection · avoidance · lock ordering"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 26))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 26), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 49", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "per_thread_state": render_per_thread_state,
    "get_set": render_get_set, "inheritance": render_inheritance, "common_patterns": render_common_patterns,
    "leaks": render_leaks, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser,
}


def clean(text): return " ".join(text.split()).strip()


def synth_beat(pipeline, text):
    chunks = []
    for _, _, audio in pipeline(text, voice=VOICE, speed=SPEED):
        chunks.append(np.asarray(audio, dtype=np.float32))
    if not chunks: raise RuntimeError(text)
    return np.concatenate(chunks)


def synth_scene_audio(pipeline, scene_id, beats):
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    audio {i+1}/{len(beats)}: {text[:70]}")
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), synth_beat(pipeline, text), 24000)
        parts.append(wav)
        if i < len(beats) - 1:
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "How to choose", "Look at")) else (0.28 if text.endswith("?") else 0.12)
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), np.zeros(int(gap * 24000), dtype=np.float32), 24000)
            parts.append(sil)
    lst = scene_dir / "list.txt"
    with open(lst, "w") as f:
        for p in parts: f.write(f"file '{p}'\n")
    out = AUDIO / f"{scene_id}.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-q:a", "2", str(out)], check=True, capture_output=True)
    return out


def _frame_job(args):
    renderer, i, n, scene_dir = args
    progress = i / max(n - 1, 1)
    RENDERERS[renderer](progress, i / FPS).save(Path(scene_dir) / f"f{i:05d}.jpg", quality=85)
    return i


def render_scene_clip(scene_id, renderer, duration):
    duration = max(duration + 0.25, 2.0)
    n = int(duration * FPS)
    scene_dir = FRAMES / scene_id
    if scene_dir.exists(): shutil.rmtree(scene_dir)
    scene_dir.mkdir(parents=True)
    print(f"  frames {scene_id}: {n}")
    with mp.Pool(max(2, min(6, os.cpu_count() or 4))) as pool:
        done = 0
        for _ in pool.imap_unordered(_frame_job, [(renderer, i, n, str(scene_dir)) for i in range(n)], chunksize=8):
            done += 1
            if done % 90 == 0 or done == n: print(f"    {scene_id}: {done}/{n}")
    out = CLIPS / f"{scene_id}.mp4"
    subprocess.run(["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(scene_dir / "f%05d.jpg"), "-i", str(AUDIO / f"{scene_id}.mp3"), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)], check=True, capture_output=True)
    shutil.rmtree(scene_dir)
    return out


def write_srt(durations, path):
    def fmt(ts):
        h, m = int(ts // 3600), int((ts % 3600) // 60)
        s = int(ts % 60); ms = int(round((ts - int(ts)) * 1000))
        if ms == 1000: s += 1; ms = 0
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    t = 0.0; idx = 1; lines = []
    for scene_id, _, beats in SCENES:
        scene_dur = durations[scene_id] + 0.25
        weights = [max(len(b), 8) for b in beats]; tw = sum(weights)
        for beat, w in zip(beats, weights):
            slot = scene_dur * (w / tw)
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{clean(beat)}\n")
            idx += 1; t += slot
    path.write_text("\n".join(lines))


def main():
    for p in [AUDIO, FRAMES, CLIPS, OUTPUT, ARTIFACTS]:
        if p in (AUDIO, FRAMES, CLIPS) and p.exists(): shutil.rmtree(p)
        p.mkdir(parents=True, exist_ok=True)
    print("==> Kokoro Episode 48...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep48_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep48.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep48_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)], check=True)
    dur = probe(narrated)
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 245:
        pace = max(dur / 250.0, 0.85)
    music = AUDIO / "music_bed.m4a"; generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep48_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_48_ThreadLocal.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_48.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_48_ThreadLocal_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep48_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_get_set'), ('00:01:40', '03_inheritance'), ('00:02:30', '04_leaks'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 48: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
