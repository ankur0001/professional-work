# Episode 45 — Criteria API

| Field | Value |
|---|---|
| Episode | 45 |
| Title | Criteria API |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 45 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Dynamic queries do not love string concatenation. The Criteria API builds queries as objects.

Here is the pain this lesson exists to remove. Object-relational work without discipline produces N+1 queries, lazy-load surprises, and SQL you only discover when production latency spikes.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Criteria API.

At a practical level, Criteria API is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring Data and JPA give a productive persistence model while still letting you drop to explicit queries when performance demands it.

Once you accept the feature, the next honest question is how it works under the hood. Entities move through lifecycle states inside a persistence context; flush and commit translate the unit of work into SQL.

As you practice Criteria API, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Criteria API inside Phase 4 — Spring Data JPA. The next natural question is waiting in Episode 46 — Specifications.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 45 (*Criteria API*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
