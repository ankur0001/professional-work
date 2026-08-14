# The Java Story (YouTube Series)

Premium short documentaries (4–5 min each) from the Java & JVM Handbook (80 lessons) plus Season 2 production-systems bonus track.

All series assets live in this `java/` folder.

## Layout

| Path | Contents |
|---|---|
| [`episodes/`](episodes/) | Per-episode READMEs (and thumbnails where present) |
| [`series/EPISODE_CATALOG.md`](series/EPISODE_CATALOG.md) | Full episode roadmap / status |
| [`video_build/`](video_build/) | Kokoro narration + motion-graphics render scripts |
| [`output/`](output/) | Rendered MP4, SRT, and thumbnail assets |

## Rebuild an episode

From the **repository root**:

```bash
pip3 install 'kokoro>=0.9.4' soundfile numpy pillow edge-tts
export KOKORO_VOICE=am_michael
python3 java/video_build/make_episode_02.py
```

Season 2 thumbnails:

```bash
python3 java/video_build/make_s2_thumbnails.py
```

## More realistic narration (Sarvam TTS)

Default builds still use local Kokoro. To pilot Sarvam Bulbul v3 (`en-IN`):

```bash
export SARVAM_API_KEY='your-api-subscription-key'   # from https://dashboard.sarvam.ai
export TTS_PROVIDER=sarvam
export SARVAM_SPEAKER=shubh    # optional; bulbul:v3 voices
export SARVAM_PACE=0.97
python3 java/video_build/make_episode_81_sarvam_pilot.py
```

Smoke-test the key:

```bash
python3 java/video_build/sarvam_tts.py
```

Free credits are limited — pilot one episode before batch re-renders.

## Rules

- One episode → one git branch → one PR
- Stop when approaching Cursor usage limits (no paid overage)
- Do not batch-generate the full catalog in one run
