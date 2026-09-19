# Spring Story

Episode-by-episode **spoken narrations** for the Spring / Spring Boot handbook series.

This folder sits **parallel to** `java-story` / `java` and is sourced from `Spring_Framework_Handbook.html` (112 lessons → 112 episodes).

## Layout

```
spring-story/
├── README.md
├── EXPANSION_STYLE.md
├── INDEX.md
├── EPISODE_CATALOG.md
├── episodes/          # source narrations
│   ├── ep01_why-spring.md
│   └── …
└── v1/                # YouTube upload packs (per episode)
    ├── README.md
    ├── INDEX.md
    └── episodes/
        ├── ep01-why-spring/
        │   ├── title.txt
        │   ├── youtube_description.txt
        │   ├── tags.txt
        │   ├── chapters.txt
        │   ├── thumbnail.jpg
        │   ├── narration.md
        │   └── README.md
        └── …
```

## YouTube upload packs (`v1/`)

Each episode has a ready-to-upload kit under [`v1/`](v1/README.md) — title, description (with timestamps), tags, chapters, and a **branded 1920×1080 thumbnail** (designed still; not a video frame, no burned-in subtitles). Video/SRT land in a later production pass. See [`v1/INDEX.md`](v1/INDEX.md).

## Review first (gold standards)

These three are hand-expanded continuous spoken lessons — start review here:

1. [`episodes/ep01_why-spring.md`](episodes/ep01_why-spring.md) — Why Spring?
2. [`episodes/ep04_dependency-injection.md`](episodes/ep04_dependency-injection.md) — Dependency Injection
3. [`episodes/ep17_why-spring-boot.md`](episodes/ep17_why-spring-boot.md) — Why Spring Boot?

## Technique

Same teaching technique as the Java Story narrative gold standards (see `EXPANSION_STYLE.md`):

- situation → problem → natural question → Spring’s answer
- integrated example / code walkthrough
- common misunderstanding
- bridge to the next episode

Runtime target per episode: **4–15 minutes** (aim ~10–12).

## Phases (handbook)

| Phase | Episodes | Theme |
|---|---|---|
| 1 | 01–16 | Spring Fundamentals |
| 2 | 17–28 | Spring Boot |
| 3 | 29–37 | Spring MVC |
| 4 | 38–51 | Spring Data JPA |
| 5 | 52–57 | Transaction Management |
| 6 | 58–65 | Spring AOP |
| 7 | 66–75 | Spring Security |
| 8 | 76–82 | Reactive Spring |
| 9 | 83–92 | Spring Cloud |
| 10 | 93–98 | Testing |
| 11 | 99–105 | Observability |
| 12 | 106–112 | Enterprise Architecture |

## Source

Narrations are derived from `Spring_Framework_Handbook.html` (InterviewPrep / public handbook), lesson-by-lesson. They are teaching scripts, not a verbatim dump of the HTML.


## Videos (`v1/`)

YouTube videos are rendered with the same motion-graphics pipeline as The Java Story v2:

- Tooling: [`v1/video_build/`](v1/video_build/README.md)
- Per episode: clean MP4, captioned MP4, and SRT alongside the upload pack
- Batch: `bash spring-story/v1/video_build/batch_render.sh`
