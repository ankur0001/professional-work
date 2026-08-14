#!/usr/bin/env python3
"""Episode 74 — Spring MVC and REST. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep74", ROOT / "frames_ep74", ROOT / "clips_ep74"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Episode Seventy-Three covered Spring Boot starters and auto-configuration.',
        'Most Boot services speak HTTP — Spring MVC is the classic request stack.',
        'REST controllers map URLs to methods and convert JSON with HttpMessageConverters.',
        'Clean API design separates transport from business rules.',
        'Interviews love status codes, validation, and exception handling details.',
        'Today — controllers, mapping, validation, advice, and REST design tips.',
    ]),
    ("title", "title", [
        'Episode Seventy-Four.',
        'Spring MVC and REST.',
    ]),
    ("controllers", "controllers", [
        'RestController combines Controller and ResponseBody.',
        'Methods return objects — Spring writes JSON to the response.',
        'RequestMapping family — GetMapping, PostMapping, PutMapping, DeleteMapping.',
        'Path variables, request params, and headers bind method arguments.',
        'Keep controllers thin — validate input, call a service, map the result.',
        'Business rules belong in services — not in mapping methods.',
    ]),
    ("request_response", "request_response", [
        'The request-response pipeline.',
        'DispatcherServlet is the front controller for Spring MVC.',
        'Handler mapping finds the controller method for the request.',
        'Argument resolvers bind parameters — body, path, query, principal.',
        'Return value handlers write the body or negotiate a view.',
        'Filters and interceptors wrap cross-cutting HTTP concerns.',
    ]),
    ("validation", "validation", [
        'Validation belongs at the edge of the API.',
        'Jakarta Validation annotations — NotNull, Size, Email — on DTOs.',
        'Valid on a request body triggers validation before your method runs.',
        'BindException or MethodArgumentNotValidException carry field errors.',
        'Return structured four-hundred responses — not stack traces.',
        'Validate again in the domain when rules are more than bean annotations.',
    ]),
    ("errors", "errors", [
        'Consistent error handling builds client trust.',
        'ControllerAdvice centralizes exception-to-response mapping.',
        'Map domain not-found to four-oh-four — conflicts to four-oh-nine.',
        'Never leak internal exception messages to public clients.',
        'Problem Details or a small error JSON schema keeps clients stable.',
        'Log with correlation IDs — respond with safe, actionable messages.',
    ]),
    ("design", "design", [
        'REST design habits that interviewers look for.',
        'Nouns for resources — verbs for HTTP methods, not URL paths.',
        'Idempotent PUT and DELETE — careful POST semantics.',
        'Use proper status codes — two-oh-one for create, two-oh-four for empty.',
        'Version deliberately — URL or header — do not break clients silently.',
        'Pagination and filtering for collections — never dump unbounded lists.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — fat controllers with transactions and SQL inside mapping methods.',
        'Two — returning entities directly — overexposes persistence fields.',
        'Three — swallowing exceptions and always returning two-hundred OK.',
        'Also — ignoring Content-Type and Accept — surprising clients with wrong formats.',
        'Treat the HTTP layer as a translation boundary — not the business core.',
    ]),
    ("interview", "interview", [
        'Interview question — how does a request reach your RestController?',
        'Embedded server hands the request to DispatcherServlet.',
        'Handler mapping selects the controller method by path and verb.',
        'Argument resolvers bind body and params — validation may run.',
        'Service executes business logic — return value becomes the HTTP body.',
        'Advice and filters can reshape errors and cross-cutting concerns.',
    ]),
    ("teaser", "teaser", [
        'HTTP is handled — next we persist data.',
        'Episode Seventy-Five — Spring Data and Persistence.',
        'Repositories, JPA mapping, transactions, and N-plus-one awareness.',
        'See you there.',
    ]),
]

def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = 'HTTP the Spring way'
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    labs = [('MVC', 'ORANGE'), ('REST', 'BLUE'), ('validation', 'GREEN')]
    for i, (lab, col) in enumerate(labs):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=3)
        d.text((x + 60, 520), lab, font=font(FONT_BOLD, 26), fill=mix(BG, c, a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ('EPISODE 74', font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ('Spring MVC and REST', font(FONT_SERIF, 48), H // 2 - 30, mix(BG, WHITE, a)),
        ('controllers · validation · error advice', font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")

def render_controllers(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Controllers', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('@RestController', 'JSON body responses', 'ORANGE'), ('mapping annotations', 'GET/POST/PUT/DELETE', 'BLUE'), ('thin layer', 'delegate to services', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_request_response(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Request Pipeline', font=font(FONT_SERIF, 44), fill=WHITE)
    steps = [('DispatcherServlet', 'ORANGE'), ('handler mapping', 'BLUE'), ('bind + validate', 'GREEN'), ('write response', 'RED')]
    for i, (step, col) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        x = 160 + i * 340
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([x, 400, x + 300, 700], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((x + 30, 520), step, font=font(FONT_REG, 22), fill=mix(BG, WHITE, a))
        if i < len(steps) - 1:
            d.text((x + 305, 530), "→", font=font(FONT_BOLD, 28), fill=MUTED)
    return img.convert("RGB")

def render_validation(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Validation', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('@Valid DTOs', 'bean validation at edge', 'ORANGE'), ('field errors', 'structured 400 responses', 'BLUE'), ('domain rules', 're-check deeper invariants', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_errors(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Error Handling', font=font(FONT_SERIF, 40), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = ['@ControllerAdvice centralizes maps', '404 / 409 from domain outcomes', 'no internal message leaks', 'Problem Details or error schema', 'correlate logs ↔ client errors']
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")

def render_design(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'REST Design', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('resource nouns', 'HTTP verbs carry action', 'ORANGE'), ('status codes', '201 create · 204 empty', 'BLUE'), ('paginate', 'never unbounded lists', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [('01', 'fat controllers', 'services own business rules'), ('02', 'return entities', 'use API DTOs'), ('03', 'always HTTP 200', 'map real status codes')]
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
    q = 'How does a request reach RestController?'
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 32)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 32), fill=WHITE)
    answers = [('DispatcherServlet', 'front controller', 'ORANGE'), ('map + bind', 'path, verb, args', 'BLUE'), ('service → body', 'advice handles errors', 'GREEN')]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 28), fill=mix(BG, c, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = 'Spring Data and Persistence'; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 42))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 42), fill=WHITE)
    sub = 'repositories · JPA · transactions'; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), 'Episode 75', font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "controllers": render_controllers,
    "request_response": render_request_response,
    "validation": render_validation,
    "errors": render_errors,
    "design": render_design,
    "mistakes": render_mistakes,
    "interview": render_interview,
    "teaser": render_teaser,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Spring", "Boot")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 74...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep74_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep74.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep74_narrated.mp4"
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
        paced = OUTPUT / "java_ep74_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_74_Spring_MVC_REST.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_74.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_74_Spring_MVC_REST_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep74_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_controllers'), ('00:01:40', '03_pipeline'), ('00:02:30', '04_validation'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 74: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
