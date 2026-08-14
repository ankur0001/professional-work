#!/usr/bin/env python3
"""Episode 13 — Enums. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep13", ROOT / "frames_ep13", ROOT / "clips_ep13"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        "Packages organize types. Enums organize fixed choices.",
        "PENDING. PAID. CANCELLED — states that should never be free-form strings.",
        "An enum is a type-safe set of named constants — with room for behavior.",
        "Today we replace magic strings with real domain states.",
        "Treat enum structure as architecture you can see in the type system.",
    ]),
    ("title", "title", [
        "Episode Thirteen.",
        "Enums — type-safe states instead of magic strings.",
    ]),
    ("basics", "basics", [
        "Declare an enum like a special class.",
        "enum OrderStatus — PENDING, PAID, SHIPPED, CANCELLED.",
        "Each constant is a singleton instance of that enum type.",
        "Compare with equals-equals safely — identity is stable.",
        "Switch expressions love enums — finite cases, clear exhaustiveness.",
        "Folder path and package declaration must agree — same for enum files.",
    ]),
    ("behavior", "behavior", [
        "Enums can carry fields and methods.",
        "Attach a display label. Attach a canTransition rule.",
        "That keeps status logic next to the status itself.",
        "Better than scattering string compares across services.",
        "Feature teams and domain packages often fit better than pure layers — enums fit domains too.",
        "Put behavior where the state lives.",
    ]),
    ("vs_string", "vs_string", [
        "Why not String status equals PAID?",
        "Typos compile. Invalid states sneak in. Refactors miss call sites.",
        "Enums make illegal states harder to represent.",
        "Serialization still needs care — name versus ordinal.",
        "Prefer name for APIs. Ordinal is a storage trap.",
        "Honest names reduce wrong imports and wrong ownership — same for status names.",
    ]),
    ("enumset", "enumset", [
        "Need a set of flags? EnumSet is built for enums.",
        "Fast. Compact. Type-safe.",
        "Permission READ, WRITE, ADMIN — store combinations cleanly.",
        "Better than bit masks scattered as magic ints — unless you truly need bits.",
        "Choose the structure that matches how the set changes.",
    ]),
    ("mistakes", "mistakes", [
        "Three common mistakes.",
        "One — Stringly typed statuses that drift across services.",
        "Two — depending on ordinal in databases or APIs.",
        "Three — stuffing volatile business config into enum constants.",
        "Also — giant enums that should have been a data table.",
        "Enums model fixed vocabularies — not every changing catalog.",
    ]),
    ("interview", "interview", [
        "Interview question — why prefer enums over string constants?",
        "Type safety. Exhaustive switches. Refactor-friendly names.",
        "Constants are real objects — can hold behavior.",
        "Avoid ordinal for persistence. Prefer name or explicit codes.",
        "That answer shows production sense.",
    ]),
    ("teaser", "teaser", [
        "Fixed states are clear. Next — when primitives become objects.",
        "Episode Fourteen — wrappers and autoboxing.",
        "Integer, nullability, and hidden allocations.",
        "See you there.",
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Stop the magic strings"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,48))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,48), fill=WHITE)
    for i,(lab,col) in enumerate([("PENDING",ORANGE),("PAID",GREEN),("CANCELLED",RED)]):
        a=ease_out_cubic(clamp((progress-i*0.2)/0.35))
        if a<=0: continue
        x=280+i*480
        d.rounded_rectangle([x,400,x+400,700], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=4)
        d.text((x+70,520), lab, font=font(FONT_MONO_B,32), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 13", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Enums", font(FONT_SERIF,72), H//2-30, mix(BG,WHITE,a)),
        ("type-safe states · behavior · EnumSet", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_basics(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Enum Basics", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,180,1720,880], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    lines=["enum OrderStatus {","  PENDING,","  PAID,","  SHIPPED,","  CANCELLED","}"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.1)/0.3))
        d.text((320,260+i*90), line, font=font(FONT_MONO,34), fill=mix(BG,WHITE if i else ORANGE, aa))
    return img.convert("RGB")

def render_behavior(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Enums Can Behave", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,200,1720,820], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    d.text((280,300), "PAID {", font=font(FONT_MONO,32), fill=mix(BG,GREEN,a))
    d.text((320,400), "public boolean canShip() { return true; }", font=font(FONT_MONO,28), fill=mix(BG,WHITE,a))
    d.text((280,500), "}", font=font(FONT_MONO,32), fill=mix(BG,GREEN,a))
    tip=ease_out_cubic(clamp((progress-0.55)/0.3))
    if tip>0:
        d.text((280,680), "Keep status rules next to the status.", font=font(FONT_REG,30), fill=mix(BG,MUTED,tip))
    return img.convert("RGB")

def render_vs_string(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Enum vs String", font=font(FONT_SERIF,46), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,200,900,860], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,RED,left), width=4)
        d.text((220,280), "String", font=font(FONT_BOLD,40), fill=mix(BG,RED,left))
        for i,line in enumerate(["typos compile","invalid states","painful refactors"]):
            d.text((220,420+i*90), f"•  {line}", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
    if right>0:
        d.rounded_rectangle([1020,200,1780,860], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,GREEN,right), width=4)
        d.text((1100,280), "Enum", font=font(FONT_BOLD,40), fill=mix(BG,GREEN,right))
        for i,line in enumerate(["type-safe","switch-friendly","behavior allowed"]):
            d.text((1100,420+i*90), f"•  {line}", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
    return img.convert("RGB")

def render_enumset(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "EnumSet", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,780], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    d.text((280,340), "EnumSet.of(READ, WRITE)", font=font(FONT_MONO,36), fill=mix(BG,WHITE,a))
    d.text((280,480), "fast · compact · type-safe flags", font=font(FONT_REG,30), fill=mix(BG,MUTED,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Stringly typed statuses","Use enums for fixed vocabularies"),("02","Persisting ordinal", "Prefer name / explicit code"),("03","Volatile config in enums","Use data, not constants")]
    for i,(num,wrong,right) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.2)/0.35))
        if a<=0: continue
        y=180+i*240
        d.rounded_rectangle([200,y,1720,y+200], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,RED,a*0.7), width=2)
        d.text((260,y+40), num, font=font(FONT_SERIF,40), fill=mix(BG,ORANGE,a))
        d.text((360,y+45), wrong, font=font(FONT_BOLD,30), fill=mix(BG,RED,a))
        d.text((360,y+110), right, font=font(FONT_REG,28), fill=mix(BG,GREEN,a))
    return img.convert("RGB")

def render_interview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Interview Question", font=font(FONT_SERIF,44), fill=WHITE)
    d.rounded_rectangle([160,150,1760,280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q="Why enums instead of string constants?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,32)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,32),fill=WHITE)
    answers=[("Type safety","illegal states harder",ORANGE),("Switch","exhaustive finite cases",BLUE),("Persist","prefer name, not ordinal",GREEN)]
    for i,(k,v,col) in enumerate(answers):
        a=ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a<=0: continue
        y=360+i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45),k,font=font(FONT_BOLD,34),fill=mix(BG,col,a))
        d.text((700,y+50),v,font=font(FONT_REG,28),fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120,200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title="Wrappers & Autoboxing"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,52))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,52), fill=WHITE)
    sub="Integer · null · hidden allocation"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 14", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "basics": render_basics, "behavior": render_behavior, "vs_string": render_vs_string, "enumset": render_enumset, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 13...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep13_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep13.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep13_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)], check=True)
    dur = probe(narrated)
    pace = min(dur / 295.0, 1.12) if dur > 300 else (max(dur / 260.0, 0.88) if dur < 255 else 1.0)
    music = AUDIO / "music_bed.m4a"; generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep13_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_13_Enums.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_13.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_13_Enums_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep13_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [("00:00:12","01_hook"),("00:00:50","02_anatomy"),("00:01:40","03_signature"),("00:02:30","04_design"),("00:03:20","05_interview")]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 13: {final_dur/60:.2f} min")
    assert 190 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
