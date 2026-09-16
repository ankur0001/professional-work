# Episode 05 — BeanFactory

| Field | Value |
|---|---|
| Episode | 05 |
| Title | BeanFactory |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 5 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Dependency injection needs a place to live. That place, at the lowest level of Spring, is BeanFactory.

Here is the pain this lesson exists to remove. Without mastering BeanFactory , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in BeanFactory misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is BeanFactory.

BeanFactory — Low-level IoC container interface; bean definition registry. This lesson is part of Phase 1 — SPRING FUNDAMENTALS . It builds on prior Phase 1 lessons. By Lesson 5, you should see how BeanFactory fits into the container's definition → registration → instantiation → injection → initialization pipeline and the broader application architecture. Primary API DefaultListableBeanFactory Related classes AbstractBeanFactory , FactoryBean Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes BeanFactory in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. DefaultListableBeanFactory , getBean() , containsBeanDefinition() . This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates BeanFactory to well-tested components: AbstractBeanFactory , FactoryBean Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for BeanFactory Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice BeanFactory, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through BeanFactory inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 06 — ApplicationContext.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 5 (*BeanFactory*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
