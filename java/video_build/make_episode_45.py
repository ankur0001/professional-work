#!/usr/bin/env python3
"""Episode 45 — BlockingQueue & Producer-Consumer. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep45", ROOT / "frames_ep45", ROOT / "clips_ep45"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Producers generate work. Consumers process it. They run at different speeds.',
        'A shared list without bounds lets producers outpace consumers — memory explodes.',
        'BlockingQueue adds capacity limits and blocking put and take semantics.',
        'When full, put waits. When empty, take waits. Natural backpressure.',
        'The producer-consumer pattern is the backbone of thread pools and pipelines.',
        'Today — BlockingQueue, the pattern, and choosing the right implementation.',
    ]),
    ("title", "title", [
        'Episode Forty-Five.',
        'BlockingQueue and Producer-Consumer.',
    ]),
    ("blocking_queue", "blocking_queue", [
        'BlockingQueue extends Queue with blocking operations.',
        'put inserts an element — blocks if the queue is full.',
        'take removes an element — blocks if the queue is empty.',
        'offer and poll provide timed or non-blocking alternatives.',
        'Thread-safe — multiple producers and consumers without external locks.',
        'The queue itself coordinates waiting and waking threads.',
    ]),
    ("producer_consumer", "producer_consumer", [
        'Producer-consumer decouples creation from processing.',
        'Producers enqueue tasks — consumers dequeue and execute.',
        'Bounded queue caps in-flight work — protects memory and downstream systems.',
        'ExecutorService thread pools use internal work queues this way.',
        'Pipeline stages connect via queues — each stage runs at its own pace.',
        'Backpressure emerges naturally when the queue fills.',
    ]),
    ("array_blocking", "array_blocking", [
        'ArrayBlockingQueue uses a fixed-capacity circular array.',
        'One lock for both put and take — simple and predictable.',
        'Fair ordering optional — FIFO for waiting threads.',
        'Bounded capacity set at construction — cannot grow.',
        'Low overhead for steady workloads with known bounds.',
        'Choose when you need a fixed-size buffer with array backing.',
    ]),
    ("linked_blocking", "linked_blocking", [
        'LinkedBlockingQueue uses linked nodes — optionally bounded.',
        'Two locks — one for put, one for take — better under mixed load.',
        'Default capacity is Integer.MAX_VALUE — effectively unbounded.',
        'Always pass an explicit capacity in production — unbounded queues hide leaks.',
        'Higher memory per element than array — but no upfront array allocation.',
        'Common in executor frameworks when capacity is configured explicitly.',
    ]),
    ("when_blocking", "when_blocking", [
        'When to use BlockingQueue.',
        'Thread pool work queues — bounded backpressure.',
        'Log or event pipelines — producers spike, consumers steady.',
        'Handoff between stages — parse, transform, persist.',
        'Replace wait-notify handoffs with a cleaner API.',
        'When not — single-threaded batch — a simple List suffices.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — unbounded LinkedBlockingQueue — memory grows under slow consumers.',
        'Two — put without handling InterruptedException — shutdown breaks cleanly.',
        'Three — multiple consumers on one queue without coordination — usually fine, but watch ordering.',
        'Also — blocking take on the only thread that should stop the pipeline.',
        'Size the queue — too small starves workers, too large hides overload.',
    ]),
    ("interview", "interview", [
        'Interview question — why BlockingQueue over synchronized List?',
        'Built-in blocking put and take — no manual wait-notify loops.',
        'Bounded capacity provides backpressure automatically.',
        'Thread-safe for multiple producers and consumers.',
        'ArrayBlockingQueue — fixed array, one lock. Linked — dual locks.',
        'Mention producer-consumer and ExecutorService work queues.',
    ]),
    ("teaser", "teaser", [
        'Queues pass work between threads. What about composing async results?',
        'Episode Forty-Six — CompletableFuture Deep Dive.',
        'thenApply, thenCompose, allOf, and exception handling.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Bounded handoff"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 50), fill=WHITE)
    for i, (lab, col) in enumerate([("producer", ORANGE), ("queue", BLUE), ("consumer", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 280 + i * 520
        d.rounded_rectangle([x, 400, x + 420, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 70, 520), lab, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        if i < 2:
            d.text((x + 430, 520), "→", font=font(FONT_BOLD, 36), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 45", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("BlockingQueue", font(FONT_SERIF, 58), H // 2 - 30, mix(BG, WHITE, a)),
        ("Producer-Consumer · backpressure", font(FONT_REG, 28), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_blocking_queue(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "BlockingQueue", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "BlockingQueue<Task> queue = new ArrayBlockingQueue<>(100);",
        "queue.put(task);  // blocks if full",
        "Task t = queue.take(); // blocks if empty",
        "// thread-safe — no external lock",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 300 + i * 120), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_producer_consumer(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Producer-Consumer", font=font(FONT_SERIF, 44), fill=WHITE)
    left = ease_out_cubic(clamp(progress / 0.4)); right = ease_out_cubic(clamp((progress - 0.3) / 0.4))
    if left > 0:
        d.rounded_rectangle([140, 220, 900, 820], radius=18, fill=mix(BG, SURFACE, left), outline=mix(BG, ORANGE, left), width=4)
        d.text((220, 280), "Producer", font=font(FONT_BOLD, 32), fill=mix(BG, ORANGE, left))
        for i, lab in enumerate(["creates work", "put when ready", "slows if full"]):
            d.text((240, 380 + i * 70), lab, font=font(FONT_REG, 28), fill=mix(BG, WHITE, left))
    if right > 0:
        d.rounded_rectangle([1020, 220, 1780, 820], radius=18, fill=mix(BG, SURFACE, right), outline=mix(BG, GREEN, right), width=4)
        d.text((1100, 280), "Consumer", font=font(FONT_BOLD, 32), fill=mix(BG, GREEN, right))
        for i, lab in enumerate(["take work", "process item", "waits if empty"]):
            d.text((1120, 380 + i * 70), lab, font=font(FONT_REG, 28), fill=mix(BG, WHITE, right))
    return img.convert("RGB")


def render_array_blocking(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "ArrayBlockingQueue", font=font(FONT_SERIF, 44), fill=WHITE)
    items = [("fixed array", "capacity at construction", ORANGE), ("one lock", "put + take share", BLUE), ("fair mode", "FIFO waiters optional", GREEN)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 220
        d.rounded_rectangle([200, y, 1720, y + 180], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_linked_blocking(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "LinkedBlockingQueue", font=font(FONT_SERIF, 42), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, GREEN, a), width=3)
    lines = [
        "new LinkedBlockingQueue<>(500); // always bound",
        "// two locks — put lock + take lock",
        "// default unbounded — dangerous in prod",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 320 + i * 140), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_when_blocking(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When BlockingQueue", font=font(FONT_SERIF, 44), fill=WHITE)
    good = [("thread pool work queue", GREEN), ("pipeline handoff", ORANGE), ("backpressure on overload", BLUE)]
    for i, (name, col) in enumerate(good):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1400, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), f"✓  {name}", font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    a = ease_out_cubic(clamp((progress - 0.55) / 0.3))
    if a > 0:
        d.rounded_rectangle([200, 700, 1720, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=2)
        d.text((280, 760), "✗  Single-thread batch — plain List", font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "unbounded queue", "memory grows forever"), ("02", "ignore InterruptedException", "bad shutdown"), ("03", "queue too large", "hides overload")]
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
    q = "BlockingQueue vs synchronized List?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [("BlockingQueue", "blocking put/take built-in", BLUE), ("bounded", "natural backpressure", GREEN), ("Array vs Linked", "one vs two locks", ORANGE)]
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
    title = "CompletableFuture Deep Dive"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 44))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 44), fill=WHITE)
    sub = "thenApply · thenCompose · allOf"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 46", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "blocking_queue": render_blocking_queue,
    "producer_consumer": render_producer_consumer, "array_blocking": render_array_blocking,
    "linked_blocking": render_linked_blocking, "when_blocking": render_when_blocking,
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
    print("==> Kokoro Episode 45...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep45_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep45.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep45_narrated.mp4"
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
        paced = OUTPUT / "java_ep45_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_45_BlockingQueue.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_45.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_45_BlockingQueue_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep45_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_blocking'), ('00:01:40', '03_producer'), ('00:02:30', '04_array'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 45: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
