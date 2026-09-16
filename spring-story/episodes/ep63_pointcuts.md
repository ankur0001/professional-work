# Episode 63 — Pointcuts

| Field | Value |
|---|---|
| Episode | 63 |
| Title | Pointcuts |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 63 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Advice without a precise join-point language sprays behavior everywhere. Pointcuts restore aim.

Here is the pain this lesson exists to remove. Logging, security, and transactions get copy-pasted into every service method until cross-cutting concerns dominate the codebase.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Pointcuts.

At a practical level, Pointcuts is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring AOP modularizes cross-cutting behavior with proxies so domain methods stay about the domain.

Once you accept the feature, the next honest question is how it works under the hood. Spring builds a proxy around the bean; join points matching a pointcut run advice before, after, or around the target method.

As you practice Pointcuts, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Pointcuts inside Phase 6 — Spring AOP. The next natural question is waiting in Episode 64 — Aspect Ordering.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 63 (*Pointcuts*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
