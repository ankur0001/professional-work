# Episode 53 — Propagation

| Field | Value |
|---|---|
| Episode | 53 |
| Title | Propagation |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 53 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Nested service calls raise a hard question: share one transaction, or start another? Propagation answers it.

Here is the pain this lesson exists to remove. Multi-step database work without clear transaction boundaries leaves partial writes, inconsistent reads, and rollback surprises.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Propagation.

At a practical level, Propagation is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring transaction management declares boundaries once and applies them consistently through proxies, not copy-pasted begin/commit code.

Once you accept the feature, the next honest question is how it works under the hood. AOP proxies intercept annotated methods, bind a transaction to the thread, and commit or roll back based on outcome and rules.

As you practice Propagation, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Propagation inside Phase 5 — Transaction Management. The next natural question is waiting in Episode 54 — Isolation Levels.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 53 (*Propagation*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
