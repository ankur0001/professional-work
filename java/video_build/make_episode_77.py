#!/usr/bin/env python3
"""Episode 77 — Spring Testing. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep77", ROOT / "frames_ep77", ROOT / "clips_ep77"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        "Episode Seventy-Six secured APIs with Spring Security's filter chain.",
        "Security and features both need proof — Spring's test story is a first-class tool.",
        'The pyramid still applies — many fast unit tests, fewer slice tests, few full contexts.',
        'Misusing at SpringBootTest for everything makes CI slow and flaky.',
        'Good tests document contracts — bad tests freeze implementation details.',
        'Today — unit, slice, MockMvc, Testcontainers, and what to assert.',
    ]),
    ("title", "title", [
        'Episode Seventy-Seven.',
        'Spring Testing.',
    ]),
    ("pyramid", "pyramid", [
        'Start with the test pyramid for Spring apps.',
        'Unit tests — pure Java, mocks for collaborators, no ApplicationContext.',
        'Slice tests — WebMvcTest, DataJpaTest — load only the layer under test.',
        'Integration tests — SpringBootTest with a real or containerized stack.',
        'End-to-end tests — few, precious, against a deployed-like environment.',
        'Push assertions down the pyramid — speed is a feature of the suite.',
    ]),
    ("unit_slice", "unit_slice", [
        'Unit and slice testing patterns.',
        'Constructor injection makes unit tests trivial — new Service with mocks.',
        'WebMvcTest stands up controllers — MockMvc drives HTTP without a server.',
        'DataJpaTest boots repositories against an embedded or Testcontainers DB.',
        'MockBean replaces a collaborator inside a slice context.',
        'Prefer AssertJ fluent assertions — readable failures save debug time.',
    ]),
    ("spring_boot_test", "spring_boot_test", [
        'When SpringBootTest earns its cost.',
        'Full context catches wiring mistakes auto-config and security filters create.',
        'Use RANDOM_PORT only when you truly need a listening server.',
        'Override properties for tests — never point CI at production databases.',
        'DirtiesContext sparingly — it is expensive and often hides design smells.',
        'If every test needs a full boot, your modules are too entangled.',
    ]),
    ("testcontainers", "testcontainers", [
        'Testcontainers bring realistic dependencies to CI.',
        'Postgres, Kafka, LocalStack — same engines your service talks to.',
        'Reuse containers across a suite when the framework supports it.',
        'Pair with DynamicPropertySource to inject JDBC URLs at runtime.',
        'Slower than H2 — faster than debugging prod-only SQL dialects.',
        'Use them for persistence and messaging contracts — not every unit test.',
    ]),
    ("what_to_assert", "what_to_assert", [
        'Assert behavior, not framework internals.',
        'HTTP status, response body shape, and headers clients rely on.',
        'Database side effects after a successful command.',
        'Security — anonymous gets four-oh-one, forbidden role gets four-oh-three.',
        'Avoid asserting log lines or private field values.',
        'Name tests as contracts — createOrder_rejectsNegativeQuantity.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — SpringBootTest on every class — hour-long pipelines.',
        'Two — shared mutable database state between tests — order-dependent flakes.',
        'Three — testing only the happy path — auth and validation unproven.',
        'Also — over-mocking until the test only proves the mock framework works.',
        'Test the risk — not the annotation count.',
    ]),
    ("interview", "interview", [
        'Interview question — how do you test a Spring Boot service?',
        'Unit-test domain and services with mocks — no container.',
        'Slice-test web and JPA layers with WebMvcTest and DataJpaTest.',
        'Reserve SpringBootTest plus Testcontainers for wiring and persistence truth.',
        'Always cover authz negative paths and validation errors.',
        'Optimize for fast feedback — full context is a scalpel, not a hammer.',
    ]),
    ("teaser", "teaser", [
        'One service is solid — next we split the system.',
        'Episode Seventy-Eight — Microservices Basics.',
        'When to split, service boundaries, sync versus async, and operational cost.',
        'See you there.',
    ]),
]

def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = 'Prove the system'
    bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 48))
    d.text(((W - (bbox[2] - bbox[0])) // 2, 120), title, font=font(FONT_SERIF, 48), fill=WHITE)
    labs = [('unit', 'ORANGE'), ('slice', 'BLUE'), ('containers', 'GREEN')]
    for i, (lab, col) in enumerate(labs):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        x = 200 + i * 560
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([x, 400, x + 480, 720], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=3)
        d.text((x + 50, 520), lab, font=font(FONT_BOLD, 24), fill=mix(BG, c, a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a = ease_out_cubic(clamp(progress * 1.3)); lw = int(240 * a)
    d.rectangle([(W - lw) // 2, H // 2 - 50, (W + lw) // 2, H // 2 - 46], fill=ORANGE)
    for txt, fnt, y, col in [
        ('EPISODE 77', font(FONT_BOLD, 28), H // 2 - 140, mix(BG, MUTED, a)),
        ('Spring Testing', font(FONT_SERIF, 46), H // 2 - 30, mix(BG, WHITE, a)),
        ('pyramid · MockMvc · Testcontainers', font(FONT_REG, 26), H // 2 + 70, mix(BG, MUTED, a)),
    ]:
        bbox = d.textbbox((0, 0), txt, font=fnt); d.text(((W - (bbox[2] - bbox[0])) // 2, y), txt, font=fnt, fill=col)
    return img.convert("RGB")

def render_pyramid(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Test Pyramid', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('unit', 'no context, fast mocks', 'ORANGE'), ('slice', 'WebMvc / DataJpa only', 'BLUE'), ('integration', 'full Boot + containers', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_unit_slice(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Unit & Slice', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('plain new + mocks', 'constructor DI helps', 'ORANGE'), ('MockMvc', 'HTTP without a server', 'BLUE'), ('@DataJpaTest', 'repos + real SQL dialect', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_spring_boot_test(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), '@SpringBootTest', font=font(FONT_SERIF, 40), fill=WHITE)
    a = ease_out_cubic(clamp(progress / 0.4))
    d.rounded_rectangle([180, 200, 1740, 840], radius=16, fill=mix(BG, SURFACE, a), outline=mix(BG, BLUE, a), width=3)
    lines = ['full context catches wiring', 'RANDOM_PORT only if needed', 'override props — never hit prod DB', '@DirtiesContext is expensive', 'entangled modules → slow suites']
    for i, line in enumerate(lines):
        aa = ease_out_cubic(clamp((progress - i * 0.08) / 0.22))
        d.text((260, 280 + i * 100), line, font=font(FONT_MONO, 26), fill=mix(BG, WHITE, aa))
    return img.convert("RGB")

def render_testcontainers(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Testcontainers', font=font(FONT_SERIF, 44), fill=WHITE)
    items = [('real engines', 'Postgres · Kafka · LocalStack', 'ORANGE'), ('DynamicPropertySource', 'inject URLs at runtime', 'BLUE'), ('use for contracts', 'not every unit test', 'GREEN')]
    for i, (k, v, col) in enumerate(items):
        a = ease_out_cubic(clamp((progress - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 220 + i * 200
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([200, y, 1720, y + 160], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((280, y + 40), k, font=font(FONT_BOLD, 30), fill=mix(BG, c, a))
        d.text((280, y + 100), v, font=font(FONT_REG, 26), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_what_to_assert(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 60), 'Assert Behavior', font=font(FONT_SERIF, 44), fill=WHITE)
    steps = [('status + body', 'ORANGE'), ('DB effects', 'BLUE'), ('401 / 403', 'GREEN'), ('name the contract', 'RED')]
    for i, (step, col) in enumerate(steps):
        a = ease_out_cubic(clamp((progress - i * 0.12) / 0.25))
        if a <= 0: continue
        x = 160 + i * 340
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([x, 400, x + 300, 700], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=2)
        d.text((x + 24, 520), step, font=font(FONT_REG, 20), fill=mix(BG, WHITE, a))
        if i < len(steps) - 1:
            d.text((x + 305, 530), "→", font=font(FONT_BOLD, 28), fill=MUTED)
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160, 70), "Common Mistakes", font=font(FONT_SERIF, 48), fill=WHITE)
    items = [('01', 'BootTest everywhere', 'push tests down the pyramid'), ('02', 'shared DB state', 'isolate or reset per test'), ('03', 'happy path only', 'cover auth + validation')]
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
    q = 'How do you test a Spring Boot service?'
    bbox = d.textbbox((0, 0), q, font=font(FONT_BOLD, 30)); d.text(((W - (bbox[2] - bbox[0])) // 2, 190), q, font=font(FONT_BOLD, 30), fill=WHITE)
    answers = [('unit + mocks', 'no container', 'ORANGE'), ('slices', 'web / JPA layers', 'BLUE'), ('Boot + containers', 'wiring truth sparingly', 'GREEN')]
    for i, (k, v, col) in enumerate(answers):
        a = ease_out_cubic(clamp((progress - 0.2 - i * 0.18) / 0.3))
        if a <= 0: continue
        y = 360 + i * 170
        c = {'ORANGE': ORANGE, 'BLUE': BLUE, 'GREEN': GREEN, 'RED': RED}[col]
        d.rounded_rectangle([260, y, 1660, y + 140], radius=14, fill=mix(BG, SURFACE, a), outline=mix(BG, c, a), width=3)
        d.text((320, y + 45), k, font=font(FONT_BOLD, 26), fill=mix(BG, c, a))
        d.text((780, y + 50), v, font=font(FONT_REG, 24), fill=mix(BG, WHITE, a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W // 2 - 120, 200), "NEXT EPISODE", font=font(FONT_BOLD, 28), fill=MUTED)
    title = 'Microservices Basics'; bbox = d.textbbox((0, 0), title, font=font(FONT_SERIF, 42))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 - 40), title, font=font(FONT_SERIF, 42), fill=WHITE)
    sub = 'boundaries · sync/async · cost'; bbox = d.textbbox((0, 0), sub, font=font(FONT_REG, 28))
    d.text(((W - (bbox[2] - bbox[0])) // 2, H // 2 + 60), sub, font=font(FONT_REG, 28), fill=BLUE)
    d.text((W // 2 - 90, H // 2 + 150), 'Episode 78', font=font(FONT_BOLD, 30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {
    "hook": render_hook,
    "title": render_title,
    "pyramid": render_pyramid,
    "unit_slice": render_unit_slice,
    "spring_boot_test": render_spring_boot_test,
    "testcontainers": render_testcontainers,
    "what_to_assert": render_what_to_assert,
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
            gap = 0.30 if any(k in text for k in ("Interview", "Three common", "Spring", "Boot", "Capstone")) else (0.28 if text.endswith("?") else 0.12)
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
    print("==> Kokoro Episode 77...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep77_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep77.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep77_narrated.mp4"
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
        paced = OUTPUT / "java_ep77_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_77_Spring_Testing.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_77.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_77_Spring_Testing_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep77_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_pyramid'), ('00:01:40', '03_slice'), ('00:02:30', '04_containers'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg", "-y", "-ss", ts, "-i", str(final), "-frames:v", "1", str(vdir / f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 77: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
