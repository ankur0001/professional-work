# Episode 32 — Validation

| Field | Value |
|---|---|
| Episode | 32 |
| Title | Validation |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 32 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Trusting request bodies is how bad data enters your system. Validation belongs at the boundary.

Here is the pain this lesson exists to remove. Without mastering Validation , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Validation misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Validation.

Validation — Bean Validation (JSR-380) with @Valid and BindingResult. This lesson is part of Phase 3 — SPRING MVC . It builds on Phase 1–2 (IoC, Boot). By Lesson 32, you should see how Validation fits into the Spring web request pipeline and the broader application architecture. Primary API @NotNull Related classes LocalValidatorFactoryBean , BindingResult , @Validated Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Validation in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. @NotNull , @Size , @Email , MethodValidationPostProcessor . This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Validation to well-tested components: LocalValidatorFactoryBean , BindingResult , @Validated Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Validation Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Validation, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Validation inside Phase 3 — Spring MVC. The next natural question is waiting in Episode 33 — Exception Handling.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 32 (*Validation*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
