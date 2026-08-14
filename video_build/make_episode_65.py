#!/usr/bin/env python3
"""Episode 65 — JVM Startup & Warmup. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep65", ROOT / "frames_ep65", ROOT / "clips_ep65"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Sixty-Four explained safepoints and stop-the-world coordination.',
        'Runtime pauses matter — but so does the time before your service is ready.',
        'Cold JVM startup loads hundreds of classes, initializes JIT, and warms caches.',
        'First requests after deploy are often slow — class loading and interpretation dominate.',
        'Class Data Sharing and warmup strategies shrink that cold-start penalty.',
        'Today — JVM startup phases, class loading cost, CDS, and warmup.',
    ]),
    ("title", "title", [
        'Episode Sixty-Five.',
        'JVM Startup and Warmup.',
    ]),
    ("startup_phases", "startup_phases", [
        'JVM startup unfolds in distinct phases before your main method runs.',
        'VM initialization — memory regions, thread system, and core subsystems.',
        'Class loading and linking — bootstrap classes, then application classpath.',
        'Interpreter executes bytecode until JIT identifies hot methods.',
        'JIT compilation kicks in — C1 quick compile, then C2 optimizing compile.',
        'Steady state — most hot code runs compiled native instructions.',
    ]),
    ("class_loading_cost", "class_loading_cost", [
        'Class loading is a major cold-start cost for large applications.',
        'Each class — parse bytecode, verify, create Class object in metaspace.',
        'Spring and dependency injection frameworks load thousands of classes at boot.',
        'Fat JARs with many dependencies multiply class count and startup time.',
        'Lazy initialization defers loading — but first touch still pays the cost.',
        'Measure with -Xlog:class+load or startup JFR events — know your baseline.',
    ]),
    ("cds_appcds", "cds_appcds", [
        'Class Data Sharing — CDS — archives loaded classes for faster restart.',
        'JVM builds a shared archive of classes at training time.',
        'Subsequent JVM instances memory-map the archive — skip parse and verify.',
        'AppCDS extends CDS to application classpath classes — not just bootstrap.',
        'java -Xshare:dump with classpath creates the archive — -Xshare:on uses it.',
        'Container images can bake the archive in — significant startup improvement.',
    ]),
    ("warmup_strategies", "warmup_strategies", [
        'Warmup brings the JVM to steady state before serving production traffic.',
        'Synthetic load — replay health checks or canary requests after deploy.',
        'AOT compilation — GraalVM native image — trades flexibility for instant start.',
        'Tiered compilation — TieredStopAtLevel tunes how aggressively JIT compiles.',
        'Spring AOT and CRaC explore checkpoint-restore for sub-second restarts.',
        'Warmup is workload-specific — exercise the code paths users actually hit.',
    ]),
    ("measurement_startup", "measurement_startup", [
        'Measure startup like any other performance metric.',
        'Time from process start to ready — health endpoint responding.',
        'JFR ApplicationStarted and ClassLoad events break down phases.',
        'Compare cold start versus warm restart — CDS impact is visible immediately.',
        'Track P99 latency for first N requests after deploy — the warmup window.',
        'Set SLOs on startup time — regressions from new dependencies are common.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — measuring only steady-state latency — ignoring cold-start after deploy.',
        'Two — skipping warmup in staging — production first request pays the cost.',
        'Three — adding dependencies without checking class count impact.',
        'Also — assuming GraalVM native image fits every service — reflection limits apply.',
        'Profile startup separately — it is a different problem than throughput tuning.',
    ]),
    ("interview", "interview", [
        'Interview question — how do you reduce JVM startup time?',
        'Identify class loading cost — log class load events, count classes.',
        'CDS and AppCDS — shared archives skip parse and verify on restart.',
        'Warmup traffic before cutting over — JIT compiles hot paths.',
        'Lazy init and smaller classpath reduce classes loaded at boot.',
        'Measure time-to-ready — not just main method entry.',
    ]),
    ("teaser", "teaser", [
        'Startup and warmup complete the internals picture — time to tie it together.',
        'Episode Sixty-Six — JVM Interview Wrap-Up.',
        'Crisp explanations of heap, stack, GC, and JIT for interviews.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Cold to ready"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    for i, (lab, col) in enumerate([("load", ORANGE), ("JIT", BLUE), ("CDS", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 160, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 65", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("JVM Startup & Warmup", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("class loading · CDS · warmup", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_startup_phases(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Startup Phases", font=font(FONT_SERIF, 44), fill=WHITE)
    phases = [("VM init", "memory, threads", ORANGE), ("class load", "parse, verify", BLUE), ("interpreter", "bytecode exec", GREEN), ("JIT", "C1 → C2 compile", RED)]
    for i, (k, v, col) in enumerate(phases):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1720, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 30), k, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
        d.text((900, y + 35), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_class_loading_cost(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Class Loading Cost", font=font(FONT_SERIF, 40), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    lines = [
        "parse bytecode → verify → metaspace",
        "Spring/DI → thousands of classes",
        "fat JARs multiply class count",
        "lazy init defers but first touch pays",
        "-Xlog:class+load for measurement",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_cds_appcds(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "CDS & AppCDS", font=font(FONT_SERIF, 44), fill=WHITE)
    items = [("CDS", "bootstrap class archive", ORANGE), ("AppCDS", "app classpath classes", BLUE), ("-Xshare:on", "mmap on restart", GREEN)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_MONO, 28), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_warmup_strategies(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Warmup Strategies", font=font(FONT_SERIF, 40), fill=WHITE)
    strats = [("synthetic load", "canary requests", ORANGE), ("GraalVM native", "AOT instant start", BLUE), ("Spring AOT / CRaC", "checkpoint restore", GREEN)]
    for i, (k, v, col) in enumerate(strats):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_measurement_startup(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Measure Startup", font=font(FONT_SERIF, 44), fill=WHITE)
    metrics = [("time-to-ready", "health endpoint up", ORANGE), ("JFR events", "ClassLoad breakdown", BLUE), ("first N requests", "P99 warmup window", GREEN)]
    for i, (k, v, col) in enumerate(metrics):
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
    items = [("01", "steady-state only", "measure cold start"), ("02", "no warmup", "first prod request pays"), ("03", "deps unchecked", "class count grows")]
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
    q = "How do you reduce JVM startup?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("CDS/AppCDS", "shared class archives", ORANGE), ("warmup", "JIT compiles hot paths", BLUE), ("measure", "time-to-ready SLO", GREEN)]
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
    title = "JVM Interview Wrap-Up"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 42))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 42), fill=WHITE)
    sub = "heap · stack · GC · JIT — crisp answers"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 66", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "startup_phases": render_startup_phases,
    "class_loading_cost": render_class_loading_cost, "cds_appcds": render_cds_appcds,
    "warmup_strategies": render_warmup_strategies, "measurement_startup": render_measurement_startup,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Measure startup", "JVM startup")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 65...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep65_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep65.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep65_narrated.mp4"
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
        paced = OUTPUT / "java_ep65_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_65_JVM_Startup.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_65.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_65_JVM_Startup_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep65_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_phases'), ('00:01:40', '03_cds'), ('00:02:30', '04_warmup'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 65: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
