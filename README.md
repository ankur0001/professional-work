# The Java Story — Episode 1

Premium YouTube educational documentary package + **rendered video**.

## Watch the video

| File | Description |
|---|---|
| [`output/Java_Episode_01_Why_Java_Exists.mp4`](output/Java_Episode_01_Why_Java_Exists.mp4) | Final cut (~12:33, 1080p30, narrated) |
| [`output/Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4`](output/Java_Episode_01_Why_Java_Exists_CAPTIONED.mp4) | Same cut with burned-in captions |
| [`output/Java_Episode_01.srt`](output/Java_Episode_01.srt) | SubRip captions |
| [`output/thumbnail.jpg`](output/thumbnail.jpg) | YouTube thumbnail |

Artifacts are also copied to `/opt/cursor/artifacts/`.

## Production bible

Full narration, storyboard, animation specs, SEO metadata:

- [`java-episode-01-production-bible.md`](java-episode-01-production-bible.md)

## Regenerate the video

```bash
export PATH="$HOME/.local/bin:$PATH"
pip3 install pillow edge-tts numpy
python3 video_build/generate_java_episode.py   # base scenes + TTS
python3 video_build/extend_and_finalize.py     # chapter bumpers + HQ encode
```

## Specs

- **Runtime:** ~15:48
- **Resolution:** 1920×1080 (16:9)
- **Frame rate:** 30 FPS
- **Narration:** Conversational Indian English (`en-IN-PrabhatNeural`), beat-based delivery with natural pauses (not paragraph read-aloud)
- **Style:** Dark UI · Java orange · JVM blue · motion graphics

## Improve / regenerate human-like audio

```bash
python3 video_build/humanize_audio.py
```

This rewrites narration into short spoken beats, synthesizes each beat separately with SSML pauses, remuxes onto the existing visuals, and rebuilds the final cut.
