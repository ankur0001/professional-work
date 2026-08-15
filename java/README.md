# The Java Story (YouTube Series)

Premium short documentaries (4–5 min each) from the Java & JVM Handbook (80 lessons) plus Season 2 production-systems bonus track.

All series assets live in this `java/` folder.

## Layout

| Path | Contents |
|---|---|
| [`episodes/`](episodes/) | Per-episode READMEs (and thumbnails where present) |
| [`series/EPISODE_CATALOG.md`](series/EPISODE_CATALOG.md) | Full episode roadmap / status |
| [`video_build/`](video_build/) | Chatterbox / Kokoro narration + motion-graphics render scripts |
| [`output/`](output/) | Rendered MP4, SRT, and thumbnail assets |

## Rebuild an episode (Chatterbox — preferred)

Local free TTS via [Chatterbox Turbo](https://github.com/resemble-ai/chatterbox) (no API key):

```bash
pip3 install chatterbox-tts torch torchaudio soundfile numpy pillow edge-tts
python3 java/video_build/chatterbox_tts.py                 # smoke test
python3 java/video_build/make_episode_81_chatterbox.py     # one episode
```

Each episode has a dedicated script: `java/video_build/make_episode_XX_chatterbox.py`.

Optional env:

```bash
export CHATTERBOX_DEVICE=cpu          # or cuda
export CHATTERBOX_VOICE_WAV=/path/to/ref.wav   # optional voice clone
export TTS_PROVIDER=chatterbox        # default
```

## Legacy Kokoro rebuild

```bash
pip3 install 'kokoro>=0.9.4' soundfile numpy pillow edge-tts
export KOKORO_VOICE=am_michael
export TTS_PROVIDER=kokoro
python3 java/video_build/make_episode_02.py
```

Season 2 thumbnails:

```bash
python3 java/video_build/make_s2_thumbnails.py
```

## Rules

- One episode → one git branch → one PR
- Prefer Chatterbox over paid cloud TTS
- Stop when approaching Cursor usage limits (no paid overage)
