# Episode 94 — Mockito

| Field | Value |
|---|---|
| Episode | 94 |
| Title | Mockito |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 94 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Tests should not need a real payment gateway. Mockito replaces collaborators with controllable doubles.

Here is the pain this lesson exists to remove. Without mastering Mockito , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Mockito misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Mockito.

Mockito — Mock dependencies for isolated unit tests — when, verify, ArgumentCaptor. This lesson is part of Phase 10 — TESTING . It builds on Phase 1–9 (full stack including Spring Cloud). By Lesson 94, you should see how Mockito fits into the test automation and quality assurance layer and the broader application architecture. Core Ideas Idea Explanation Purpose Mock dependencies for isolated unit tests — when, verify, ArgumentCaptor. Primary API @Mock Related classes Mockito , MockitoExtension , ArgumentCaptor Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Mockito in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. @Mock, @InjectMocks, MockitoExtension, stubbing void methods. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Mockito to well-tested components: Mockito , MockitoExtension , ArgumentCaptor Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Mockito Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Mockito, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Mockito inside Phase 10 — Testing. The next natural question is waiting in Episode 95 — Spring Test.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 94 (*Mockito*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
