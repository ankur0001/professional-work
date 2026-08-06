# The Java Story — Episode 02

**JDK, JRE, and JVM** · Handbook Lesson 2 · ~4–5 minutes

## Watch

| File | Description |
|---|---|
| [`output/Java_Episode_02_JDK_JRE_JVM.mp4`](output/Java_Episode_02_JDK_JRE_JVM.mp4) | Final cut |
| [`output/Java_Episode_02_JDK_JRE_JVM_CAPTIONED.mp4`](output/Java_Episode_02_JDK_JRE_JVM_CAPTIONED.mp4) | Captioned |
| [`output/Java_Episode_02.srt`](output/Java_Episode_02.srt) | Subtitles |

## Rebuild

```bash
pip3 install 'kokoro>=0.9.4' soundfile
export KOKORO_VOICE=am_michael
python3 video_build/make_episode_02.py
```

## Continuity

- Previous: Episode 01 — Why Java Exists
- Next: Episode 03 — Java Program Structure

See [`series/EPISODE_CATALOG.md`](series/EPISODE_CATALOG.md) for the full 80-lesson roadmap.

**Policy:** one episode per PR; stop at Cursor usage limits — do not batch-render the catalog.
