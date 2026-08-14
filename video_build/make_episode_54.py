#!/usr/bin/env python3
"""Episode 54 — Garbage Collection Intro. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep54", ROOT / "frames_ep54", ROOT / "clips_ep54"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-Three placed objects on the shared heap.',
        'Who frees memory when those objects are no longer needed?',
        'Java has no free or delete — the garbage collector reclaims unreachable objects.',
        'GC traces from roots — stack locals, static fields, JNI references.',
        'Generations exploit the observation that most objects die young.',
        'Today — garbage collection basics, mark-sweep, and stop-the-world pauses.',
    ]),
    ("title", "title", [
        'Episode Fifty-Four.',
        'Garbage Collection Intro.',
    ]),
    ("gc_roots", "gc_roots", [
        'GC roots are starting points for reachability analysis.',
        'Local variables and operand stacks in active frames are roots.',
        'Static fields in loaded classes hold root references.',
        'JNI global references and JVM internal structures are roots too.',
        'An object is live if reachable from any root through references.',
        'Unreachable objects are garbage — eligible for collection.',
    ]),
    ("mark_sweep", "mark_sweep", [
        'Mark-sweep is the foundational GC algorithm.',
        'Mark phase — traverse from roots, flag every reachable object.',
        'Sweep phase — walk the heap, reclaim unmarked objects.',
        'Compact phase in some collectors — defragment live objects.',
        'Simple but can fragment memory without compaction.',
        'Modern collectors extend this with copying and concurrent marking.',
    ]),
    ("generations", "generations", [
        'The generational hypothesis — most objects die young.',
        'Young generation — Eden plus Survivor spaces — frequent minor GC.',
        'Objects that survive several collections promote to old generation.',
        'Old generation — long-lived data — collected less often, more expensive.',
        'Minor GC is fast — scans only the young region.',
        'Major or full GC collects the entire heap — longer pauses.',
    ]),
    ("stop_the_world", "stop_the_world", [
        'Stop-the-world means all application threads pause during GC.',
        'Safepoints are locations where the JVM can safely halt threads.',
        'During STW, roots are scanned and the heap is processed.',
        'Pause time is the metric users feel — latency spikes in production.',
        'Concurrent collectors reduce STW but add complexity.',
        'GC logs show pause durations — always monitor in production.',
    ]),
    ("gc_triggers", "gc_triggers", [
        'Minor GC triggers when Eden fills up.',
        'Major GC triggers when old generation is full or explicitly requested.',
        'System.gc is a hint — JVM may ignore it depending on collector.',
        'OutOfMemoryError fires only after GC fails to reclaim enough space.',
        'Heap flags like Xms and Xmx control generation sizes.',
        'Tuning starts with understanding what triggers each collection.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — calling System.gc expecting immediate cleanup — unreliable hint.',
        'Two — setting heap huge without understanding GC pause trade-offs.',
        'Three — ignoring GC logs until production latency spikes.',
        'Also — assuming all unreachable objects collect instantly — GC is periodic.',
        'Measure pause times before tuning — data beats folklore.',
    ]),
    ("interview", "interview", [
        'Interview question — how does Java GC work?',
        'Trace from roots — stack locals, statics, JNI refs.',
        'Mark reachable objects — sweep or compact unreachable ones.',
        'Generational — young collected often, old collected rarely.',
        'Stop-the-world pauses all threads at safepoints.',
        'Collector choice and heap sizing affect pause versus throughput.',
    ]),
    ("teaser", "teaser", [
        'Bytecode starts in the interpreter — hot code gets compiled.',
        'Episode Fifty-Five — JIT Compilation.',
        'Interpreter, C1, C2 tiers, hot methods, and deoptimization.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Automatic memory reclaim"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 44))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 44), fill=WHITE)
    for i, (lab, col) in enumerate([("roots", ORANGE), ("mark", BLUE), ("sweep", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 140, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 54", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Garbage Collection Intro", font(FONT_SERIF, 44), H // 2 - 30, mix(BG, WHITE, a)),
        ("roots · mark-sweep · generations", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_gc_roots(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "GC Roots", font=font(FONT_SERIF, 48), fill=WHITE)
    roots = [("stack locals", "active frame references", ORANGE), ("static fields", "class-level refs", BLUE), ("JNI globals", "native references", GREEN)]
    for i, (k, v, col) in enumerate(roots):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mark_sweep(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Mark-Sweep", font=font(FONT_SERIF, 48), fill=WHITE)
    phases = [("1 mark", "trace from roots → flag live", ORANGE), ("2 sweep", "reclaim unmarked objects", BLUE), ("3 compact", "defragment (optional)", GREEN)]
    for i, (k, v, col) in enumerate(phases):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_generations(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Generations", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([200, 200, 1000, 500], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    d.text((280, 240), "Young Gen", font=font(FONT_BOLD, 32), fill=mix(BG, ORANGE, a))
    d.text((280, 320), "Eden + Survivors", font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    d.text((280, 400), "minor GC (frequent)", font=font(FONT_REG, 24), fill=mix(BG, MUTED, a))
    d.rounded_rectangle([200, 560, 1700, 820], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    d.text((280, 600), "Old Gen", font=font(FONT_BOLD, 32), fill=mix(BG, BLUE, a))
    d.text((280, 680), "long-lived objects — major GC (rare, costly)", font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_stop_the_world(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Stop-The-World", font=font(FONT_SERIF, 42), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=3)
    lines = [
        "app threads ──► PAUSE at safepoint",
        "GC scans roots + processes heap",
        "app threads ──► RESUME",
        "pause time = latency users feel",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 300 + i * 120), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_gc_triggers(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "GC Triggers", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("Eden full", "minor GC", ORANGE), ("Old gen full", "major / full GC", BLUE), ("System.gc()", "hint — may ignore", GREEN)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "System.gc() magic", "unreliable hint"), ("02", "huge heap blindly", "longer pauses"), ("03", "no GC logs", "surprise latency")]
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
    q = "How does Java GC work?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("trace", "roots → mark reachable", ORANGE), ("reclaim", "sweep unmarked objects", BLUE), ("generations", "young often, old rarely", GREEN)]
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
    title = "JIT Compilation"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "interpreter · C1/C2 · deoptimization"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 55", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "gc_roots": render_gc_roots,
    "mark_sweep": render_mark_sweep, "generations": render_generations,
    "stop_the_world": render_stop_the_world, "gc_triggers": render_gc_triggers,
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
    print("==> Kokoro Episode 54...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep54_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep54.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep54_narrated.mp4"
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
        paced = OUTPUT / "java_ep54_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_54_Garbage_Collection.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_54.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_54_Garbage_Collection_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep54_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_roots'), ('00:01:40', '03_mark'), ('00:02:30', '04_generations'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 54: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
