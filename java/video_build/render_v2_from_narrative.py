#!/usr/bin/env python3
"""Render The Java Story v2 videos from coherent narrative markdown.

Output layout (common across episode PRs):
  java/output/v2/Java_Episode_XX_<Slug>.mp4
  java/output/v2/Java_Episode_XX_<Slug>_CAPTIONED.mp4
  java/output/v2/Java_Episode_XX.srt
  java/output/v2/SOURCE.md   (pointer to narrative used)

Usage:
  python3 java/video_build/render_v2_from_narrative.py --ep 1
  python3 java/video_build/render_v2_from_narrative.py --ep 1-5
  python3 java/video_build/render_v2_from_narrative.py --all
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/workspace")
NARR_DIR = ROOT / "java" / "narrative_review" / "episodes"
BUILD = ROOT / "java" / "video_build"
WORK = BUILD / "v2_work"
OUT = ROOT / "java" / "output" / "v2"
SYS_PATH_TTS = BUILD

W, H = 1920, 1080
BG = (13, 17, 23)
SURFACE = (22, 27, 34)
ORANGE = (248, 152, 32)
BLUE = (74, 158, 255)
WHITE = (255, 255, 255)
MUTED = (139, 148, 158)
ACCENT = (248, 152, 32)

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

sys.path.insert(0, str(SYS_PATH_TTS))
from chatterbox_tts import SAMPLE_RATE, synth_beat  # noqa: E402


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)


def slugify(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return s[:60] or "Episode"


def parse_narrative(path: Path) -> tuple[int, str, str]:
    text = path.read_text()
    m = re.search(r"^# Episode (\d+) — (.+)$", text, re.M)
    if not m:
        raise ValueError(f"No episode header in {path}")
    ep = int(m.group(1))
    title = m.group(2).strip()
    body_m = re.search(r"## Full narration\n\n(.*?)(?:\n## Source|\Z)", text, re.S)
    if not body_m:
        raise ValueError(f"No Full narration in {path}")
    body = body_m.group(1).strip()
    # Strip fenced code for spoken narration; keep a short spoken cue instead
    def _code_repl(match: re.Match) -> str:
        lang = (match.group(1) or "").strip()
        code = match.group(2).strip().splitlines()
        preview = code[0][:80] if code else ""
        if lang.lower() in {"java", "bash", "text", ""}:
            return f" Look at this {lang or 'code'} for a moment. "
        return f" Look at this example. {preview} "

    spoken = re.sub(r"```(\w*)\n(.*?)```", _code_repl, body, flags=re.S)
    spoken = re.sub(r"`([^`]+)`", r"\1", spoken)
    spoken = re.sub(r"\*\*([^*]+)\*\*", r"\1", spoken)
    spoken = re.sub(r"\s+", " ", spoken).strip()
    return ep, title, spoken


def split_beats(spoken: str, max_chars: int = 220) -> list[str]:
    # Sentence-ish splits, then pack to max_chars
    parts = re.split(r"(?<=[.!?])\s+", spoken)
    beats: list[str] = []
    buf = ""
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if len(part) > max_chars:
            if buf:
                beats.append(buf)
                buf = ""
            # split long part on commas/semicolons
            chunks = re.split(r"(?<=[,;:])\s+", part)
            cur = ""
            for ch in chunks:
                if len(cur) + len(ch) + 1 <= max_chars:
                    cur = f"{cur} {ch}".strip()
                else:
                    if cur:
                        beats.append(cur)
                    if len(ch) <= max_chars:
                        cur = ch
                    else:
                        for i in range(0, len(ch), max_chars):
                            beats.append(ch[i : i + max_chars])
                        cur = ""
            if cur:
                beats.append(cur)
            continue
        if len(buf) + len(part) + 1 <= max_chars:
            buf = f"{buf} {part}".strip()
        else:
            if buf:
                beats.append(buf)
            buf = part
    if buf:
        beats.append(buf)
    return beats


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:8]


def make_slide(ep: int, title: str, beat: str, idx: int, total: int) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # top bar
    draw.rectangle([0, 0, W, 8], fill=ORANGE)
    draw.rectangle([0, H - 8, W, H], fill=SURFACE)
    # brand
    fb = font(FONT_BOLD, 36)
    fr = font(FONT_REG, 28)
    draw.text((80, 48), "The Java Story", font=fb, fill=ORANGE)
    draw.text((80, 100), f"Episode {ep:02d}  ·  {title}", font=fr, fill=MUTED)
    # progress
    prog = (idx + 1) / max(total, 1)
    draw.rectangle([80, 150, W - 80, 158], fill=SURFACE)
    draw.rectangle([80, 150, 80 + int((W - 160) * prog), 158], fill=BLUE)
    # body card
    draw.rounded_rectangle([80, 200, W - 80, H - 120], radius=24, fill=SURFACE)
    body_font = font(FONT_REG, 44)
    lines = wrap_text(draw, beat, body_font, W - 220)
    y = 260
    for line in lines:
        draw.text((120, y), line, font=body_font, fill=WHITE)
        y += 64
    # footer
    draw.text((80, H - 70), f"{idx + 1} / {total}", font=font(FONT_REG, 24), fill=MUTED)
    draw.text((W - 320, H - 70), "v2 narrative cut", font=font(FONT_REG, 24), fill=MUTED)
    return img


def probe(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def synth_episode_audio(beats: list[str], audio_dir: Path) -> tuple[Path, list[tuple[float, float, str]]]:
    audio_dir.mkdir(parents=True, exist_ok=True)
    wavs: list[Path] = []
    cues: list[tuple[float, float, str]] = []
    t = 0.0
    for i, beat in enumerate(beats):
        print(f"    TTS {i+1}/{len(beats)}: {beat[:70]}")
        wav = audio_dir / f"b{i:04d}.wav"
        audio = synth_beat(beat)
        sf.write(str(wav), audio, SAMPLE_RATE)
        dur = len(audio) / SAMPLE_RATE
        cues.append((t, t + dur, beat))
        wavs.append(wav)
        # short gap
        if i < len(beats) - 1:
            gap = 0.18 if beat.endswith("?") else 0.12
            sil = audio_dir / f"s{i:04d}.wav"
            sf.write(str(sil), np.zeros(int(gap * SAMPLE_RATE), dtype=np.float32), SAMPLE_RATE)
            wavs.append(sil)
            t += dur + gap
        else:
            t += dur
    lst = audio_dir / "concat.txt"
    with open(lst, "w") as f:
        for p in wavs:
            f.write(f"file '{p}'\n")
    out = audio_dir / "narration.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:a", "libmp3lame", "-q:a", "2", str(out)],
        check=True,
        capture_output=True,
    )
    return out, cues


def write_srt(cues: list[tuple[float, float, str]], path: Path) -> None:
    def ts(sec: float) -> str:
        h = int(sec // 3600)
        m = int((sec % 3600) // 60)
        s = int(sec % 60)
        ms = int((sec - int(sec)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, (a, b, text) in enumerate(cues, 1):
        wrapped = "\n".join(textwrap.wrap(text, width=42)[:3])
        lines.append(f"{i}\n{ts(a)} --> {ts(b)}\n{wrapped}\n")
    path.write_text("\n".join(lines))


def build_video(ep: int, title: str, beats: list[str], cues, narration: Path, work: Path, out_mp4: Path) -> None:
    slides = work / "slides"
    clips = work / "clips"
    if slides.exists():
        shutil.rmtree(slides)
    if clips.exists():
        shutil.rmtree(clips)
    slides.mkdir(parents=True)
    clips.mkdir(parents=True)

    # map each beat duration from cues
    for i, beat in enumerate(beats):
        start, end, _ = cues[i]
        dur = max(end - start, 0.8)
        img = make_slide(ep, title, beat, i, len(beats))
        jpg = slides / f"s{i:04d}.jpg"
        img.save(jpg, quality=90)
        clip = clips / f"c{i:04d}.mp4"
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-loop", "1", "-i", str(jpg),
                "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
                "-t", f"{dur:.3f}",
                "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest",
                str(clip),
            ],
            check=True,
            capture_output=True,
        )

    clist = work / "clips.txt"
    with open(clist, "w") as f:
        for i in range(len(beats)):
            f.write(f"file '{clips / f'c{i:04d}.mp4'}'\n")
    silent = work / "silent.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(clist), "-c", "copy", str(silent)],
        check=True,
        capture_output=True,
    )
    # mux narration
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-i", str(silent),
            "-i", str(narration),
            "-c:v", "copy",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-map", "0:v:0", "-map", "1:a:0",
            str(out_mp4),
        ],
        check=True,
        capture_output=True,
    )


def burn_captions(mp4: Path, srt: Path, out: Path) -> None:
    # ffmpeg subtitles filter needs escaped path
    srt_esc = str(srt).replace(":", "\\:").replace("'", "\\'")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(mp4),
            "-vf", f"subtitles={srt_esc}:force_style='FontSize=22,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
            "-c:a", "copy",
            str(out),
        ],
        check=True,
        capture_output=True,
    )


def render_one(path: Path) -> dict:
    ep, title, spoken = parse_narrative(path)
    beats = split_beats(spoken)
    print(f"==> EP{ep:02d} {title}: {len(beats)} beats, ~{len(spoken.split())} words")
    work = WORK / f"ep{ep:02d}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    audio_dir = work / "audio"
    narration, cues = synth_episode_audio(beats, audio_dir)
    # cues currently include gaps incorrectly for video; rebuild cues aligned to beats only
    # Re-probe each beat wav for accurate durations
    t = 0.0
    cues2: list[tuple[float, float, str]] = []
    for i, beat in enumerate(beats):
        wav = audio_dir / f"b{i:04d}.wav"
        dur = probe(wav)
        gap = 0.18 if beat.endswith("?") else 0.12
        if i == len(beats) - 1:
            gap = 0.0
        cues2.append((t, t + dur, beat))
        t += dur + gap

    slug = slugify(title)
    OUT.mkdir(parents=True, exist_ok=True)
    base = f"Java_Episode_{ep:02d}_{slug}"
    mp4 = OUT / f"{base}.mp4"
    cap = OUT / f"{base}_CAPTIONED.mp4"
    srt = OUT / f"Java_Episode_{ep:02d}.srt"
    write_srt(cues2, srt)
    build_video(ep, title, beats, cues2, narration, work, mp4)
    burn_captions(mp4, srt, cap)
    # per-episode source pointer
    src = OUT / f"Java_Episode_{ep:02d}_SOURCE.md"
    src.write_text(
        f"# v2 source\n\nEpisode {ep:02d}: {title}\n\n"
        f"Narration: `java/narrative_review/episodes/{path.name}`\n"
        f"Renderer: `java/video_build/render_v2_from_narrative.py`\n"
        f"TTS: local Chatterbox Turbo\n"
    )
    dur = probe(mp4)
    print(f"    wrote {mp4.name} ({dur/60:.1f} min)")
    return {"ep": ep, "title": title, "beats": len(beats), "duration_sec": dur, "mp4": str(mp4)}


def episode_files(spec: str) -> list[Path]:
    files = sorted(NARR_DIR.glob("ep*.md"))
    by_n = {int(p.name[2:4]): p for p in files}
    if spec == "all":
        return [by_n[n] for n in sorted(by_n)]
    out: list[Path] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            for n in range(int(a), int(b) + 1):
                out.append(by_n[n])
        else:
            out.append(by_n[int(part)])
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ep", default="", help="e.g. 1 or 1-5 or 1,4,7 or all")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    spec = "all" if args.all or args.ep in {"", "all"} and args.all else (args.ep or "")
    if args.all:
        spec = "all"
    if not spec:
        ap.error("pass --ep N or --all")
    results = []
    for path in episode_files(spec):
        results.append(render_one(path))
    (OUT / "v2_manifest.json").write_text(json.dumps(results, indent=2))
    print("DONE", len(results), "episodes ->", OUT)


if __name__ == "__main__":
    main()
