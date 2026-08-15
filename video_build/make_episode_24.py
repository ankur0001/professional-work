#!/usr/bin/env python3
"""Episode 24 — Queues and Deques. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep24", ROOT / "frames_ep24", ROOT / "clips_ep24"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Maps associate. Queues sequence work over time.',
        'First in, first out — producers and consumers meet in the middle.',
        'Deque goes further — both ends open for stacks and queues.',
        'ArrayDeque. PriorityQueue. Knowing the failure modes of offer versus add.',
        'Today — waiting lines with explicit rules.',
        'Order of arrival — or order of priority. Choose deliberately.',
    ]),
    ("title", "title", [
        'Episode Twenty-Four.',
        'Queues and Deques — flow structures.',
    ]),
    ("queue", "queue", [
        'Queue models a waiting line.',
        'Insert at the tail. Remove from the head.',
        'offer and poll return special values on failure.',
        'add and remove throw when the operation cannot proceed.',
        'peek inspects without removing — element is the throwing twin.',
        'Pick the style that matches capacity constraints and call-site clarity.',
    ]),
    ("exception", "exception", [
        'Remember the paired APIs.',
        'Special-value methods suit bounded buffers and optional work.',
        'Exception methods suit invariants — failure should be loud.',
        'Mixing them casually makes empty-queue bugs harder to read.',
        'Document which style your module uses.',
        'Consistency beats cleverness at the call site.',
    ]),
    ("deque", "deque", [
        'Deque means double-ended queue.',
        'Add and remove at head or tail.',
        'That makes Deque a clean stack — push and pop at one end.',
        'It also makes a clean queue — offer last, poll first.',
        'One interface, two classic structures, fewer legacy types.',
        'Prefer Deque over the old Stack class in new code.',
    ]),
    ("arraydeque", "arraydeque", [
        'ArrayDeque is the usual workhorse.',
        'Resizable array — no capacity restriction by default.',
        'Faster than Stack for stack operations in typical cases.',
        'Often faster than LinkedList as a FIFO queue.',
        'Null elements are not allowed — fail fast on null offer.',
        'For single-threaded queues and stacks, start with ArrayDeque.',
    ]),
    ("priority", "priority", [
        'PriorityQueue breaks FIFO on purpose.',
        'The next element is the least — by natural order or Comparator.',
        'Under the hood it is a heap — peek is cheap, arbitrary index access is not.',
        'Iteration order is not sorted order — do not be fooled.',
        'Great for schedulers and best-next algorithms.',
        'Wrong when you needed a fair waiting line.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — using java.util.Stack in new code.',
        'Two — ignoring whether your queue is bounded when choosing add versus offer.',
        'Three — defaulting to LinkedList as a queue without measuring.',
        'Also — treating PriorityQueue iteration as sorted output.',
        'Queues are simple. Semantics are the whole game.',
    ]),
    ("interview", "interview", [
        'Interview question — Queue versus Deque, and why ArrayDeque?',
        'Queue — FIFO waiting line with paired success and failure APIs.',
        'Deque — both ends, covers stack and queue roles.',
        'ArrayDeque — fast general-purpose implementation for single-threaded use.',
        'Mention PriorityQueue when ordering is by priority, not arrival.',
        'That answer shows API judgment.',
    ]),
    ("teaser", "teaser", [
        'Flow structures are clear. Next — how collections decide order.',
        'Episode Twenty-Five — Sorting and Comparators.',
        'Comparable, Comparator, and stable sort expectations.',
        'See you there.',
    ]),
]



def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Waiting lines with rules"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,48))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,48), fill=WHITE)
    for i,lab in enumerate(["1","2","3","4","5"]):
        a=ease_out_cubic(clamp((progress-i*0.1)/0.28))
        if a<=0: continue
        x=180+i*340
        d.rounded_rectangle([x,420,x+280,700], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE if i==0 else BLUE,a), width=3)
        d.text((x+110,520), lab, font=font(FONT_SERIF,48), fill=mix(BG,WHITE,a))
    a=ease_out_cubic(clamp((progress-0.6)/0.3))
    if a>0:
        d.text((200,780), "offer → … → poll", font=font(FONT_MONO,30), fill=mix(BG,GREEN,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(260*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 24", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Queues & Deques", font(FONT_SERIF,64), H//2-30, mix(BG,WHITE,a)),
        ("FIFO · stacks · ArrayDeque", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_queue(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Queue Contract", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("offer / add","insert at tail",ORANGE),("poll / remove","take from head",BLUE),("peek / element","inspect head",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_exception(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Two Styles of Failure", font=font(FONT_SERIF,46), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,220,900,820], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,GREEN,left), width=4)
        d.text((220,300), "Special value", font=font(FONT_BOLD,34), fill=mix(BG,GREEN,left))
        d.text((220,450), "offer → false", font=font(FONT_MONO,28), fill=mix(BG,WHITE,left))
        d.text((220,530), "poll → null", font=font(FONT_MONO,28), fill=mix(BG,WHITE,left))
        d.text((220,610), "peek → null", font=font(FONT_MONO,28), fill=mix(BG,WHITE,left))
    if right>0:
        d.rounded_rectangle([1020,220,1780,820], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,RED,right), width=4)
        d.text((1100,300), "Exception", font=font(FONT_BOLD,34), fill=mix(BG,RED,right))
        d.text((1100,450), "add → throws", font=font(FONT_MONO,28), fill=mix(BG,WHITE,right))
        d.text((1100,530), "remove → throws", font=font(FONT_MONO,28), fill=mix(BG,WHITE,right))
        d.text((1100,610), "element → throws", font=font(FONT_MONO,28), fill=mix(BG,WHITE,right))
    return img.convert("RGB")

def render_deque(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Deque — two ends", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.35))
    d.rounded_rectangle([200,300,1720,700], radius=18, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=4)
    d.text((280,420), "head", font=font(FONT_BOLD,30), fill=mix(BG,GREEN,a))
    d.text((860,420), "……", font=font(FONT_BOLD,30), fill=mix(BG,MUTED,a))
    d.text((1480,420), "tail", font=font(FONT_BOLD,30), fill=mix(BG,BLUE,a))
    d.text((280,560), "stack or queue with one type", font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_arraydeque(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "ArrayDeque", font=font(FONT_SERIF,48), fill=WHITE)
    rows=[("Faster stack than Stack","use Deque API",ORANGE),("Faster queue than LinkedList","for many workloads",GREEN),("No capacity restrictions","resizes as needed",BLUE)]
    for i,(k,v,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,32), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_priority(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "PriorityQueue", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,800], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    lines=["Not FIFO — best-next by ordering","Comparable or Comparator required","Heap under the hood — peek is cheapest"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        d.text((320,360+i*120), line, font=font(FONT_REG,32), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Using Stack class","Prefer ArrayDeque as stack"),("02","Ignoring offer vs add","Match capacity semantics"),("03","LinkedList as default queue","Benchmark ArrayDeque first")]
    for i,(num,wrong,right) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.2)/0.35))
        if a<=0: continue
        y=180+i*240
        d.rounded_rectangle([200,y,1720,y+200], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,RED,a*0.7), width=2)
        d.text((260,y+40), num, font=font(FONT_SERIF,40), fill=mix(BG,ORANGE,a))
        d.text((360,y+45), wrong, font=font(FONT_BOLD,28), fill=mix(BG,RED,a))
        d.text((360,y+110), right, font=font(FONT_REG,28), fill=mix(BG,GREEN,a))
    return img.convert("RGB")

def render_interview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Interview Question", font=font(FONT_SERIF,44), fill=WHITE)
    d.rounded_rectangle([160,150,1760,280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q="Queue vs Deque — and why ArrayDeque?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,30)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,30),fill=WHITE)
    answers=[("Queue","FIFO producer/consumer",ORANGE),("Deque","both ends / stack+queue",BLUE),("ArrayDeque","fast general-purpose choice",GREEN)]
    for i,(k,v,col) in enumerate(answers):
        a=ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a<=0: continue
        y=360+i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45),k,font=font(FONT_BOLD,32),fill=mix(BG,col,a))
        d.text((700,y+50),v,font=font(FONT_REG,28),fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120,200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title="Sorting & Comparators"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,54))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,54), fill=WHITE)
    sub="Comparable · Comparator · stable order"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 25", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "queue": render_queue, "exception": render_exception, "deque": render_deque, "arraydeque": render_arraydeque, "priority": render_priority, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 24...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep24_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep24.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep24_narrated.mp4"
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
        paced = OUTPUT / "java_ep24_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_24_Queues_Deques.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_24.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_24_Queues_Deques_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep24_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_queue'), ('00:01:40', '03_deque'), ('00:02:30', '04_priority'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 24: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
