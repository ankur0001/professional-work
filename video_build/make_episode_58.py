#!/usr/bin/env python3
"""Episode 58 — Diagnostic Tools. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep58", ROOT / "frames_ep58", ROOT / "clips_ep58"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-Seven showed heap dumps and MAT for memory leaks.',
        'But production incidents need fast answers from a running JVM.',
        'JDK ships diagnostic tools — no extra install required.',
        'jcmd is the Swiss Army knife — list, trigger, and inspect.',
        'jmap, jstack, and JFR each target a different runtime view.',
        'Today — jcmd, jmap, jstack, and JFR for live JVM diagnostics.',
    ]),
    ("title", "title", [
        'Episode Fifty-Eight.',
        'Diagnostic Tools.',
    ]),
    ("jcmd_overview", "jcmd_overview", [
        'jcmd sends diagnostic commands to a running Java process.',
        'List JVMs with jcmd — shows PID and main class name.',
        'jcmd <pid> help — lists every available subcommand.',
        'VM.flags prints active JVM flags — verify your tuning.',
        'GC.heap_info and GC.class_histogram — quick heap snapshot.',
        'JFR.start and JFR.dump — record and export flight recordings.',
    ]),
    ("jmap_heap", "jmap_heap", [
        'jmap inspects heap layout and creates dumps.',
        'jmap -heap <pid> — summary of generations and usage.',
        'jmap -histo:live <pid> — object histogram of live instances.',
        'jmap -dump:live,format=b,file=heap.hprof <pid> — full dump.',
        'Prefer jcmd GC.heap_dump on modern JDK — same result, cleaner API.',
        'Histogram first — confirms leak class before multi-gigabyte dump.',
    ]),
    ("jstack_threads", "jstack_threads", [
        'jstack captures thread stacks — essential for deadlocks and hangs.',
        'jstack <pid> — prints every thread name, state, and stack trace.',
        'Look for BLOCKED threads and circular lock dependencies.',
        'jcmd <pid> Thread.print — equivalent output on modern JDK.',
        'Take multiple samples seconds apart — distinguish transient waits.',
        'Thread dump alone does not show heap — pair with jmap or JFR.',
    ]),
    ("jfr_overview", "jfr_overview", [
        'Java Flight Recorder — low-overhead event recorder built into the JDK.',
        'Enable with -XX:+FlightRecorder or jcmd JFR.start.',
        'Records GC, allocation, lock, and method samples continuously.',
        'jcmd <pid> JFR.dump filename=rec.jfr — export for JDK Mission Control.',
        'Allocation and OldObjectSample events help find leak sources live.',
        'Production-safe when configured — microseconds of overhead per event.',
    ]),
    ("diagnostic_workflow", "diagnostic_workflow", [
        'A practical on-call diagnostic workflow.',
        'Step one — jcmd <pid> help and VM.flags — confirm JVM state.',
        'Step two — high CPU? async-profiler or JFR MethodProfiling.',
        'Step three — high heap? GC.heap_info then histogram or heap dump.',
        'Step four — stuck threads? Thread.print twice, check BLOCKED.',
        'Document PID, timestamp, and command output for post-incident review.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — running jmap -heap on a 32-gig heap under load — long STW pause.',
        'Two — single thread dump for deadlock — need two samples or JFR lock events.',
        'Three — leaving JFR recording forever without rotation — disk fills up.',
        'Also — using tools from a different JDK version than the target JVM.',
        'Match JDK major version — diagnostic output formats change.',
    ]),
    ("interview", "interview", [
        'Interview question — how do you diagnose a production JVM issue?',
        'jcmd — list processes, VM.flags, GC.heap_info, Thread.print.',
        'jmap histogram or heap dump for memory — jstack for thread deadlocks.',
        'JFR for continuous low-overhead profiling — export to Mission Control.',
        'Sample under load — idle JVM hides contention and allocation hotspots.',
        'Always capture timestamp, PID, and JDK version with every artifact.',
    ]),
    ("teaser", "teaser", [
        'Diagnostics show what the JVM does at runtime — the compiler optimizes before that.',
        'Episode Fifty-Nine — Escape Analysis.',
        'Stack allocation, scalar replacement, and when objects escape.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Inspect a live JVM"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("jcmd", ORANGE), ("jmap", BLUE), ("JFR", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 140, 520), lab, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 58", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Diagnostic Tools", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("jcmd · jmap · jstack · JFR", font(FONT_REG, 28), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_jcmd_overview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "jcmd", font=font(FONT_SERIF, 48), fill=WHITE)
    cmds = [("jcmd", "list JVMs", ORANGE), ("jcmd <pid> help", "all subcommands", BLUE), ("VM.flags", "active tuning", GREEN)]
    for i, (k, v, col) in enumerate(cmds):
        a = ease_out_cubic(clamp((progress - i * 0.2) / 0.35))
        if a <= 0: continue
        y = 250 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_MONO, 26), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_jmap_heap(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "jmap", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "jmap -heap <pid>     → layout summary",
        "jmap -histo:live     → class histogram",
        "jmap -dump:live      → HPROF file",
        "prefer: jcmd GC.heap_dump",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        d.text((260, 320 + i * 120), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_jstack_threads(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "jstack", font=font(FONT_SERIF, 48), fill=WHITE)
    states = [("RUNNABLE", "active execution", GREEN), ("BLOCKED", "waiting for lock", RED), ("WAITING", "park / join", ORANGE)]
    for i, (k, v, col) in enumerate(states):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 45), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_jfr_overview(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Java Flight Recorder", font=font(FONT_SERIF, 40), fill=WHITE)
    feats = [("JFR.start", "begin recording", ORANGE), ("JFR.dump", "export .jfr file", BLUE), ("Mission Control", "analyze events", GREEN)]
    for i, (k, v, col) in enumerate(feats):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 45), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_diagnostic_workflow(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "On-Call Workflow", font=font(FONT_SERIF, 44), fill=WHITE)
    steps = [("1", "jcmd VM.flags", ORANGE), ("2", "CPU → JFR / profiler", BLUE), ("3", "heap → histogram / dump", GREEN), ("4", "threads → jstack × 2", RED)]
    for i, (num, step, col) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1720, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((260, y + 35), num, font=font(FONT_SERIF, 36), fill=mix(BG, col, a))
        d.text((360, y + 40), step, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "jmap -heap on huge heap", "long STW pause"), ("02", "one thread dump", "need two samples"), ("03", "JFR never rotated", "disk fills up")]
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
    q = "Diagnose a production JVM?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("jcmd", "flags, heap, threads", ORANGE), ("jmap / dump", "memory issues", BLUE), ("JFR", "continuous profile", GREEN)]
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
    title = "Escape Analysis"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 44))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 44), fill=WHITE)
    sub = "stack allocation · scalar replacement"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 59", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "jcmd_overview": render_jcmd_overview,
    "jmap_heap": render_jmap_heap, "jstack_threads": render_jstack_threads,
    "jfr_overview": render_jfr_overview, "diagnostic_workflow": render_diagnostic_workflow,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "A practical", "Look at")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 58...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep58_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep58.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep58_narrated.mp4"
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
        paced = OUTPUT / "java_ep58_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_58_Diagnostic_Tools.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_58.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_58_Diagnostic_Tools_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep58_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_jcmd'), ('00:01:40', '03_jmap'), ('00:02:30', '04_jfr'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 58: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
