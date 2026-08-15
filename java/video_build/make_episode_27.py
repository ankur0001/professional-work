#!/usr/bin/env python3
"""Episode 27 — Stream Collectors. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep27", ROOT / "frames_ep27", ROOT / "clips_ep27"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Streams build pipelines. Collectors decide the shape of the answer.',
        'List, Set, Map, string, summary — same stream, different endings.',
        'groupingBy and partitioningBy turn flat data into structure.',
        'Downstream collectors nest work inside each group.',
        'Today — finish pipelines with intent, not afterthoughts.',
        'Collect is not dump. Collect is design.',
    ]),
    ("title", "title", [
        'Episode Twenty-Seven.',
        'Stream Collectors — shaping results.',
    ]),
    ("basics", "basics", [
        'Start with the basics in Collectors.',
        'toList and toSet materialize elements.',
        'toMap needs a key function, a value function, and often a merge function.',
        'Duplicate keys without a merge function throw — loudly.',
        'joining builds delimited strings without manual StringBuilder noise.',
        'Pick the collector that matches the type you need next.',
    ]),
    ("grouping", "grouping", [
        'groupingBy is the workhorse for classification.',
        'A classifier function produces keys.',
        'By default each key maps to a List of matching elements.',
        'Orders by region. Users by status. Events by day.',
        'You get a Map whose values are groups — ready for reports.',
        'Think pivot table — expressed as a pipeline.',
    ]),
    ("partition", "partition", [
        'partitioningBy is groupingBy for a boolean question.',
        'Predicate true goes one side. False the other.',
        'The result is Map of Boolean to the grouped values.',
        'Active versus inactive. Valid versus invalid. Paid versus unpaid.',
        'Two buckets — when two is exactly the model.',
        'Do not use it when you really needed many keys.',
    ]),
    ("downstream", "downstream", [
        'Downstream collectors avoid second passes.',
        'groupingBy with counting gives sizes per key.',
        'summingInt and averagingDouble summarize in place.',
        'mapping then toSet reshapes each group.',
        'collectingAndThen applies a finisher — like making the map unmodifiable.',
        'Nest the work. Keep the pipeline honest.',
    ]),
    ("reduce", "reduce", [
        'Beyond grouping — reducing and summarizing.',
        'reducing folds with an identity and an operator.',
        'summarizingInt returns count, sum, min, max, and average together.',
        'teeing runs two collectors and merges their results — Java sixteen and later.',
        'Use summaries when dashboards need several stats at once.',
        'Collectors are a toolbox — learn the shapes, not every overload by heart.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — toMap without a merge function when duplicates exist.',
        'Two — mutating shared accumulators and hoping parallel collect survives.',
        'Three — groupingBy then a manual loop that a downstream collector already covers.',
        'Also — assuming toList is always unmodifiable — know your Java version.',
        'Clear collectors beat clever post-processing.',
    ]),
    ("interview", "interview", [
        'Interview question — groupingBy versus partitioningBy?',
        'groupingBy — many keys from a classifier function.',
        'partitioningBy — boolean predicate, always two sides.',
        'Mention downstream collectors for counting or summing inside groups.',
        'Give a domain example — orders by region versus paid versus unpaid.',
        'That answer shows practical stream fluency.',
    ]),
    ("teaser", "teaser", [
        'Results have shape. Next — expanding elements inside the pipeline.',
        'Episode Twenty-Eight — flatMap and composition.',
        'One-to-many transforms without nested collections mess.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Shape the result"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,50))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,50), fill=WHITE)
    for i,(lab,col) in enumerate([("stream",ORANGE),("collect",BLUE),("List / Map",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        x=200+i*540
        d.rounded_rectangle([x,400,x+460,720], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+60,520), lab, font=font(FONT_BOLD,30), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(260*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 27", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("Stream Collectors", font(FONT_SERIF,60), H//2-30, mix(BG,WHITE,a)),
        ("grouping · partitioning · downstream", font(FONT_REG,28), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_basics(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Basic Collectors", font=font(FONT_SERIF,46), fill=WHITE)
    items=[("toList / toSet","materialize a collection",ORANGE),("toMap","keys, values, merge fn",BLUE),("joining","strings without builders",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_grouping(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "groupingBy", font=font(FONT_SERIF,48), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.35))
    d.rounded_rectangle([160,200,1760,400], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    d.text((240,270), "classifier → Map<K, List<T>>", font=font(FONT_MONO,32), fill=mix(BG,WHITE,a))
    for i,(k,v) in enumerate([("EU","3 orders"),("US","5 orders"),("APAC","2 orders")]):
        aa=ease_out_cubic(clamp((progress-0.25-i*0.12)/0.25))
        if aa<=0: continue
        x=220+i*540
        d.rounded_rectangle([x,500,x+460,820], radius=12, fill=mix(BG,SURFACE,aa), outline=mix(BG,BLUE,aa), width=2)
        d.text((x+140,580), k, font=font(FONT_BOLD,34), fill=mix(BG,BLUE,aa))
        d.text((x+120,680), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_partition(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "partitioningBy", font=font(FONT_SERIF,46), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,240,900,800], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,GREEN,left), width=4)
        d.text((380,400), "true", font=font(FONT_BOLD,40), fill=mix(BG,GREEN,left))
        d.text((240,520), "predicate matches", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
    if right>0:
        d.rounded_rectangle([1020,240,1780,800], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,RED,right), width=4)
        d.text((1180,400), "false", font=font(FONT_BOLD,40), fill=mix(BG,RED,right))
        d.text((1120,520), "everything else", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
    return img.convert("RGB")

def render_downstream(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Downstream Collectors", font=font(FONT_SERIF,44), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    lines=["groupingBy(region, counting())","groupingBy(region, summingInt(...))","groupingBy(region, mapping(..., toSet()))","collectingAndThen(...) for finishers"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((280,300+i*120), line, font=font(FONT_MONO,28), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_reduce(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "reducing & summarizing", font=font(FONT_SERIF,44), fill=WHITE)
    rows=[("reducing","custom fold with identity",ORANGE),("summarizingInt","count / sum / min / max / avg",GREEN),("teeing","two collectors → one result",BLUE)]
    for i,(k,v,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","toMap duplicate keys","Provide a merge function"),("02","mutable accumulators in parallel","Use proper collectors"),("03","grouping then manual loop","Use a downstream collector")]
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
    q="groupingBy vs partitioningBy — when each?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,28)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,28),fill=WHITE)
    answers=[("groupingBy","many keys from classifier",ORANGE),("partitioningBy","boolean split",BLUE),("Downstream","count/sum inside groups",GREEN)]
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
    title="flatMap & Composition"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,54))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,54), fill=WHITE)
    sub="one-to-many · flatten · readable pipelines"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,28))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,28), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 28", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {"hook": render_hook, "title": render_title, "basics": render_basics, "grouping": render_grouping, "partition": render_partition, "downstream": render_downstream, "reduce": render_reduce, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 27...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep27_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep27.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep27_narrated.mp4"
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
        paced = OUTPUT / "java_ep27_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_27_Stream_Collectors.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_27.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_27_Stream_Collectors_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep27_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_ops'), ('00:01:40', '03_lazy'), ('00:02:30', '04_collect'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 27: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
