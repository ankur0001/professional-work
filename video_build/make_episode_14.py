#!/usr/bin/env python3
"""Episode 14 — Wrappers and Autoboxing. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep14", ROOT / "frames_ep14", ROOT / "clips_ep14"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        "Enums gave us type-safe states. Now look at numbers as objects.",
        "int is a primitive. Integer is a wrapper — an object that can be null.",
        "Autoboxing hides the conversion — and can hide costs and crashes.",
        "Today we make that invisible work visible.",
        "Get this mental model right — collections depend on it.",
        "Lists and maps need objects — wrappers bridge that gap.",
    ]),
    ("title", "title", [
        "Episode Fourteen.",
        "Wrappers and Autoboxing — objects around primitives.",
    ]),
    ("pairs", "pairs", [
        "Eight primitives. Eight wrappers.",
        "int and Integer. long and Long. boolean and Boolean.",
        "Wrappers live on the heap. They have identity. They can be null.",
        "Primitives cannot be null — and that alone prevents many bugs.",
        "Choose intentionally — do not default to wrappers everywhere.",
        "Default to primitives unless nullability is required.",
    ]),
    ("autobox", "autobox", [
        "Autoboxing converts automatically.",
        "Integer x equals ten — boxes the int.",
        "int y equals x — unboxes the Integer.",
        "Convenient in Lists and Maps that need objects.",
        "Dangerous when x is null — unboxing throws NullPointerException.",
        "Null plus silent conversion is a classic production trap.",
    ]),
    ("cost", "cost", [
        "Wrappers cost more than primitives.",
        "Object header. Indirection. Extra allocations.",
        "A List of Integer can thrash the heap versus an int array.",
        "Hot loops that box every iteration pay a quiet tax.",
        "Prefer primitives in hot paths. Use wrappers when null is a real signal.",
        "Measure before you box every number in a tight loop.",
    ]),
    ("cache", "cache", [
        "One more quirk — Integer caching.",
        "Small values are often cached — so equals-equals may look true by accident.",
        "Do not rely on that. Compare wrappers with equals.",
        "Autoboxing is not a reason to forget object equality rules.",
        "Be explicit — always.",
    ]),
    ("mistakes", "mistakes", [
        "Three common mistakes.",
        "One — unboxing a null wrapper into a primitive.",
        "Two — using wrappers in hot numeric loops without need.",
        "Three — comparing wrappers with equals-equals.",
        "Also — Boolean in conditions without null checks.",
        "Nullability is a feature — treat it like one.",
    ]),
    ("interview", "interview", [
        "Interview question — primitive versus wrapper?",
        "Primitive — value, non-null, compact, fast.",
        "Wrapper — object, nullable, overhead, autoboxing risk.",
        "Then mention NullPointerException on unboxing.",
        "That lands the production-level detail.",
        "Interviewers listen for null and allocation awareness.",
    ]),
    ("teaser", "teaser", [
        "Objects around values. Next — type-safe containers.",
        "Episode Fifteen — generics.",
        "List of Order — compile-time safety without casts.",
        "See you there.",
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Primitive ↔ Object"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,52))
    d.text(((W-(bbox[2]-bbox[0]))//2, 140), title, font=font(FONT_SERIF,52), fill=WHITE)
    for i,(lab,col) in enumerate([("int",ORANGE),("↔",MUTED),("Integer",BLUE)]):
        a=ease_out_cubic(clamp((progress-i*0.2)/0.35))
        if a<=0: continue
        x=360+i*380
        d.rounded_rectangle([x,420,x+320,680], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+70,520), lab, font=font(FONT_MONO_B,36), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 14", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Wrappers & Autoboxing", font(FONT_SERIF,56), H//2-30, mix(BG,WHITE,a)),
        ("null · allocation · equality traps", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_pairs(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Primitive / Wrapper", font=font(FONT_SERIF,46), fill=WHITE)
    pairs=[("int","Integer"),("long","Long"),("boolean","Boolean"),("double","Double")]
    for i,(p,w) in enumerate(pairs):
        a=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        if a<=0: continue
        y=180+i*180
        d.rounded_rectangle([200,y,1720,y+150], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE if i%2==0 else BLUE,a), width=2)
        d.text((320,y+45), p, font=font(FONT_MONO_B,36), fill=mix(BG,ORANGE,a))
        d.text((900,y+45), w, font=font(FONT_MONO_B,36), fill=mix(BG,BLUE,a))
    return img.convert("RGB")

def render_autobox(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Autoboxing", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.35))
    d.rounded_rectangle([200,180,1720,420], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,GREEN,a), width=3)
    d.text((280,260), "Integer x = 10;   // boxes", font=font(FONT_MONO,34), fill=mix(BG,WHITE,a))
    d.text((280,340), "int y = x;        // unboxes", font=font(FONT_MONO,34), fill=mix(BG,WHITE,a))
    tip=ease_out_cubic(clamp((progress-0.45)/0.35))
    if tip>0:
        d.rounded_rectangle([200,500,1720,820], radius=16, fill=mix(BG,(40,18,18),tip), outline=mix(BG,RED,tip), width=3)
        d.text((280,620), "If x is null → unboxing NPE", font=font(FONT_BOLD,34), fill=mix(BG,WHITE,tip))
    return img.convert("RGB")

def render_cost(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Cost of Wrappers", font=font(FONT_SERIF,46), fill=WHITE)
    cards=[("int[]", "compact primitives", GREEN,0.1),("List<Integer>", "objects + boxing", ORANGE,0.4),("Hot loop", "avoid needless box/unbox", BLUE,0.7)]
    for i,(name,note,col,start) in enumerate(cards):
        a=ease_out_cubic(clamp((progress-start)/0.3))
        if a<=0: continue
        y=200+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), name, font=font(FONT_MONO_B,34), fill=mix(BG,col,a))
        d.text((280,y+100), note, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_cache(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Cache Quirk", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,240,1720,780], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    d.text((280,360), "Integer a = 100; Integer b = 100;", font=font(FONT_MONO,30), fill=mix(BG,WHITE,a))
    d.text((280,480), "a == b may be true  (cached)", font=font(FONT_REG,30), fill=mix(BG,MUTED,a))
    d.text((280,600), "Still use equals — never rely on ==" , font=font(FONT_BOLD,30), fill=mix(BG,GREEN,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Unboxing null wrappers","Check null / use primitives"),("02","Boxing in hot loops","Prefer primitive arrays"),("03","== on wrappers","Use equals()")]
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
    q="Primitive vs wrapper — what's the difference?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,32)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,32),fill=WHITE)
    answers=[("Primitive","value · non-null · fast",ORANGE),("Wrapper","object · nullable · overhead",BLUE),("Risk","NPE on unboxing",GREEN)]
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
    title="Generics"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,72))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,72), fill=WHITE)
    sub="List<Order> · type parameters · erasure"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 15", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "pairs": render_pairs, "autobox": render_autobox, "cost": render_cost, "cache": render_cache, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 14...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep14_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep14.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep14_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)], check=True)
    dur = probe(narrated)
    pace = min(dur / 295.0, 1.12) if dur > 300 else (max(dur / 260.0, 0.88) if dur < 255 else 1.0)
    music = AUDIO / "music_bed.m4a"; generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep14_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_14_Wrappers_Autoboxing.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_14.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_14_Wrappers_Autoboxing_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep14_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [("00:00:12","01_hook"),("00:00:50","02_anatomy"),("00:01:40","03_signature"),("00:02:30","04_design"),("00:03:20","05_interview")]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 14: {final_dur/60:.2f} min")
    assert 190 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
