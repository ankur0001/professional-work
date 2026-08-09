#!/usr/bin/env python3
"""Episode 46 — CompletableFuture Deep Dive. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep46", ROOT / "frames_ep46", ROOT / "clips_ep46"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Forty-One introduced CompletableFuture — supplyAsync and a quick chain.',
        'Production async code needs richer composition and solid error handling.',
        'thenApply transforms a result synchronously on the completion thread.',
        'thenCompose flattens nested futures — the async equivalent of flatMap.',
        'allOf waits for every future — anyOf for the first to complete.',
        'Today — deep dive into composing and recovering CompletableFuture pipelines.',
    ]),
    ("title", "title", [
        'Episode Forty-Six.',
        'CompletableFuture Deep Dive.',
    ]),
    ("then_apply", "then_apply", [
        'thenApply maps the result when the previous stage completes.',
        'Runs on the same executor as the completing thread by default.',
        'thenApplyAsync runs the mapping function on a specified executor.',
        'Use for pure transformations — parse JSON, format strings, map values.',
        'Returns a new CompletableFuture of the transformed type.',
        'Chain multiple thenApply calls — each waits for the prior stage.',
    ]),
    ("then_compose", "then_compose", [
        'thenCompose chains when the next step itself returns a CompletableFuture.',
        'Flattens CompletableFuture of CompletableFuture into a single future.',
        'Without compose you nest futures — blocking get inside thenApply.',
        'thenComposeAsync runs the composing function on an executor.',
        'Essential for dependent async calls — fetch then save then notify.',
        'Think flatMap for futures — compose, do not nest.',
    ]),
    ("all_of", "all_of", [
        'allOf accepts an array or collection of CompletableFuture instances.',
        'Returns CompletableFuture of Void — completion means all inputs finished.',
        'Join individual futures after allOf completes to collect results.',
        'anyOf completes when any one input future completes.',
        'Use allOf for parallel fan-out — aggregate when every branch is done.',
        'anyOf for racing alternatives — first successful or fastest response wins.',
    ]),
    ("exception_handling", "exception_handling", [
        'exceptionally recovers from failure — returns a fallback value.',
        'handle receives both result and exception — unified success and failure path.',
        'whenComplete is a side-effect hook — does not transform the result.',
        'completeExceptionally manually fails a future you created.',
        'orTimeout and completeOnTimeout add deadline semantics in Java 9+.',
        'Never swallow exceptions — log in whenComplete, recover in handle.',
    ]),
    ("when_compose", "when_compose", [
        'When to use each combinator.',
        'thenApply — synchronous transform of a completed value.',
        'thenCompose — next step is itself async — dependent chain.',
        'allOf — parallel independent work — wait for all.',
        'exceptionally or handle — explicit failure recovery.',
        'Avoid blocking get in callbacks — keep the pipeline non-blocking.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — thenApply when the lambda returns a Future — use thenCompose.',
        'Two — ignoring exceptions — pipeline fails silently downstream.',
        'Three — blocking get inside thenApply — stalls the executor.',
        'Also — allOf without collecting individual results — Void only signals done.',
        'Compose async work — do not turn CompletableFuture back into blocking code.',
    ]),
    ("interview", "interview", [
        'Interview question — thenApply versus thenCompose?',
        'thenApply — function returns a plain value — map the result.',
        'thenCompose — function returns CompletableFuture — flatten nested futures.',
        'thenApply nests CompletableFuture of CompletableFuture — compose flattens.',
        'allOf waits for all — anyOf for first completion.',
        'handle and exceptionally for unified error handling in pipelines.',
    ]),
    ("teaser", "teaser", [
        'CompletableFuture defaults to ForkJoinPool.commonPool.',
        'Episode Forty-Seven — ForkJoinPool and Work-Stealing.',
        'Parallel decomposition, recursive tasks, and the common pool.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Compose async pipelines"
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 46))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 46), fill=WHITE)
    for i, (lab, col) in enumerate([("thenApply", ORANGE), ("thenCompose", BLUE), ("allOf", GREEN)]):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((x + 60, 520), lab, font=font(FONT_BOLD, 26), fill=mix(BG, col, a))
    return img.convert("RGB")


def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ("EPISODE 46", font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ("CompletableFuture Deep Dive", font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ("thenApply · thenCompose · allOf", font(FONT_REG, 28), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")


def render_then_apply(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "thenApply", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, ORANGE, a), width=3)
    lines = [
        "future.thenApply(data -> parse(data))",
        "  .thenApply(doc -> format(doc));",
        "// map completed value — sync transform",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 340 + i * 140), line, font=font(FONT_MONO, 28), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_then_compose(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "thenCompose", font=font(FONT_SERIF, 48), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = [
        "fetchUser(id)",
        "  .thenCompose(user -> saveAsync(user))",
        "  .thenCompose(saved -> notifyAsync(saved));",
        "// flatMap — no nested Future",
    ]
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.12) / 0.28))
        d.text((280, 300 + i * 120), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")


def render_all_of(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "allOf & anyOf", font=font(FONT_SERIF, 46), fill=WHITE)
    items = [("allOf", "wait until every future completes", GREEN), ("anyOf", "first completion wins", ORANGE), ("join", "collect results after allOf", BLUE)]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 220
        d.rounded_rectangle([200, y, 1720, y + 180], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((280, y + 40), k, font=font(FONT_MONO, 32), fill=mix(BG, col, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 28), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_exception_handling(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "Exception Handling", font=font(FONT_SERIF, 44), fill=WHITE)
    handlers = [("exceptionally", "fallback on failure", RED), ("handle", "result + exception unified", ORANGE), ("whenComplete", "side-effect hook", BLUE)]
    for i, (name, desc, col) in enumerate(handlers):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 200 + i * 200
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 35), name, font=font(FONT_MONO, 28), fill=mix(BG, col, a))
        d.text((280, y + 95), desc, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_when_compose(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), "When to Use", font=font(FONT_SERIF, 46), fill=WHITE)
    good = [("thenApply — sync transform", GREEN), ("thenCompose — async chain", ORANGE), ("allOf — parallel fan-out", BLUE)]
    for i, (name, col) in enumerate(good):
        a = ease_out_cubic(clamp((progress - i * 0.15) / 0.3))
        if a <= 0: continue
        y = 180 + i * 160
        d.rounded_rectangle([200, y, 1400, y + 130], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=2)
        d.text((280, y + 40), f"✓  {name}", font=font(FONT_BOLD, 28), fill=mix(BG, col, a))
    a = ease_out_cubic(clamp((progress - 0.55) / 0.3))
    if a > 0:
        d.rounded_rectangle([200, 700, 1720, 860], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, RED, a), width=2)
        d.text((280, 760), "✗  blocking get() inside callbacks", font=font(FONT_BOLD, 28), fill=mix(BG, RED, a))
    return img.convert("RGB")


def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [("01", "thenApply returns Future", "use thenCompose"), ("02", "silent failures", "handle / exceptionally"), ("03", "get() in callback", "blocks executor")]
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
    q = "thenApply vs thenCompose?"
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 34)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 34), fill=WHITE)
    answers = [("thenApply", "maps plain value", ORANGE), ("thenCompose", "flattens nested Future", BLUE), ("allOf / anyOf", "wait all / first wins", GREEN)]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, col, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 30), fill=mix(BG, col, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")


def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = "ForkJoinPool"; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 50))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 50), fill=WHITE)
    sub = "Work-stealing · common pool"; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), "Episode 47", font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {
    "hook": render_hook, "title": render_title, "then_apply": render_then_apply,
    "then_compose": render_then_compose, "all_of": render_all_of,
    "exception_handling": render_exception_handling, "when_compose": render_when_compose,
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
    print("==> Kokoro Episode 46...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep46_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep46.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep46_narrated.mp4"
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
        paced = OUTPUT / "java_ep46_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_46_CompletableFuture.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_46.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_46_CompletableFuture_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep46_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_then_apply'), ('00:01:40', '03_then_compose'), ('00:02:30', '04_all_of'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 46: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
