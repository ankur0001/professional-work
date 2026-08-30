#!/usr/bin/env python3
"""
Regenerate narration to sound conversational (not read-aloud),
then remux onto existing scene videos and rebuild the final cut.
"""

from __future__ import annotations

import asyncio
import json
import random
import shutil
import subprocess
import struct
import wave
from pathlib import Path

import edge_tts
import numpy as np

ROOT = Path("/workspace/all-work/java-story/video_build")
AUDIO = ROOT / "audio_human"
CLIPS_IN = ROOT / "clips"
CLIPS_OUT = ROOT / "clips_human"
OUTPUT = Path("/workspace/all-work/java-story/output")
ARTIFACTS = Path("/opt/cursor/artifacts")

VOICE = "en-IN-PrabhatNeural"
# Slightly slower, warmer — less “newsreader”
RATE = "-8%"
PITCH = "-2Hz"

# Each scene = list of short spoken beats (1 thought each).
# Use <break> sparingly inside a beat; prefer separate beats for pauses.
BEATS: dict[str, list[str]] = {
    "hook": [
        "Okay… imagine this.",
        "Nearly every bank… every airline… every stock exchange… Android apps… big enterprise systems…",
        "They all depend on one programming language.",
    ],
    "question": [
        "That language… is Java.",
        "But here's what I find fascinating.",
        "A language created almost thirty years ago… is still everywhere.",
        "Hundreds of other languages disappeared. Java didn't.",
        "So… why?",
    ],
    "promise": [
        "Today, we're going to find out.",
        "And no — this is not a textbook lecture.",
        "We're going to tell it like a story.",
        "How Java was born. What problem it actually solved. And why it's still running the world.",
    ],
    "chapter_bump_1": [
        "Chapter one.",
        "Why Java exists.",
        "Before the frameworks… before the buzzwords… there was a real engineering headache.",
        "And solving it? That changed software forever.",
    ],
    "curiosity1": [
        "But first — a quick question.",
        "C++ was already powerful, right?",
        "So why did the industry need another language at all?",
        "Alright. Let's go back to the nineteen nineties.",
    ],
    "nineties": [
        "Picture this.",
        "Early nineties. The internet is about to explode.",
        "At Sun Microsystems, a team led by James Gosling is building software for devices — interactive TVs, set-top boxes, handheld gadgets.",
        "And they started with C++.",
    ],
    "cpp_pain": [
        "Very quickly… they hit a wall.",
        "C++ gave them power. Absolutely.",
        "But that power came with a price.",
        "Manual memory management. One tiny mistake — and boom. Memory leak. Or a crash.",
        "And platform dependency? Code that worked on one operating system could break completely on another.",
        "For a team targeting many devices… that was a nightmare.",
    ],
    "curiosity2": [
        "So here's the real problem.",
        "How do you write software once…",
        "and run it on Windows, Mac, Unix, embedded devices…",
        "without rewriting everything?",
    ],
    "birth": [
        "Gosling's team made a bold call.",
        "Build something new.",
        "It was first called Oak. Later renamed Java — yes, inspired by the coffee that kept those late nights alive.",
        "The goal sounded simple. Safer than C++. Easier to maintain. And portable across platforms.",
        "Simple to say. Incredibly hard to build.",
    ],
    "chapter_bump_2": [
        "Chapter two.",
        "What makes Java special.",
        "This is the idea that made Java famous — and the reason it still matters.",
    ],
    "wora_intro": [
        "When Java launched in nineteen ninety-five… it didn't whisper.",
        "It came with a promise that sounded almost too good to be true.",
        "Write once. Run anywhere.",
        "And for an industry tired of porting the same code again and again? That promise was everything.",
    ],
    "wora_explain": [
        "So what does Write Once, Run Anywhere actually mean?",
        "Imagine this. You write one instruction manual…",
        "and every machine on Earth can follow it.",
        "Not because every machine speaks the same language…",
        "but because every machine has the same translator.",
    ],
    "curiosity3": [
        "But wait.",
        "Windows and Mac don't run the same programs natively.",
        "So how does Java run on every operating system?",
        "Watch carefully. This is the secret.",
    ],
    "bytecode": [
        "When you write Java… you don't hand your program straight to Windows or Mac.",
        "First, the compiler turns your source into bytecode.",
        "Think of bytecode like an international language — not tied to one operating system.",
        "Then the JVM — the Java Virtual Machine — takes that bytecode and translates it for your system.",
        "Honestly? The JVM is like Google Translate… for computers.",
        "Windows has a JVM. Mac has a JVM. Linux has a JVM.",
        "Same bytecode. Different translator. Same result.",
    ],
    "analogy": [
        "Think about it this way.",
        "Your Java source code is like handwritten notes.",
        "The compiler turns those notes into a clean blueprint — that's bytecode.",
        "The JVM is the construction crew. It reads the blueprint and builds the house…",
        "whether the site is Windows, Mac, or Linux.",
        "You don't redraw the blueprint for every site. Same blueprint. The crew adapts.",
    ],
    "curiosity4": [
        "Okay — so Java solved portability beautifully.",
        "But is that enough to explain thirty years of dominance?",
        "Let's look at where Java actually lives today.",
    ],
    "chapter_bump_3": [
        "Chapter three.",
        "Java in the real world.",
        "Enough theory. Let's see where this language earns its keep.",
    ],
    "industry": [
        "Java didn't survive because of a slogan.",
        "It survived because it became infrastructure.",
        "When a bank processes millions of transactions a day — it needs stability, not hype.",
        "When Android needed a language millions of developers already knew — Java was already there.",
        "And when companies built backends that had to scale globally — Java's ecosystem was battle-tested.",
        "Enterprise teams don't switch languages because something is trendy.",
        "They switch when the cost of failure is too high.",
        "Java earned trust… one production deployment at a time.",
    ],
    "others": [
        "Now you might ask — what about Python? JavaScript? Go?",
        "They're excellent. Seriously.",
        "But Java carved out a lane that still matters — large backends, Android, finance, enterprise systems.",
        "Places where performance, strong typing, and decades of tooling create real business value.",
        "Not the only choice. Still one of the most important.",
    ],
    "chapter_bump_4": [
        "Chapter four.",
        "Your first Java program.",
        "No more waiting. Let's open the editor and write some real code.",
    ],
    "code_intro": [
        "Alright — enough history.",
        "Let's write Java.",
        "Your first program.",
        "And I want you to watch every keyword… because each one is doing something on purpose.",
    ],
    "code_public": [
        "See that word — public?",
        "It means this class is accessible from outside.",
        "Think of it like… this code is open for business.",
    ],
    "code_class": [
        "Next — class HelloWorld.",
        "A class is a blueprint.",
        "HelloWorld is the name we chose.",
        "And the filename must match — HelloWorld.java.",
        "That tiny detail trips up a lot of beginners.",
    ],
    "code_main": [
        "Now this line — public static void main… String args.",
        "This is the entry point.",
        "When you hit run, the JVM looks for this exact method.",
        "This is where execution begins.",
    ],
    "code_print": [
        "And finally — System.out.println.",
        "This prints text to the console.",
        "Println means print line — print the text, then move to the next line.",
        "Okay… let's run it.",
    ],
    "run": [
        "Watch what happens behind the scenes.",
        "You hit Run.",
        "Compiler reads HelloWorld.java… turns it into bytecode…",
        "JVM loads it… finds main… and executes println.",
        "And there it is — Hello, World!",
    ],
    "memory": [
        "Here's where most beginners get confused.",
        "They think Java runs directly on Windows.",
        "It doesn't.",
        "Your source goes to the compiler… becomes bytecode… the JVM loads it into memory…",
        "and the CPU runs machine instructions through the JVM.",
        "Every step matters.",
        "This tiny detail… changes everything.",
    ],
    "mistakes": [
        "Quick reality check — common beginner mistakes.",
        "Mistake one: thinking Java runs like a normal Windows exe. Nope. The JVM is doing the heavy lifting.",
        "Mistake two: mixing up JDK, JRE, and JVM.",
        "Quick version — JDK means develop. JRE means run. JVM is the engine inside.",
        "Mistake three: naming the file helloworld.java when the class is HelloWorld.",
        "Java is case-sensitive. Filename must match the public class name.",
        "Don't worry if this feels like a lot. We'll unpack it properly in Episode Two.",
    ],
    "jdk_note": [
        "One more useful detail before we wrap up.",
        "When people say install Java… they usually mean the JDK — the Java Development Kit.",
        "Inside it, you get the compiler, the tools, and a runtime that includes the JVM.",
        "Clean mental model: JDK for developers. JRE for running. JVM is the engine that executes bytecode.",
        "Keep that in your head — Episode Two will make it crystal clear.",
    ],
    "interview": [
        "Alright — interview time.",
        "Why is Java platform independent?",
        "Here's how you answer… like someone who's actually shipped code.",
        "Java becomes platform independent through bytecode and the JVM.",
        "We don't compile to machine-specific code. We compile to bytecode — a platform-neutral format.",
        "Then the JVM on each OS turns that bytecode into native instructions.",
        "Same class files. Windows, Mac, Linux — as long as a compatible JVM is there.",
        "If you can explain that calmly in an interview? You're already ahead of half the candidates.",
    ],
    "summary": [
        "Let's land the plane.",
        "Java exists because the nineties needed something safer and more portable than C++.",
        "Write Once, Run Anywhere works because of bytecode and the JVM.",
        "Industry adopted it because stability at scale beats hype.",
        "And your first program? Public class… main… println.",
        "You now understand why Java became one of the most successful languages ever created.",
    ],
    "teaser": [
        "But one huge mystery still remains.",
        "If Java code doesn't run directly on your computer…",
        "what exactly is the JVM doing inside memory?",
        "Heap. Stack. Garbage collection. JIT compilation.",
        "What's actually happening when you press Run?",
        "That's what we'll uncover in Episode Two.",
    ],
    "closing_cta": [
        "If something clicked for you today — stick around for Episode Two.",
        "We're going inside the JVM. Stack, heap, garbage collection — the stuff interviewers love.",
        "I'll see you there.",
    ],
}

# Scene visual order from previous build
ORDER = [
    "hook",
    "question",
    "promise",
    "chapter_bump_1",
    "curiosity1",
    "nineties",
    "cpp_pain",
    "curiosity2",
    "birth",
    "chapter_bump_2",
    "wora_intro",
    "wora_explain",
    "curiosity3",
    "bytecode",
    "analogy",
    "curiosity4",
    "chapter_bump_3",
    "industry",
    "others",
    "chapter_bump_4",
    "code_intro",
    "code_public",
    "code_class",
    "code_main",
    "code_print",
    "run",
    "memory",
    "mistakes",
    "jdk_note",
    "interview",
    "summary",
    "teaser",
    "closing_cta",
]


def probe(path: Path) -> float:
    r = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(r.stdout.strip())


def write_silence_wav(path: Path, seconds: float, sr: int = 24000):
    n = int(seconds * sr)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(b"\x00\x00" * n)


async def tts_beat(text: str, out: Path):
    # Ellipses + short sentences already help; add light SSML pause after questions/hooks
    spoken = text
    if not spoken.strip().endswith(">"):
        # Convert ellipses into a short breath — not a long dead pause
        spoken = spoken.replace("…", '. <break time="180ms"/> ')
        spoken = spoken.replace("...", '. <break time="180ms"/> ')
        # Em-dash style asides
        spoken = spoken.replace(" — ", '. <break time="120ms"/> ')
        spoken = spoken.replace(" - ", '. <break time="120ms"/> ')
    communicate = edge_tts.Communicate(spoken, VOICE, rate=RATE, pitch=PITCH)
    await communicate.save(str(out))


async def synthesize_scene(scene_id: str):
    beats = BEATS[scene_id]
    scene_dir = AUDIO / scene_id
    scene_dir.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, beat in enumerate(beats):
        mp3 = scene_dir / f"b{i:02d}.mp3"
        await tts_beat(beat, mp3)
        parts.append(mp3)
        # Natural gap between thoughts — short enough to keep energy,
        # long enough to avoid "reading a paragraph" cadence.
        gap = 0.10
        if beat.strip().endswith("?"):
            gap = 0.28
        elif beat.strip().endswith((".", "!")):
            gap = 0.16
        if i == 0:
            gap = 0.08
        if any(k in beat for k in ("Watch carefully", "secret", "imagine this", "Picture this")):
            gap = 0.32
        # no trailing silence after final beat
        if i < len(beats) - 1:
            sil = scene_dir / f"s{i:02d}.wav"
            write_silence_wav(sil, gap)
            parts.append(sil)

    # concat to one mp3 via ffmpeg
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


async def synthesize_all():
    if AUDIO.exists():
        shutil.rmtree(AUDIO)
    AUDIO.mkdir(parents=True)
    for i, sid in enumerate(ORDER):
        print(f"  TTS {i+1}/{len(ORDER)}: {sid} ({len(BEATS[sid])} beats)")
        await synthesize_scene(sid)


def remux_scene(scene_id: str) -> Path:
    """Attach new audio to existing video; freeze-frame or trim to match audio."""
    vin = CLIPS_IN / f"{scene_id}.mp4"
    ain = AUDIO / f"{scene_id}.mp3"
    vout = CLIPS_OUT / f"{scene_id}.mp4"
    if not vin.exists():
        raise FileNotFoundError(vin)

    vd = probe(vin)
    ad = probe(ain)
    # target = audio + small tail hold
    target = ad + 0.35

    if target > vd:
        # freeze last frame to extend
        pad = target - vd
        # tpad adds clone frames at end; also need audio
        filter_v = f"tpad=stop_mode=clone:stop_duration={pad:.3f}"
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(vin),
                "-i",
                str(ain),
                "-filter_complex",
                f"[0:v]{filter_v}[v]",
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
            ],
            check=True,
            capture_output=True,
        )
    else:
        # trim video to audio length
        subprocess.run(
            [
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
            ],
            check=True,
            capture_output=True,
        )
    return vout


def generate_music_bed(duration: float, out_path: Path):
    sr = 44100
    n = int(duration * sr)
    t = np.linspace(0, duration, n, endpoint=False)
    pad1 = 0.07 * np.sin(2 * np.pi * 110 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.05 * t))
    pad2 = 0.05 * np.sin(2 * np.pi * 164.81 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.07 * t + 1))
    pad3 = 0.04 * np.sin(2 * np.pi * 220 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.03 * t + 2))
    pulse = 0.025 * np.sin(2 * np.pi * 55 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.45 * t))
    noise = 0.006 * np.random.randn(n)
    sig = pad1 + pad2 + pad3 + pulse + noise
    sig = np.convolve(sig, np.ones(64) / 64, mode="same")
    fade = int(2.5 * sr)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    sig = (sig * env)
    peak = np.max(np.abs(sig)) + 1e-9
    sig = (sig / peak * 0.32).astype(np.float32)
    wav_path = out_path.with_suffix(".wav")
    with wave.open(str(wav_path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes((sig * 32767).astype(np.int16).tobytes())
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "aac", "-b:a", "192k", str(out_path)],
        check=True,
        capture_output=True,
    )


def write_srt(durations: dict[str, float], out_path: Path):
    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    t = 0.0
    idx = 1
    lines = []
    for sid in ORDER:
        beats = BEATS[sid]
        scene_dur = durations[sid] + 0.35
        # allocate time proportional to beat length
        weights = [max(len(b), 8) for b in beats]
        total_w = sum(weights)
        for beat, w in zip(beats, weights):
            slot = scene_dur * (w / total_w)
            # strip ssml-ish leftovers
            text = beat.replace("<break time=\"280ms\"/>", "").replace("<break time=\"350ms\"/>", "")
            text = " ".join(text.split())
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{text}\n")
            idx += 1
            t += slot
    out_path.write_text("\n".join(lines))


def main():
    CLIPS_OUT.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    print("==> Synthesizing conversational narration (beat-based)...")
    asyncio.run(synthesize_all())

    durations = {sid: probe(AUDIO / f"{sid}.mp3") for sid in ORDER}
    total = sum(durations.values()) + 0.35 * len(ORDER)
    print(f"==> New narration runtime ≈ {total/60:.1f} min")
    (ROOT / "human_durations.json").write_text(json.dumps(durations, indent=2))

    print("==> Remuxing audio onto scene videos...")
    outs = []
    for sid in ORDER:
        print(f"  remux {sid}")
        outs.append(remux_scene(sid))

    print("==> Concatenating...")
    lst = ROOT / "concat_human.txt"
    with open(lst, "w") as f:
        for p in outs:
            f.write(f"file '{p}'\n")
    narrated = OUTPUT / "java_ep1_human_narrated.mp4"
    # re-encode on concat to avoid timestamp issues
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

    print("==> Music bed...")
    music = AUDIO / "music_bed.m4a"
    generate_music_bed(probe(narrated) + 2, music)

    print("==> Mix final...")
    final = OUTPUT / "Java_Episode_01_Why_Java_Exists.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(narrated),
            "-i",
            str(music),
            "-filter_complex",
            "[1:a]volume=0.11[m];[0:a]volume=1.15[v];[v][m]amix=inputs=2:duration=first:dropout_transition=2[a]",
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
            "-ar",
            "48000",
            "-movflags",
            "+faststart",
            str(final),
        ],
        check=True,
    )
    shutil.copy2(final, ARTIFACTS / "Java_Episode_01_Why_Java_Exists.mp4")

    write_srt(durations, OUTPUT / "Java_Episode_01.srt")
    shutil.copy2(OUTPUT / "Java_Episode_01.srt", ARTIFACTS / "Java_Episode_01.srt")

    # captioned version
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

    # short before/after voice sample for review
    sample = ARTIFACTS / "narration_sample_human.mp3"
    shutil.copy2(AUDIO / "hook.mp3", sample)
    # also stitch hook+question+promise for a longer listen
    lst2 = ROOT / "sample_list.txt"
    with open(lst2, "w") as f:
        for sid in ["hook", "question", "promise", "curiosity3", "bytecode"]:
            f.write(f"file '{AUDIO / (sid + '.mp3')}'\n")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst2),
            "-c",
            "copy",
            str(ARTIFACTS / "narration_sample_human_long.mp3"),
        ],
        check=True,
        capture_output=True,
    )

    subprocess.run(["ffprobe", "-hide_banner", str(final)])
    print("DONE humanized audio rebuild")


if __name__ == "__main__":
    main()
