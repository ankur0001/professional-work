# Episode 35 — Interceptors

| Field | Value |
|---|---|
| Episode | 35 |
| Title | Interceptors |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 35 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Filters are servlet-level. Interceptors speak Spring MVC’s language — handlers, models, and views.

Here is the pain this lesson exists to remove. Without a clear request pipeline, encoding, security, exception handling, and routing get duplicated across servlets and controllers.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Interceptors.

At a practical level, Interceptors is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Spring MVC centralizes the HTTP pipeline so controllers stay thin and cross-cutting request concerns stay consistent.

Once you accept the feature, the next honest question is how it works under the hood. DispatcherServlet receives the request, resolves a handler, runs interceptors/advice, invokes the controller, and renders the response.

As you practice Interceptors, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Interceptors inside Phase 3 — Spring MVC. The next natural question is waiting in Episode 36 — File Upload.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 35 (*Interceptors*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
