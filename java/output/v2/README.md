# The Java Story — v2 narrative video cuts

Rendered from coherent spoken narrations in `java/narrative_review/episodes/`
using local Chatterbox Turbo TTS + slide assembly.

Per episode deliverables (copied into each episode PR under this same folder):

- `Java_Episode_XX_*.mp4` — clean cut
- `Java_Episode_XX_*_CAPTIONED.mp4` — burned captions
- `Java_Episode_XX.srt` — subtitles
- `Java_Episode_XX_SOURCE.md` / `narration.md` — source pointer

Renderer: `java/video_build/render_v2_from_narrative.py`
Distributor: `java/video_build/distribute_v2_to_episode_prs.py`
