# The Java Story — v2 (current)

Current series cut: coherent narrations, animated visuals (`visual_engine.py`), Chatterbox TTS, end-cut-fixed full audio.

## Contents

| Path | Description |
|------|-------------|
| [`output/`](output/) | All 85 episodes: clean + CAPTIONED mp4, srt, SOURCE.md |
| [`narrative_review/`](narrative_review/) | ep01–ep85 full narrations + style guides |
| [`video_build/`](video_build/) | Render, TTS, distribute, rebuild scripts |

## Render

```bash
python3 java-story/v2/video_build/render_v2_from_narrative.py --ep 1
python3 java-story/v2/video_build/distribute_v2_to_episode_prs.py --ep 1
```
