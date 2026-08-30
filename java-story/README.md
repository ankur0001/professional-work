# The Java Story

85-episode YouTube-style Java series.

## Layout

```
java-story/
├── v1/                 ← original episode cut (videos + episode notes)
│   ├── output/         ← clean + CAPTIONED mp4, srt, thumbnails
│   ├── episodes/       ← per-episode README notes
│   ├── EPISODE_CATALOG.md
│   └── manifest.json
└── v2/                 ← current cut (coherent narration + animated visuals)
    ├── output/         ← clean + CAPTIONED mp4, srt, SOURCE.md
    ├── narrative_review/
    └── video_build/
```

## Quick links

- **v1 videos:** [`v1/output/`](v1/output/)
- **v2 videos:** [`v2/output/`](v2/output/)
- **v2 narrations:** [`v2/narrative_review/`](v2/narrative_review/)

## Render v2

```bash
python3 java-story/v2/video_build/render_v2_from_narrative.py --ep 1
python3 java-story/v2/video_build/distribute_v2_to_episode_prs.py --ep 1
```
