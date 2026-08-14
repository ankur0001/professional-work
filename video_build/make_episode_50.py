#!/usr/bin/env python3
"""Episode 50 — Virtual Threads (Project Loom). Narration + visuals authored together."""
from __future__ import annotations

import json, multiprocessing as mp, os, shutil, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
from kokoro import KPipeline
from PIL import Image, ImageDraw

sys.path.insert(0, "/workspace/video_build")
from generate_java_episode import (  # noqa: E402
    ARTIFACTS, BG, BLUE, FONT_BOLD, FONT_MONO, FONT_MONO_B, FONT_REG, FONT_SERIF,
    FPS, GREEN, H, MUTED, ORANGE, OUTPUT, RED, SURFACE, W, WHITE,
    base_canvas, clamp, ease_out_cubic, font, mix,
)
from humanize_audio import generate_music_bed, probe  # noqa: E402

ROOT = Path("/workspace/video_build")
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep50", ROOT / "frames_ep50", ROOT / "clips_ep50"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Forty-Nine showed how platform threads deadlock under bad lock order.',
        'Platform threads are expensive — one megabyte stack, OS scheduling overhead.',
        'A web server handling ten thousand concurrent requests cannot spawn ten thousand threads.',
        'Project Loom brings virtual threads — lightweight, JVM-managed, millions per process.',
        'Block on I/O and the carrier thread serves another virtual thread.',
        'Today — virtual threads, pinning, and an intro to structured concurrency.',
    ]),
    ("title", "title", [
        'Episode Fifty.',
        'Virtual Threads — Project Loom.',
    ]),
    ("project_loom", "project_loom", [
        'Project Loom reimagined threads without rewriting your Java code.',
        'Virtual threads are cheap — create with Thread.startVirtualThread or Executors.newVirtualThreadPerTaskExecutor.',
        'The JVM multiplexes many virtual threads onto few platform carrier threads.',
        'Blocking I/O unmounts the virtual thread — carrier runs another.',
        'Same Thread API — Runnable, Callable, synchronized — mostly unchanged.',
        'Shipped as a preview in Java 19, finalized in Java 21.',
    ]),
    ("virtual_vs_platform", "virtual_vs_platform", [
        'Platform thread — one-to-one with an OS thread.',
        'Virtual thread — many-to-one on carrier pool threads.',
        'Platform threads suit CPU-bound parallel work — limited by cores.',
        'Virtual threads suit I/O-bound concurrency — waiting on network or disk.',
        'Do not pool virtual threads — create one per task, they are cheap.',
        'Do pool platform threads or use ForkJoinPool for CPU parallelism.',
    ]),
    ("pinning", "pinning", [
        'Pinning — when a virtual thread cannot unmount from its carrier.',
        'synchronized blocks may pin — carrier stuck until monitor released.',
        'Native code or JNI can pin — carrier blocked in native layer.',
        'Long CPU work on a virtual thread pins the carrier — hurts throughput.',
        'Prefer ReentrantLock over synchronized for hot paths with virtual threads.',
        'Monitor jfr events or thread dumps for pinned carrier warnings.',
    ]),
    ("structured_concurrency", "structured_concurrency", [
        'Structured concurrency — scope owns child tasks, cancels on failure.',
        'StructuredTaskScope in preview — fork subtasks, join or shutdown on error.',
        'Parent lifetime bounds children — no orphaned background work.',
        'ShutdownOnFailure — first exception cancels siblings.',
        'ShutdownOnSuccess — first success cancels the rest.',
        'Pairs naturally with virtual threads — cheap fan-out and clean teardown.',
    ]),
    ("when_to_use", "when_to_use", [
        'When virtual threads shine.',
        'HTTP servers — one virtual thread per request blocking on I/O.',
        'Database calls, REST clients, file reads — classic blocking APIs.',
        'Replace reactive frameworks only when simplicity beats throughput tuning.',
        'When not — heavy CPU computation — use platform threads or ForkJoinPool.',
        'When not — massive synchronized hot paths — pinning negates benefits.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — pooling virtual threads — unnecessary, create per task.',
        'Two — CPU-bound work on virtual threads — pins carriers.',
        'Three — ignoring synchronized pinning — switch to ReentrantLock.',
        'Also — thread-local assumptions with millions of virtual threads.',
        'Virtual threads change scale — not every old pattern still fits.',
    ]),
    ("interview", "interview", [
        'Interview question — virtual threads versus platform threads?',
        'Virtual — lightweight, JVM-scheduled, millions possible, great for I/O.',
        'Platform — OS thread, heavier, best for CPU-bound parallelism.',
        'Blocking unmounts virtual thread — carrier serves another.',
        'Pinning from synchronized or native code blocks the carrier.',
        'Mention Java 21 finalization and structured concurrency preview.',
    ]),
    ("teaser", "teaser", [
        'Threads run code — but where does that code come from?',
        'Episode Fifty-One — Class Loading Basics.',
        'ClassLoader hierarchy, linkage, and initialization.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Millions of threads"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("platform", RED), ("→", MUTED), ("virtual", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 280 + i * 520
        if lab == "→":
            d.text((x + 40, 520), lab, font=font(FONT_BOLD, 48), fill=mix(BG, ORANGE, a))
        else:
            d.rounded_rectangle([x, 400, x + 420, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
            d.text((x + 70, 520), lab, font=font(FONT_BOLD, 26), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 50", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Virtual Threads", font(FONT_SERIF, 52), H // 2 - 30, mix(BG, WHITE, a)),
        ("Loom · pinning · structured concurrency", font(FONT_REG, 24), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_project_loom(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Project Loom", font=font(FONT_SERIF, 46), fill=WHITE)
    items = [("Thread.startVirtualThread()", "cheap per-task thread", GREEN), ("carrier pool", "few OS threads, many virtual", ORANGE), ("Java 21", "finalized feature", BLUE)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 220
        d.rounded_rectangle([200, y, 1720, y + 180], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), k, font=font(FONT_MONO, 26), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_virtual_vs_platform(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Virtual vs Platform", font=font(FONT_SERIF, 42), fill=WHITE)
    left = ease_out_cubic(clamp(progress / 0.4)); right = ease_out_cubic(clamp((progress - 0.3) / 0.4))
    if left > 0:
        d.rounded_rectangle([140, 220, 900, 820], radius=18, fill=mix(BG, SURFACE, left), outline=mix(BG, GREEN, left), width=4)
        d.text((220, 280), "Virtual", font=font(FONT_BOLD, 32), fill=mix(BG, GREEN, left))
        for i, line in enumerate(["I/O-bound", "millions OK", "unmount on block"]):
            d.text((240, 380 + i * 120), line, font=font(FONT_REG, 26), fill=mix(BG, WHITE, left))
    if right > 0:
        d.rounded_rectangle([1000, 220, 1760, 820], radius=18, fill=mix(BG, SURFACE, right), outline=mix(BG, ORANGE, right), width=4)
        d.text((1080, 280), "Platform", font=font(FONT_BOLD, 32), fill=mix(BG, ORANGE, right))
        for i, line in enumerate(["CPU-bound", "OS thread each", "ForkJoinPool"]):
            d.text((1100, 380 + i * 120), line, font=font(FONT_REG, 26), fill=mix(BG, WHITE, right))
    return img.convert("RGB")


def render_pinning(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Pinning", font=font(FONT_SERIF, 48), fill=WHITE)
    causes = [("synchronized", "monitor may pin carrier", RED), ("native / JNI", "blocked in native code", ORANGE), ("long CPU work", "carrier cannot switch", BLUE)]
    for i, (k, v, col) in enumerate(causes):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_structured_concurrency(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Structured Concurrency", font=font(FONT_SERIF, 38), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {",
        "  scope.fork(() -> fetchA());",
        "  scope.fork(() -> fetchB());",
        "  scope.join(); // parent bounds children",
        "}",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 300 + i * 110), line, font=font(FONT_MONO, 24), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_when_to_use(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When to Use", font=font(FONT_SERIF, 46), fill=WHITE)
    good = [("blocking I/O servers", GREEN), ("JDBC / HTTP clients", ORANGE), ("simple per-request threads", BLUE)]
    for i, (name, col) in enumerate(good):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1400, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), f"✓  {name}", font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    a = ease_out_cubic(clamp((progress - 0.55) / 0.3))
    if a > 0:
        d.rounded_rectangle([200, 700, 1720, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=2)
        d.text((280, 760), "✗  CPU-bound work on virtual threads", font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "pooling virtual threads", "create per task"), ("02", "CPU on virtual thread", "pins carrier"), ("03", "synchronized hot paths", "use ReentrantLock")]
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
    q = "Virtual vs platform threads?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("virtual", "cheap, I/O, unmount", GREEN), ("platform", "CPU, OS thread", ORANGE), ("pinning", "synchronized blocks carrier", RED)]
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
    title = "Class Loading"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "ClassLoader hierarchy · linkage"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 51", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "project_loom": render_project_loom,
    "virtual_vs_platform": render_virtual_vs_platform, "pinning": render_pinning,
    "structured_concurrency": render_structured_concurrency, "when_to_use": render_when_to_use,
    "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser,
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
    print("==> Kokoro Episode 50...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep50_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep50.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep50_narrated.mp4"
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
        paced = OUTPUT / "java_ep50_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_50_Virtual_Threads.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_50.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_50_Virtual_Threads_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep50_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_virtual_vs_platform'), ('00:01:40', '03_pinning'), ('00:02:30', '04_structured'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 50: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
