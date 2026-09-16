# Episode 10 — Configuration Styles

| Field | Value |
|---|---|
| Episode | 10 |
| Title | Configuration Styles |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 10 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You can tell Spring what to build in more than one language: XML, annotations, or Java config. The choice is not fashion — it is how teams express intent.

Here is the pain this lesson exists to remove. Without mastering Configuration Styles , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Configuration Styles misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Configuration Styles.

This lesson is part of Phase 1 — SPRING FUNDAMENTALS . It builds on prior Phase 1 lessons. By Lesson 10, you should see how Configuration Styles fits into the container's definition → registration → instantiation → injection → initialization pipeline and the broader application architecture. Primary API Hybrid migration from XML to Java config Related classes XmlBeanDefinitionReader , @Import Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Configuration Styles in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. Hybrid migration from XML to Java config. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Configuration Styles to well-tested components: XmlBeanDefinitionReader , @Import Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Configuration Styles Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Configuration Styles, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Configuration Styles inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 11 — Component Scanning.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 10 (*Configuration Styles*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
