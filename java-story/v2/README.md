# The Java Story — v2 (current cut)

YouTube upload packs for all 85 episodes (coherent narration + animated visuals).

Each folder under [`episodes/`](episodes/) contains title, description with timestamps, tags, thumbnail, videos, SRT, narration, and SOURCE.

Shared:
- [`narrative_review/`](narrative_review/) — narration sources
- [`video_build/`](video_build/) — render tooling

See [`INDEX.md`](INDEX.md).

## Thumbnails

Episode `thumbnail.jpg` files are **branded stills** (1920×1080) in a blue Spring-Story-style layout — not video frames and not captioned frames. Regenerate with:

```bash
python3 java-story/v2/video_build/regenerate_blue_thumbnails.py
```
