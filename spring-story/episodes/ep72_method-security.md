# Episode 72 — Method Security

| Field | Value |
|---|---|
| Episode | 72 |
| Title | Method Security |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 72 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

URL rules are not enough when service methods are the real boundary. Method security guards the domain.

Here is the pain this lesson exists to remove. Open endpoints, weak identity checks, and ad-hoc authorization rules turn APIs into production incidents waiting to happen.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Method Security.

At a practical level, Method Security is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring Security provides a filter chain and authorization model so identity and access rules are explicit and testable.

Once you accept the feature, the next honest question is how it works under the hood. Security filters sit in a chain before controllers; Authentication establishes identity and Authorization enforces decisions.

As you practice Method Security, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Method Security inside Phase 7 — Spring Security. The next natural question is waiting in Episode 73 — CSRF.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 72 (*Method Security*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
