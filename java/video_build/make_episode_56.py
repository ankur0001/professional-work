#!/usr/bin/env python3
"""Episode 56 — GC Collectors. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep56", ROOT / "frames_ep56", ROOT / "clips_ep56"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-Five showed the JIT compiling hot bytecode to native code.',
        'Garbage collection algorithms matter just as much for production latency.',
        'Different collectors trade throughput against pause time differently.',
        'Serial GC — one thread, simple, fine for tiny heaps.',
        'G1 and ZGC target low pause times for large heaps.',
        'Today — Serial, Parallel, G1, and ZGC — and when to choose each.',
    ]),
    ("title", "title", [
        'Episode Fifty-Six.',
        'GC Collectors.',
    ]),
    ("serial_parallel", "serial_parallel", [
        'Serial GC uses a single thread for all collection work.',
        'Flag UseSerialGC — good for small client apps and single-core machines.',
        'Parallel GC — formerly Parallel Old plus Parallel New — multi-threaded.',
        'Flag UseParallelGC — maximizes throughput on batch workloads.',
        'Parallel pauses all threads but uses multiple GC threads to finish faster.',
        'Default before Java 9 — still valid for compute-heavy, pause-tolerant jobs.',
    ]),
    ("g1_collector", "g1_collector", [
        'G1 — Garbage First — is the default collector since Java 9.',
        'Divides heap into equal-sized regions instead of fixed generations.',
        'Concurrent marking identifies regions with the most garbage.',
        'Mixed collections reclaim both young and old regions together.',
        'Target pause time via MaxGCPauseMillis — best-effort, not guaranteed.',
        'Good general-purpose choice for heaps from hundreds of MB to tens of GB.',
    ]),
    ("zgc_overview", "zgc_overview", [
        'ZGC targets sub-millisecond pauses on large heaps.',
        'Uses colored pointers and load barriers for concurrent compaction.',
        'Most work happens concurrently — STW phases are tiny.',
        'Flag UseZGC — available since Java 15, production-ready in LTS releases.',
        'Shenandoah is an alternative low-pause collector with similar goals.',
        'Choose ZGC when pause latency is critical and heap is large.',
    ]),
    ("choosing_collector", "choosing_collector", [
        'How to choose a collector for your workload.',
        'Small heap, single core — Serial GC, minimal overhead.',
        'Batch processing, throughput priority — Parallel GC.',
        'General web services, moderate heaps — G1 default is a solid start.',
        'Large heap, strict latency SLA — ZGC or Shenandoah.',
        'Always validate with GC logs and load tests — not blog posts.',
    ]),
    ("flags_overview", "flags_overview", [
        'Key GC flags to know.',
        'UseG1GC, UseParallelGC, UseSerialGC, UseZGC — select the collector.',
        'Xms and Xmx set initial and maximum heap size.',
        'MaxGCPauseMillis tunes G1 pause target.',
        'Xlog:gc* enables unified GC logging in modern JDK.',
        'Print flags with java -XX:+PrintFlagsFinal -version for your JVM.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — switching to ZGC without measuring — adds overhead for small heaps.',
        'Two — setting MaxGCPauseMillis to one millisecond — unrealistic expectation.',
        'Three — copying GC flags from another app without matching workload.',
        'Also — ignoring GC logs after a collector change.',
        'Collector choice is empirical — profile your actual traffic patterns.',
    ]),
    ("interview", "interview", [
        'Interview question — which GC collector would you choose?',
        'Serial — tiny single-core apps. Parallel — throughput batch jobs.',
        'G1 — default general purpose, region-based, pause-time target.',
        'ZGC — large heap, sub-ms pause goals, concurrent compaction.',
        'Trade throughput versus latency — no one-size-fits-all answer.',
        'Tune with GC logs, heap sizing, and realistic load tests.',
    ]),
    ("teaser", "teaser", [
        'Even the best collector cannot fix memory leaks.',
        'Episode Fifty-Seven — Memory Leaks and Profiling.',
        'Heap dumps, MAT, and finding what holds references alive.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Pick your collector"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("Serial", ORANGE), ("G1", BLUE), ("ZGC", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 120, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 56", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("GC Collectors", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("Serial · Parallel · G1 · ZGC", font(FONT_REG, 28), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_serial_parallel(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Serial & Parallel", font=font(FONT_SERIF, 42), fill=WHITE)
    cols = [("Serial GC", "1 thread, small heaps", ORANGE), ("Parallel GC", "multi-thread, throughput", BLUE)]
    for i, (k, v, col) in enumerate(cols):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        y = 250 + i * 280
        d.rounded_rectangle([200, y, 1720, y + 200], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 50), k, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
        d.text((280, y + 120), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_g1_collector(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "G1 Garbage First", font=font(FONT_SERIF, 40), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "heap → equal-sized regions",
        "concurrent marking finds garbage-heavy regions",
        "mixed GC reclaims young + old regions",
        "-XX:+UseG1GC  (default since Java 9)",
        "-XX:MaxGCPauseMillis=200",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_zgc_overview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "ZGC", font=font(FONT_SERIF, 48), fill=WHITE)
    feats = [("colored pointers", "track object state", ORANGE), ("load barriers", "concurrent compaction", BLUE), ("sub-ms pauses", "large heaps", GREEN)]
    for i, (k, v, col) in enumerate(feats):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 95), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_choosing_collector(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "How to Choose", font=font(FONT_SERIF, 44), fill=WHITE)
    choices = [("tiny / single-core", "Serial", ORANGE), ("batch throughput", "Parallel", BLUE), ("web services", "G1", GREEN), ("strict latency", "ZGC", RED)]
    for i, (k, v, col) in enumerate(choices):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1720, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 30), k, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
        d.text((1100, y + 30), v, font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_flags_overview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "GC Flags", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    lines = [
        "-XX:+UseG1GC / UseZGC / UseParallelGC",
        "-Xms4g -Xmx4g",
        "-XX:MaxGCPauseMillis=200",
        "-Xlog:gc*",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 320 + i * 120), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "ZGC for tiny heap", "overhead not worth it"), ("02", "pause target = 1ms", "unrealistic"), ("03", "copy flags blindly", "match workload")]
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
    q = "Which GC collector?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("Serial/Parallel", "small or throughput", ORANGE), ("G1", "default general purpose", BLUE), ("ZGC", "large heap, low pause", GREEN)]
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
    title = "Memory Leaks & Profiling"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 44))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 44), fill=WHITE)
    sub = "heap dumps · MAT · reference chains"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 57", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "serial_parallel": render_serial_parallel,
    "g1_collector": render_g1_collector, "zgc_overview": render_zgc_overview,
    "choosing_collector": render_choosing_collector, "flags_overview": render_flags_overview,
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
    print("==> Kokoro Episode 56...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep56_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep56.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep56_narrated.mp4"
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
        paced = OUTPUT / "java_ep56_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_56_GC_Collectors.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_56.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_56_GC_Collectors_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep56_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_serial'), ('00:01:40', '03_g1'), ('00:02:30', '04_zgc'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 56: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
