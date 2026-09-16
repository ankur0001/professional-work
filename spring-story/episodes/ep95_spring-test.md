# Episode 95 — Spring Test

| Field | Value |
|---|---|
| Episode | 95 |
| Title | Spring Test |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 95 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Unit tests miss the container. Spring Test loads slices of the context so wiring can be verified.

Here is the pain this lesson exists to remove. Without mastering Spring Test , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Spring Test misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Spring Test.

Spring Test — Spring TestContext Framework — load partial or full context in tests. This lesson is part of Phase 10 — TESTING . It builds on Phase 1–9 (full stack including Spring Cloud). By Lesson 95, you should see how Spring Test fits into the test automation and quality assurance layer and the broader application architecture. Core Ideas Idea Explanation Purpose Spring TestContext Framework — load partial or full context in tests. Primary API @SpringBootTest Related classes SpringExtension , TestContextManager , @MockBean Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Spring Test in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. @SpringBootTest, @WebMvcTest, @DataJpaTest, @MockBean, ApplicationContextRunner. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Spring Test to well-tested components: SpringExtension , TestContextManager , @MockBean Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Spring Test Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Spring Test, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Spring Test inside Phase 10 — Testing. The next natural question is waiting in Episode 96 — Integration Testing.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 95 (*Spring Test*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
