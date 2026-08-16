#!/usr/bin/env python3
"""
4–5 minute condensed Java Episode 1 — local Chatterbox Turbo narration.

Same short-cut SCENES / visuals as make_short_episode.py, but TTS is free
local Chatterbox (no Kokoro / Sarvam / ElevenLabs).
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf

from chatterbox_tts import SAMPLE_RATE, synth_beat as cb_synth
from humanize_audio import generate_music_bed, probe

ROOT = Path("/workspace/video_build")
AUDIO = ROOT / "audio_chatterbox_short"
CLIPS_IN = ROOT / "clips"
CLIPS_OUT = ROOT / "clips_chatterbox_short"
OUTPUT = Path("/workspace/output")
ARTIFACTS = Path("/opt/cursor/artifacts")

# Target ~4–5 min spoken — identical beats to make_short_episode.SCENES
SCENES: list[tuple[str, str, list[str]]] = [
    (
        "hook",
        "hook",
        [
            "Okay… imagine this.",
            "Banks. Airlines. Stock exchanges. Android apps. Enterprise software.",
            "Nearly all of them depend on one programming language.",
            "That language is Java.",
        ],
    ),
    (
        "question",
        "question",
        [
            "But here's what I find fascinating.",
            "Java was born in the nineteen nineties.",
            "Hundreds of languages came and went.",
            "Java stayed.",
            "So why? Let's find out — in the next few minutes.",
        ],
    ),
    (
        "cpp_pain",
        "cpp_pain",
        [
            "Go back to the early nineties.",
            "At Sun Microsystems, James Gosling's team started with C++.",
            "C++ was powerful — no doubt.",
            "But it came with pain.",
            "Manual memory management. One mistake — leak, or crash.",
            "And platform dependency. Code that worked on Windows could break on Unix.",
            "For software meant to run on many devices, that was a nightmare.",
        ],
    ),
    (
        "birth",
        "birth",
        [
            "So they built something new.",
            "First called Oak. Later renamed Java — yes, after the coffee.",
            "The mission was clear: safer than C++, simpler to maintain, and portable across platforms.",
        ],
    ),
    (
        "wora",
        "wora_intro",
        [
            "In nineteen ninety-five, Java arrived with a bold promise.",
            "Write once. Run anywhere.",
            "And for an industry tired of rewriting the same code again and again… that promise mattered.",
        ],
    ),
    (
        "bytecode",
        "bytecode",
        [
            "Here's the secret. Watch carefully.",
            "Java doesn't run directly on Windows or Mac.",
            "First, the compiler turns your source into bytecode — like an international language.",
            "Then the JVM — the Java Virtual Machine — translates that bytecode for your system.",
            "Windows has a JVM. Mac has a JVM. Linux has a JVM.",
            "Same bytecode. Different translator. Same result.",
            "That's Write Once, Run Anywhere — for real.",
        ],
    ),
    (
        "industry",
        "industry",
        [
            "And that's why Java became infrastructure.",
            "Banks need stability, not hype.",
            "Android needed a language millions already knew.",
            "Large backends needed scale that was battle-tested.",
            "Enterprise teams don't switch for trends. They switch when failure costs too much.",
            "Java earned trust — one production system at a time.",
        ],
    ),
    (
        "code",
        "code_print",
        [
            "Alright — your first program.",
            "You write a public class. That's the blueprint.",
            "Inside it, public static void main — the entry point. The JVM starts here.",
            "Then System.out.println — print a line to the console.",
            "Filename must match the class name. Java is case-sensitive. Don't forget that.",
        ],
    ),
    (
        "run",
        "run",
        [
            "Hit Run.",
            "Compiler to bytecode. JVM loads it. Finds main. Executes println.",
            "Hello, World.",
            "Behind the scenes, the JVM did the heavy lifting — not Windows directly.",
        ],
    ),
    (
        "interview",
        "interview",
        [
            "Quick interview question.",
            "Why is Java platform independent?",
            "Answer like this: we compile to bytecode, not machine code.",
            "Bytecode is platform-neutral.",
            "The JVM on each OS turns it into native instructions.",
            "Same class files. Windows, Mac, Linux — as long as a compatible JVM is there.",
        ],
    ),
    (
        "teaser",
        "teaser",
        [
            "So now you know why Java still runs the world.",
            "Safer. Portable. Trusted at scale.",
            "But one mystery remains.",
            "When people say install Java… what are they actually installing?",
            "JDK. JRE. JVM — three names beginners mix up every day.",
            "That's Episode Two. I'll see you there.",
        ],
    ),
]


def clean(text: str) -> str:
    return " ".join(text.split()).strip()


def silence(seconds: float, sr: int = SAMPLE_RATE) -> np.ndarray:
    return np.zeros(max(1, int(seconds * sr)), dtype=np.float32)


def synth_scene(scene_id: str, beats: list[str]) -> Path:
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    for i, beat in enumerate(beats):
        text = clean(beat)
        print(f"    {i+1}/{len(beats)} [chatterbox]: {text[:72]}")
        audio = cb_synth(text)
        wav = scene_dir / f"b{i:02d}.wav"
        sf.write(str(wav), audio, SAMPLE_RATE)
        parts.append(wav)
        if i < len(beats) - 1:
            gap = 0.26 if text.endswith("?") else 0.12
            if any(k in text for k in ("secret", "imagine", "Interview", "Watch carefully")):
                gap = 0.30
            sil = scene_dir / f"s{i:02d}.wav"
            sf.write(str(sil), silence(gap), SAMPLE_RATE)
            parts.append(sil)
    lst = scene_dir / "list.txt"
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    out = AUDIO / f"{scene_id}.mp3"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(out),
        ],
        check=True,
        capture_output=True,
    )
    return out


def remux(scene_id: str, clip_id: str) -> Path:
    vin = CLIPS_IN / f"{clip_id}.mp4"
    ain = AUDIO / f"{scene_id}.mp3"
    vout = CLIPS_OUT / f"{scene_id}.mp4"
    if not vin.exists():
        raise FileNotFoundError(vin)
    vd = probe(vin)
    ad = probe(ain)
    target = ad + 0.22
    if target > vd:
        pad = target - vd
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(vin),
            "-i",
            str(ain),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={pad:.3f}[v]",
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-shortest",
            "-movflags",
            "+faststart",
            str(vout),
        ]
    else:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(vin),
            "-i",
            str(ain),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-t",
            f"{target:.3f}",
            "-movflags",
            "+faststart",
            str(vout),
        ]
    subprocess.run(cmd, check=True, capture_output=True)
    return vout


def write_srt(durations: dict[str, float], out_path: Path):
    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int(round((ts - int(ts)) * 1000))
        if ms == 1000:
            s += 1
            ms = 0
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    t = 0.0
    idx = 1
    lines = []
    for scene_id, _, beats in SCENES:
        scene_dur = durations[scene_id] + 0.22
        weights = [max(len(b), 8) for b in beats]
        tw = sum(weights)
        for beat, w in zip(beats, weights):
            slot = scene_dur * (w / tw)
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{clean(beat)}\n")
            idx += 1
            t += slot
    out_path.write_text("\n".join(lines))


def main():
    if AUDIO.exists():
        shutil.rmtree(AUDIO)
    if CLIPS_OUT.exists():
        shutil.rmtree(CLIPS_OUT)
    AUDIO.mkdir(parents=True)
    CLIPS_OUT.mkdir(parents=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    print("==> Episode 1 short cut — Chatterbox Turbo")
    for i, (scene_id, _clip, beats) in enumerate(SCENES):
        print(f"  [{i+1}/{len(SCENES)}] {scene_id}")
        synth_scene(scene_id, beats)

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid, _, _ in SCENES}
    total = sum(durations.values()) + 0.22 * len(SCENES)
    print(f"==> Spoken runtime ≈ {total/60:.2f} min ({total:.1f}s)")
    (ROOT / "chatterbox_short_durations.json").write_text(json.dumps(durations, indent=2))

    outs = []
    for scene_id, clip_id, _ in SCENES:
        print(f"  remux {scene_id} <- {clip_id}")
        outs.append(remux(scene_id, clip_id))

    lst = ROOT / "concat_chatterbox_short.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep1_chatterbox_narrated.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-movflags",
            "+faststart",
            str(narrated),
        ],
        check=True,
    )

    dur = probe(narrated)
    print(f"==> Assembled {dur:.1f}s ({dur/60:.2f} min)")

    pace = 1.0
    if dur > 300:
        pace = min(dur / 295.0, 1.12)
    elif dur < 240:
        pace = max(dur / 250.0, 0.5)

    music = AUDIO / "music_bed.m4a"
    generate_music_bed((dur / pace) + 2, music)

    base = narrated
    if abs(pace - 1.0) > 0.015:
        print(f"==> Light pace x{pace:.3f}")
        paced = OUTPUT / "java_ep1_chatterbox_paced.mp4"
        at = min(max(pace, 0.5), 2.0)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(narrated),
                "-filter_complex",
                f"[0:v]setpts=PTS/{at}[v];[0:a]atempo={at}[a]",
                "-map",
                "[v]",
                "-map",
                "[a]",
                "-c:v",
                "libx264",
                "-preset",
                "veryfast",
                "-crf",
                "18",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
                str(paced),
            ],
            check=True,
        )
        base = paced
    else:
        print("==> Natural length — no heavy time-stretch")

    final = OUTPUT / "Java_Episode_01_Why_Java_Exists.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(base),
            "-i",
            str(music),
            "-filter_complex",
            "[1:a]volume=0.10[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
            "-map",
            "0:v",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "256k",
            "-movflags",
            "+faststart",
            str(final),
        ],
        check=True,
    )
    shutil.copy2(final, ARTIFACTS / "Java_Episode_01_Why_Java_Exists.mp4")

    write_srt(durations, OUTPUT / "Java_Episode_01.srt")
    if abs(pace - 1.0) > 0.015:
        srt_lines = Path(OUTPUT / "Java_Episode_01.srt").read_text().splitlines()
        out_lines = []

        def scale_ts(ts: str) -> str:
            h, m, rest = ts.split(":")
            s, ms = rest.split(",")
            total = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
            total /= pace
            h = int(total // 3600)
            m = int((total % 3600) // 60)
            s = int(total % 60)
            ms = int(round((total - int(total)) * 1000))
            return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

        for line in srt_lines:
            if "-->" in line:
                a, b = line.split(" --> ")
                out_lines.append(f"{scale_ts(a.strip())} --> {scale_ts(b.strip())}")
            else:
                out_lines.append(line)
        Path(OUTPUT / "Java_Episode_01.srt").write_text("\n".join(out_lines) + "\n")

    shutil.copy2(OUTPUT / "Java_Episode_01.srt", ARTIFACTS / "Java_Episode_01.srt")

    burned = OUTPUT / "Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-vf",
            f"subtitles={OUTPUT / 'Java_Episode_01.srt'}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "19",
            "-c:a",
            "copy",
            "-movflags",
            "+faststart",
            str(burned),
        ],
        check=True,
    )
    shutil.copy2(burned, ARTIFACTS / "Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-t",
            "40",
            "-vn",
            "-c:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(ARTIFACTS / "narration_CHATTERBOX_ep01_preview.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    final_dur = probe(final)
    print(f"DONE: {final_dur/60:.2f} min ({final_dur:.1f}s)")
    assert 240 <= final_dur <= 330, f"Duration {final_dur}s outside 240–330s window"
    subprocess.run(["ffprobe", "-hide_banner", str(final)])


if __name__ == "__main__":
    main()
