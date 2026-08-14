#!/usr/bin/env python3
"""Episode 44 — Synchronizers. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep44", ROOT / "frames_ep44", ROOT / "clips_ep44"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Threads often need to meet at a point — start together or wait for completion.',
        'Synchronizers coordinate thread arrival and departure without shared data structures.',
        'CountDownLatch — one thread waits until others finish a countdown.',
        'CyclicBarrier — threads rendezvous at a barrier, then release together.',
        'Semaphore — limit how many threads access a resource at once.',
        'Today — the three core synchronizers and when each fits.',
    ]),
    ("title", "title", [
        'Episode Forty-Four.',
        'Synchronizers.',
    ]),
    ("countdown_latch", "countdown_latch", [
        'CountDownLatch initializes with a count — typically the number of workers.',
        'Each worker calls countDown when finished — the latch decrements.',
        'await blocks until the count reaches zero — then all waiters proceed.',
        'One-shot — cannot reset the count after it reaches zero.',
        'Classic pattern — main thread waits for parallel startup or shutdown.',
        'Example — wait for N services to finish initialization before accepting traffic.',
    ]),
    ("cyclic_barrier", "cyclic_barrier", [
        'CyclicBarrier sets a party count — the number of threads that must arrive.',
        'Each thread calls await — the barrier releases when all parties arrive.',
        'Reusable — after release, the barrier resets for the next cycle.',
        'Optional barrier action runs once when the last thread arrives.',
        'Use for phased parallel computation — each phase ends at the barrier.',
        'BrokenBarrierException if a waiting thread is interrupted or times out.',
    ]),
    ("semaphore", "semaphore", [
        'Semaphore maintains a set of permits — acquire takes one, release returns one.',
        'new Semaphore of N allows up to N concurrent accessors.',
        'acquire blocks when no permits remain — release wakes a waiter.',
        'tryAcquire with timeout avoids indefinite blocking.',
        'Binary semaphore with one permit acts like a mutex — but not reentrant.',
        'Use for connection pools, rate limiting, and bounded resource access.',
    ]),
    ("coordination", "coordination", [
        'Choosing the right synchronizer.',
        'CountDownLatch — wait for a fixed number of events — one direction.',
        'CyclicBarrier — threads meet repeatedly at the same point.',
        'Semaphore — cap concurrent access to a limited resource.',
        'Phaser offers flexible phase-based coordination — advanced alternative.',
        'Exchanger swaps objects between two threads at a rendezvous point.',
    ]),
    ("when_sync", "when_sync", [
        'When to use each synchronizer.',
        'Service startup gate — CountDownLatch until all workers ready.',
        'Parallel matrix phases — CyclicBarrier between compute steps.',
        'Database connection cap — Semaphore with pool size permits.',
        'Fork-join style shutdown — latch counts completed tasks.',
        'When not — simple flag — volatile or AtomicBoolean may suffice.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — reusing a CountDownLatch after count hits zero — it is one-shot.',
        'Two — wrong party count on CyclicBarrier — threads hang forever.',
        'Three — Semaphore acquire without matching release — permits leak.',
        'Also — calling await on the only thread that should countDown.',
        'Synchronizers coordinate timing — they do not protect mutable state alone.',
    ]),
    ("interview", "interview", [
        'Interview question — CountDownLatch versus CyclicBarrier?',
        'CountDownLatch — one or more threads wait for others to finish events.',
        'Count is decremented — cannot reset after reaching zero.',
        'CyclicBarrier — threads rendezvous; all must arrive before any proceed.',
        'Barrier resets and is reusable for the next cycle.',
        'Semaphore limits concurrent access — different problem entirely.',
    ]),
    ("teaser", "teaser", [
        'Synchronizers coordinate arrival. What about passing work between threads?',
        'Episode Forty-Five — BlockingQueue and Producer-Consumer.',
        'Bounded queues, backpressure, and the classic pattern.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Threads rendezvous"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 50), fill=WHITE)
    for i, (lab, col) in enumerate([("Latch", ORANGE), ("Barrier", BLUE), ("Semaphore", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 80, 520), lab, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 44", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Synchronizers", font(FONT_SERIF, 58), H // 2 - 30, mix(BG, WHITE, a)),
        ("Latch · Barrier · Semaphore", font(FONT_REG, 28), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_countdown_latch(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "CountDownLatch", font=font(FONT_SERIF, 46), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    lines = [
        "CountDownLatch latch = new CountDownLatch(3);",
        "worker -> latch.countDown();",
        "mainThread.await(); // until count == 0",
        "// one-shot — cannot reset",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 300 + i * 120), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_cyclic_barrier(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "CyclicBarrier", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("await()", "block until all parties arrive", BLUE), ("reset", "reusable next cycle", GREEN), ("action", "runs when last arrives", ORANGE)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 220
        d.rounded_rectangle([200, y, 1720, y + 180], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), k, font=font(FONT_MONO, 32), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_semaphore(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Semaphore", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, GREEN, a), width=3)
    lines = [
        "Semaphore permits = new Semaphore(10);",
        "permits.acquire(); // take one permit",
        "useResource();",
        "permits.release(); // return permit",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 300 + i * 120), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_coordination(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Pick the Right Tool", font=font(FONT_SERIF, 44), fill=WHITE)
    tools = [("CountDownLatch", "wait for N events", ORANGE), ("CyclicBarrier", "repeated rendezvous", BLUE), ("Semaphore", "limit concurrency", GREEN)]
    for i, (name, desc, col) in enumerate(tools):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), name, font=font(FONT_MONO, 28), fill=mix(BG, col, a))
        d.text((280, y + 95), desc, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_when_sync(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When to Use", font=font(FONT_SERIF, 46), fill=WHITE)
    good = [("startup gate — latch", GREEN), ("phased compute — barrier", ORANGE), ("connection cap — semaphore", BLUE)]
    for i, (name, col) in enumerate(good):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1400, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), f"✓  {name}", font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    a = ease_out_cubic(clamp((progress - 0.55) / 0.3))
    if a > 0:
        d.rounded_rectangle([200, 700, 1720, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=2)
        d.text((280, 760), "✗  Simple flag — AtomicBoolean may suffice", font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "reuse CountDownLatch", "one-shot only"), ("02", "wrong barrier count", "threads hang"), ("03", "missing release()", "permits leak")]
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
    q = "CountDownLatch vs CyclicBarrier?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 34)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 34), fill=WHITE)
    answers = [("Latch", "wait for N events, one-shot", ORANGE), ("Barrier", "all arrive, reusable", BLUE), ("Semaphore", "limits concurrent access", GREEN)]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "BlockingQueue"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "Producer-Consumer · backpressure"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 45", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "countdown_latch": render_countdown_latch,
    "cyclic_barrier": render_cyclic_barrier, "semaphore": render_semaphore, "coordination": render_coordination,
    "when_sync": render_when_sync, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser,
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
    print("==> Kokoro Episode 44...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep44_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep44.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep44_narrated.mp4"
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
        paced = OUTPUT / "java_ep44_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_44_Synchronizers.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_44.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_44_Synchronizers_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep44_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_latch'), ('00:01:40', '03_barrier'), ('00:02:30', '04_semaphore'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 44: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
