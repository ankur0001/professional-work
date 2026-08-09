#!/usr/bin/env python3
"""Episode 53 — Heap and Stack. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep53", ROOT / "frames_ep53", ROOT / "clips_ep53"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-Two decoded bytecode on the operand stack.',
        'But where do method frames and objects actually live in memory?',
        'Each thread owns a stack of frames — locals and operand stacks inside.',
        'The heap holds every object your program allocates with new.',
        'Class metadata lives in metaspace — separate from the object heap.',
        'Today — heap and stack, frames, locals, and object layout.',
    ]),
    ("title", "title", [
        'Episode Fifty-Three.',
        'Heap and Stack.',
    ]),
    ("stack_frames", "stack_frames", [
        'Each Java thread has its own call stack — one frame per active method.',
        'A frame stores local variables, the operand stack, and a reference to the constant pool.',
        'When a method is invoked, a new frame is pushed — return pops it.',
        'StackOverflowError means too many nested calls — usually infinite recursion.',
        'Frames are thread-local — no sharing between threads on the stack.',
        'The stack is fast and automatically reclaimed when a method returns.',
    ]),
    ("locals_array", "locals_array", [
        'Local variable slot zero is always this for instance methods.',
        'Parameters occupy the next slots — iload and istore reference them.',
        'Wide types like long and double consume two consecutive slots.',
        'The operand stack is separate from locals — temporary computation space.',
        'Compiler assigns slot numbers — visible in javap with -v.',
        'Locals die with the frame — no manual cleanup needed.',
    ]),
    ("heap_objects", "heap_objects", [
        'Every new keyword allocates an object on the heap.',
        'All threads share the heap — objects are visible across threads.',
        'References on the stack or in other objects point to heap instances.',
        'Heap memory is managed by the garbage collector — not freed manually.',
        'OutOfMemoryError means the heap cannot grow further.',
        'Large object graphs live here — caches, collections, domain models.',
    ]),
    ("object_layout", "object_layout", [
        'A heap object starts with a mark word and a klass pointer header.',
        'Instance fields follow the header — primitives inline, references are pointers.',
        'Arrays store length then elements — int arrays pack ints contiguously.',
        'Object size depends on header plus fields plus alignment padding.',
        'Compressed oops shorten reference fields on 64-bit JVMs with less than 32 GB heap.',
        'Understanding layout helps reason about memory footprint and cache behavior.',
    ]),
    ("metaspace", "metaspace", [
        'Class metadata — method tables, constant pools, field layouts — lives in metaspace.',
        'Metaspace replaced PermGen in Java 8 — native memory, not part of the heap.',
        'Grows as classes load — reclaimed when ClassLoader is collected.',
        'ClassLoader leaks can exhaust metaspace — a common production issue.',
        'Flag MaxMetaspaceSize caps growth — default is effectively unlimited.',
        'Heap holds objects — metaspace holds class definitions.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — storing large objects on the stack — only references live on the stack.',
        'Two — assuming stack variables are thread-safe — only if not escaped.',
        'Three — ignoring metaspace when leaking ClassLoaders in hot-reload apps.',
        'Also — confusing heap size with total JVM memory footprint.',
        'Know which memory region each piece of data occupies.',
    ]),
    ("interview", "interview", [
        'Interview question — heap versus stack in Java?',
        'Stack — per-thread frames with locals and operand stacks — automatic cleanup.',
        'Heap — shared object storage — garbage collected.',
        'References on stack point to objects on heap.',
        'Metaspace holds class metadata — separate from heap since Java 8.',
        'StackOverflowError versus OutOfMemoryError — different regions, different causes.',
    ]),
    ("teaser", "teaser", [
        'Objects on the heap outlive their frames — something must reclaim them.',
        'Episode Fifty-Four — Garbage Collection Intro.',
        'Roots, mark-sweep, generations, and stop-the-world pauses.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Where data lives"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("stack", ORANGE), ("heap", BLUE), ("metaspace", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 120, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 53", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Heap and Stack", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("frames · locals · object layout", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_stack_frames(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Call Stack", font=font(FONT_SERIF, 44), fill=WHITE)
    frames = [("main()", ORANGE), ("process()", BLUE), ("compute()", GREEN)]
    for i, (k, col) in enumerate(frames):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([400, y, 1520, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((480, y + 45), k, font=font(FONT_MONO, 30), fill=mix(BG, col, a))
        if i < 2:
            d.text((920, y + 155), "↓ push frame", font=font(FONT_REG, 22), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_locals_array(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Locals & Operand Stack", font=font(FONT_SERIF, 40), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([200, 180, 900, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=2)
    d.text((280, 200), "locals[]", font=font(FONT_BOLD, 28), fill=mix(BG, ORANGE, a))
    for i, slot in enumerate(["this", "arg0", "arg1", "temp"]):
        d.text((280, 280 + i * 100), f"[{i}] {slot}", font=font(FONT_MONO, 24), fill=mix(BG, WHITE, ease_out_cubic(clamp((progress - i * 0.1) / 0.3))))
    d.rounded_rectangle([1000, 300, 1700, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=2)
    d.text((1080, 320), "operand stack", font=font(FONT_BOLD, 28), fill=mix(BG, BLUE, a))
    for i, val in enumerate(["3", "7", "10"]):
        d.text((1200, 700 - i * 120), val, font=font(FONT_MONO, 32), fill=mix(BG, WHITE, ease_out_cubic(clamp((progress - 0.3 - i * 0.1) / 0.3))))
    return img.convert("RGB")


def render_heap_objects(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Heap Objects", font=font(FONT_SERIF, 44), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "String s = new String(\"hi\");",
        "// ref on stack → object on heap",
        "List<String> list = new ArrayList<>();",
        "// shared across all threads",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 300 + i * 120), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_object_layout(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Object Layout", font=font(FONT_SERIF, 44), fill=WHITE)
    parts = [("mark word", "GC + hash + lock state", ORANGE), ("klass ptr", "points to class metadata", BLUE), ("fields", "primitives + references", GREEN)]
    for i, (k, v, col) in enumerate(parts):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_metaspace(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Metaspace", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, GREEN, a), width=3)
    lines = [
        "Heap     → objects (new)",
        "Metaspace → class metadata",
        "  method tables, constant pools",
        "Freed when ClassLoader collected",
        "-XX:MaxMetaspaceSize=256m",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 300 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "objects on stack", "only references"), ("02", "stack = thread-safe", "escaped refs"), ("03", "ignore metaspace", "ClassLoader leaks")]
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
    q = "Heap vs stack in Java?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("stack", "per-thread frames, locals", ORANGE), ("heap", "shared objects, GC managed", BLUE), ("metaspace", "class metadata, native mem", GREEN)]
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
    title = "Garbage Collection Intro"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 46), fill=WHITE)
    sub = "roots · generations · stop-the-world"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 54", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "stack_frames": render_stack_frames,
    "locals_array": render_locals_array, "heap_objects": render_heap_objects,
    "object_layout": render_object_layout, "metaspace": render_metaspace,
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
    print("==> Kokoro Episode 53...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep53_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep53.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep53_narrated.mp4"
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
        paced = OUTPUT / "java_ep53_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_53_Heap_and_Stack.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_53.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_53_Heap_and_Stack_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep53_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_frames'), ('00:01:40', '03_heap'), ('00:02:30', '04_layout'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 53: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
