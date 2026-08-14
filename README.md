# The Java Story (YouTube Series)

Premium short documentaries (4–5 min each) from the Java & JVM Handbook (80 lessons).

## Episodes

| Ep | Title | Video |
|---:|---|---|
| 01 | Why Java Exists | See PR #1 branch |
| 02 | JDK, JRE, and JVM | [`output/Java_Episode_02_JDK_JRE_JVM.mp4`](output/Java_Episode_02_JDK_JRE_JVM.mp4) |

Full roadmap: [`series/EPISODE_CATALOG.md`](series/EPISODE_CATALOG.md)

## Rebuild Episode 02

```bash
pip3 install 'kokoro>=0.9.4' soundfile numpy pillow
export KOKORO_VOICE=am_michael
python3 video_build/make_episode_02.py
```

## Rules

- One episode → one git branch → one PR
- Stop when approaching Cursor usage limits (no paid overage)
- Do not batch-generate the full catalog in one run
