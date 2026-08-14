#!/usr/bin/env python3
"""Episode 17 — Reflection. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep17", ROOT / "frames_ep17", ROOT / "clips_ep17"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        "Annotations are metadata. Reflection is how code reads the structure of types at runtime.",
        "Ask a class for its methods. Read fields. Create instances by name.",
        "Frameworks do this constantly — Spring, serializers, test tools.",
        "Powerful. Flexible. Easy to misuse.",
        "Today we open the hood — carefully.",
        "Know the tool. Respect the cost.",
    ]),
    ("title", "title", [
        "Episode Seventeen.",
        "Reflection — inspect and invoke types at runtime.",
    ]),
    ("basics", "basics", [
        "Start with Class.",
        "Order.class or order.getClass — you get a Class object.",
        "From there — getMethods, getFields, getConstructors.",
        "You can discover what a type offers without hardcoding every name.",
        "That discovery is the heart of reflective programming.",
        "Dynamic systems are built on this doorway.",
    ]),
    ("invoke", "invoke", [
        "Reflection can call methods too.",
        "Lookup a Method. Invoke it with arguments.",
        "You can even reach private members — with setAccessible.",
        "That breaks encapsulation walls — use it only with clear cause.",
        "Libraries may need it. Business code usually should not.",
        "If you reach for private access daily — redesign the API.",
    ]),
    ("frameworks", "frameworks", [
        "Why frameworks love reflection.",
        "Dependency injection scans annotations and constructs beans.",
        "JSON mappers bind properties without hand-written glue for every class.",
        "ORMs inspect entities and map tables.",
        "You get productivity — the platform pays with complexity.",
        "Understanding reflection makes those magic layers less magical.",
    ]),
    ("cost", "cost", [
        "Reflection is not free.",
        "Lookups are slower than direct calls.",
        "Security managers and modules can restrict access.",
        "Native images and Graal may need extra config for reflective use.",
        "Cache Method handles if you must reflect in a hot path.",
        "Prefer normal calls when the type is known at compile time.",
    ]),
    ("safety", "safety", [
        "Safety rules of thumb.",
        "Validate names and inputs — reflective calls can become injection surfaces.",
        "Do not suppress access checks casually in application code.",
        "Log clearly when reflective fallbacks run — they hide bugs.",
        "If a feature needs reflection, quarantine it behind a small module.",
        "Power without boundaries becomes an incident.",
    ]),
    ("mistakes", "mistakes", [
        "Three common mistakes.",
        "One — using reflection where an interface would do.",
        "Two — calling setAccessible everywhere and calling it fine.",
        "Three — ignoring performance until the profiler screams.",
        "Also — assuming field names are a stable public API.",
        "Reflect on purpose — not as a default style.",
    ]),
    ("interview", "interview", [
        "Interview question — what is reflection in Java?",
        "Runtime inspection and interaction with classes, methods, and fields.",
        "Used heavily by frameworks for wiring and mapping.",
        "Tradeoffs — flexibility versus speed, safety, and clarity.",
        "Mention modules and native-image constraints for senior signal.",
        "That answer balances power and caution.",
    ]),
    ("teaser", "teaser", [
        "We can inspect types. Next — a cleaner way to carry data.",
        "Episode Eighteen — records.",
        "Transparent data carriers with less boilerplate.",
        "See you there.",
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Look inside the type"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,50))
    d.text(((W-(bbox[2]-bbox[0]))//2, 140), title, font=font(FONT_SERIF,50), fill=WHITE)
    for i,(lab,col) in enumerate([("Class",ORANGE),("Method",BLUE),("Field",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.2)/0.35))
        if a<=0: continue
        x=300+i*440
        d.rounded_rectangle([x,420,x+380,700], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=4)
        d.text((x+90,520), lab, font=font(FONT_BOLD,36), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 17", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Reflection", font(FONT_SERIF,72), H//2-30, mix(BG,WHITE,a)),
        ("inspect · invoke · respect the cost", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_basics(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Class Objects", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,820], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    for i,line in enumerate(["Class<?> c = Order.class;","c.getMethods();","c.getDeclaredFields();","c.getConstructors();"]):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.3))
        d.text((320,300+i*110), line, font=font(FONT_MONO,32), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_invoke(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Invoke at Runtime", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,700], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    d.text((300,320), "Method m = c.getMethod(\"name\");", font=font(FONT_MONO,30), fill=mix(BG,WHITE,a))
    d.text((300,440), "m.invoke(instance, args);", font=font(FONT_MONO,30), fill=mix(BG,GREEN,a))
    tip=ease_out_cubic(clamp((progress-0.55)/0.3))
    if tip>0:
        d.text((300,820), "setAccessible breaks walls — use rarely.", font=font(FONT_REG,28), fill=mix(BG,RED,tip))
    return img.convert("RGB")

def render_frameworks(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Who Uses Reflection?", font=font(FONT_SERIF,46), fill=WHITE)
    items=[("DI / Spring","wire beans by type"),("JSON mappers","bind properties"),("ORMs","map entities"),("Tests","framework runners")]
    cols=[ORANGE,BLUE,GREEN,MUTED]
    for i,(name,note) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        if a<=0: continue
        x=160+(i%2)*880; y=180+(i//2)*340; col=cols[i]
        d.rounded_rectangle([x,y,x+800,y+280], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+50,y+80), name, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((x+50,y+160), note, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_cost(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Costs & Constraints", font=font(FONT_SERIF,46), fill=WHITE)
    rows=[("Slower than direct calls",ORANGE),("Access checks / modules",BLUE),("Native-image config needed",GREEN),("Cache Method handles if hot",MUTED)]
    for i,(note,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        if a<=0: continue
        y=180+i*180
        d.rounded_rectangle([200,y,1720,y+150], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=2)
        d.text((280,y+50), note, font=font(FONT_BOLD,30), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_safety(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Safety Rules", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    tips=["Validate names and inputs","Don't casually break encapsulation","Quarantine reflective code","Log reflective fallbacks"]
    for i,tip in enumerate(tips):
        aa=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        y=200+i*160
        d.rounded_rectangle([220,y,1700,y+130], radius=14, fill=mix(BG,SURFACE,aa), outline=mix(BG,ORANGE if i==0 else BLUE,aa), width=2)
        d.text((300,y+40), f"{i+1}.  {tip}", font=font(FONT_REG,30), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Reflection instead of interfaces","Model with types first"),("02","setAccessible everywhere","Redesign the API"),("03","Ignoring performance","Cache or avoid in hot paths")]
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
    q="What is reflection, and when should you use it?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,30)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,30),fill=WHITE)
    answers=[("What","runtime inspect/invoke members",ORANGE),("Where","frameworks, mappers, tools",BLUE),("Tradeoff","flexibility vs cost/safety",GREEN)]
    for i,(k,v,col) in enumerate(answers):
        a=ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a<=0: continue
        y=360+i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45),k,font=font(FONT_BOLD,34),fill=mix(BG,col,a))
        d.text((620,y+50),v,font=font(FONT_REG,28),fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120,200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title="Records"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,72))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,72), fill=WHITE)
    sub="data carriers · less boilerplate"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 18", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "basics": render_basics, "invoke": render_invoke, "frameworks": render_frameworks, "cost": render_cost, "safety": render_safety, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 17...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep17_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep17.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep17_narrated.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(narrated)], check=True)
    dur = probe(narrated)
    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 245:
        # stretch into ≥4:05 band
        pace = max(dur / 250.0, 0.85)
    music = AUDIO / "music_bed.m4a"; generate_music_bed(dur / pace + 2, music)
    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep17_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_17_Reflection.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_17.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_17_Reflection_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep17_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [("00:00:12","01_hook"),("00:00:50","02_anatomy"),("00:01:40","03_signature"),("00:02:30","04_design"),("00:03:20","05_interview")]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 17: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
