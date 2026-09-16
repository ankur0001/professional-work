# Episode 05 — BeanFactory

| Field | Value |
|---|---|
| Episode | 05 |
| Title | BeanFactory |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 5 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Dependency injection needs a place to live. At the lowest level of Spring, that place is BeanFactory.

Here is the pain this lesson exists to remove. Object graphs assembled with new, lookups, and static holders become untestable and impossible to swap safely.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is BeanFactory.

At a practical level, BeanFactory is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring’s container owns creation, wiring, and lifecycle so business types can stay plain and testable.

Once you accept the feature, the next honest question is how it works under the hood. Bean definitions are registered, post-processed, instantiated, injected, and initialized inside the ApplicationContext refresh cycle.

As you practice BeanFactory, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through BeanFactory inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 06 — ApplicationContext.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 5 (*BeanFactory*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
