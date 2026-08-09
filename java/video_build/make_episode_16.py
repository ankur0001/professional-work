#!/usr/bin/env python3
"""Episode 16 — Annotations. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep16", ROOT / "frames_ep16", ROOT / "clips_ep16"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        "Generics typed our containers. Annotations label our code.",
        "An annotation is metadata — information about the code, attached to the code.",
        "Override. Deprecated. Spring markers. Validation rules.",
        "Tiny symbols. Huge framework power.",
        "Today we learn what annotations are — and what they are not.",
        "Angle brackets were contracts. At-signs are signals.",
    ]),
    ("title", "title", [
        "Episode Sixteen.",
        "Annotations — metadata that frameworks and compilers read.",
    ]),
    ("what", "what", [
        "An annotation starts with an at-sign.",
        "It can mark a class, a method, a field, a parameter — even another annotation.",
        "By itself, most annotations do nothing magical at runtime.",
        "Something must read them — the compiler, a tool, or a framework.",
        "Think of them as sticky notes with structure.",
        "The note matters only if someone looks.",
    ]),
    ("builtin", "builtin", [
        "Start with built-ins you already use.",
        "Override — catch signature mistakes when you think you are overriding.",
        "Deprecated — warn callers that an API is going away.",
        "SuppressWarnings — silence a warning you have consciously accepted.",
        "FunctionalInterface — document a single abstract method type.",
        "These are small, precise, and compile-time friendly.",
    ]),
    ("retention", "retention", [
        "Retention answers — how long does this annotation live?",
        "Source — only in source. Gone after compile.",
        "Class — in the class file. Not necessarily visible at runtime.",
        "Runtime — readable through reflection while the program runs.",
        "Spring and many frameworks need runtime retention.",
        "If retention is wrong, your marker is invisible when it matters.",
    ]),
    ("spring", "spring", [
        "In Spring, annotations drive wiring.",
        "SpringBootApplication. RestController. Service. Autowired.",
        "They tell the framework what to scan, create, and inject.",
        "That is powerful — and easy to overuse.",
        "Prefer clear boundaries. Do not decorate every line into a mystery.",
        "Annotations should clarify intent — not hide architecture.",
    ]),
    ("custom", "custom", [
        "You can define your own annotations.",
        "Declare an interface with an at-sign — interface RoleRequired.",
        "Add retention and target so tools know where it applies.",
        "Then write a processor or runtime check that enforces it.",
        "Without a reader, a custom annotation is just documentation in disguise.",
        "Design the annotation and the enforcement together.",
    ]),
    ("mistakes", "mistakes", [
        "Three common mistakes.",
        "One — assuming an annotation does work with no processor behind it.",
        "Two — wrong retention — runtime framework never sees your marker.",
        "Three — annotation soup — so many markers the real flow disappears.",
        "Also — using SuppressWarnings to hide problems instead of fixing types.",
        "Annotations amplify discipline. They do not replace it.",
    ]),
    ("interview", "interview", [
        "Interview question — what is an annotation in Java?",
        "Structured metadata attached to code elements.",
        "Useful when compilers, tools, or frameworks read it.",
        "Mention retention — source, class, runtime.",
        "Then give Override versus a Spring stereotype as examples.",
        "That answer covers language and ecosystem.",
    ]),
    ("teaser", "teaser", [
        "Metadata is clear. Next — looking inside types at runtime.",
        "Episode Seventeen — reflection.",
        "Inspect classes, call methods, and know the costs.",
        "See you there.",
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Metadata on code"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,52))
    d.text(((W-(bbox[2]-bbox[0]))//2, 140), title, font=font(FONT_SERIF,52), fill=WHITE)
    for i,(lab,col) in enumerate([("@Override",ORANGE),("@Service",BLUE),("@Deprecated",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.35))
        if a<=0: continue
        x=260+i*500
        d.rounded_rectangle([x,420,x+440,700], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=4)
        d.text((x+60,520), lab, font=font(FONT_MONO_B,32), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 16", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Annotations", font(FONT_SERIF,72), H//2-30, mix(BG,WHITE,a)),
        ("metadata · retention · frameworks", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_what(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "What Is an Annotation?", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([220,220,1700,820], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    lines=["@Target(METHOD)","@Retention(RUNTIME)","public @interface Audited { }"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.15)/0.35))
        d.text((340,340+i*120), line, font=font(FONT_MONO,34), fill=mix(BG,WHITE if i<2 else GREEN, aa))
    return img.convert("RGB")

def render_builtin(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Built-in Annotations", font=font(FONT_SERIF,46), fill=WHITE)
    items=[("@Override","catch wrong signatures",ORANGE),("@Deprecated","warn API consumers",BLUE),("@SuppressWarnings","conscious silence",GREEN),("@FunctionalInterface","SAM contract",MUTED)]
    for i,(name,note,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        if a<=0: continue
        y=170+i*180
        d.rounded_rectangle([200,y,1720,y+150], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=2)
        d.text((260,y+45), name, font=font(FONT_MONO_B,32), fill=mix(BG,col,a))
        d.text((900,y+50), note, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_retention(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Retention Policy", font=font(FONT_SERIF,46), fill=WHITE)
    rows=[("SOURCE","discard after compile",ORANGE),("CLASS","in bytecode",BLUE),("RUNTIME","visible via reflection",GREEN)]
    for i,(name,note,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.2)/0.3))
        if a<=0: continue
        x=160+i*560
        d.rounded_rectangle([x,280,x+520,780], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+60,400), name, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((x+60,520), note, font=font(FONT_REG,26), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_spring(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Framework Markers", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,200,1720,780], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    for i,line in enumerate(["@SpringBootApplication","@RestController","@Service","@Autowired"]):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.3))
        d.text((360,280+i*110), line, font=font(FONT_MONO,34), fill=mix(BG,ORANGE if i==0 else WHITE, aa))
    return img.convert("RGB")

def render_custom(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Custom Annotations", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,780], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,GREEN,a), width=3)
    d.text((300,340), "@Retention(RUNTIME)", font=font(FONT_MONO,32), fill=mix(BG,MUTED,a))
    d.text((300,440), "public @interface RoleRequired {", font=font(FONT_MONO,32), fill=mix(BG,WHITE,a))
    d.text((340,540), "String value();", font=font(FONT_MONO,32), fill=mix(BG,ORANGE,a))
    d.text((300,640), "}", font=font(FONT_MONO,32), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Annotation with no reader","Pair marker + enforcement"),("02","Wrong retention","RUNTIME when frameworks need it"),("03","Annotation soup","Keep intent readable")]
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
    q="What is an annotation in Java?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,34)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,34),fill=WHITE)
    answers=[("Metadata","structured notes on code",ORANGE),("Readers","compiler / tools / frameworks",BLUE),("Retention","SOURCE · CLASS · RUNTIME",GREEN)]
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
    title="Reflection"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,72))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,72), fill=WHITE)
    sub="inspect · invoke · know the cost"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 17", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "what": render_what, "builtin": render_builtin, "retention": render_retention, "spring": render_spring, "custom": render_custom, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 16...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep16_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep16.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep16_narrated.mp4"
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
        paced = OUTPUT / "java_ep16_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_16_Annotations.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_16.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_16_Annotations_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep16_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [("00:00:12","01_hook"),("00:00:50","02_anatomy"),("00:01:40","03_signature"),("00:02:30","04_design"),("00:03:20","05_interview")]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 16: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
