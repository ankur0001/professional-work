# The Java Story — v2 video output

Animated narrative cut (not text-wall slides):

- **Audio:** Chatterbox Turbo TTS from coherent episode narrations
- **Visuals:** `visual_engine.py` scene types — title, flow, stack, pipeline,
  lanes, code window, nodes, rings, compare, callout, question
- **Motion:** per-beat frame animation (draw-in, arrows, task motion) + lower-thirds

## Rebuild visuals only (keep existing narration)

```bash
python3 all-work/java-story/video_build/render_v2_from_narrative.py --ep 1-5 --reuse-audio
python3 all-work/java-story/video_build/distribute_v2_to_episode_prs.py --ep 1-5
```

## Full render (TTS + visuals)

```bash
python3 all-work/java-story/video_build/render_v2_from_narrative.py --ep 85
```
