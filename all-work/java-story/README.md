# The Java Story

85-episode YouTube-style Java series — coherent narrations, animated visuals, and local Chatterbox TTS video builds.

## Layout

```
all-work/java-story/
├── narrative_review/     ← episode narrations (ep01–ep85) + style guides
├── video_build/          ← TTS, visual engine, render + distribute scripts
└── output/v2/            ← local render outputs (mp4/srt mostly gitignored)
```

## Quick start

```bash
# Render one episode (full audio end-cut fix included)
python3 all-work/java-story/video_build/render_v2_from_narrative.py --ep 1

# Distribute into that episode's PR branch
python3 all-work/java-story/video_build/distribute_v2_to_episode_prs.py --ep 1
```

See [`narrative_review/README.md`](narrative_review/README.md) for narration standards.
