#!/usr/bin/env python3
"""Episode 09 — Strings. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep09", ROOT / "frames_ep09", ROOT / "clips_ep09"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))


SCENES = [
    ("hook", "hook", [
        "Arrays hold many values. Strings hold text — and text is everywhere.",
        "APIs, logs, JSON, HTTP, configuration, identifiers.",
        "String is immutable. That safety is powerful — and easy to misuse.",
        "Today we treat String like the production type it is.",
        "Small mistakes here show up in security and performance.",
    ]),
    ("title", "title", [
        "Episode Nine.",
        "Strings — immutability, equality, and careful construction.",
    ]),
    ("immutable", "immutable", [
        "Immutability means the characters never change after creation.",
        "s equals s plus world does not edit s — it creates a new String.",
        "That sharing and safety help concurrency and caching.",
        "But careless concatenation can allocate again and again.",
        "Understand create versus modify — String only creates.",
        "That one idea prevents a whole class of confusion.",
    ]),
    ("equality", "equality", [
        "Equality is the classic trap.",
        "Equals-equals compares references — same String object?",
        "For text content — use equals.",
        "Safer pattern — literal first. PAID dot equals status.",
        "Null-safe and clear. Interviewers listen for this.",
    ]),
    ("build", "build", [
        "Building strings in a loop?",
        "Do not use plus repeatedly in hot loops.",
        "Use StringBuilder — append in place, then toString once.",
        "Modern compilers help simple cases — but builders win when you loop.",
        "Measure hot paths. Clarity first — then allocation discipline.",
    ]),
    ("charset", "charset", [
        "Bytes are not characters without a charset.",
        "Prefer UTF-8 explicitly when encoding or decoding.",
        "toLowerCase without a locale can surprise you in Turkish and beyond.",
        "For identifiers, be explicit about case rules.",
        "Never assume the platform default will match production.",
        "Be explicit — always.",
    ]),
    ("mistakes", "mistakes", [
        "Three common mistakes.",
        "One — equals-equals for text content.",
        "Two — logging secrets inside strings — tokens, passwords, cards.",
        "Three — accepting unbounded string input until memory cries.",
        "Also — pushing raw strings deep into domain code. Prefer typed values.",
    ]),
    ("interview", "interview", [
        "Interview question — why is String immutable?",
        "Safety, sharing, hash stability for maps, and simpler concurrency reasoning.",
        "Then add — use StringBuilder when you mutate often.",
        "And never compare text with equals-equals.",
        "That trio covers language design and daily practice.",
    ]),
    ("teaser", "teaser", [
        "Text is under control. Next we model the world.",
        "Episode Ten — object-oriented programming.",
        "Classes, objects, encapsulation — how Java scales design.",
        "See you there.",
    ]),
]

def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Immutable text"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 52))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 140), title, font=font(FONT_SERIF, 52), fill=WHITE)
    parts = [("APIs", ORANGE), ("logs", BLUE), ("JSON", GREEN), ("HTTP", ORANGE)]
    for i, (lab, col) in enumerate(parts):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        x = 200 + i * 420
        d.rounded_rectangle([x, 400, x + 340, 700], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=4)
        d.text((x + 70, 520), lab, font=font(FONT_BOLD, 36), fill=mix(BG, col, a))
        if i < 3 and progress > i * 0.15 + 0.15:
            d.polygon([(x + 350, 540), (x + 380, 550), (x + 350, 560)], fill=ORANGE)
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 09", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Strings", font(FONT_SERIF, 72), H // 2 - 30, mix(BG, WHITE, a)),
        ("immutability · equality · construction", font(FONT_REG, 32), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_immutable(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Immutable Strings", font=font(FONT_SERIF, 48), fill=WHITE)
    code = "String s = \"hi\"; s = s + \"!\";  // new String"
    pieces = [
        ("\"hi\"", "original", ORANGE, 0.1),
        ("s + \"!\"", "concat", BLUE, 0.35),
        ("new String", "new object", GREEN, 0.6),
        ("old GC'd", "unchanged", MUTED, 0.8),
    ]
    d.rounded_rectangle([160, 180, 1760, 360], radius=16, fill=SURFACE, outline=BLUE, width=3)
    d.text((220, 240), code, font=font(FONT_MONO, 34), fill=WHITE)
    for i, (tok, note, col, start) in enumerate(pieces):
        a = ease_out_cubic(clamp((progress - start) / 0.28))
        if a <= 0: continue
        x = 180 + i * 340
        d.rounded_rectangle([x, 460, x + 300, 780], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((x + 30, 540), tok, font=font(FONT_MONO_B, 26), fill=mix(BG, col, a))
        d.text((x + 30, 640), note, font=font(FONT_REG, 24), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_equality(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "== vs .equals", font=font(FONT_SERIF, 46), fill=WHITE)
    cards = [
        ("==", "reference equality", "same object in memory?", RED, 0.15),
        (".equals", "value equality", "same text content?", GREEN, 0.45),
        ("\"PAID\".equals(status)", "null-safe pattern", "constant on the left", ORANGE, 0.7),
    ]
    for i, (name, line, note, col, start) in enumerate(cards):
        a = ease_out_cubic(clamp((progress - start) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 170], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=4)
        d.text((260, y + 30), name, font=font(FONT_MONO_B, 36), fill=mix(BG, col, a))
        d.text((260, y + 90), line, font=font(FONT_REG, 30), fill=mix(BG, WHITE, a))
        d.text((260, y + 130), note, font=font(FONT_REG, 26), fill=mix(BG, MUTED, a))
    return img.convert("RGB")


def render_build(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Building Strings", font=font(FONT_SERIF, 46), fill=WHITE)
    left_a = ease_out_cubic(clamp(progress / 0.4))
    right_a = ease_out_cubic(clamp((progress - 0.3) / 0.4))
    if left_a > 0:
        d.rounded_rectangle([140, 200, 900, 860], radius=18, fill=mix(BG, SURFACE, left_a), outline=mix(BG, RED, left_a), width=4)
        d.text((220, 280), "loop + plus", font=font(FONT_BOLD, 40), fill=mix(BG, RED, left_a))
        for i, line in enumerate(["Many temp objects", "GC pressure in hot loops", "Avoid in production"]):
            d.text((220, 420 + i * 90), f"•  {line}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, left_a))
    if right_a > 0:
        d.rounded_rectangle([1020, 200, 1780, 860], radius=18, fill=mix(BG, SURFACE, right_a), outline=mix(BG, GREEN, right_a), width=4)
        d.text((1100, 280), "StringBuilder", font=font(FONT_BOLD, 40), fill=mix(BG, GREEN, right_a))
        for i, line in enumerate(["Mutates in place", "One buffer grows", "Right tool for loops"]):
            d.text((1100, 420 + i * 90), f"•  {line}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, right_a))
    return img.convert("RGB")


def render_charset(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Bytes & Charset", font=font(FONT_SERIF, 46), fill=WHITE)
    tips = [
        ("UTF-8", "default for APIs, JSON, web", GREEN),
        ("bytes[]", "not text until decoded", ORANGE),
        ("toLowerCase()", "needs Locale — Turkish trap", RED),
        ("StandardCharsets.UTF_8", "explicit, portable", BLUE),
    ]
    for i, (num, tip, col) in enumerate(tips):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 170 + i * 180
        d.rounded_rectangle([200, y, 1720, y + 150], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((260, y + 45), num, font=font(FONT_MONO_B, 30), fill=mix(BG, col, a))
        d.text((560, y + 50), tip, font=font(FONT_BOLD, 32), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [
        ("01", "== for text comparison", "Use .equals or Objects.equals"),
        ("02", "Logging secrets in plain text", "Redact tokens and passwords"),
        ("03", "Unbounded user input", "Validate length and content"),
        ("04", "Raw strings in domain logic", "Prefer typed values and enums"),
    ]
    for i, (num, wrong, right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.16) / 0.32))
        if a <= 0: continue
        y = 160 + i * 185
        d.rounded_rectangle([200, y, 1720, y + 160], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a * 0.7), width=2)
        d.text((260, y + 30), num, font=font(FONT_SERIF, 36), fill=mix(BG, ORANGE, a))
        d.text((360, y + 35), wrong, font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
        d.text((360, y + 95), right, font=font(FONT_REG, 26), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_interview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Interview Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "Why is String immutable in Java?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [
        ("Pool / sharing", "safe interning · fewer copies", ORANGE),
        ("Thread safety", "read-only · no locks needed", BLUE),
        ("StringBuilder", "when mutating often in loops", GREEN),
    ]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 34), fill=mix(BG, col, a))
        d.text((700, y + 50), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "Object-Oriented Programming"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 58))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 50), title, font=font(FONT_SERIF, 58), fill=WHITE)
    sub = "classes · objects · encapsulation"
    bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 32))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 50), sub, font=font(FONT_REG, 32), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 140), "Episode 10", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "immutable": render_immutable,
    "equality": render_equality, "build": render_build, "charset": render_charset,
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
            gap = 0.30 if any(k in text for k in ("Once created", "Never use", "Hot loops", "Bytes are", "Four common", "Interview", "Why is")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 09...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep09_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep09.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep09_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)], check=True)
    dur = probe(narrated)
    pace = min(dur / 295.0, 1.12) if dur > 300 else (max(dur / 260.0, 0.88) if dur < 255 else 1.0)
    music = AUDIO / "music_bed.m4a"; generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep09_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_09_Strings.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_09.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_09_Strings_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep09_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [("00:00:12","01_hook"),("00:00:50","02_immutable"),("00:01:40","03_equality"),("00:02:30","04_build"),("00:03:20","05_interview")]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 09: {final_dur/60:.2f} min")
    assert 190 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
