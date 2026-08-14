#!/usr/bin/env python3
"""Episode 36 — Threads Introduction. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep36", ROOT / "frames_ep36", ROOT / "clips_ep36"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'One CPU core can only do one thing at a time — unless you switch fast enough.',
        'Threads let a program do multiple tasks concurrently within one process.',
        'Download a file while updating the UI. Process requests while logging metrics.',
        'Concurrency is about structure — parallelism is about simultaneous execution.',
        'Threads share memory — powerful, but dangerous without coordination.',
        'Today — the thread model in Java and how to start your first concurrent task.',
    ]),
    ("title", "title", [
        'Episode Thirty-Six.',
        'Threads Introduction — concurrency in Java.',
    ]),
    ("thread", "thread", [
        'A Thread is a lightweight unit of execution inside a JVM process.',
        'The JVM maps Java threads to OS threads — one-to-one on most platforms.',
        'Every Java program starts with a main thread — the one running main.',
        'Creating more threads lets work proceed on separate call stacks.',
        'Threads share the heap — instance fields are visible across threads.',
        'Each thread has its own stack — local variables are thread-confined.',
    ]),
    ("runnable", "runnable", [
        'Runnable is a functional interface — void run with no arguments.',
        'Pass a Runnable to a Thread constructor, then call start.',
        'Callable is like Runnable but returns a value and can throw.',
        'ExecutorService is the modern way — submit tasks to a thread pool.',
        'Prefer Runnable lambdas over subclassing Thread directly.',
        'Separate task logic from thread management.',
    ]),
    ("lifecycle", "lifecycle", [
        'Thread states — NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.',
        'NEW until start is called — then RUNNABLE when eligible to run.',
        'BLOCKED waiting for a monitor lock. WAITING until notified.',
        'The scheduler decides which RUNNABLE thread runs on which core.',
        'You do not control scheduling — design for unpredictability.',
        'Understanding states helps you debug stuck and starving threads.',
    ]),
    ("starting", "starting", [
        'Never call run directly — that executes on the current thread.',
        'Call start to launch a new thread that invokes run.',
        'join waits for another thread to finish — useful for coordination.',
        'sleep pauses the current thread for a duration — does not release locks.',
        'yield hints the scheduler to let other threads run — rarely needed.',
        'Start threads deliberately — unbounded thread creation exhausts memory.',
    ]),
    ("shared", "shared", [
        'Threads share the heap — all threads see the same object fields.',
        'Local variables live on each thread stack — no sharing by default.',
        'Mutable shared state without coordination causes race conditions.',
        'Two threads reading and writing the same field — unpredictable results.',
        'Visibility matters — changes by one thread may not be seen by another.',
        'Shared memory is the reason synchronization exists — next episode.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — calling run instead of start — no new thread created.',
        'Two — sharing mutable state without synchronization — race conditions.',
        'Three — spawning unlimited threads — one per request does not scale.',
        'Also — assuming operations are atomic when they are not — count plus plus.',
        'Concurrency bugs are intermittent — design defensively from the start.',
    ]),
    ("interview", "interview", [
        'Interview question — start versus run on a Thread?',
        'start creates a new thread and schedules run on it.',
        'run called directly — executes synchronously on the caller thread.',
        'Mention Runnable, shared heap, and thread-local stacks.',
        'Note race conditions when sharing mutable state.',
        'That answer opens the door to synchronization next episode.',
    ]),
    ("teaser", "teaser", [
        'Threads share memory. Next — making that safe.',
        'Episode Thirty-Seven — Synchronization.',
        'synchronized, locks, and coordinating access to shared data.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Many tasks, one program"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,50))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,50), fill=WHITE)
    for i,(lab,col) in enumerate([("main",ORANGE),("thread-1",BLUE),("thread-2",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        x=280+i*520
        d.rounded_rectangle([x,400,x+420,720], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+90,520), lab, font=font(FONT_BOLD,28), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 36", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Threads Intro", font(FONT_SERIF,62), H//2-30, mix(BG,WHITE,a)),
        ("Runnable · lifecycle · start()", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_thread(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "What Is a Thread?", font=font(FONT_SERIF,44), fill=WHITE)
    items=[("process","one JVM instance",ORANGE),("shared heap","instance fields visible",BLUE),("own stack","local vars per thread",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_runnable(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Runnable & Callable", font=font(FONT_SERIF,44), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    lines=["Runnable task = () -> doWork();","Thread t = new Thread(task);","t.start();  // not t.run()!","ExecutorService for thread pools"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((280,300+i*120), line, font=font(FONT_MONO,28), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_lifecycle(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Thread States", font=font(FONT_SERIF,46), fill=WHITE)
    states=[("NEW","before start()",ORANGE),("RUNNABLE","eligible to run",BLUE),("BLOCKED","waiting for lock",GREEN),("TERMINATED","finished",MUTED)]
    for i,(k,v,col) in enumerate(states):
        a=ease_out_cubic(clamp((progress-i*0.14)/0.28))
        if a<=0: continue
        x=160+i*420
        d.rounded_rectangle([x,280,x+380,680], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+40,380), k, font=font(FONT_BOLD,26), fill=mix(BG,col,a))
        d.text((x+30,460), v, font=font(FONT_REG,24), fill=mix(BG,WHITE,a))
        if i<3:
            d.text((x+390,420), "→", font=font(FONT_BOLD,32), fill=mix(BG,MUTED,a))
    return img.convert("RGB")

def render_starting(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Starting Threads", font=font(FONT_SERIF,46), fill=WHITE)
    items=[("start()","new thread runs run()",ORANGE),("join()","wait for completion",BLUE),("sleep()","pause current thread",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_MONO,32), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_shared(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Shared Memory", font=font(FONT_SERIF,46), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,220,900,820], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,ORANGE,left), width=4)
        d.text((220,280), "Heap (shared)", font=font(FONT_BOLD,32), fill=mix(BG,ORANGE,left))
        d.text((240,380), "instance fields", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
        d.text((240,460), "visible to all threads", font=font(FONT_MONO,26), fill=mix(BG,MUTED,left))
    if right>0:
        d.rounded_rectangle([1020,220,1780,820], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,BLUE,right), width=4)
        d.text((1100,280), "Stack (per thread)", font=font(FONT_BOLD,32), fill=mix(BG,BLUE,right))
        d.text((1120,380), "local variables", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
        d.text((1120,460), "thread-confined", font=font(FONT_MONO,26), fill=mix(BG,MUTED,right))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","call run() not start()","start() for new thread"),("02","unsynchronized shared state","race conditions"),("03","unbounded thread creation","use thread pools")]
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
    q="start() vs run() on Thread?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,32)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,32),fill=WHITE)
    answers=[("start()","new thread, async",ORANGE),("run()","sync on caller",BLUE),("shared","heap visible, stack local",GREEN)]
    for i,(k,v,col) in enumerate(answers):
        a=ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a<=0: continue
        y=360+i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45),k,font=font(FONT_BOLD,30),fill=mix(BG,col,a))
        d.text((780,y+50),v,font=font(FONT_REG,26),fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120,200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title="Synchronization"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,58))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,58), fill=WHITE)
    sub="synchronized · locks · safe sharing"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 37", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {"hook": render_hook, "title": render_title, "thread": render_thread, "runnable": render_runnable, "lifecycle": render_lifecycle, "starting": render_starting, "shared": render_shared, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 36...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep36_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep36.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep36_narrated.mp4"
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
        paced = OUTPUT / "java_ep36_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_36_Threads_Intro.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_36.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_36_Threads_Intro_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep36_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_thread'), ('00:01:40', '03_runnable'), ('00:02:30', '04_lifecycle'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 36: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
