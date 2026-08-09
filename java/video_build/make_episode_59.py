#!/usr/bin/env python3
"""Episode 59 — Escape Analysis. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep59", ROOT / "frames_ep59", ROOT / "clips_ep59"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-Eight showed jcmd, jmap, and JFR for live diagnostics.',
        'But the JIT compiler makes invisible optimizations before runtime tools see them.',
        'Escape analysis asks — does this object leave the current scope?',
        'If not, the JVM may never allocate it on the heap at all.',
        'Stack allocation and scalar replacement eliminate heap pressure silently.',
        'Today — escape analysis, stack allocation, and when objects escape.',
    ]),
    ("title", "title", [
        'Episode Fifty-Nine.',
        'Escape Analysis.',
    ]),
    ("escape_definition", "escape_definition", [
        'An object escapes when a reference outlives the creating method or thread.',
        'Returned from a method — escapes to the caller.',
        'Stored in a field or static variable — escapes to the object graph.',
        'Passed to another thread — escapes across thread boundaries.',
        'Published to a collection visible elsewhere — escapes globally.',
        'No escape means the JIT can treat the object as method-local only.',
    ]),
    ("stack_allocation", "stack_allocation", [
        'Stack allocation places short-lived objects on the thread stack frame.',
        'Avoids heap allocation and GC pressure entirely for non-escaping objects.',
        'The object dies when the stack frame pops — no collector involvement.',
        'Enabled by escape analysis during C2 compilation.',
        'You cannot observe stack allocation directly — it is a compiler optimization.',
        'Micro-benchmarks with millions of tiny allocations may show zero GC impact.',
    ]),
    ("scalar_replacement", "scalar_replacement", [
        'Scalar replacement goes further — the object may not exist at all.',
        'Fields of a non-escaping object become local variables in registers.',
        'No object header, no alignment padding — just primitive values.',
        'Point class with int x and int y — replaced by two local ints.',
        'Combines with dead code elimination and constant folding.',
        'Most powerful when objects are small and method-local.',
    ]),
    ("escape_scenarios", "escape_scenarios", [
        'When does escape analysis fail to optimize?',
        'Returning the object — always escapes to the caller heap.',
        'Storing in an instance field — escapes with the enclosing object.',
        'Synchronized blocks publishing to shared state — escapes globally.',
        'Logging or debug toString that captures references — subtle escape.',
        'Inlining boundaries — if callee escapes, caller object may escape too.',
    ]),
    ("jit_flags", "jit_flags", [
        'Observing escape analysis in practice.',
        'C2 compiler performs escape analysis by default — no flag needed.',
        'PrintCompilation shows when methods reach C2 optimized level.',
        'JITWatch and -XX:+PrintInlining reveal inlining decisions.',
        'Async Profiler allocation samples drop when optimizations kick in after warmup.',
        'Do not disable escape analysis in production — it is a core C2 optimization.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — assuming every new creates a heap object — escape analysis may elide it.',
        'Two — benchmarking without warmup — measures interpreter, not optimized code.',
        'Three — storing objects in fields to avoid allocation — guarantees escape.',
        'Also — relying on object identity for non-escaping locals — may be scalar-replaced.',
        'Write clear, short-lived objects — let the JIT optimize naturally.',
    ]),
    ("interview", "interview", [
        'Interview question — what is escape analysis?',
        'JIT analyzes whether object references leave method or thread scope.',
        'No escape — stack allocate or scalar replace fields into locals.',
        'Escapes on return, field store, or cross-thread publish.',
        'Reduces allocation rate and GC pressure invisibly at C2 compile time.',
        'Warmup required — optimization appears after hot method compilation.',
    ]),
    ("teaser", "teaser", [
        'Heap objects are only part of JVM memory — classes and native buffers live elsewhere.',
        'Episode Sixty — Metaspace and Native Memory.',
        'Metaspace versus PermGen, direct buffers, and NMT.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Objects that never hit the heap"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 40))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 40), fill=WHITE)
    for i, (lab, col) in enumerate([("method", ORANGE), ("stack", BLUE), ("scalar", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 100, 520), lab, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 59", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Escape Analysis", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("stack allocation · scalar replacement", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_escape_definition(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "What Is Escape?", font=font(FONT_SERIF, 44), fill=WHITE)
    cases = [("return obj", "escapes to caller", RED), ("field = obj", "escapes to graph", ORANGE), ("other thread", "cross-thread", BLUE)]
    for i, (k, v, col) in enumerate(cases):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        y = 280 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 45), k, font=font(FONT_MONO, 28), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_stack_allocation(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Stack Allocation", font=font(FONT_SERIF, 44), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, GREEN, a), width=3)
    lines = [
        "non-escaping object → thread stack frame",
        "dies when frame pops — no GC",
        "C2 escape analysis enables this",
        "invisible in heap dumps",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 320 + i * 120), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_scalar_replacement(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Scalar Replacement", font=font(FONT_SERIF, 44), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.35))
    d.rounded_rectangle([200, 220, 1720, 500], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=2)
    d.text((280, 280), "Point p = new Point(1, 2);", font=font(FONT_MONO, 26), fill=mix(BG, WHITE, a))
    d.text((280, 360), "→ int x = 1; int y = 2;", font=font(FONT_MONO, 26), fill=mix(BG, GREEN, a))
    a2 = ease_out_cubic(clamp((progress - 0.4) / 0.35))
    d.rounded_rectangle([200, 560, 1720, 780], radius=14, fill=mix(BG, SURFACE, a2), outline=mix(BG, BLUE, a2), width=2)
    d.text((280, 620), "no object header · fields in registers", font=font(FONT_REG, 28), fill=mix(BG, WHITE, a2))
    return img.convert("RGB")


def render_escape_scenarios(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When Objects Escape", font=font(FONT_SERIF, 40), fill=WHITE)
    scenarios = [("return", "caller heap", RED), ("instance field", "object graph", ORANGE), ("shared state", "global visibility", BLUE), ("logging ref", "subtle escape", GREEN)]
    for i, (k, v, col) in enumerate(scenarios):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1720, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((900, y + 40), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_jit_flags(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Observing Optimizations", font=font(FONT_SERIF, 40), fill=WHITE)
    tips = [("warmup first", "C2 must compile", ORANGE), ("PrintCompilation", "tier levels", BLUE), ("alloc profiler", "drops after optimize", GREEN)]
    for i, (k, v, col) in enumerate(tips):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 45), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "every new = heap", "may be elided"), ("02", "no JVM warmup", "interpreter only"), ("03", "store in field", "forces escape")]
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
    q = "What is escape analysis?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("scope check", "reference leaves method?", ORANGE), ("no escape", "stack / scalar replace", BLUE), ("warmup", "C2 compile time", GREEN)]
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
    title = "Metaspace & Native Memory"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 40))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 40), fill=WHITE)
    sub = "metaspace · direct buffers · NMT"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 60", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "escape_definition": render_escape_definition,
    "stack_allocation": render_stack_allocation, "scalar_replacement": render_scalar_replacement,
    "escape_scenarios": render_escape_scenarios, "jit_flags": render_jit_flags,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Observing", "Look at")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 59...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep59_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep59.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep59_narrated.mp4"
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
        paced = OUTPUT / "java_ep59_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_59_Escape_Analysis.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_59.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_59_Escape_Analysis_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep59_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_escape'), ('00:01:40', '03_stack'), ('00:02:30', '04_scalar'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 59: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
