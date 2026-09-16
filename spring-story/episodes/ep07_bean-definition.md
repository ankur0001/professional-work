# Episode 07 — Bean Definition

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Bean Definition |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 7 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The container cannot invent beans from thin air. It needs a description of what to build. That description is a bean definition.

Here is the pain this lesson exists to remove. Object graphs assembled with new, lookups, and static holders become untestable and impossible to swap safely.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Bean Definition.

At a practical level, Bean Definition is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring’s container owns creation, wiring, and lifecycle so business types can stay plain and testable.

Once you accept the feature, the next honest question is how it works under the hood. Bean definitions are registered, post-processed, instantiated, injected, and initialized inside the ApplicationContext refresh cycle.

As you practice Bean Definition, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Bean Definition inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 08 — Bean Scopes.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 7 (*Bean Definition*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
