#!/usr/bin/env python3
"""Episode 60 — Metaspace & Native Memory. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep60", ROOT / "frames_ep60", ROOT / "clips_ep60"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Fifty-Nine showed escape analysis eliminating heap allocations.',
        'But JVM memory is more than the heap — classes and native buffers matter too.',
        'Before Java 8, PermGen held class metadata with a fixed size limit.',
        'Metaspace replaced PermGen — class metadata in native memory, auto-growing.',
        'Direct ByteBuffers and JNI allocations live outside the heap entirely.',
        'Today — metaspace, native memory, direct buffers, and NMT.',
    ]),
    ("title", "title", [
        'Episode Sixty.',
        'Metaspace and Native Memory.',
    ]),
    ("permgen_history", "permgen_history", [
        'PermGen — Permanent Generation — stored class metadata until Java 7.',
        'Fixed maximum size — PermGenSpace OutOfMemoryError on class-heavy apps.',
        'Hot redeploy in app servers leaked class loaders into PermGen.',
        'Java 8 removed PermGen — metadata moved to native metaspace.',
        'Metaspace grows on demand — limited by MaxMetaspaceSize flag.',
        'Understanding the history explains old PermGen tuning advice still online.',
    ]),
    ("metaspace_basics", "metaspace_basics", [
        'Metaspace stores class metadata — method tables, constant pools, annotations.',
        'Allocated from native OS memory — not counted in -Xmx heap limit.',
        'Grows as classes load — shrinks when class loaders become unreachable.',
        'MaxMetaspaceSize caps growth — default unlimited on 64-bit JVM.',
        'Compressed class pointers — UseCompressedClassPointers saves space on 64-bit.',
        'Class unloading requires collecting the defining ClassLoader — rare in long-lived apps.',
    ]),
    ("direct_buffers", "direct_buffers", [
        'Direct ByteBuffers allocate memory outside the Java heap.',
        'ByteBuffer.allocateDirect — native memory for zero-copy I/O with OS.',
        'Not tracked by heap -Xmx — can exhaust process memory silently.',
        'Cleaner or explicit free releases native memory when buffer is garbage collected.',
        'Netty and NIO frameworks use direct buffers heavily — watch native usage.',
        'MaxDirectMemorySize flag sets the cap — default is roughly max heap size.',
    ]),
    ("nmt_native_memory", "nmt_native_memory", [
        'Native Memory Tracking — NMT — accounts for JVM native allocations.',
        'Enable with -XX:NativeMemoryTracking=summary or detail at startup.',
        'jcmd <pid> VM.native_memory summary — breakdown by category.',
        'Categories include Java Heap, Metaspace, Code, Thread, and Internal.',
        'Compare baseline versus after load test — spot metaspace or direct buffer growth.',
        'Detail mode has overhead — use summary in production, detail in staging.',
    ]),
    ("sizing_tuning", "sizing_tuning", [
        'Sizing native memory for production workloads.',
        'Set MaxMetaspaceSize if class loaders leak or dynamic codegen runs wild.',
        'Set MaxDirectMemorySize when using heavy NIO or off-heap caches.',
        'Monitor RSS process size — heap plus metaspace plus code cache plus threads.',
        'NMT diff before and after deployment catches class loader leaks early.',
        'Native OOM kills the process — no catchable Java exception.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — sizing only -Xmx and ignoring metaspace and direct memory.',
        'Two — assuming GC frees direct buffer memory immediately — Cleaner is async.',
        'Three — enabling NMT detail in production — measurable overhead.',
        'Also — redeploying without restarting — class loader leaks accumulate.',
        'Watch RSS and NMT — heap metrics alone miss half the story.',
    ]),
    ("interview", "interview", [
        'Interview question — what is metaspace and how does it differ from the heap?',
        'Metaspace holds class metadata in native memory — not Java objects.',
        'Replaced PermGen in Java 8 — grows on demand, capped by MaxMetaspaceSize.',
        'Direct buffers and code cache also live outside -Xmx heap.',
        'NMT with jcmd VM.native_memory tracks native allocation categories.',
        'RSS is the real process limit — heap plus all native JVM regions.',
    ]),
    ("teaser", "teaser", [
        'Not all references are strong — the JVM offers softer cleanup contracts.',
        'Episode Sixty-One — Soft, Weak, and Phantom References.',
        'ReferenceQueue, caches, and cleanup patterns.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Beyond the heap"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    for i, (lab, col) in enumerate([("heap", ORANGE), ("metaspace", BLUE), ("native", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 80, 520), lab, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 60", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("Metaspace & Native Memory", font(FONT_SERIF, 40), H // 2 - 30, mix(BG, WHITE, a)),
        ("PermGen history · direct buffers · NMT", font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_permgen_history(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "PermGen → Metaspace", font=font(FONT_SERIF, 40), fill=WHITE)
    eras = [("Java ≤7", "PermGen fixed size", RED), ("Java 8+", "Metaspace native", GREEN)]
    for i, (k, v, col) in enumerate(eras):
        a = ease_out_cubic(clamp((progress - i * 0.25) / 0.4))
        if a <= 0: continue
        y = 300 + i * 280
        d.rounded_rectangle([200, y, 1720, y + 200], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 50), k, font=font(FONT_BOLD, 32), fill=mix(BG, col, a))
        d.text((280, y + 120), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_metaspace_basics(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Metaspace", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "class metadata → native memory",
        "not counted in -Xmx",
        "-XX:MaxMetaspaceSize=256m",
        "unloads with ClassLoader GC",
        "UseCompressedClassPointers",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_direct_buffers(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Direct Buffers", font=font(FONT_SERIF, 44), fill=WHITE)
    feats = [("allocateDirect()", "native off-heap", ORANGE), ("zero-copy I/O", "NIO / Netty", BLUE), ("MaxDirectMemorySize", "cap native use", GREEN)]
    for i, (k, v, col) in enumerate(feats):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 45), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_nmt_native_memory(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Native Memory Tracking", font=font(FONT_SERIF, 38), fill=WHITE)
    cats = [("Java Heap", ORANGE), ("Metaspace", BLUE), ("Code", GREEN), ("Thread", RED), ("Internal", MUTED)]
    for i, (cat, col) in enumerate(cats):
        a = ease_out_cubic(clamp((progress - i * 0.1) / 0.25))
        if a <= 0: continue
        y = 200 + i * 120
        d.rounded_rectangle([220, y, 1680, y + 90], radius=12, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((300, y + 25), cat, font=font(FONT_BOLD, 26), fill=mix(BG, col, a))
    d.text((300, 820), "jcmd <pid> VM.native_memory summary", font=font(FONT_MONO, 24), fill=WHITE)
    return img.convert("RGB")


def render_sizing_tuning(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Sizing & Tuning", font=font(FONT_SERIF, 44), fill=WHITE)
    flags = [("-Xmx", "heap cap", ORANGE), ("MaxMetaspaceSize", "class metadata", BLUE), ("MaxDirectMemorySize", "off-heap I/O", GREEN), ("RSS", "process total", RED)]
    for i, (k, v, col) in enumerate(flags):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1720, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 30), k, font=font(FONT_MONO, 26), fill=mix(BG, col, a))
        d.text((900, y + 35), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "only -Xmx tuning", "ignore native memory"), ("02", "direct buffer freed?", "Cleaner is async"), ("03", "NMT detail prod", "use summary")]
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
    q = "Metaspace vs heap?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 36)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 36), fill=WHITE)
    answers = [("metaspace", "class metadata native", ORANGE), ("direct buffers", "off-heap NIO", BLUE), ("NMT + RSS", "full picture", GREEN)]
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
    title = "Soft, Weak & Phantom References"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 38))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 38), fill=WHITE)
    sub = "ReferenceQueue · caches · cleanup"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 61", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "permgen_history": render_permgen_history,
    "metaspace_basics": render_metaspace_basics, "direct_buffers": render_direct_buffers,
    "nmt_native_memory": render_nmt_native_memory, "sizing_tuning": render_sizing_tuning,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Sizing", "Look at")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 60...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep60_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep60.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep60_narrated.mp4"
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
        paced = OUTPUT / "java_ep60_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_60_Metaspace_Native_Memory.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_60.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_60_Metaspace_Native_Memory_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep60_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_permgen'), ('00:01:40', '03_metaspace'), ('00:02:30', '04_direct'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 60: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
