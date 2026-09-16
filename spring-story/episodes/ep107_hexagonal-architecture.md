# Episode 107 — Hexagonal Architecture

| Field | Value |
|---|---|
| Episode | 107 |
| Title | Hexagonal Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 107 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

When frameworks leak into the domain, change gets expensive. Hexagonal architecture puts the domain in the center.

Here is the pain this lesson exists to remove. Without clear boundaries, frameworks leak into the domain and every change becomes expensive.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Hexagonal Architecture.

At a practical level, Hexagonal Architecture is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Architectural styles give teams a shared language for boundaries, dependencies, and change.

Once you accept the feature, the next honest question is how it works under the hood. Dependency direction and boundary rules decide what can know about what — and what stays replaceable.

As you practice Hexagonal Architecture, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Hexagonal Architecture inside Phase 12 — Enterprise Architecture. The next natural question is waiting in Episode 108 — Clean Architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 107 (*Hexagonal Architecture*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
