# Episode 105 — Production Readiness

| Field | Value |
|---|---|
| Episode | 105 |
| Title | Production Readiness |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 105 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Feature-complete is not production-ready. Readiness is the checklist that ships with confidence.

Here is the pain this lesson exists to remove. Without mastering Production Readiness , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Production Readiness misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Production Readiness.

Production Readiness — 12-factor checklist: health, metrics, graceful shutdown, runbooks. This lesson is part of Phase 11 — OBSERVABILITY & PERFORMANCE . It builds on Phase 1–10 (complete Spring development and testing stack). By Lesson 105, you should see how Production Readiness fits into the observability, performance, and production operations layer and the broader application architecture. Core Ideas Idea Explanation Purpose 12-factor checklist: health, metrics, graceful shutdown, runbooks. Primary API SLOs Related classes Actuator health groups, readiness/liveness, server.shutdown=graceful Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Production Readiness in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. SLOs, on-call playbooks, chaos testing, capacity planning. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Production Readiness to well-tested components: Actuator health groups, readiness/liveness, server.shutdown=graceful Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Production Readiness Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases).

As you practice Production Readiness, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Production Readiness inside Phase 11 — Observability. The next natural question is waiting in Episode 106 — Layered Architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 105 (*Production Readiness*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
