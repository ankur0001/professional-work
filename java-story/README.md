# The Java Story

85-episode YouTube-style Java series — coherent narrations, animated visuals, and local Chatterbox TTS video builds.

## Layout

```
java-story/
├── narrative_review/     ← episode narrations (ep01–ep85) + style guides
├── video_build/          ← TTS, visual engine, render + distribute scripts
└── output/v2/            ← all 85 episode videos (clean + CAPTIONED + srt)
```

## Videos

All episodes: [`output/v2/`](output/v2/)

## Quick start

```bash
python3 java-story/video_build/render_v2_from_narrative.py --ep 1
python3 java-story/video_build/distribute_v2_to_episode_prs.py --ep 1
```

See [`narrative_review/README.md`](narrative_review/README.md) for narration standards.
