# Episode 108 — Clean Architecture

| Field | Value |
|---|---|
| Episode | 108 |
| Title | Clean Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 108 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Clean architecture sharpens the dependency rule: business rules should not know about web or database details.

Here is the pain this lesson exists to remove. Without mastering Clean Architecture , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Clean Architecture misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Clean Architecture.

Clean Architecture — Uncle Bob concentric rings — dependencies point inward to domain. This lesson is part of Phase 12 — ENTERPRISE ARCHITECTURE . It builds on Phases 1–11 (complete Spring platform mastery). By Lesson 108, you should see how Clean Architecture fits into the enterprise architecture and Solution Architect decision layer and the broader application architecture. Core Ideas Idea Explanation Purpose Uncle Bob concentric rings — dependencies point inward to domain.

Spring's design choice here is deliberate. Spring centralizes Clean Architecture in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Clean Architecture to well-tested components: Use case classes, boundary interfaces, framework as outer shell Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Clean Architecture Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases).

As you practice Clean Architecture, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Clean Architecture inside Phase 12 — Enterprise Architecture. The next natural question is waiting in Episode 109 — DDD Basics.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 108 (*Clean Architecture*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
