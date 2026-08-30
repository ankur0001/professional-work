# The Java Story

85-episode YouTube-style Java series.

## Layout

```
java-story/
├── v1/                      ← original cut (all episode files here)
│   ├── Java_Episode_XX_*.mp4 / _CAPTIONED.mp4 / .srt
│   ├── episodes/            ← episode README notes
│   ├── EPISODE_CATALOG.md
│   └── manifest.json
└── v2/                      ← current cut (all episode files here)
    ├── Java_Episode_XX_*.mp4 / _CAPTIONED.mp4 / .srt / _SOURCE.md
    ├── narrative_review/    ← coherent narrations
    └── video_build/         ← render tooling
```

## Browse

- **v1 files:** [`v1/`](v1/)
- **v2 files (current):** [`v2/`](v2/)

## Render v2

```bash
python3 java-story/v2/video_build/render_v2_from_narrative.py --ep 1
python3 java-story/v2/video_build/distribute_v2_to_episode_prs.py --ep 1
```
