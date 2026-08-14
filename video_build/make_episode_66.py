#!/usr/bin/env python3
"""Episode 66 — JVM Interview Wrap-Up. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep66", ROOT / "frames_ep66", ROOT / "clips_ep66"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Sixty-Five covered JVM startup, class loading, and warmup strategies.',
        'You have studied heap, stack, GC, JIT, flags, layout, safepoints, and startup.',
        'Interviewers do not want a textbook — they want crisp, structured answers.',
        'The best JVM answers connect concepts — heap holds objects, stack holds frames.',
        'GC reclaims unreachable heap objects — JIT compiles hot bytecode to native code.',
        'Today — how to explain JVM internals crisply in interview settings.',
    ]),
    ("title", "title", [
        'Episode Sixty-Six.',
        'JVM Interview Wrap-Up.',
    ]),
    ("heap_stack_crisp", "heap_stack_crisp", [
        'Heap versus stack — the foundation answer.',
        'Stack — per-thread, stores method frames, local primitives, and reference variables.',
        'Heap — shared, stores all objects and arrays — GC manages this region.',
        'Reference on stack points to object on heap — Episodes Fifty-Three and Sixty-One.',
        'Stack is fast and automatic — pops when method returns.',
        'Heap objects live until GC proves them unreachable — no deterministic destruction.',
    ]),
    ("gc_crisp", "gc_crisp", [
        'Garbage collection — concise interview framing.',
        'GC finds reachable objects from roots — stack refs, static fields, JNI handles.',
        'Everything else is garbage — memory reclaimed automatically.',
        'Generational hypothesis — most objects die young — Eden and survivor spaces.',
        'Collectors trade throughput versus pause — G1 default, ZGC for low latency.',
        'Tune with GC logs and measurement — not memorized flag lists.',
    ]),
    ("jit_crisp", "jit_crisp", [
        'JIT compilation — why Java can be fast.',
        'Interpreter runs bytecode immediately — no upfront compile wait.',
        'HotSpot profiles execution — frequently called methods get JIT compiled.',
        'C1 quick compile first — C2 optimizes hot paths with inlining and escape analysis.',
        'Deoptimization falls back to interpreter when assumptions break.',
        'Warmup matters — first requests run interpreted until JIT kicks in.',
    ]),
    ("tying_together", "tying_together", [
        'Tie the internals story together for interview depth.',
        'Class loading puts metadata in metaspace — objects on heap reference classes.',
        'Object layout — headers, padding, compressed oops — affects memory footprint.',
        'Safepoints coordinate GC and deoptimization — sync time can dominate pauses.',
        'Flags tune heap, collector, and diagnostics — always measure before changing.',
        'This stack of knowledge is what separates junior from senior JVM answers.',
    ]),
    ("interview_framework", "interview_framework", [
        'A reusable framework for any JVM interview question.',
        'Define the concept in one sentence — what it is and where it lives.',
        'Explain why it exists — the problem it solves for the runtime.',
        'Give a concrete example — code snippet or production scenario.',
        'Mention trade-offs — nothing in the JVM is free.',
        'Close with how you would investigate — logs, JFR, profilers, flags.',
    ]),
    ("mistakes", "mistakes", [
        'Three common interview mistakes.',
        'One — reciting flags without explaining what problem they solve.',
        'Two — conflating heap and metaspace — different memory regions.',
        'Three — claiming Java is always slow — ignoring JIT and modern collectors.',
        'Also — diving into implementation details before answering the question asked.',
        'Structure beats depth — interviewers reward clarity over encyclopedic knowledge.',
    ]),
    ("interview", "interview", [
        'Capstone question — explain how the JVM runs a Java program.',
        'Source compiles to bytecode — class loader brings classes into metaspace.',
        'Interpreter executes — stack frames on thread stacks, objects on heap.',
        'JIT compiles hot methods — GC reclaims unreachable heap objects.',
        'Safepoints coordinate pauses — flags tune heap, collector, and logging.',
        'Measurement validates every claim — that is the senior engineer answer.',
    ]),
    ("teaser", "teaser", [
        'JVM internals complete — next we shift to application architecture.',
        'Episode Sixty-Seven — Design Patterns Intro.',
        'Reusable solutions before we reach Spring at Episode Seventy-One.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Crisp JVM answers"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    for i, (lab, col) in enumerate([("heap", ORANGE), ("GC", BLUE), ("JIT", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 150, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 66", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("JVM Interview Wrap-Up", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("heap · stack · GC · JIT — crisply", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_heap_stack_crisp(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Heap vs Stack", font=font(FONT_SERIF, 44), fill=WHITE)
    cols = [("Stack", "per-thread frames, locals", ORANGE), ("Heap", "shared objects, GC managed", BLUE)]
    for i, (k, v, col) in enumerate(cols):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        y = 250 + i * 280
        d.rounded_rectangle([200, y, 1720, y + 200], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 50), k, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
        d.text((280, y + 120), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_gc_crisp(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "GC — Crisp Answer", font=font(FONT_SERIF, 40), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, GREEN, a), width=3)
    lines = [
        "roots → reachable objects kept",
        "unreachable → reclaimed automatically",
        "generational: young die fast",
        "G1 default · ZGC low pause",
        "tune with GC logs + measurement",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_jit_crisp(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "JIT — Crisp Answer", font=font(FONT_SERIF, 40), fill=WHITE)
    feats = [("interpreter", "immediate bytecode exec", ORANGE), ("profiler", "finds hot methods", BLUE), ("C1 → C2", "quick then optimize", GREEN)]
    for i, (k, v, col) in enumerate(feats):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_tying_together(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Tie It Together", font=font(FONT_SERIF, 44), fill=WHITE)
    chain = [("class load", "metaspace", ORANGE), ("objects", "heap layout", BLUE), ("safepoints", "GC sync", GREEN), ("flags", "tune + measure", RED)]
    for i, (k, v, col) in enumerate(chain):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1720, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 30), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((900, y + 35), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_interview_framework(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Answer Framework", font=font(FONT_SERIF, 44), fill=WHITE)
    steps = [("define", ORANGE), ("why", BLUE), ("example", GREEN), ("trade-offs", RED), ("investigate", ORANGE)]
    for i, (step, col) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        x = 160 + i * 340
        d.rounded_rectangle([x, 400, x + 300, 700], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((x + 70, 520), step, font=font(FONT_REG, 24), fill=mix(BG, WHITE, a))
        if i < 4:
            d.text((x + 305, 530), "→", font=font(FONT_BOLD, 28), fill=MUTED)
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "flags without why", "explain the problem"), ("02", "heap = metaspace", "different regions"), ("03", "Java is slow", "JIT + modern GC")]
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
    d.text((160, 70), "Capstone Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "How does the JVM run Java?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("load + interpret", "classes → bytecode exec", ORANGE), ("JIT + GC", "compile hot, reclaim heap", BLUE), ("measure", "flags, JFR, profilers", GREEN)]
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
    title = "Design Patterns Intro"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 42))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 42), fill=WHITE)
    sub = "reusable architecture · bridge to Spring at Ep71"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 67", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "heap_stack_crisp": render_heap_stack_crisp,
    "gc_crisp": render_gc_crisp, "jit_crisp": render_jit_crisp, "tying_together": render_tying_together,
    "interview_framework": render_interview_framework, "mistakes": render_mistakes,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Capstone", "A reusable")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 66...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep66_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep66.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep66_narrated.mp4"
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
        paced = OUTPUT / "java_ep66_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_66_JVM_Interview_Wrap.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_66.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_66_JVM_Interview_Wrap_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep66_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_heap_stack'), ('00:01:40', '03_gc'), ('00:02:30', '04_framework'), ('00:03:20', '05_capstone')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 66: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
