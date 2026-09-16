# Episode 09 — Bean Lifecycle

| Field | Value |
|---|---|
| Episode | 09 |
| Title | Bean Lifecycle |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 9 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A bean is not only created. It is initialized, ready, used, and eventually destroyed. Lifecycle hooks exist because production needs that control.

Here is the pain this lesson exists to remove. Object graphs assembled with new, lookups, and static holders become untestable and impossible to swap safely.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Bean Lifecycle.

At a practical level, Bean Lifecycle is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring’s container owns creation, wiring, and lifecycle so business types can stay plain and testable.

Once you accept the feature, the next honest question is how it works under the hood. Bean definitions are registered, post-processed, instantiated, injected, and initialized inside the ApplicationContext refresh cycle.

As you practice Bean Lifecycle, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Bean Lifecycle inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 10 — Configuration Styles.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 9 (*Bean Lifecycle*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
