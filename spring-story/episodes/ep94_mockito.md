# Episode 94 — Mockito

| Field | Value |
|---|---|
| Episode | 94 |
| Title | Mockito |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 94 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Tests should not need a real payment gateway. Mockito replaces collaborators with controllable doubles.

Here is the pain this lesson exists to remove. Without automated proof at the right layer, regressions slip through and teams fear every deploy.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Mockito.

At a practical level, Mockito is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring’s test support and the wider Java test ecosystem let you verify units, slices, and full integrations deliberately.

Once you accept the feature, the next honest question is how it works under the hood. Test slices load only the relevant context; containers and mocks replace the rest so feedback stays fast and honest.

As you practice Mockito, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Mockito inside Phase 10 — Testing. The next natural question is waiting in Episode 95 — Spring Test.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 94 (*Mockito*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
