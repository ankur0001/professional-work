#!/usr/bin/env python3
"""Episode 31 — java.time. Narration + visuals authored together."""
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
AUDIO, FRAMES, CLIPS = ROOT / "audio_ep31", ROOT / "frames_ep31", ROOT / "clips_ep31"
VOICE = os.environ.get("KOKORO_VOICE", "am_michael")
SPEED = float(os.environ.get("KOKORO_SPEED", "0.97"))

SCENES = [
    ("hook", "hook", [
        'Optional modeled absence. java.time models moments — without Calendar pain.',
        'Old java.util.Date and Calendar were mutable, confusing, and error-prone.',
        'Java eight introduced java.time — immutable, clear, and ISO-based.',
        'Instant for machine timestamps. LocalDate for birthdays. ZonedDateTime for meetings.',
        'Today — the modern date-time toolkit every Java developer needs.',
        'Time is hard. Good APIs make it less hard.',
    ]),
    ("title", "title", [
        'Episode Thirty-One.',
        'java.time — dates, times, and zones done right.',
    ]),
    ("instant", "instant", [
        'Instant is a point on the UTC timeline.',
        'Machine timestamps — logs, events, database instants.',
        'Instant.now captures the current moment in UTC.',
        'Compare with isBefore and isAfter — natural ordering.',
        'Convert to epoch seconds or millis when legacy APIs require it.',
        'Think Instant when the zone does not matter yet.',
    ]),
    ("zoned", "zoned", [
        'ZonedDateTime ties a local date-time to a time zone.',
        'ZoneId identifies a region — Europe/Paris, America/New_York.',
        'Meetings, flight departures, user-facing clocks need zones.',
        'withZoneSameInstant converts between zones without shifting the instant.',
        'Daylight saving transitions are handled by the rules in ZoneId.',
        'Store Instants in databases — render ZonedDateTime for users.',
    ]),
    ("local", "local", [
        'LocalDate is a calendar date without time or zone.',
        'LocalTime is a time of day without date or zone.',
        'LocalDateTime combines both — still no zone attached.',
        'Birthdays, due dates, business hours templates use local types.',
        'Do not attach a zone until you know which zone.',
        'Parse and format with consistent patterns — DateTimeFormatter.',
    ]),
    ("formatting", "formatting", [
        'DateTimeFormatter replaces SimpleDateFormat for new code.',
        'Predefined constants — ISO_LOCAL_DATE, ISO_INSTANT.',
        'ofPattern for custom layouts — but prefer ISO when possible.',
        'format and parse are symmetric — define once, reuse.',
        'Locale affects human-readable month and day names.',
        'Immutable formatters are thread-safe — share them freely.',
    ]),
    ("chrono", "chrono", [
        'Arithmetic uses clear units — ChronoUnit.DAYS, HOURS, MINUTES.',
        'plus and minus on local and zoned types read naturally.',
        'Period covers calendar amounts — two months, three years.',
        'Duration covers exact time amounts — ninety minutes.',
        'between measures the gap between two points.',
        'Pick Period versus Duration based on calendar versus clock semantics.',
    ]),
    ("mistakes", "mistakes", [
        'Three common mistakes.',
        'One — mixing legacy Date with java.time without explicit conversion.',
        'Two — assuming LocalDateTime has a zone — it does not.',
        'Three — storing zoned strings instead of Instant in the database.',
        'Also — ignoring daylight saving when scheduling recurring events.',
        'Model instants in UTC. Display in the user zone.',
    ]),
    ("interview", "interview", [
        'Interview question — Instant versus LocalDateTime?',
        'Instant — absolute point on the UTC timeline.',
        'LocalDateTime — date and time without zone context.',
        'Mention ZonedDateTime when user zones matter.',
        'Note immutability and DateTimeFormatter for parsing.',
        'That answer shows you escaped the Date era.',
    ]),
    ("teaser", "teaser", [
        'Time is typed. Next — when things go wrong.',
        'Episode Thirty-Two — Exceptions.',
        'Checked, unchecked, and handling failure with intent.',
        'See you there.',
    ]),
]


def render_hook(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    title = "Time, typed clearly"
    bbox = d.textbbox((0,0), title, font=font(FONT_SERIF,50))
    d.text(((W-(bbox[2]-bbox[0]))//2, 120), title, font=font(FONT_SERIF,50), fill=WHITE)
    for i,(lab,col) in enumerate([("Instant",ORANGE),("LocalDate",BLUE),("Zoned",GREEN)]):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        x=280+i*520
        d.rounded_rectangle([x,400,x+420,720], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((x+60,520), lab, font=font(FONT_BOLD,30), fill=mix(BG,col,a))
    return img.convert("RGB")

def render_title(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    a=ease_out_cubic(clamp(progress*1.3)); lw=int(240*a)
    d.rectangle([(W-lw)//2,H//2-50,(W+lw)//2,H//2-46], fill=ORANGE)
    for txt,fnt,y,col in [
        ("EPISODE 31", font(FONT_BOLD,28), H//2-140, mix(BG,MUTED,a)),
        ("java.time", font(FONT_SERIF,68), H//2-30, mix(BG,WHITE,a)),
        ("Instant · Local · Zoned", font(FONT_REG,30), H//2+70, mix(BG,MUTED,a)),
    ]:
        bbox=d.textbbox((0,0),txt,font=fnt); d.text(((W-(bbox[2]-bbox[0]))//2,y),txt,font=fnt,fill=col)
    return img.convert("RGB")

def render_instant(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Instant — UTC Timeline", font=font(FONT_SERIF,44), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([200,220,1720,800], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,ORANGE,a), width=3)
    lines=["Instant.now()","epoch seconds / millis","isBefore / isAfter","logs · events · DB timestamps"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((320,320+i*110), line, font=font(FONT_MONO,30), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_zoned(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "ZonedDateTime", font=font(FONT_SERIF,46), fill=WHITE)
    items=[("ZoneId","Europe/Paris · America/New_York",ORANGE),("withZoneSameInstant","same moment, new zone",BLUE),("user-facing","meetings · flights",GREEN)]
    for i,(k,v,col) in enumerate(items):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_BOLD,34), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_local(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Local Types", font=font(FONT_SERIF,46), fill=WHITE)
    rows=[("LocalDate","calendar date only",ORANGE),("LocalTime","time of day only",BLUE),("LocalDateTime","date + time, no zone",GREEN)]
    for i,(k,v,col) in enumerate(rows):
        a=ease_out_cubic(clamp((progress-i*0.18)/0.3))
        if a<=0: continue
        y=220+i*220
        d.rounded_rectangle([200,y,1720,y+180], radius=14, fill=mix(BG,SURFACE,a), outline=mix(BG,col,a), width=3)
        d.text((280,y+40), k, font=font(FONT_MONO,32), fill=mix(BG,col,a))
        d.text((280,y+100), v, font=font(FONT_REG,28), fill=mix(BG,WHITE,a))
    return img.convert("RGB")

def render_formatting(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "DateTimeFormatter", font=font(FONT_SERIF,44), fill=WHITE)
    a=ease_out_cubic(clamp(progress/0.4))
    d.rounded_rectangle([180,200,1740,840], radius=16, fill=mix(BG,SURFACE,a), outline=mix(BG,BLUE,a), width=3)
    lines=["DateTimeFormatter.ISO_LOCAL_DATE","DateTimeFormatter.ofPattern(\"yyyy-MM-dd\")","formatter.format(date)","type.parse(text)"]
    for i,line in enumerate(lines):
        aa=ease_out_cubic(clamp((progress-i*0.12)/0.28))
        d.text((280,300+i*120), line, font=font(FONT_MONO,28), fill=mix(BG,WHITE,aa))
    return img.convert("RGB")

def render_chrono(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,60), "Period & Duration", font=font(FONT_SERIF,44), fill=WHITE)
    left=ease_out_cubic(clamp(progress/0.4)); right=ease_out_cubic(clamp((progress-0.3)/0.4))
    if left>0:
        d.rounded_rectangle([140,220,900,820], radius=18, fill=mix(BG,SURFACE,left), outline=mix(BG,ORANGE,left), width=4)
        d.text((220,280), "Period", font=font(FONT_BOLD,32), fill=mix(BG,ORANGE,left))
        d.text((240,380), "calendar amounts", font=font(FONT_REG,28), fill=mix(BG,WHITE,left))
        d.text((240,460), "2 months, 3 years", font=font(FONT_MONO,26), fill=mix(BG,MUTED,left))
    if right>0:
        d.rounded_rectangle([1020,220,1780,820], radius=18, fill=mix(BG,SURFACE,right), outline=mix(BG,BLUE,right), width=4)
        d.text((1100,280), "Duration", font=font(FONT_BOLD,32), fill=mix(BG,BLUE,right))
        d.text((1120,380), "exact time amounts", font=font(FONT_REG,28), fill=mix(BG,WHITE,right))
        d.text((1120,460), "90 minutes, 5 hours", font=font(FONT_MONO,26), fill=mix(BG,MUTED,right))
    return img.convert("RGB")

def render_mistakes(progress, t):
    img = base_canvas(t); d = ImageDraw.Draw(img)
    d.text((160,70), "Common Mistakes", font=font(FONT_SERIF,48), fill=WHITE)
    items=[("01","mix Date + java.time","Explicit conversion"),("02","zone on LocalDateTime","Use ZonedDateTime"),("03","zoned strings in DB","Store Instant UTC")]
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
    q="Instant vs LocalDateTime?"
    bbox=d.textbbox((0,0),q,font=font(FONT_BOLD,32)); d.text(((W-(bbox[2]-bbox[0]))//2,190),q,font=font(FONT_BOLD,32),fill=WHITE)
    answers=[("Instant","UTC timeline point",ORANGE),("LocalDateTime","no zone attached",BLUE),("ZonedDateTime","user-facing clock",GREEN)]
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
    title="Exceptions"; bbox=d.textbbox((0,0),title,font=font(FONT_SERIF,58))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2-40), title, font=font(FONT_SERIF,58), fill=WHITE)
    sub="checked · unchecked · handling failure"; bbox=d.textbbox((0,0),sub,font=font(FONT_REG,30))
    d.text(((W-(bbox[2]-bbox[0]))//2, H//2+60), sub, font=font(FONT_REG,30), fill=BLUE)
    d.text((W//2-90, H//2+150), "Episode 32", font=font(FONT_BOLD,30), fill=ORANGE)
    return img.convert("RGB")

RENDERERS = {"hook": render_hook, "title": render_title, "instant": render_instant, "zoned": render_zoned, "local": render_local, "formatting": render_formatting, "chrono": render_chrono, "mistakes": render_mistakes, "interview": render_interview, "teaser": render_teaser}

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
    print("==> Kokoro Episode 31...")
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    for i, (sid, _, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {sid}"); synth_scene_audio(pipeline, sid, beats)
    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    print(f"==> Spoken ≈ {(sum(durations.values()) + 0.25*len(SCENES))/60:.2f} min")
    (ROOT / "ep31_durations.json").write_text(json.dumps(durations, indent=2))
    outs = [render_scene_clip(sid, r, durations[sid]) for sid, r, _ in SCENES]
    lst = ROOT / "concat_ep31.txt"
    with open(lst, "w") as f:
        for p in outs: f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep31_narrated.mp4"
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
        paced = OUTPUT / "java_ep31_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(["ffmpeg", "-y", "-i", str(narrated), "-filter_complex", f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(paced)], check=True)
        base = paced
    final = OUTPUT / "Java_Episode_31_Java_Time.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(base), "-i", str(music), "-filter_complex", "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", str(final)], check=True)
    shutil.copy2(final, ARTIFACTS / final.name)
    srt = OUTPUT / "Java_Episode_31.srt"; write_srt(durations, srt); shutil.copy2(srt, ARTIFACTS / srt.name)
    burned = OUTPUT / "Java_Episode_31_Java_Time_CAPTIONED.mp4"
    subprocess.run(["ffmpeg", "-y", "-i", str(final), "-vf", f"subtitles={srt}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-movflags", "+faststart", str(burned)], check=True)
    shutil.copy2(burned, ARTIFACTS / burned.name)
    vdir = ARTIFACTS / "ep31_verify"; vdir.mkdir(exist_ok=True)
    for ts, name in [('00:00:12', '01_hook'), ('00:00:50', '02_instant'), ('00:01:40', '03_local'), ('00:02:30', '04_chrono'), ('00:03:20', '05_interview')]:
        subprocess.run(["ffmpeg","-y","-ss",ts,"-i",str(final),"-frames:v","1",str(vdir/f"{name}.jpg")], capture_output=True)
    final_dur = probe(final)
    print(f"DONE Episode 31: {final_dur/60:.2f} min")
    assert 240 <= final_dur <= 330, f"duration {final_dur:.1f}s"


if __name__ == "__main__":
    main()
