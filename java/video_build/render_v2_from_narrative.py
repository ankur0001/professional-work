#!/usr/bin/env python3
"""Render The Java Story v2 videos from coherent narrative markdown.

Animated visual cut: flows, stacks, pipelines, lanes, diagrams — not
text-wall slides. Narration audio stays Chatterbox TTS (unchanged text).

Output layout (common across episode PRs):
  java/output/v2/Java_Episode_XX_<Slug>.mp4
  java/output/v2/Java_Episode_XX_<Slug>_CAPTIONED.mp4
  java/output/v2/Java_Episode_XX.srt
  java/output/v2/SOURCE.md

Usage:
  python3 java/video_build/render_v2_from_narrative.py --ep 1
  python3 java/video_build/render_v2_from_narrative.py --ep 1-5 --reuse-audio
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
FPS = 8.0

FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

sys.path.insert(0, str(SYS_PATH_TTS))
from chatterbox_tts import SAMPLE_RATE, synth_beat  # noqa: E402
from visual_engine import render_beat_frames  # noqa: E402


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
    """Legacy single-frame preview (first frame of animated beat)."""
    frames = render_beat_frames(ep, title, beat, idx, total, duration=1.0, fps=1.0)
    return frames[0]


def probe(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def parse_srt(path: Path) -> list[tuple[float, float, str]]:
    text = path.read_text(errors="replace")
    blocks = re.split(r"\n\s*\n", text.strip())
    cues: list[tuple[float, float, str]] = []

    def parse_ts(ts: str) -> float:
        h, m, rest = ts.split(":")
        s, ms = rest.replace(",", ".").split(".")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0

    for block in blocks:
        lines = [ln for ln in block.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue
        # skip index line if present
        if "-->" not in lines[0] and len(lines) >= 2 and "-->" in lines[1]:
            lines = lines[1:]
        if "-->" not in lines[0]:
            continue
        a, b = [p.strip() for p in lines[0].split("-->")]
        body = " ".join(lines[1:]).replace("\n", " ").strip()
        cues.append((parse_ts(a), parse_ts(b), body))
    return cues


def find_existing_mp4(ep: int) -> Path | None:
    matches = sorted(OUT.glob(f"Java_Episode_{ep:02d}_*_CAPTIONED.mp4"))
    if matches:
        return matches[0]
    matches = sorted(OUT.glob(f"Java_Episode_{ep:02d}_*.mp4"))
    matches = [p for p in matches if "CAPTIONED" not in p.name]
    return matches[0] if matches else None


def extract_audio_from_mp4(mp4: Path, out_mp3: Path) -> Path:
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp4), "-vn", "-c:a", "libmp3lame", "-q:a", "2", str(out_mp3)],
        check=True,
        capture_output=True,
    )
    return out_mp3


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


def encode_clip_from_frames(frames: list[Image.Image], clip: Path, duration: float, fps: float = FPS) -> None:
    frames_dir = clip.with_suffix("").parent / f"_frames_{clip.stem}"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir(parents=True)
    for i, fr in enumerate(frames):
        fr.save(frames_dir / f"f{i:04d}.jpg", quality=88)
    # Hold last frame to fill full beat duration if frame count is capped.
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", str(frames_dir / "f%04d.jpg"),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-vf", "tpad=stop_mode=clone:stop=-1",
            "-t", f"{duration:.3f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast", "-crf", "20",
            "-c:a", "aac", "-shortest",
            str(clip),
        ],
        check=True,
        capture_output=True,
    )
    shutil.rmtree(frames_dir, ignore_errors=True)


def build_video(ep: int, title: str, beats: list[str], cues, narration: Path, work: Path, out_mp4: Path) -> None:
    clips = work / "clips"
    if clips.exists():
        shutil.rmtree(clips)
    clips.mkdir(parents=True)

    for i, beat in enumerate(beats):
        start, end, _ = cues[i]
        dur = max(end - start, 0.8)
        print(f"    VISUAL {i+1}/{len(beats)} ({dur:.1f}s)")
        frames = render_beat_frames(ep, title, beat, i, len(beats), duration=dur, fps=FPS)
        clip = clips / f"c{i:04d}.mp4"
        encode_clip_from_frames(frames, clip, duration=dur, fps=FPS)

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
    srt_esc = str(srt).replace(":", "\\:").replace("'", "\\'")
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(mp4),
            "-vf", f"subtitles={srt_esc}:force_style='FontSize=20,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BorderStyle=3,Outline=1,Shadow=0,MarginV=36'",
            "-c:a", "copy",
            str(out),
        ],
        check=True,
        capture_output=True,
    )


def render_one(path: Path, reuse_audio: bool = False, max_beats: int | None = None) -> dict:
    ep, title, spoken = parse_narrative(path)
    beats = split_beats(spoken)
    if max_beats is not None:
        beats = beats[:max_beats]
    print(f"==> EP{ep:02d} {title}: {len(beats)} beats, ~{len(spoken.split())} words")
    work = WORK / f"ep{ep:02d}"
    # keep audio dir if reusing
    audio_dir = work / "audio"
    if work.exists() and not reuse_audio:
        shutil.rmtree(work)
        work.mkdir(parents=True)
    elif not work.exists():
        work.mkdir(parents=True)

    srt = OUT / f"Java_Episode_{ep:02d}.srt"
    narration = audio_dir / "narration.mp3"
    cues2: list[tuple[float, float, str]]

    if reuse_audio and srt.exists() and (narration.exists() or find_existing_mp4(ep)):
        print("    reusing existing audio + SRT timings")
        if not narration.exists():
            mp4_src = find_existing_mp4(ep)
            assert mp4_src is not None
            extract_audio_from_mp4(mp4_src, narration)
        cues2 = parse_srt(srt)
        if max_beats is not None:
            cues2 = cues2[:max_beats]
        # align beat count: if mismatch, prefer SRT texts as beats for visuals
        if len(cues2) != len(beats):
            print(f"    note: beats {len(beats)} vs srt {len(cues2)} — using SRT texts for visuals")
            beats = [c[2] for c in cues2]
        # trim narration to preview end if max_beats
        if max_beats is not None and cues2:
            end_t = cues2[-1][1] + 0.15
            trimmed = audio_dir / "narration_trim.mp3"
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(narration), "-t", f"{end_t:.3f}", "-c:a", "libmp3lame", "-q:a", "2", str(trimmed)],
                check=True,
                capture_output=True,
            )
            narration = trimmed
    else:
        if audio_dir.exists():
            shutil.rmtree(audio_dir)
        narration, cues = synth_episode_audio(beats, audio_dir)
        t = 0.0
        cues2 = []
        for i, beat in enumerate(beats):
            wav = audio_dir / f"b{i:04d}.wav"
            dur = probe(wav)
            gap = 0.18 if beat.endswith("?") else 0.12
            if i == len(beats) - 1:
                gap = 0.0
            cues2.append((t, t + dur, beat))
            t += dur + gap
        if max_beats is None:
            write_srt(cues2, srt)

    slug = slugify(title)
    OUT.mkdir(parents=True, exist_ok=True)
    base = f"Java_Episode_{ep:02d}_{slug}"
    if max_beats is not None:
        base = f"{base}_PREVIEW"
    mp4 = OUT / f"{base}.mp4"
    cap = OUT / f"{base}_CAPTIONED.mp4"
    build_video(ep, title, beats, cues2, narration, work, mp4)
    preview_srt = work / "preview.srt" if max_beats is not None else srt
    if max_beats is not None:
        write_srt(cues2, preview_srt)
    burn_captions(mp4, preview_srt if max_beats is not None else srt, cap)
    src = OUT / f"Java_Episode_{ep:02d}_SOURCE.md"
    src.write_text(
        f"# v2 source\n\nEpisode {ep:02d}: {title}\n\n"
        f"Narration: `java/narrative_review/episodes/{path.name}`\n"
        f"Renderer: `java/video_build/render_v2_from_narrative.py`\n"
        f"Visuals: animated scenes via `java/video_build/visual_engine.py`\n"
        f"TTS: local Chatterbox Turbo (narration text unchanged)\n"
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
    ap.add_argument(
        "--reuse-audio",
        action="store_true",
        help="Rebuild visuals only; keep existing narration audio + SRT timings",
    )
    ap.add_argument("--max-beats", type=int, default=None, help="Smoke/preview: only first N beats")
    args = ap.parse_args()
    spec = "all" if args.all or args.ep in {"", "all"} and args.all else (args.ep or "")
    if args.all:
        spec = "all"
    if not spec:
        ap.error("pass --ep N or --all")
    results = []
    for path in episode_files(spec):
        results.append(render_one(path, reuse_audio=args.reuse_audio, max_beats=args.max_beats))
    (OUT / "v2_manifest.json").write_text(json.dumps(results, indent=2))
    print("DONE", len(results), "episodes ->", OUT)


if __name__ == "__main__":
    main()
