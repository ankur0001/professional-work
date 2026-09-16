# Episode 65 — Performance

| Field | Value |
|---|---|
| Episode | 65 |
| Title | Performance |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 65 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Proxies are not free. AOP performance is about knowing when the abstraction costs real latency.

Here is the pain this lesson exists to remove. Without mastering Performance , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in AOP Performance misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Performance.

Performance — Proxy overhead, pointcut matching cost, excessive @Around. This lesson is part of Phase 6 — SPRING AOP . By Lesson 65, you should see how AOP Performance fits into the cross-cutting concern interception layer and the broader application architecture. Core Ideas Idea Explanation Purpose Proxy overhead, pointcut matching cost, excessive @Around. Primary API Prefer @Before/@AfterReturning over @Around when possible Related classes ReflectiveMethodInvocation , proxy caching, hot path profiling Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes AOP Performance in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. Prefer @Before/@AfterReturning over @Around when possible. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates AOP Performance to well-tested components: ReflectiveMethodInvocation , proxy caching, hot path profiling Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for AOP Performance Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Performance, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Performance inside Phase 6 — Spring AOP. The next natural question is waiting in Episode 66 — Security Fundamentals.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 65 (*Performance*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
