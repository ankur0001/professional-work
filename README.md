# The Java Story — Episode 1

Premium YouTube educational documentary package + **rendered video**.

## Watch the video

| File | Description |
|---|---|
| [`output/Java_Episode_01_Why_Java_Exists.mp4`](output/Java_Episode_01_Why_Java_Exists.mp4) | Final cut (~4–5 min, 1080p30, Kokoro narration) |
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

- **Runtime:** ~4–5 minutes (condensed cut)
- **Resolution:** 1920×1080 (16:9)
- **Frame rate:** 30 FPS
- **Narration:** Kokoro-82M (`am_michael`) — open ElevenLabs-class TTS
- **Style:** Dark UI · Java orange · JVM blue · motion graphics

### Rebuild short cut

```bash
export KOKORO_VOICE=am_michael
python3 video_build/make_short_episode.py
```

## Best TTS (no API key) — Kokoro-82M

Closest free/open alternative to ElevenLabs that runs locally on CPU:

```bash
pip3 install 'kokoro>=0.9.4' soundfile
export KOKORO_VOICE=am_michael   # warm mentor; also try bm_fable, am_liam
python3 video_build/kokoro_narrate.py
```

Voice samples are in `/opt/cursor/artifacts/kokoro_*.mp3`.

## Optional: ElevenLabs (if you have a key)

```bash
export ELEVENLABS_API_KEY="your_key_here"
python3 video_build/elevenlabs_narrate.py
```

## Older fallback (edge-tts)

```bash
python3 video_build/humanize_audio.py
```
