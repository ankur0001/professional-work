# Episode 20 — Starter Dependencies

| Field | Value |
|---|---|
| Episode | 20 |
| Title | Starter Dependencies |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 20 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Version conflicts and twenty manual dependencies used to burn a morning. Starters package a coherent stack.

Here is the pain this lesson exists to remove. Teams lost days to version alignment, manual datasource config, WAR deployment friction, and missing health endpoints before the first useful API was live.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Starter Dependencies.

At a practical level, Starter Dependencies is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Boot keeps Framework power and removes repetitive platform wiring through auto-configuration, starters, and an executable deployment model.

Once you accept the feature, the next honest question is how it works under the hood. Startup follows Environment → context creation → auto-configuration import → refresh → embedded server → readiness events.

As you practice Starter Dependencies, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Starter Dependencies inside Phase 2 — Spring Boot. The next natural question is waiting in Episode 21 — @SpringBootApplication.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 20 (*Starter Dependencies*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
