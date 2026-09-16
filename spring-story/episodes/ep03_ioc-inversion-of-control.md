# Episode 03 — IoC (Inversion of Control)

| Field | Value |
|---|---|
| Episode | 03 |
| Title | IoC (Inversion of Control) |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 3 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

If Spring’s job is to assemble your application for you, then something has flipped: control no longer starts in your constructors.

Here is the pain this lesson exists to remove. Object graphs assembled with new, lookups, and static holders become untestable and impossible to swap safely.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is IoC (Inversion of Control).

At a practical level, IoC (Inversion of Control) is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring’s container owns creation, wiring, and lifecycle so business types can stay plain and testable.

Once you accept the feature, the next honest question is how it works under the hood. Bean definitions are registered, post-processed, instantiated, injected, and initialized inside the ApplicationContext refresh cycle.

As you practice IoC (Inversion of Control), keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through IoC (Inversion of Control) inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 04 — Dependency Injection.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 3 (*IoC (Inversion of Control)*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
