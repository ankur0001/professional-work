#!/usr/bin/env python3
"""Episode 52 — Bytecode Basics. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep52", ROOT / "frames_ep52", ROOT / "clips_ep52"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-One showed how the JVM loads class files.',
        'But what is actually inside those bytes?',
        'Java source compiles to bytecode — a stack-machine instruction set.',
        'Opcodes like iload, invokevirtual, and return drive every method.',
        'javap disassembles class files so you can read what the JVM runs.',
        'Today — bytecode basics, the constant pool, and the stack machine model.',
    ]),
    ("title", "title", [
        'Episode Fifty-Two.',
        'Bytecode Basics.',
    ]),
    ("class_file", "class_file", [
        'A class file is a structured binary format — not human-readable source.',
        'Magic number CA FE BA BE identifies a valid Java class file.',
        'Constant pool holds strings, class names, method signatures, and literals.',
        'Fields, methods, and attributes describe the class structure.',
        'Code attribute contains the actual bytecode instructions for each method.',
        'The JVM never sees your .java file — only verified .class bytecode.',
    ]),
    ("javap", "javap", [
        'javap is the JDK disassembler — your window into bytecode.',
        'javap -c MyClass prints disassembled method bodies.',
        'javap -v adds verbose output — constant pool entries and stack maps.',
        'javap -p shows private members — useful for debugging generated code.',
        'Compare source to javap output — see what the compiler actually emitted.',
        'Every senior Java developer should read javap at least once per project.',
    ]),
    ("stack_machine", "stack_machine", [
        'The JVM is a stack machine — operands live on an operand stack.',
        'Each method frame has its own operand stack and local variable array.',
        'Instructions push values, operate, and pop results.',
        'iload pushes a local int — iadd pops two ints and pushes the sum.',
        'No general-purpose registers — the stack is the workspace.',
        'Think push, operate, pop — that mental model unlocks every opcode.',
    ]),
    ("opcodes", "opcodes", [
        'Opcodes are single-byte instructions — some have operands.',
        'Constants — iconst_1, ldc, bipush load values onto the stack.',
        'Locals — iload, istore, aload, astore read and write local slots.',
        'Fields — getfield, putfield, getstatic access object and class data.',
        'Methods — invokevirtual, invokestatic, invokespecial dispatch calls.',
        'Control flow — ifeq, goto, tableswitch branch on stack values.',
    ]),
    ("reading_bytecode", "reading_bytecode", [
        'Walk through a simple method bytecode by bytecode.',
        'aload_0 pushes this — getfield reads an instance field.',
        'invokevirtual calls a method — return ends the frame.',
        'Stack depth must match what verification expects — stack map tables help.',
        'Compiler optimizations change bytecode — loops may unroll or inline.',
        'Reading bytecode connects source code to runtime behavior.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — assuming bytecode matches source line-for-line — compilers optimize.',
        'Two — ignoring stack depth errors — VerifyError at class load time.',
        'Three — confusing invokevirtual with invokestatic — wrong dispatch semantics.',
        'Also — editing .class files by hand without understanding verification.',
        'Use javap as a learning tool — not as something to fear.',
    ]),
    ("interview", "interview", [
        'Interview question — what is Java bytecode?',
        'Platform-independent instruction set for the JVM stack machine.',
        'Compiled from .java by javac into .class files.',
        'Constant pool, fields, methods, and Code attributes per class.',
        'javap disassembles bytecode — read opcodes like iload and invokevirtual.',
        'Verification ensures type safety and stack consistency before execution.',
    ]),
    ("teaser", "teaser", [
        'Bytecode runs on stacks — but where do objects actually live?',
        'Episode Fifty-Three — Heap and Stack.',
        'Frames, locals, object layout, and metaspace.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Source to bytecode"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("javac", ORANGE), ("CAFEBABE", BLUE), ("javap", GREEN)]):
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
        ("EPISODE 52", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Bytecode Basics", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("javap · opcodes · stack machine", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_class_file(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Class File Layout", font=font(FONT_SERIF, 44), fill=WHITE)
    parts = [("magic", "CA FE BA BE", ORANGE), ("constant pool", "strings, refs, literals", BLUE), ("methods", "Code attribute → bytecode", GREEN)]
    for i, (k, v, col) in enumerate(parts):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_javap(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "javap", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    lines = [
        "$ javap -c -p MyClass",
        "  public void run();",
        "    Code:",
        "       0: aload_0",
        "       1: invokevirtual #7",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 260 + i * 100), line, font=font(FONT_MONO, 24), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_stack_machine(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Stack Machine", font=font(FONT_SERIF, 44), fill=WHITE)
    stack = ["sum", "b", "a"]
    for i, val in enumerate(stack):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 700 - i * 120
        d.rounded_rectangle([1200, y, 1600, y + 90], radius=10, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=2)
        d.text((1280, y + 25), val, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, a))
    d.text((300, 300), "iload_1  → push a", font=font(FONT_MONO, 26), fill=mix(BG, ORANGE, ease_out_cubic(clamp(progress / 0.35))))
    d.text((300, 420), "iload_2  → push b", font=font(FONT_MONO, 26), fill=mix(BG, ORANGE, ease_out_cubic(clamp((progress - 0.2) / 0.35))))
    d.text((300, 540), "iadd     → pop, pop, push", font=font(FONT_MONO, 26), fill=mix(BG, GREEN, ease_out_cubic(clamp((progress - 0.4) / 0.35))))
    d.text((1200, 180), "operand stack ↑", font=font(FONT_REG, 24), fill=MUTED)
    return img.convert("RGB")


def render_opcodes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Opcode Families", font=font(FONT_SERIF, 42), fill=WHITE)
    groups = [("constants", "iconst, ldc, bipush", ORANGE), ("locals", "iload, istore, aload", BLUE), ("invoke", "virtual, static, special", GREEN)]
    for i, (k, v, col) in enumerate(groups):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_reading_bytecode(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Reading Bytecode", font=font(FONT_SERIF, 42), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, GREEN, a), width=3)
    lines = [
        "int add(int a, int b) { return a + b; }",
        "// javap:",
        "  iload_1",
        "  iload_2",
        "  iadd",
        "  ireturn",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        fnt = FONT_MONO if i > 0 else FONT_REG
        d.text((260, 260 + i * 90), line, font=font(fnt, 24), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "source == bytecode", "compiler optimizes"), ("02", "ignore stack depth", "VerifyError"), ("03", "wrong invoke opcode", "dispatch semantics")]
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
    q = "What is Java bytecode?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("format", "stack-machine .class files", ORANGE), ("tool", "javap disassembles methods", BLUE), ("verify", "type + stack safety checks", GREEN)]
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
    title = "Heap and Stack"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "frames · locals · object layout"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 53", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "class_file": render_class_file,
    "javap": render_javap, "stack_machine": render_stack_machine, "opcodes": render_opcodes,
    "reading_bytecode": render_reading_bytecode, "mistakes": render_mistakes,
    "interview": render_interview, "teaser": render_teaser,
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
    print("==> Kokoro Episode 52...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep52_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep52.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep52_narrated.mp4"
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
        paced = OUTPUT / "java_ep52_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_52_Bytecode_Basics.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_52.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_52_Bytecode_Basics_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep52_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_javap'), ('00:01:40', '03_stack'), ('00:02:30', '04_opcodes'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 52: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
