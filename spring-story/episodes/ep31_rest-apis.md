# Episode 31 — REST APIs

| Field | Value |
|---|---|
| Episode | 31 |
| Title | REST APIs |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 31 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

JSON over HTTP became the default integration style. REST APIs in Spring are controllers with a contract mindset.

Here is the pain this lesson exists to remove. Without mastering REST APIs , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in REST APIs misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is REST APIs.

REST APIs — Resource-oriented HTTP APIs with proper status codes and content negotiation. This lesson is part of Phase 3 — SPRING MVC . It builds on Phase 1–2 (IoC, Boot). By Lesson 31, you should see how REST APIs fits into the Spring web request pipeline and the broader application architecture. Core Ideas Idea Explanation Purpose Resource-oriented HTTP APIs with proper status codes and content negotiation. Primary API ResponseEntity Related classes MappingJackson2HttpMessageConverter , RestController Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes REST APIs in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. ResponseEntity , @GetMapping , HATEOAS, JSON via HttpMessageConverter. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates REST APIs to well-tested components: MappingJackson2HttpMessageConverter , RestController Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for REST APIs Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice REST APIs, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through REST APIs inside Phase 3 — Spring MVC. The next natural question is waiting in Episode 32 — Validation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 31 (*REST APIs*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
