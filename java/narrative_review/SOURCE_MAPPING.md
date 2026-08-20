# Handbook → Episode source mapping

## Reference document

| Field | Value |
|---|---|
| Original attachment | `Java_JVM_Handbook_GPT55__1_.html` (uploaded in the Cursor agent chat) |
| Document title | **Java & JVM Handbook — 80 Lessons** |
| How the series used it | **Topic / curriculum reference** — not a verbatim teleprompter script |
| User instruction (paraphrase) | Take content reference from the attached HTML; write narration that matches the on-screen presentation; raise one PR per episode video |

The full HTML is **not in git**. Recovered fragments live in [`reference/`](reference/).

## Mapping rules used in this review pack

1. **Episodes 01–20** — treat as **1:1** with handbook Lessons 1–20 (titles align in the recovered TOC).
2. **Episodes 21–25** — handbook Lesson 21 was *Collection Framework Overview*; the YouTube catalog **shifts** List/Set/Map/Queue into Ep 21–24 and inserts *Sorting and Comparators* as Ep 25. Attribution files call out the handbook lesson that matches the **topic**, not only the same number.
3. **Episodes 26–80** — follow `reference/EPISODE_CATALOG.md`. Where recovered handbook nav titles diverge from the catalog (see `handbook_toc_recovered.md`), the episode file states the divergence and attributes by **topic**.
4. **Episodes 81–85** — Season 2 bonus; **not** handbook lessons.
5. **Narration text** in each `episodes/epXX_*.md` is extracted from the production `SCENES` lists in `make_episode_XX.py` (Episode 01 from the short-cut script). Those beats are what Chatterbox/Kokoro spoke in the rendered videos.

## What “took from the handbook” means

| Taken from handbook | Not taken verbatim |
|---|---|
| Lesson topic / learning objective | Full lesson prose / long explanations |
| Core definitions & distinctions (e.g. JDK vs JRE vs JVM) | Textbook tone |
| Standard examples & interview angles | Exact sentence order |
| Phase structure (language → collections → concurrency → JVM → Spring) | 12–15 minute lesson length |

Videos target a **4–15 minute** conversational documentary (floor 4 minutes, soft aim ~8–12, ceiling ~15) with continuity teasers between episodes. Narration in this pack was **expanded** after review feedback that the first short-cut scripts were too thin.

## Episode 01 special case

Episode 01 also has a long-form production bible (`java-episode-01-production-bible.md` on the Episode 01 PR branch). The review file `ep01_*.md` is now the **expanded conversational narration** (history + bytecode/JVM + walked-through `HelloWorld`), based on handbook Lesson 1 (*Introduction to Java*), not the ultra-short headline cut.
