#!/usr/bin/env python3
"""Episode 22 — Sets. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep22", ROOT / "frames_ep22", ROOT / "clips_ep22"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Lists keep order and duplicates. Sets answer a different question.',
        'Is this value already in the collection — yes or no?',
        'Uniqueness is the product. Membership is the verb.',
        'HashSet. LinkedHashSet. TreeSet. Same contract — different trade-offs.',
        'Today we pick the right Set for the job.',
        'One of each — with rules you must respect.',
    ]),
    ("title", "title", [
        'Episode Twenty-Two.',
        'Sets — uniqueness in java.util.',
    ]),
    ("contract", "contract", [
        'Set is a Collection that forbids duplicates.',
        'Whether two elements collide is decided by equals — not by ==.',
        'There is no get by index. You ask contains.',
        'Iteration order depends on the implementation you chose.',
        'Prefer the Set interface in APIs until performance forces a concrete type.',
        'Model membership. Do not pretend it is a list.',
    ]),
    ("hashset", "hashset", [
        'HashSet is the default for most uniqueness needs.',
        'It uses hashing for average constant-time add, remove, and contains.',
        'Do not rely on iteration order — it is not a feature.',
        'Your element type must honor equals and hashCode together.',
        'Mutable fields that participate in equals make sets unstable.',
        'For fast membership tests, start with HashSet.',
    ]),
    ("ordered", "ordered", [
        'When order matters, reach for a sibling.',
        'LinkedHashSet preserves insertion order while keeping hash performance.',
        'TreeSet keeps elements sorted — natural order or a Comparator.',
        'Tree operations are logarithmic — fine, until you pretend they are free.',
        'Need sorted ranges or first and last — TreeSet earns its keep.',
        'Need stable encounter order — LinkedHashSet is cleaner than sorting later.',
    ]),
    ("equals", "equals", [
        'The silent dependency — equals and hashCode.',
        'If two objects are equal, their hash codes must match.',
        'Break that contract and HashSet will lose or duplicate your data.',
        'TreeSet uses compareTo or a Comparator — consistency with equals still matters.',
        'Immutable value types make safer set elements.',
        'Identity is a design decision. Sets enforce it ruthlessly.',
    ]),
    ("choose", "choose", [
        'How to choose.',
        'Pure membership, order irrelevant — HashSet.',
        'Need predictable iteration in insertion order — LinkedHashSet.',
        'Need sorted traversal or range queries — TreeSet.',
        'Set.of gives an unmodifiable set — great for constants.',
        'Choose for access pattern, not for how advanced the class name sounds.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — putting mutable objects in a HashSet, then mutating their keys.',
        'Two — implementing equals without hashCode — or the reverse.',
        'Three — using TreeSet with types that have no natural ordering.',
        'Also — expecting HashSet iteration to stay stable across JVMs.',
        'Sets are simple. Contracts are not optional.',
    ]),
    ("interview", "interview", [
        'Interview question — HashSet versus LinkedHashSet versus TreeSet?',
        'HashSet — fastest typical membership, no order guarantees.',
        'LinkedHashSet — hash performance with insertion-order iteration.',
        'TreeSet — sorted, logarithmic, needs ordering rules.',
        'Mention equals and hashCode — interviewers listen for that.',
        'That answer shows judgment, not memorization.',
    ]),
    ("teaser", "teaser", [
        'Uniqueness is clear. Next — associating keys with values.',
        'Episode Twenty-Three — Maps.',
        'HashMap realities, ordering variants, and null rules.',
        'See you there.',
    ]),
]



def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Uniqueness with rules"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,50))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,50), fill=WHITE)
    vals = ["A", "B", "A", "C", "B"]
    for i, v in enumerate(vals):
        a=ease_out_cubic(clamp((progress-i*0.08)/0.25))
        if a<=0: continue
        x=160+i*340
        col = RED if vals[:i+1].count(v)>1 and progress>0.45 else ORANGE
        d.rounded_rectangle([x,400,x+280,700], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+105,520), v, font=font(FONT_SERIF,48), fill=mix(BG,WHITE,a))
    note=ease_out_cubic(clamp((progress-0.55)/0.3))
    if note>0:
        d.text((W//2-220, 780), "Set keeps one of each", font=font(FONT_REG,28), fill=mix(BG,GREEN,note))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 22", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Sets", font(FONT_SERIF,76), H//2-30, mix(BG,WHITE,a)),
        ("uniqueness · hashing · order variants", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_contract(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Set Contract", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("no duplicates","equals decides sameness",ORANGE),("unordered by default","iteration order not positional",BLUE),("membership focus","contains / add / remove",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_hashset(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "HashSet", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.35))
    d.rounded_rectangle([160,200,1760,400], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    d.text((240,270), "hashCode buckets  ·  fast contains  ·  no guaranteed order", font=font(FONT_REG,30), fill=mix(BG,WHITE,a))
    for i,lab in enumerate(["h0","h1","h2","h3"]):
        aa=ease_out_cubic(clamp((progress-0.25-i*0.1)/0.25))
        if aa<=0: continue
        x=220+i*420
        d.rounded_rectangle([x,500,x+340,820], radius=12, fill=mix(BG,SURFACE,aa), outline=mix(BG,BLUE,aa), width=2)
        d.text((x+110,620), lab, font=font(FONT_MONO_B,36), fill=mix(BG,BLUE,aa))
    return img.convert("RGB")

def render_ordered(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "When Order Matters", font=font(FONT_SERIF,46), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,220,900,820], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,GREEN,left), width=4)
        d.text((200,300), "LinkedHashSet", font=font(FONT_BOLD,34), fill=mix(BG,GREEN,left))
        d.text((200,420), "insertion order", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
        d.text((200,500), "stable iteration", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
        d.text((200,580), "hash speed + order", font=font(FONT_REG,28), fill=mix(BG,MUTED,left))
    if right>0:
        d.rounded_rectangle([1020,220,1780,820], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,ORANGE,right), width=4)
        d.text((1100,300), "TreeSet", font=font(FONT_BOLD,34), fill=mix(BG,ORANGE,right))
        d.text((1100,420), "sorted order", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
        d.text((1100,500), "Comparable / Comparator", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
        d.text((1100,580), "log n operations", font=font(FONT_REG,28), fill=mix(BG,MUTED,right))
    return img.convert("RGB")

def render_equals(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "equals & hashCode", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,800], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    lines=["If a.equals(b) is true,","hashCode must match.","Break that — HashSet lies."]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        d.text((320,340+i*120), line, font=font(FONT_REG if i else FONT_BOLD,34), fill=mix(BG,RED if i==2 else WHITE, aa))
    return img.convert("RGB")

def render_choose(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "How to Choose", font=font(FONT_SERIF,48), fill=WHITE)
    rows=[("HashSet","fast membership, order irrelevant",ORANGE),("LinkedHashSet","need insertion-order iteration",GREEN),("TreeSet","need sorted / range views",BLUE)]
    for i,(k,v,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=200+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Mutable keys in a set","Freeze identity fields"),("02","Broken hashCode/equals","Contract or chaos"),("03","TreeSet without ordering","Implement Comparable")]
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
    q="HashSet vs LinkedHashSet vs TreeSet?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,32)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,32),fill=WHITE)
    answers=[("HashSet","O(1) membership, no order",ORANGE),("LinkedHashSet","hash + insertion order",GREEN),("TreeSet","sorted, log n",BLUE)]
    for i,(k,v,col) in enumerate(answers):
        a=ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a<=0: continue
        y=360+i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45),k,font=font(FONT_BOLD,32),fill=mix(BG,col,a))
        d.text((780,y+50),v,font=font(FONT_REG,28),fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120,200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title="Maps"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,72))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,72), fill=WHITE)
    sub="keys · values · HashMap realities"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 23", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "contract": render_contract, "hashset": render_hashset, "ordered": render_ordered, "equals": render_equals, "choose": render_choose, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 22...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep22_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep22.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep22_narrated.mp4"
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
        paced = OUTPUT / "java_ep22_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_22_Sets.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_22.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_22_Sets_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep22_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_hashset'), ('00:01:40', '03_ordered'), ('00:02:30', '04_equals'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 22: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
