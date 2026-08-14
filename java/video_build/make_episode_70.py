#!/usr/bin/env python3
"""Episode 70 — Behavioral Patterns. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep70", ROOT / "frames_ep70", ROOT / "clips_ep70"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Sixty-Nine covered structural patterns — adapting, wrapping, and composing.',
        'Behavioral patterns focus on algorithms and communication between objects.',
        'They let you vary what happens without rewriting call sites every time.',
        'Strategy swaps algorithms — Observer broadcasts events — Command queues actions.',
        'These patterns dominate service code and interview whiteboards alike.',
        'Today — Strategy, Observer, Command, Template Method, and Iterator — then Spring next.',
    ]),
    ("title", "title", [
        'Episode Seventy.',
        'Behavioral Patterns.',
    ]),
    ("strategy", "strategy", [
        'Strategy defines a family of algorithms and makes them interchangeable.',
        'Clients depend on a strategy interface — concrete strategies plug in.',
        'Comparator in Java is Strategy — sort order injected at call time.',
        'Payment processors, pricing rules, and retry policies are classic Strategies.',
        'Prefer Strategy over deep if-else chains that grow every quarter.',
        'Keep strategies focused — one decision axis per strategy type.',
    ]),
    ("observer", "observer", [
        'Observer notifies dependents automatically when a subject changes.',
        'Publish-subscribe and event listeners are Observer in modern clothes.',
        'Swing listeners, reactive streams, and message topics follow the shape.',
        'Decouples producers from consumers — but watch notification storms.',
        'Unregister carefully — leaked listeners are memory leak classics.',
        'Use Observer when many parties care about the same state change.',
    ]),
    ("command", "command", [
        'Command encapsulates a request as an object.',
        'You can queue, log, undo, and retry actions uniformly.',
        'Runnable and Callable are lightweight command shapes in Java.',
        'GUI actions, job queues, and transactional outboxes use Command ideas.',
        'Macro commands compose smaller commands into workflows.',
        'Command separates invoker from receiver — great for undo stacks.',
    ]),
    ("template_iterator", "template_iterator", [
        'Template Method defines an algorithm skeleton in a base class.',
        'Subclasses override steps without changing the overall sequence.',
        'JdbcTemplate and many framework hooks follow Template Method spirit.',
        'Iterator provides sequential access without exposing collection structure.',
        'Enhanced for-loops and Stream pipelines rest on Iterator ideas.',
        'Together they show behavior reuse — hooks and traversal, not inheritance for data.',
    ]),
    ("choose", "choose", [
        'Choosing behavioral patterns in practice.',
        'Vary an algorithm — Strategy or a simple function parameter.',
        'Broadcast state changes — Observer or an event bus with clear ownership.',
        'Queue or undo work — Command objects with explicit lifecycle.',
        'Framework-defined steps — Template Method or modern composition hooks.',
        'Prefer small interfaces — behavioral patterns should shrink switch statements.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — Strategy explosion — dozens of one-line classes for dead branches.',
        'Two — Observer spaghetti — unclear who listens and who owns cleanup.',
        'Three — Command without idempotency — retries double-charge users.',
        'Also — Template Method locking teams into brittle inheritance.',
        'Behavior patterns need ownership rules — not just class diagrams.',
    ]),
    ("interview", "interview", [
        'Interview question — how do Strategy and Template Method differ?',
        'Strategy composes algorithms via interfaces — swap at runtime.',
        'Template Method inherits a skeleton — subclasses fill in steps.',
        'Strategy favors composition — Template Method favors inheritance.',
        'Modern Java often prefers Strategy plus lambdas over deep templates.',
        'Say the force — runtime swap versus fixed sequence with customizable steps.',
    ]),
    ("teaser", "teaser", [
        'Patterns prepared the design vocabulary — frameworks apply it at scale.',
        'Episode Seventy-One — Spring Framework Intro.',
        'IoC, dependency injection, and why Spring beans feel like patterns in production.',
        'See you there.',
    ]),
]

def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = 'Collaboration patterns'
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    labs = [('Strategy', 'ORANGE'), ('Observer', 'BLUE'), ('Command', 'GREEN')]
    for i, (lab, col) in enumerate(labs):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=3)
        d.text((x + 80, 520), lab, font=font(FONT_BOLD, 28), fill=mix(BG, c, a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ('EPISODE 70', font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ('Behavioral Patterns', font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ('Strategy · Observer · Command · Template · Iterator', font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")

def render_strategy(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Strategy', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('swap algorithms', 'same client, different policy', 'ORANGE'), ('Comparator', 'JDK strategy classic', 'BLUE'), ('beat if-else', 'open for new variants', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_observer(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Observer', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('publish / subscribe', 'notify on change', 'ORANGE'), ('decouple parties', 'producers ≠ consumers', 'BLUE'), ('unregister!', 'avoid listener leaks', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_command(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Command', font=font(FONT_SERIF, 44), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = ['request as an object', 'queue · log · undo · retry', 'Runnable / Callable cousins', 'macro commands compose', 'separate invoker & receiver']
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")

def render_template_iterator(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Template & Iterator', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('Template Method', 'skeleton + override steps', 'ORANGE'), ('Iterator', 'traverse without expose', 'BLUE'), ('JdbcTemplate spirit', 'framework fills the loop', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_choose(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Choose Wisely', font=font(FONT_SERIF, 44), fill=WHITE)
    steps = [('vary algo?', 'ORANGE'), ('broadcast?', 'BLUE'), ('queue/undo?', 'GREEN'), ('fixed steps?', 'RED')]
    for i, (step, col) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        x = 160 + i * 340
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([x, 400, x + 300, 700], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((x + 40, 520), step, font=font(FONT_REG, 22), fill=mix(BG, WHITE, a))
        if i < len(steps) - 1:
            d.text((x + 305, 530), "→", font=font(FONT_BOLD, 28), fill=MUTED)
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Common Mistakes', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('01', 'strategy explosion', 'keep real variants only'), ('02', 'observer spaghetti', 'own register/unregister'), ('03', 'non-idempotent command', 'safe retries')]
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
    d.text((160, 60), 'Interview Question', font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = 'Strategy vs Template Method?'
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 34)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 34), fill=WHITE)
    answers = [('Strategy', 'compose & swap runtime', 'ORANGE'), ('Template', 'inherit fixed skeleton', 'BLUE'), ('prefer compose', 'lambdas over deep bases', 'GREEN')]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 28), fill=mix(BG, c, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = 'Spring Framework Intro'; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 42))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 42), fill=WHITE)
    sub = 'IoC · DI · beans as patterns'; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), 'Episode 71', font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "strategy": render_strategy,
    "observer": render_observer,
    "command": render_command,
    "template_iterator": render_template_iterator,
    "choose": render_choose,
    "mistakes": render_mistakes,
    "interview": render_interview,
    "teaser": render_teaser,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Capstone", "A reusable", "Patterns")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 70...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep70_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep70.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep70_narrated.mp4"
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
        paced = OUTPUT / "java_ep70_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_70_Behavioral_Patterns.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_70.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_70_Behavioral_Patterns_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep70_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_strategy'), ('00:01:40', '03_observer'), ('00:02:30', '04_command'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 70: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
