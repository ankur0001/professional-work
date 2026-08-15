#!/usr/bin/env python3
"""Episode 42 — Concurrent Collections. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep42", ROOT / "frames_ep42", ROOT / "clips_ep42"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Multiple threads reading and writing the same HashMap can corrupt it.',
        'Synchronized wrappers lock the entire collection — every operation blocks.',
        'Concurrent collections offer finer-grained safety without one global lock.',
        'ConcurrentHashMap scales reads and writes across internal segments.',
        'CopyOnWriteArrayList snapshots the backing array on each mutation.',
        'Today — thread-safe collections and when each design wins.',
    ]),
    ("title", "title", [
        'Episode Forty-Two.',
        'Concurrent Collections.',
    ]),
    ("concurrent_hashmap", "concurrent_hashmap", [
        'ConcurrentHashMap is the go-to concurrent map in Java.',
        'It never throws ConcurrentModificationException on concurrent access.',
        'Internal locking is segment-based — not one lock for the whole map.',
        'get is usually lock-free. put and remove lock only a segment.',
        'null keys and null values are not permitted — unlike HashMap.',
        'Use ConcurrentHashMap when many threads share a mutable map.',
    ]),
    ("copy_on_write", "copy_on_write", [
        'CopyOnWriteArrayList copies the entire array on every write.',
        'Reads iterate a stable snapshot — no locks during traversal.',
        'Writes are expensive — copy plus replace the reference.',
        'Perfect when reads vastly outnumber writes — listener lists, caches.',
        'Iterator never throws ConcurrentModificationException.',
        'Do not use for write-heavy workloads — copying dominates.',
    ]),
    ("thread_safe_queues", "thread_safe_queues", [
        'ConcurrentLinkedQueue — lock-free linked nodes for high-throughput queues.',
        'BlockingQueue variants add wait and notify semantics — covered next episode.',
        'ConcurrentSkipListMap and ConcurrentSkipListSet offer sorted concurrent access.',
        'Collections.synchronizedList wraps with a mutex — simple but coarse.',
        'Prefer java.util.concurrent types over synchronized wrappers at scale.',
        'Match the collection to your read-write ratio and ordering needs.',
    ]),
    ("vs_synchronized", "vs_synchronized", [
        'Synchronized collections versus concurrent collections.',
        'SynchronizedMap — one lock per operation — simple but contended.',
        'ConcurrentHashMap — segmented or striped locking — scales better.',
        'CopyOnWriteArrayList — no read locks — ideal for read-heavy lists.',
        'Vector and synchronized ArrayList block every reader and writer.',
        'Legacy wrappers still appear — know the modern replacements.',
    ]),
    ("when_use", "when_use", [
        'When to choose each concurrent collection.',
        'Shared cache or registry — ConcurrentHashMap.',
        'Event listeners or config snapshots — CopyOnWriteArrayList.',
        'High-throughput work queues — ConcurrentLinkedQueue.',
        'Sorted concurrent map — ConcurrentSkipListMap.',
        'When not — single-threaded code — plain HashMap is faster.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — using HashMap from multiple threads without external locking.',
        'Two — CopyOnWriteArrayList for write-heavy lists — copies explode.',
        'Three — assuming compound actions are atomic — check-then-act needs care.',
        'Also — iterating a synchronized list without holding its lock.',
        'Concurrent collections help — but logical consistency is still your job.',
    ]),
    ("interview", "interview", [
        'Interview question — ConcurrentHashMap versus synchronized HashMap?',
        'ConcurrentHashMap uses finer locking — better scalability under contention.',
        'No ConcurrentModificationException on concurrent iteration patterns.',
        'Null keys and values forbidden — enforced at API level.',
        'CopyOnWriteArrayList for read-heavy, rarely mutated lists.',
        'Mention when synchronized wrappers are still acceptable — low contention.',
    ]),
    ("teaser", "teaser", [
        'Collections protect shared structures. What about single counters?',
        'Episode Forty-Three — Atomic Variables.',
        'AtomicInteger, compare-and-swap, and lock-free updates.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Share safely"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 50), fill=WHITE)
    for i, (lab, col) in enumerate([("threads", ORANGE), ("ConcurrentMap", BLUE), ("safe", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 280 + i * 520
        d.rounded_rectangle([x, 400, x + 420, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 60, 520), lab, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        if i < 2:
            d.text((x + 430, 520), "→", font=font(FONT_BOLD, 36), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 42", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Concurrent Collections", font(FONT_SERIF, 52), H // 2 - 30, mix(BG, WHITE, a)),
        ("ConcurrentHashMap · CopyOnWrite", font(FONT_REG, 28), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_concurrent_hashmap(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "ConcurrentHashMap", font=font(FONT_SERIF, 44), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();",
        "map.put(\"key\", 1);",
        "map.computeIfAbsent(\"key\", k -> load(k));",
        "// segment locks — not one global mutex",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 300 + i * 120), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_copy_on_write(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "CopyOnWriteArrayList", font=font(FONT_SERIF, 42), fill=WHITE)
    items = [("read", "snapshot — no lock", GREEN), ("write", "copy array + replace", ORANGE), ("ratio", "many reads, few writes", BLUE)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 220
        d.rounded_rectangle([200, y, 1720, y + 180], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_thread_safe_queues(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Concurrent Queues", font=font(FONT_SERIF, 46), fill=WHITE)
    queues = [("ConcurrentLinkedQueue", "lock-free FIFO", ORANGE), ("ConcurrentSkipListMap", "sorted concurrent", BLUE), ("synchronizedList", "coarse mutex", MUTED)]
    for i, (name, desc, col) in enumerate(queues):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), name, font=font(FONT_MONO, 28), fill=mix(BG, col, a))
        d.text((280, y + 95), desc, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_vs_synchronized(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "vs Synchronized Wrappers", font=font(FONT_SERIF, 42), fill=WHITE)
    left = ease_out_cubic(clamp(progress / 0.4)); right = ease_out_cubic(clamp((progress - 0.3) / 0.4))
    if left > 0:
        d.rounded_rectangle([140, 220, 900, 820], radius=18, fill=mix(BG, SURFACE, left), outline=mix(BG, RED, left), width=4)
        d.text((220, 280), "Synchronized", font=font(FONT_BOLD, 32), fill=mix(BG, RED, left))
        for i, lab in enumerate(["one lock per op", "all readers block", "simple API"]):
            d.text((240, 380 + i * 70), lab, font=font(FONT_REG, 28), fill=mix(BG, WHITE, left))
    if right > 0:
        d.rounded_rectangle([1020, 220, 1780, 820], radius=18, fill=mix(BG, SURFACE, right), outline=mix(BG, GREEN, right), width=4)
        d.text((1100, 280), "Concurrent", font=font(FONT_BOLD, 32), fill=mix(BG, GREEN, right))
        for i, lab in enumerate(["finer locking", "scales under load", "modern default"]):
            d.text((1120, 380 + i * 70), lab, font=font(FONT_REG, 28), fill=mix(BG, WHITE, right))
    return img.convert("RGB")


def render_when_use(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When to Use", font=font(FONT_SERIF, 46), fill=WHITE)
    good = [("shared map / cache", GREEN), ("read-heavy listener list", ORANGE), ("high-throughput queue", BLUE)]
    for i, (name, col) in enumerate(good):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1400, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), f"✓  {name}", font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    a = ease_out_cubic(clamp((progress - 0.55) / 0.3))
    if a > 0:
        d.rounded_rectangle([200, 700, 1720, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=2)
        d.text((280, 760), "✗  Single-threaded — plain HashMap wins", font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "HashMap + threads", "use ConcurrentHashMap"), ("02", "COW for write-heavy", "copy cost dominates"), ("03", "check-then-act", "use compute/putIfAbsent")]
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
    q = "ConcurrentHashMap vs synchronized Map?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [("ConcurrentHashMap", "finer locks, scales", BLUE), ("CopyOnWrite", "read-heavy lists", GREEN), ("Wrappers", "OK when low contention", ORANGE)]
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
    title = "Atomic Variables"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "AtomicInteger · compare-and-swap"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 43", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "concurrent_hashmap": render_concurrent_hashmap,
    "copy_on_write": render_copy_on_write, "thread_safe_queues": render_thread_safe_queues,
    "vs_synchronized": render_vs_synchronized, "when_use": render_when_use,
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
    print("==> Kokoro Episode 42...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep42_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep42.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep42_narrated.mp4"
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
        paced = OUTPUT / "java_ep42_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_42_Concurrent_Collections.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_42.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_42_Concurrent_Collections_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep42_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_hashmap'), ('00:01:40', '03_copy_on_write'), ('00:02:30', '04_when_use'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 42: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
