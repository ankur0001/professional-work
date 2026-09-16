# Episode 34 — Filters

| Field | Value |
|---|---|
| Episode | 34 |
| Title | Filters |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 34 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Some work must run before controllers wake up. Filters sit on the servlet chain for that reason.

Here is the pain this lesson exists to remove. Without a clear request pipeline, encoding, security, exception handling, and routing get duplicated across servlets and controllers.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Filters.

At a practical level, Filters is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring MVC centralizes the HTTP pipeline so controllers stay thin and cross-cutting request concerns stay consistent.

Once you accept the feature, the next honest question is how it works under the hood. DispatcherServlet receives the request, resolves a handler, runs interceptors/advice, invokes the controller, and renders the response.

As you practice Filters, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Filters inside Phase 3 — Spring MVC. The next natural question is waiting in Episode 35 — Interceptors.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 34 (*Filters*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
