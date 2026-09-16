# Episode 33 — Exception Handling

| Field | Value |
|---|---|
| Episode | 33 |
| Title | Exception Handling |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 33 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Failures will happen. Exception handling decides whether clients see chaos or a deliberate API error model.

Here is the pain this lesson exists to remove. Without mastering Exception Handling , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Exception Handling misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Exception Handling.

Exception Handling — @ControllerAdvice + @ExceptionHandler global error handling. This lesson is part of Phase 3 — SPRING MVC . It builds on Phase 1–2 (IoC, Boot). By Lesson 33, you should see how Exception Handling fits into the Spring web request pipeline and the broader application architecture. Core Ideas Idea Explanation Purpose @ControllerAdvice + @ExceptionHandler global error handling. Primary API @RestControllerAdvice Related classes ExceptionHandlerExceptionResolver , HandlerExceptionResolver Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Exception Handling in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. @RestControllerAdvice , ProblemDetail (RFC 7807), @ResponseStatus . This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Exception Handling to well-tested components: ExceptionHandlerExceptionResolver , HandlerExceptionResolver Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Exception Handling Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases).

As you practice Exception Handling, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Exception Handling inside Phase 3 — Spring MVC. The next natural question is waiting in Episode 34 — Filters.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 33 (*Exception Handling*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
