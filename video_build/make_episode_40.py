#!/usr/bin/env python3
"""Episode 40 — ExecutorService & Thread Pools. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep40", ROOT / "frames_ep40", ROOT / "clips_ep40"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Creating a new Thread per request does not scale — creation is expensive.',
        'Thread pools reuse a fixed set of worker threads for many tasks.',
        'ExecutorService is the standard abstraction for submitting work.',
        'Submit a Runnable, get back control — the pool handles scheduling.',
        'Shutdown gracefully — in-flight tasks deserve a clean finish.',
        'Today — ExecutorService, thread pools, and task submission.',
    ]),
    ("title", "title", [
        'Episode Forty.',
        'ExecutorService and Thread Pools.',
    ]),
    ("executor", "executor", [
        'ExecutorService decouples task submission from thread management.',
        'You describe what to run — the executor decides how and when.',
        'Factories in Executors create common pool configurations.',
        'newFixedThreadPool — bounded pool, unbounded queue.',
        'newCachedThreadPool — grows on demand, reclaims idle threads.',
        'Prefer factory methods — they encode sensible defaults.',
    ]),
    ("pool", "pool", [
        'A thread pool maintains a queue of tasks and a set of worker threads.',
        'Workers pull tasks from the queue and execute them.',
        'Bounded pools cap resource usage — critical for server applications.',
        'Too few threads — tasks wait. Too many — context-switch overhead.',
        'Size pools based on workload — CPU-bound versus I/O-bound.',
        'Thread pools turn unbounded thread creation into managed concurrency.',
    ]),
    ("submit_shutdown", "submit_shutdown", [
        'submit takes a Runnable or Callable and returns a Future.',
        'execute is fire-and-forget — no result handle.',
        'shutdown stops accepting new tasks — existing tasks still run.',
        'shutdownNow attempts to cancel pending and interrupt running tasks.',
        'awaitTermination waits for the pool to finish — with optional timeout.',
        'Always shut down executors — leaked pools keep JVM threads alive.',
    ]),
    ("types", "types", [
        'Common executor types.',
        'Fixed thread pool — predictable concurrency for steady workloads.',
        'Cached thread pool — bursty short tasks, grows and shrinks.',
        'Single-thread executor — sequential execution, ordered results.',
        'ScheduledThreadPoolExecutor — delayed and periodic tasks.',
        'ForkJoinPool — work-stealing for divide-and-conquer parallelism.',
    ]),
    ("when_pools", "when_pools", [
        'When to use thread pools.',
        'Server request handling — bound concurrent work.',
        'Background processing — logging, indexing, notifications.',
        'Batch jobs with many independent units of work.',
        'When not — trivial one-off tasks — maybe just start one thread.',
        'Always size and monitor — blind defaults cause outages.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — never calling shutdown — threads leak, JVM hangs on exit.',
        'Two — unbounded queue with fixed pool — memory grows forever.',
        'Three — submitting blocking tasks to a small CPU-bound pool.',
        'Also — ignoring rejected execution when the queue is full.',
        'Treat the executor as a managed resource — lifecycle matters.',
    ]),
    ("interview", "interview", [
        'Interview question — why use ExecutorService over raw Thread?',
        'Decouples task logic from thread lifecycle management.',
        'Reuses threads — avoids creation overhead per task.',
        'Provides bounded concurrency — protects system resources.',
        'Returns Future for results — supports graceful shutdown.',
        'Mention shutdown and awaitTermination in production code.',
    ]),
    ("teaser", "teaser", [
        'Pools run tasks. What about tasks that return values?',
        'Episode Forty-One — Callable and Future.',
        'Typed results, blocking get, and CompletableFuture intro.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Reuse, don't recreate"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,48))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,48), fill=WHITE)
    for i,(lab,col) in enumerate([("task queue",ORANGE),("worker pool",BLUE),("submit",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        x=280+i*520
        d.rounded_rectangle([x,400,x+420,720], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+70,520), lab, font=font(FONT_BOLD,28), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 40", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("ExecutorService", font(FONT_SERIF,58), H//2-30, mix(BG,WHITE,a)),
        ("thread pools · submit · shutdown", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_executor(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "ExecutorService", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    lines=["ExecutorService pool =","  Executors.newFixedThreadPool(4);","pool.submit(() -> doWork());","pool.shutdown();"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((280,300+i*120), line, font=font(FONT_MONO,28), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_pool(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Thread Pool Model", font=font(FONT_SERIF,44), fill=WHITE)
    items=[("task queue","pending work waits here",ORANGE),("worker threads","fixed pool executes tasks",BLUE),("bounded","caps resource usage",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_submit_shutdown(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Submit & Shutdown", font=font(FONT_SERIF,44), fill=WHITE)
    items=[("submit(task)","returns Future",ORANGE),("shutdown()","no new tasks",BLUE),("awaitTermination()","wait for finish",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_MONO,30), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_types(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Pool Types", font=font(FONT_SERIF,48), fill=WHITE)
    pools=[("fixed","steady workload",ORANGE),("cached","bursty short tasks",BLUE),("scheduled","delayed / periodic",GREEN),("single","ordered sequential",MUTED)]
    for i,(k,v,col) in enumerate(pools):
        a=ease_out_cubic(clamp((progress-i*0.14)/0.28))
        if a<=0: continue
        x=160+i*420
        d.rounded_rectangle([x,280,x+380,680], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+40,380), k, font=font(FONT_BOLD,28), fill=mix(BG,col,a))
        d.text((x+30,460), v, font=font(FONT_REG,24), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_when_pools(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "When Thread Pools", font=font(FONT_SERIF,46), fill=WHITE)
    good=[("server request handling",GREEN),("background processing",ORANGE),("batch independent work",BLUE)]
    for i,(name,col) in enumerate(good):
        a=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        if a<=0: continue
        y=180+i*160
        d.rounded_rectangle([200,y,1400,y+130], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=2)
        d.text((280,y+40), f"✓  {name}", font=font(FONT_BOLD,28), fill=mix(BG,col,a))
    a=ease_out_cubic(clamp((progress-0.55)/0.3))
    if a>0:
        d.rounded_rectangle([200,700,1720,860], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,RED,a), width=2)
        d.text((280,760), "✗  One-off trivial tasks — overhead not worth it", font=font(FONT_BOLD,28), fill=mix(BG,RED,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","never shutdown()","threads leak forever"),("02","unbounded queue","memory exhaustion"),("03","blocking on small pool","deadlock risk")]
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
    q="Why ExecutorService over raw Thread?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,30)); d.text(((W-(bbox[2]-bbox[0]))//2,195),q,font=font(FONT_BOLD,30),fill=WHITE)
    answers=[("reuse","avoids thread creation cost",ORANGE),("bounded","caps concurrent work",BLUE),("lifecycle","shutdown + Future",GREEN)]
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
    title="Callable & Future"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,54))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,54), fill=WHITE)
    sub="typed results · get() · CompletableFuture"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,28))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,28), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 41", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {"hook": render_hook, "title": render_title, "executor": render_executor, "pool": render_pool, "submit_shutdown": render_submit_shutdown, "types": render_types, "when_pools": render_when_pools, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 40...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep40_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep40.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep40_narrated.mp4"
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
        paced = OUTPUT / "java_ep40_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_40_ExecutorService.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_40.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_40_ExecutorService_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep40_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_executor'), ('00:01:40', '03_pool'), ('00:02:30', '04_submit'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 40: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
