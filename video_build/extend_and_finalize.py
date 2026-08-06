#!/usr/bin/env python3
"""Extend Episode 1 to ~13 minutes and re-encode at higher quality."""

from __future__ import annotations

import asyncio
import json
import shutil
import subprocess
from pathlib import Path

import edge_tts
from generate_java_episode import (
    AUDIO,
    CLIPS,
    OUTPUT,
    ARTIFACTS,
    Scene,
    VOICE,
    probe_duration,
    render_scene_clip,
    concat_clips,
    mix_music,
    generate_music_bed,
    write_srt,
    SCENES,
    render_question,
    font,
    FONT_SERIF,
    FONT_BOLD,
    WHITE,
    ORANGE,
    W,
    H,
)
from PIL import ImageDraw

EXTRA_SCENES = [
    Scene(
        "chapter_bump_1",
        "Chapter one. Why Java exists. Before the buzzwords… before the frameworks… there was a real engineering problem. And solving it changed software forever.",
        "title_card",
        "Chapter 1",
        "Why Java Exists",
    ),
    Scene(
        "chapter_bump_2",
        "Chapter two. What makes Java special. This is the idea that made Java famous — and the reason it still matters today.",
        "title_card",
        "Chapter 2",
        "What Makes Java Special",
    ),
    Scene(
        "chapter_bump_3",
        "Chapter three. Java in the real world. Let's stop talking theory — and look at where this language actually earns its keep.",
        "title_card",
        "Chapter 3",
        "Java in the Real World",
    ),
    Scene(
        "chapter_bump_4",
        "Chapter four. Your first Java program. No more waiting. Let's open the editor… and write some real code.",
        "title_card",
        "Chapter 4",
        "Your First Java Program",
    ),
    Scene(
        "jdk_note",
        "One more important detail before we wrap up. When people say install Java, they usually mean the JDK — the Java Development Kit. Inside it, you get the compiler, tools, and a runtime that includes the JVM. Beginners often mix these terms. Here's the clean mental model. JDK is for developers. JRE is for running programs. JVM is the engine that actually executes bytecode. Keep that model in your head — Episode Two will make it crystal clear.",
        "analogy",
        "JDK · JRE · JVM",
        "Developer kit · Runtime · Engine",
    ),
    Scene(
        "closing_cta",
        "If this video helped something click for you, subscribe for Episode Two. We'll unpack JDK, JRE, and JVM — the three names everyone confuses. I'll see you there.",
        "teaser",
        "Subscribe for Episode 2",
        "JDK, JRE & JVM",
    ),
]

# Insert extras into full order
FULL_ORDER = []
for sc in SCENES:
    if sc.id == "curiosity1":
        FULL_ORDER.append(EXTRA_SCENES[0])  # chapter 1 before history continues
    if sc.id == "wora_intro":
        FULL_ORDER.append(EXTRA_SCENES[1])
    if sc.id == "industry":
        FULL_ORDER.append(EXTRA_SCENES[2])
    if sc.id == "code_intro":
        FULL_ORDER.append(EXTRA_SCENES[3])
    FULL_ORDER.append(sc)
    if sc.id == "mistakes":
        FULL_ORDER.append(EXTRA_SCENES[4])
FULL_ORDER.append(EXTRA_SCENES[5])


async def synth(scene: Scene):
    out = AUDIO / f"{scene.id}.mp3"
    if out.exists() and out.stat().st_size > 1000:
        return
    c = edge_tts.Communicate(scene.narration, VOICE, rate="-5%", pitch="-2Hz")
    await c.save(str(out))
    print(f"  TTS {scene.id}")


async def synth_all_extra():
    for sc in EXTRA_SCENES:
        await synth(sc)


def main():
    print("==> Extra narration...")
    asyncio.run(synth_all_extra())

    durations = {}
    total = 0.0
    for sc in FULL_ORDER:
        d = probe_duration(AUDIO / f"{sc.id}.mp3")
        durations[sc.id] = d
        total += d + 0.55
    print(f"==> Extended runtime ≈ {total/60:.1f} min ({total:.1f}s)")

    print("==> Render missing clips...")
    clips = []
    for sc in FULL_ORDER:
        clip = CLIPS / f"{sc.id}.mp4"
        if not clip.exists():
            # temporarily bump pad via duration arg
            render_scene_clip(sc, durations[sc.id] + 0.2, clip)
        clips.append(clip)

    print("==> Rebuild music for new length...")
    music = AUDIO / "music_bed_ext.m4a"
    generate_music_bed(total + 5, music)

    print("==> Concatenate...")
    narrated = OUTPUT / "java_ep1_narrated_ext.mp4"
    concat_clips(clips, narrated)

    print("==> Mix + high-quality re-encode...")
    # mix to temp then re-encode video for higher bitrate
    mixed = OUTPUT / "java_ep1_mixed_tmp.mp4"
    mix_music(narrated, music, mixed)

    final = OUTPUT / "Java_Episode_01_Why_Java_Exists.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(mixed),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
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
    # rewrite srt with full order durations - quick custom
    t = 0.0
    idx = 1
    lines = []

    def fmt(ts: float) -> str:
        h = int(ts // 3600)
        m = int((ts % 3600) // 60)
        s = int(ts % 60)
        ms = int((ts - int(ts)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    for sc in FULL_ORDER:
        dur = durations[sc.id] + 0.55
        words = sc.narration.split()
        chunks = [" ".join(words[i : i + 12]) for i in range(0, len(words), 12)]
        slot = dur / max(len(chunks), 1)
        for ch in chunks:
            lines.append(f"{idx}\n{fmt(t)} --> {fmt(t + slot)}\n{ch}\n")
            idx += 1
            t += slot
    (OUTPUT / "Java_Episode_01.srt").write_text("\n".join(lines))
    shutil.copy2(OUTPUT / "Java_Episode_01.srt", ARTIFACTS / "Java_Episode_01.srt")

    # burn captions into a captions version as well
    burned = OUTPUT / "Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(final),
            "-vf",
            f"subtitles={OUTPUT / 'Java_Episode_01.srt'}:force_style='FontName=Noto Sans,FontSize=22,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,BorderStyle=3,Outline=1,Shadow=0,MarginV=40'",
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

    # thumbnail refresh
    thumb = render_question(1.0, 1.0)
    d = ImageDraw.Draw(thumb)
    f = font(FONT_SERIF, 72)
    text = "WHY JAVA?"
    bbox = d.textbbox((0, 0), text, font=f)
    d.text(((W - (bbox[2] - bbox[0])) // 2, 80), text, font=f, fill=WHITE)
    d.text((W // 2 - 90, H - 120), "Episode 1", font=font(FONT_BOLD, 36), fill=ORANGE)
    thumb.save(OUTPUT / "thumbnail.jpg", quality=95)
    shutil.copy2(OUTPUT / "thumbnail.jpg", ARTIFACTS / "thumbnail.jpg")

    (Path("/workspace/video_build") / "full_order.json").write_text(
        json.dumps([{"id": s.id, "dur": durations[s.id]} for s in FULL_ORDER], indent=2)
    )
    subprocess.run(["ffprobe", "-hide_banner", str(final)])
    print("DONE extended final")


if __name__ == "__main__":
    main()
