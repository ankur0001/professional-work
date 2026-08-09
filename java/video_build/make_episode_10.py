#!/usr/bin/env python3
"""Episode 10 — Object-Oriented Programming. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep10", ROOT / "frames_ep10", ROOT / "clips_ep10"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        "Strings and arrays hold data. Objects model the world.",
        "Object-oriented programming — state, behavior, and identity working together.",
        "In Java, OOP is how we manage domain complexity — not just a syntax style.",
        "Classes define blueprints. Objects are living instances.",
        "Get this mental model right — everything else in OOP builds on it.",
    ]),
    ("title", "title", [
        "Episode Ten.",
        "Object-Oriented Programming — classes, objects, and encapsulation.",
    ]),
    ("class_obj", "class_obj", [
        "A class is the blueprint.",
        "Fields hold state. Methods hold behavior.",
        "new Order creates an object — its own identity on the heap.",
        "Two Order objects can share the same class and still be different instances.",
        "Identity matters. Equals can compare values — but identity is the object itself.",
    ]),
    ("encaps", "encaps", [
        "Encapsulation hides internals behind a clear API.",
        "private fields. public methods that protect invariants.",
        "Callers should not poke amountInCents directly if rules apply.",
        "Hide data. Expose intention — like isHighValue or applyDiscount.",
        "That is how objects stay consistent as the system grows.",
        "Encapsulation is not ceremony — it is protection.",
    ]),
    ("pillars", "pillars", [
        "Four ideas you will hear forever.",
        "Encapsulation — hide details.",
        "Abstraction — show only what matters.",
        "Inheritance — share and specialize — carefully.",
        "Polymorphism — one contract, many implementations.",
        "Prefer composition when inheritance trees get deep and fragile.",
    ]),
    ("compose", "compose", [
        "Composition says has-a.",
        "An Order has Money. A Customer has an Address.",
        "Small objects collaborating beat one god class that knows everything.",
        "Anemic models — data bags with all logic in services — often lose domain clarity.",
        "Put behavior next to the data it protects.",
        "That is domain modeling that survives real change.",
    ]),
    ("mistakes", "mistakes", [
        "Three common mistakes.",
        "One — god services that do every use-case in one class.",
        "Two — deep inheritance trees nobody can reason about.",
        "Three — public mutable fields that break encapsulation overnight.",
        "Also — leaking persistence entities straight through APIs.",
    ]),
    ("interview", "interview", [
        "Interview question — class versus object?",
        "Class — blueprint. Object — instance with identity and state.",
        "Then encapsulation — hide fields, expose safe behavior.",
        "Prefer composition over deep inheritance when design gets complex.",
        "That answer sounds like an engineer, not a memorizer.",
    ]),
    ("teaser", "teaser", [
        "Objects need boundaries. Next — who can see what.",
        "Episode Eleven — access modifiers.",
        "private, public, protected, package-private — ownership in code.",
        "See you there.",
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Model the world as objects"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 140), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("state", ORANGE), ("behavior", BLUE), ("identity", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        x = 320 + i * 420
        d.rounded_rectangle([x, 400, x + 340, 700], radius=18, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=4)
        d.text((x + 70, 520), lab, font=font(FONT_BOLD, 34), fill=mix(BG, col, a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3))
    lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 10", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Object-Oriented Programming", font(FONT_SERIF, 52), H // 2 - 20, mix(BG, WHITE, a)),
        ("classes · objects · encapsulation", font(FONT_REG, 30), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")

def render_class_obj(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Class vs Object", font=font(FONT_SERIF, 48), fill=WHITE)
    left = ease_out_cubic(clamp(progress / 0.4)); right = ease_out_cubic(clamp((progress - 0.3) / 0.4))
    if left > 0:
        d.rounded_rectangle([140, 200, 900, 860], radius=18, fill=mix(BG, SURFACE, left), outline=mix(BG, ORANGE, left), width=4)
        d.text((220, 280), "Class", font=font(FONT_BOLD, 40), fill=mix(BG, ORANGE, left))
        for i, line in enumerate(["Blueprint", "fields + methods", "Order { … }"]):
            d.text((220, 420 + i * 90), f"•  {line}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, left))
    if right > 0:
        d.rounded_rectangle([1020, 200, 1780, 860], radius=18, fill=mix(BG, SURFACE, right), outline=mix(BG, BLUE, right), width=4)
        d.text((1100, 280), "Object", font=font(FONT_BOLD, 40), fill=mix(BG, BLUE, right))
        for i, line in enumerate(["Instance on heap", "own identity", "new Order(...)"]):
            d.text((1100, 420 + i * 90), f"•  {line}", font=font(FONT_REG, 30), fill=mix(BG, WHITE, right))
    return img.convert("RGB")

def render_encaps(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Encapsulation", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([300, 200, 1620, 820], radius=20, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=4)
    d.text((380, 280), "private long amountInCents;", font=font(FONT_MONO, 32), fill=mix(BG, RED, a))
    d.text((380, 400), "public boolean isHighValue() { … }", font=font(FONT_MONO, 32), fill=mix(BG, GREEN, a))
    tip = ease_out_cubic(clamp((progress - 0.5) / 0.35))
    if tip > 0:
        d.text((380, 560), "Hide data. Expose intention.", font=font(FONT_BOLD, 34), fill=mix(BG, WHITE, tip))
        d.text((380, 660), "Protect invariants behind methods.", font=font(FONT_REG, 28), fill=mix(BG, MUTED, tip))
    return img.convert("RGB")

def render_pillars(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Four Pillars", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("Encapsulation","hide details",ORANGE),("Abstraction","show what matters",BLUE),("Inheritance","specialize carefully",GREEN),("Polymorphism","one contract, many forms",MUTED)]
    for i,(name,note,col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i*0.15)/0.3))
        if a <= 0: continue
        x = 160 + (i%2)*880; y = 180 + (i//2)*340
        d.rounded_rectangle([x,y,x+800,y+280], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+50,y+80), name, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((x+50,y+160), note, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_compose(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Composition — has-a", font=font(FONT_SERIF, 46), fill=WHITE)
    boxes = [("Order", ORANGE, 0.1), ("Money", BLUE, 0.35), ("Customer", GREEN, 0.55), ("Address", MUTED, 0.7)]
    for i,(name,col,start) in enumerate(boxes):
        a = ease_out_cubic(clamp((progress-start)/0.28))
        if a <= 0: continue
        x = 200 + i*400
        d.rounded_rectangle([x, 360, x+340, 620], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+80, 460), name, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
    tip = ease_out_cubic(clamp((progress-0.75)/0.2))
    if tip>0:
        d.text((300, 740), "Small collaborating objects beat one god class.", font=font(FONT_REG,30), fill=mix(BG,MUTED,tip))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01","God services / god classes","Split by responsibility"),("02","Deep inheritance trees","Prefer composition"),("03","Public mutable fields","Encapsulate state")]
    for i,(num,wrong,right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i*0.2)/0.35))
        if a <= 0: continue
        y = 180 + i*240
        d.rounded_rectangle([200,y,1720,y+200], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,RED,a*0.7), width=2)
        d.text((260,y+40), num, font=font(FONT_SERIF,40), fill=mix(BG,ORANGE,a))
        d.text((360,y+45), wrong, font=font(FONT_BOLD,30), fill=mix(BG,RED,a))
        d.text((360,y+110), right, font=font(FONT_REG,28), fill=mix(BG,GREEN,a))
    return img.convert("RGB")

def render_interview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Interview Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160,150,1760,280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "Class vs object — what's the difference?"
    bbox = d.textbbox((0,0), q, font=font(FONT_BOLD,32))
    d.text(((W-(bbox[2]-bbox[0]))//2, 190), q, font=font(FONT_BOLD,32), fill=WHITE)
    answers = [("Class","Blueprint — fields + methods",ORANGE),("Object","Instance with identity + state",BLUE),("Bonus","Encapsulate; prefer composition",GREEN)]
    for i,(k,v,col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a <= 0: continue
        y = 360 + i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((620,y+50), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120, 200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title = "Access Modifiers"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,60))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,60), fill=WHITE)
    sub = "private · public · protected · package-private"
    bbox = d.textbbox((0,0), sub, font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 11", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "class_obj": render_class_obj,
    "encaps": render_encaps, "pillars": render_pillars, "compose": render_compose,
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
            gap = 0.30 if any(k in text for k in ("Look at", "signature", "Design", "Interview", "Three common")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 10...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep10_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep10.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep10_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)], check=True)
    dur = probe(narrated)
    pace = min(dur / 295.0, 1.12) if dur > 300 else (max(dur / 260.0, 0.88) if dur < 255 else 1.0)
    music = AUDIO / "music_bed.m4a"; generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep10_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_10_OOP.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_10.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_10_OOP_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep10_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [("00:00:12","01_hook"),("00:00:50","02_anatomy"),("00:01:40","03_signature"),("00:02:30","04_design"),("00:03:20","05_interview")]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 10: {final_dur/60:.2f} min")
    assert 190 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
