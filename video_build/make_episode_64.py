#!/usr/bin/env python3
"""Episode 64 — Safepoints. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep64", ROOT / "frames_ep64", ROOT / "clips_ep64"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Sixty-Three showed how object headers and padding affect heap footprint.',
        'Memory layout is static — safepoints are dynamic coordination points in the JVM.',
        'GC, deoptimization, and some JVM operations need every thread to reach a known state.',
        'That coordination is called a safepoint — and it can pause your application threads.',
        'Long-running loops without safepoint polls can delay GC for seconds.',
        'Today — what safepoints are, when the JVM pauses, and safepoint bias.',
    ]),
    ("title", "title", [
        'Episode Sixty-Four.',
        'Safepoints.',
    ]),
    ("what_safepoints", "what_safepoints", [
        'A safepoint is a point in compiled code where the JVM can safely inspect thread state.',
        'At a safepoint, the JVM knows every live reference and every stack frame.',
        'GC roots are scanned, biased locking is revoked, and deoptimization can occur.',
        'Threads not at a safepoint must be brought there before STW work begins.',
        'Safepoints are not GC-only — many JVM subsystems depend on them.',
        'Think of them as coordinated parking spots for all application threads.',
    ]),
    ("when_pauses", "when_pauses", [
        'Stop-the-world phases require all mutator threads at safepoints.',
        'Young GC often pauses briefly — all threads must park at safepoints first.',
        'Full GC and some old-gen collections extend STW while roots are processed.',
        'Deoptimization — switching compiled code back to interpreter — uses safepoints.',
        'Biased lock revocation and some JVMTI operations trigger safepoint synchronization.',
        'Pause time includes time waiting for slow threads to reach a safepoint.',
    ]),
    ("safepoint_bias", "safepoint_bias", [
        'Safepoint bias — JVM prefers certain code locations for safepoint polls.',
        'Counted loops have safepoint back-edges — every N iterations thread checks.',
        'Non-counted loops and JNI calls may lack frequent poll sites.',
        'A tight infinite loop without polls can block GC indefinitely — rare but real.',
        'SafepointSynchronize events in JFR show time spent waiting for threads.',
        'Long safepoint sync times point to threads stuck between poll sites.',
    ]),
    ("safepoint_polling", "safepoint_polling", [
        'Threads poll a global safepoint flag at compiled poll sites.',
        'When a safepoint is requested, running threads trap at the next poll.',
        'Interpreter and JIT insert polls in method prologues and loop back-edges.',
        'JNI transitions and blocking I/O eventually reach safepoints on return.',
        'UseAsyncLogDecoration and some intrinsics affect poll placement.',
        'Understanding polls explains why CPU-bound loops affect GC responsiveness.',
    ]),
    ("stw_awareness", "stw_awareness", [
        'Practical awareness for production engineers.',
        'JFR SafepointBegin and SafepointEnd events measure sync plus STW duration.',
        'High sync time — look for long non-polling loops or JNI critical sections.',
        'ZGC and Shenandoah reduce but do not eliminate all safepoint coordination.',
        'Do not micro-optimize poll sites — fix algorithmic long loops instead.',
        'Safepoint knowledge connects GC pauses to actual thread behavior.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — blaming GC alone for pauses — sync time may dominate.',
        'Two — writing busy loops without considering safepoint reachability.',
        'Three — ignoring JFR safepoint events during latency investigations.',
        'Also — assuming concurrent collectors have zero STW — they still safepoint.',
        'Measure sync versus STW separately — the cause differs.',
    ]),
    ("interview", "interview", [
        'Interview question — what is a safepoint and why does it matter?',
        'Coordination point where JVM can inspect all thread stacks safely.',
        'Required for GC root scanning, deoptimization, and lock bias revocation.',
        'Threads poll at loop back-edges — must reach safepoint before STW work.',
        'Long sync time means threads slow to park — not always GC algorithm fault.',
        'JFR safepoint events separate sync wait from actual stop-the-world work.',
    ]),
    ("teaser", "teaser", [
        'Safepoints coordinate runtime — startup decides how fast you reach steady state.',
        'Episode Sixty-Five — JVM Startup and Warmup.',
        'Class loading cost, CDS, and warmup strategies.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Park every thread"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    for i, (lab, col) in enumerate([("poll", ORANGE), ("sync", BLUE), ("STW", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 150, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 64", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Safepoints", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("coordination · polling · STW pauses", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_what_safepoints(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "What Is a Safepoint?", font=font(FONT_SERIF, 40), fill=WHITE)
    feats = [("known state", "all refs + stacks visible", ORANGE), ("coordination", "every thread parks", BLUE), ("not GC-only", "deopt, locks, JVMTI", GREEN)]
    for i, (k, v, col) in enumerate(feats):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_when_pauses(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When JVM Pauses", font=font(FONT_SERIF, 44), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=3)
    lines = [
        "GC root scan → all threads at safepoint",
        "young / full GC STW phases",
        "deoptimization (compiled → interpreter)",
        "biased lock revocation",
        "pause = sync wait + STW work",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_safepoint_bias(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Safepoint Bias", font=font(FONT_SERIF, 44), fill=WHITE)
    items = [("counted loops", "poll every N iterations", ORANGE), ("tight loop", "may block GC", RED), ("JFR sync", "measure wait time", GREEN)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_safepoint_polling(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Safepoint Polling", font=font(FONT_SERIF, 40), fill=WHITE)
    steps = [("global flag", ORANGE), ("poll site", BLUE), ("thread parks", GREEN), ("STW runs", RED)]
    for i, (step, col) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        x = 200 + i * 420
        d.rounded_rectangle([x, 400, x + 360, 700], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((x + 60, 520), step, font=font(FONT_REG, 24), fill=mix(BG, WHITE, a))
        if i < 3:
            d.text((x + 370, 530), "→", font=font(FONT_BOLD, 28), fill=MUTED)
    return img.convert("RGB")


def render_stw_awareness(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Production Awareness", font=font(FONT_SERIF, 40), fill=WHITE)
    tips = [("JFR events", "SafepointBegin/End", ORANGE), ("high sync", "check long loops", BLUE), ("concurrent GC", "still safepoints", GREEN)]
    for i, (k, v, col) in enumerate(tips):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "blame GC only", "check sync time"), ("02", "busy loops", "no poll sites"), ("03", "ignore JFR", "measure sync vs STW")]
    for i, (num, wrong, right) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        y = 180 + i * 240
        d.rounded_rectangle([200, y, 1720, y + 200], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a * 0.7), width=2)
        d.text((260, y + 40), num, font=font(FONT_SERIF, 40), fill=mix(BG, ORANGE, a))
        d.text((360, y + 45), wrong, font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
        d.text((360, y + 110), right, font=font(FONT_REG, 28), fill=mix(BG, GREEN, a))
    return img.convert("RGB")


def render_interview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Interview Question", font=font(FONT_SERIF, 44), fill=WHITE)
    d.rounded_rectangle([160, 150, 1760, 280], radius=16, fill=SURFACE, outline=ORANGE, width=3)
    q = "What is a safepoint?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("coordination", "all threads park", ORANGE), ("for GC/deopt", "known thread state", BLUE), ("sync vs STW", "JFR separates them", GREEN)]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "JVM Startup & Warmup"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 42))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 42), fill=WHITE)
    sub = "class loading · CDS · warmup strategies"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 65", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "what_safepoints": render_what_safepoints,
    "when_pauses": render_when_pauses, "safepoint_bias": render_safepoint_bias,
    "safepoint_polling": render_safepoint_polling, "stw_awareness": render_stw_awareness,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Practical awareness", "A safepoint")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 64...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep64_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep64.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep64_narrated.mp4"
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
        paced = OUTPUT / "java_ep64_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_64_Safepoints.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_64.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_64_Safepoints_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep64_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_what'), ('00:01:40', '03_pauses'), ('00:02:30', '04_polling'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 64: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
