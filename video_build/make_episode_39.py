#!/usr/bin/env python3
"""Episode 39 — Explicit Locks. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep39", ROOT / "frames_ep39", ROOT / "clips_ep39"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'synchronized is built in — but sometimes you need more control.',
        'What if you want to try acquiring a lock without blocking forever?',
        'What if you need multiple wait conditions on the same lock?',
        'Explicit locks in java.util.concurrent give you those options.',
        'ReentrantLock, tryLock, and Condition — the flexible toolkit.',
        'Today — explicit locks beyond synchronized.',
    ]),
    ("title", "title", [
        'Episode Thirty-Nine.',
        'Explicit Locks — ReentrantLock and Condition.',
    ]),
    ("reentrant", "reentrant", [
        'ReentrantLock is a mutual-exclusion lock with explicit API.',
        'lock acquires. unlock releases — you must unlock in a finally block.',
        'Reentrant — the same thread can lock again without deadlocking itself.',
        'Fair mode optional — threads acquire in arrival order.',
        'Use try-finally — never forget unlock after lock.',
        'ReentrantLock provides the same exclusion as synchronized — with more features.',
    ]),
    ("trylock", "trylock", [
        'tryLock attempts acquisition without indefinite blocking.',
        'Returns true if the lock was acquired — false if not available.',
        'tryLock with timeout — wait up to a duration, then give up.',
        'Useful for avoiding deadlocks — back off and retry or fail gracefully.',
        'lockInterruptibly responds to thread interruption while waiting.',
        'Explicit locks shine when blocking forever is not acceptable.',
    ]),
    ("condition", "condition", [
        'Condition replaces wait and notify with a clearer API.',
        'lock.newCondition creates a condition variable bound to that lock.',
        'await releases the lock and waits. signal wakes one waiter.',
        'Multiple conditions per lock — separate queues for different events.',
        'Always await inside a loop checking the predicate — spurious wakeups happen.',
        'Condition variables enable producer-consumer patterns cleanly.',
    ]),
    ("compare", "compare", [
        'ReentrantLock versus synchronized.',
        'Both provide mutual exclusion and memory visibility.',
        'synchronized is simpler — automatic release, no forgotten unlock.',
        'ReentrantLock adds tryLock, fairness, interruptible waits, multiple conditions.',
        'synchronized is fine for most cases — do not reach for locks by default.',
        'Use explicit locks when you need their specific capabilities.',
    ]),
    ("when_locks", "when_locks", [
        'When to choose explicit locks.',
        'Timed or non-blocking lock attempts — tryLock with timeout.',
        'Fair ordering when starvation is a real concern.',
        'Multiple condition variables on one lock object.',
        'When not — simple critical sections — synchronized is cleaner.',
        'Measure contention before optimizing lock strategy.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — forgetting unlock in finally — lock leaked forever.',
        'Two — locking without holding the lock when calling await or signal.',
        'Three — using tryLock but not handling the false return path.',
        'Also — fair locks cost throughput — enable only when needed.',
        'Explicit locks demand discipline — synchronized is harder to misuse.',
    ]),
    ("interview", "interview", [
        'Interview question — ReentrantLock versus synchronized?',
        'Both provide mutual exclusion and happens-before visibility.',
        'ReentrantLock offers tryLock, fairness, interruptible lock, multiple Conditions.',
        'synchronized is simpler — JVM-managed, always released on exit.',
        'Prefer synchronized unless you need a specific ReentrantLock feature.',
        'Mention always unlocking in finally with explicit locks.',
    ]),
    ("teaser", "teaser", [
        'Locks coordinate threads. Who manages the threads themselves?',
        'Episode Forty — ExecutorService and Thread Pools.',
        'Submit tasks, reuse threads, and shut down gracefully.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "More than synchronized"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,46))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,46), fill=WHITE)
    for i,(lab,col) in enumerate([("tryLock",ORANGE),("fair",BLUE),("Condition",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        x=280+i*520
        d.rounded_rectangle([x,400,x+420,720], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+80,520), lab, font=font(FONT_BOLD,30), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 39", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Explicit Locks", font(FONT_SERIF,62), H//2-30, mix(BG,WHITE,a)),
        ("ReentrantLock · tryLock · Condition", font(FONT_REG,28), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_reentrant(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "ReentrantLock", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    lines=["ReentrantLock lock = new ReentrantLock();","lock.lock();","try { /* critical */ }","finally { lock.unlock(); }"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((280,300+i*120), line, font=font(FONT_MONO,28), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_trylock(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "tryLock", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("tryLock()","non-blocking attempt",ORANGE),("tryLock(time, unit)","wait with timeout",BLUE),("lockInterruptibly()","respond to interrupt",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_MONO,30), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_condition(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Condition Variables", font=font(FONT_SERIF,44), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,GREEN,a), width=3)
    lines=["Condition notEmpty = lock.newCondition();","lock.lock();","while (queue.isEmpty()) notEmpty.await();","notEmpty.signal();  // wake one waiter"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((280,300+i*120), line, font=font(FONT_MONO,26), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_compare(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Lock vs synchronized", font=font(FONT_SERIF,44), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,220,900,820], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,ORANGE,left), width=4)
        d.text((220,280), "synchronized", font=font(FONT_BOLD,32), fill=mix(BG,ORANGE,left))
        for i,lab in enumerate(["simple syntax","auto release","built-in monitor"]):
            d.text((240,380+i*70), lab, font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
    if right>0:
        d.rounded_rectangle([1020,220,1780,820], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,BLUE,right), width=4)
        d.text((1100,280), "ReentrantLock", font=font(FONT_BOLD,32), fill=mix(BG,BLUE,right))
        for i,lab in enumerate(["tryLock / timeout","fair mode","multiple Conditions"]):
            d.text((1120,380+i*70), lab, font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
    return img.convert("RGB")

def render_when_locks(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "When Explicit Locks", font=font(FONT_SERIF,46), fill=WHITE)
    good=[("timed or non-blocking acquire",GREEN),("fair ordering needed",ORANGE),("multiple Conditions per lock",BLUE)]
    for i,(name,col) in enumerate(good):
        a=ease_out_cubic(clamp((progress-i*0.15)/0.3))
        if a<=0: continue
        y=180+i*160
        d.rounded_rectangle([200,y,1400,y+130], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=2)
        d.text((280,y+40), f"✓  {name}", font=font(FONT_BOLD,28), fill=mix(BG,col,a))
    a=ease_out_cubic(clamp((progress-0.55)/0.3))
    if a>0:
        d.rounded_rectangle([200,700,1720,860], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,RED,a), width=2)
        d.text((280,760), "✗  Simple critical sections — synchronized is enough", font=font(FONT_BOLD,28), fill=mix(BG,RED,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","forget unlock()","always use finally"),("02","await without lock held","must hold lock first"),("03","ignore tryLock false","handle failure path")]
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
    q="ReentrantLock vs synchronized?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,32)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,32),fill=WHITE)
    answers=[("both","mutual exclusion + visibility",ORANGE),("lock extras","tryLock, fair, Condition",BLUE),("prefer sync","unless you need extras",GREEN)]
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
    title="ExecutorService"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,58))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,58), fill=WHITE)
    sub="thread pools · submit · shutdown"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 40", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {"hook": render_hook, "title": render_title, "reentrant": render_reentrant, "trylock": render_trylock, "condition": render_condition, "compare": render_compare, "when_locks": render_when_locks, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 39...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep39_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep39.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep39_narrated.mp4"
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
        paced = OUTPUT / "java_ep39_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_39_Explicit_Locks.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_39.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_39_Explicit_Locks_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep39_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_reentrant'), ('00:01:40', '03_trylock'), ('00:02:30', '04_condition'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 39: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
