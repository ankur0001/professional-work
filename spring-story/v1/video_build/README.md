# The Spring Story — video build

Renders YouTube-ready episode videos in the same style as **The Java Story v2**:
animated motion-graphics beats + full narration TTS + clean + captioned MP4 + SRT.

## Outputs (per episode folder)

| File | Purpose |
|---|---|
| `Spring_Episode_XX_<Slug>.mp4` | Clean 1080p30-family cut (encoded from 8 fps motion holds) |
| `Spring_Episode_XX_<Slug>_CAPTIONED.mp4` | Same cut with burned-in captions |
| `Spring_Episode_XX.srt` | SubRip captions |
| `Spring_Episode_XX_SOURCE.md` | Provenance note |

Existing upload pack files (`title.txt`, `youtube_description.txt`, `tags.txt`, `thumbnail.jpg`, `narration.md`, …) stay in place.

## Dependencies

```bash
pip3 install --user edge-tts soundfile pillow numpy
# ffmpeg / ffprobe already required on PATH
```

## Render one episode

```bash
python3 spring-story/v1/video_build/render_spring_episode.py --ep 1
python3 spring-story/v1/video_build/render_spring_episode.py --ep 1 --max-beats 3   # preview
python3 spring-story/v1/video_build/render_spring_episode.py --ep 1 --reuse-audio  # rebuild visuals only
```

## Batch (resume-safe)

```bash
bash spring-story/v1/video_build/batch_render.sh        # all 112
bash spring-story/v1/video_build/batch_render.sh 1 20   # EP01–EP20
```

Completed episode numbers are appended to `logs/completed.txt`.

## Design notes

- **Palette:** dark forest green + Spring leaf accents (not Java amber).
- **Chrome:** “The Spring Story” series label on every beat.
- **TTS:** Edge-TTS (`en-US-GuyNeural` by default; override with `SPRING_TTS_VOICE`).
- **Visuals:** same animated scene planner as Java v2 (`visual_engine.py`) — flows, stacks, pipelines, comparisons — not text-wall slides.
- Work audio/clips live under `video_build/work/` (gitignored).
