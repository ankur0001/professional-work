# The Spring Story — v1 YouTube upload packs

Episode-by-episode upload kits for **The Spring Story**, parallel to `java-story/v1`.

## Per-episode contents

| File | Purpose |
|---|---|
| `title.txt` | YouTube title |
| `youtube_description.txt` | Description + timestamps |
| `tags.txt` | Comma-separated tags |
| `chapters.txt` | Chapter list (estimated from narration pacing) |
| `thumbnail.jpg` | 1920×1080 branded thumbnail (**not** a video frame; no burned-in subtitles) |
| `narration.md` | Full spoken narration / transcript source |
| `README.md` | Upload checklist |

## Notes

- Thumbnails are designed stills for upload CTR — they intentionally do **not** use screenshots or captioned video frames.
- Chapter timestamps are estimates from narration length (~155 wpm) until final video timing is available.
- MP4 / SRT assets are produced by `video_build/render_spring_episode.py` (clean + captioned + SRT).

## Video production

```bash
python3 spring-story/v1/video_build/render_spring_episode.py --ep 1
bash spring-story/v1/video_build/batch_render.sh
```

See [`video_build/README.md`](video_build/README.md).
