#!/usr/bin/env python3
"""Episode 23 — Maps. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep23", ROOT / "frames_ep23", ROOT / "clips_ep23"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Sets answer membership. Maps answer association.',
        'Given this key — what value belongs with it?',
        'Lookups, caches, indexes, configuration — maps are everywhere.',
        'HashMap is the workhorse. Ordering variants exist for a reason.',
        'Today — Map contracts, null rules, and modern helpers.',
        'Keys find values. Contracts keep them honest.',
    ]),
    ("title", "title", [
        'Episode Twenty-Three.',
        'Maps — key to value in java.util.',
    ]),
    ("contract", "contract", [
        'Map is not a Collection — it is its own hierarchy.',
        'Each key maps to at most one value.',
        'put replaces. get returns null when absent — or when the value is null.',
        'Views matter — keySet, values, and entrySet share the underlying map.',
        'Mutating a view mutates the map. That surprise shows up in code reviews.',
        'Model associations. Do not stuff pairs into a list forever.',
    ]),
    ("hashmap", "hashmap", [
        'HashMap is the default map for single-threaded use.',
        'Average constant-time put and get when hashing behaves.',
        'Keys need equals and hashCode — same story as HashSet.',
        'One null key is allowed. Many null values are allowed.',
        'Prefer computeIfAbsent and merge over get-then-put races of logic.',
        'For most application maps, start here.',
    ]),
    ("variants", "variants", [
        'Ordering and specialized maps.',
        'LinkedHashMap preserves insertion order — or access order for LRU-style caches.',
        'TreeMap keeps keys sorted — natural order or Comparator.',
        'EnumMap is compact and fast when keys are enum constants.',
        'IdentityHashMap uses reference equality — rare, sharp tool.',
        'Pick the variant that matches your iteration and key domain.',
    ]),
    ("nulls", "nulls", [
        'Null rules are implementation-specific.',
        'HashMap tolerates a null key. TreeMap does not.',
        'Hashtable rejects nulls entirely — and brings legacy synchronization.',
        'Never assume null policy from the Map interface alone.',
        'In modern code, ConcurrentHashMap also rejects nulls.',
        'Read the implementation before you lean on null as a signal.',
    ]),
    ("modern", "modern", [
        'Modern Map APIs reduce boilerplate bugs.',
        'getOrDefault avoids null checks for simple fallbacks.',
        'computeIfAbsent builds values lazily and cleanly.',
        'merge combines values with an explicit remapping function.',
        'Map.of and Map.copyOf create unmodifiable maps for safer APIs.',
        'Prefer these helpers over fragile get-then-mutate sequences.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — mutable keys whose equals fields change after insertion.',
        'Two — modifying a map while iterating its keySet carelessly.',
        'Three — reaching for Hashtable in new code out of habit.',
        'Also — using null values as a secret third state without documenting it.',
        'Maps amplify clear key design — and punish sloppy identity.',
    ]),
    ("interview", "interview", [
        'Interview question — how does HashMap work, and when TreeMap?',
        'HashMap — hash buckets, equals for collisions, average O(1).',
        'TreeMap — red-black tree, sorted keys, logarithmic ops.',
        'Call out mutable keys and null differences.',
        'Mention LinkedHashMap if they ask about predictable order.',
        'That answer is solid for junior and mid-level interviews.',
    ]),
    ("teaser", "teaser", [
        'Associations are clear. Next — waiting lines and two-ended queues.',
        'Episode Twenty-Four — Queues and Deques.',
        'FIFO, stacks, and why ArrayDeque wins often.',
        'See you there.',
    ]),
]



def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Keys that find values"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,50))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,50), fill=WHITE)
    pairs=[("userId","42"),("role","ADMIN"),("region","EU")]
    for i,(k,v) in enumerate(pairs):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=280+i*200
        d.rounded_rectangle([280,y,900,y+150], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
        d.text((340,y+50), k, font=font(FONT_MONO,30), fill=mix(BG,ORANGE,a))
        d.rounded_rectangle([1020,y,1640,y+150], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
        d.text((1100,y+50), v, font=font(FONT_MONO,30), fill=mix(BG,BLUE,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 23", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Maps", font(FONT_SERIF,76), H//2-30, mix(BG,WHITE,a)),
        ("HashMap · ordering · null rules", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_contract(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Map Contract", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("key → value","one mapping per key",ORANGE),("not a Collection","separate hierarchy",BLUE),("views","keySet / values / entrySet",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_hashmap(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "HashMap", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.35))
    d.rounded_rectangle([160,200,1760,400], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    d.text((240,270), "default map  ·  average O(1)  ·  allows one null key", font=font(FONT_REG,30), fill=mix(BG,WHITE,a))
    for i,lab in enumerate(["put","get","compute","merge"]):
        aa=ease_out_cubic(clamp((progress-0.25-i*0.1)/0.25))
        if aa<=0: continue
        x=200+i*420
        d.rounded_rectangle([x,520,x+360,780], radius=12, fill=mix(BG,SURFACE,aa), outline=mix(BG,BLUE,aa), width=2)
        d.text((x+90,620), lab, font=font(FONT_MONO_B,34), fill=mix(BG,BLUE,aa))
    return img.convert("RGB")

def render_variants(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Ordering Variants", font=font(FONT_SERIF,46), fill=WHITE)
    rows=[("LinkedHashMap","insertion or access order",GREEN),("TreeMap","sorted keys",ORANGE),("EnumMap","enum keys, compact",BLUE)]
    for i,(k,v,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=200+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_nulls(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Null Rules", font=font(FONT_SERIF,48), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,220,900,820], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,GREEN,left), width=4)
        d.text((220,320), "HashMap", font=font(FONT_BOLD,34), fill=mix(BG,GREEN,left))
        d.text((220,450), "one null key", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
        d.text((220,530), "many null values", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
    if right>0:
        d.rounded_rectangle([1020,220,1780,820], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,RED,right), width=4)
        d.text((1100,320), "TreeMap / Hashtable", font=font(FONT_BOLD,30), fill=mix(BG,RED,right))
        d.text((1100,450), "null keys rejected", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
        d.text((1100,530), "know your impl", font=font(FONT_REG,28), fill=mix(BG,MUTED,right))
    return img.convert("RGB")

def render_modern(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Modern Map APIs", font=font(FONT_SERIF,46), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    lines=["getOrDefault(key, fallback)","computeIfAbsent(key, mappingFn)","merge(key, value, remappingFn)","Map.of(...) — unmodifiable"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((300,300+i*120), line, font=font(FONT_MONO,30), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","Mutable map keys","Immutable key types"),("02","iterate + mutate casually","Use iterator / copy keys"),("03","Hashtable by default","Prefer HashMap + concurrency tools")]
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
    q="How does HashMap work, and when use TreeMap?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,28)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,28),fill=WHITE)
    answers=[("HashMap","buckets + hashCode/equals",ORANGE),("TreeMap","sorted keys, log n",BLUE),("Watch","mutable keys & null rules",GREEN)]
    for i,(k,v,col) in enumerate(answers):
        a=ease_out_cubic(clamp((progress-0.2-i*0.18)/0.3))
        if a<=0: continue
        y=360+i*170
        d.rounded_rectangle([260,y,1660,y+140], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((320,y+45),k,font=font(FONT_BOLD,32),fill=mix(BG,col,a))
        d.text((700,y+50),v,font=font(FONT_REG,28),fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_teaser(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((W//2-120,200), "NEXT EPISODE", font=font(FONT_BOLD,28), fill=MUTED)
    title="Queues & Deques"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,58))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,58), fill=WHITE)
    sub="FIFO · stacks · ArrayDeque"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 24", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")


RENDERERS = {"hook": render_hook, "title": render_title, "contract": render_contract, "hashmap": render_hashmap, "variants": render_variants, "nulls": render_nulls, "modern": render_modern, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 23...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep23_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep23.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep23_narrated.mp4"
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
        paced = OUTPUT / "java_ep23_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_23_Maps.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_23.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_23_Maps_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep23_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_hashmap'), ('00:01:40', '03_variants'), ('00:02:30', '04_modern'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 23: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
