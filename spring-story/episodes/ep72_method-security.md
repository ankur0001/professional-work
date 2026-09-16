# Episode 72 — Method Security

| Field | Value |
|---|---|
| Episode | 72 |
| Title | Method Security |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 72 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

URL rules are not enough when service methods are the real boundary. Method security guards the domain.

Here is the pain this lesson exists to remove. Without mastering Method Security , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Method Security misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Method Security.

Method Security — @PreAuthorize, @PostAuthorize, @Secured on service methods. This lesson is part of Phase 7 — SPRING SECURITY . By Lesson 72, you should see how Method Security fits into the authentication and authorization security layer and the broader application architecture. Core Ideas Idea Explanation Purpose @PreAuthorize, @PostAuthorize, @Secured on service methods. Primary API @EnableMethodSecurity Related classes MethodSecurityInterceptor , @PreAuthorize , PrePostAnnotationSecurityMetadataSource Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Method Security in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. @EnableMethodSecurity, SpEL expressions, JSR-250. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Method Security to well-tested components: MethodSecurityInterceptor , @PreAuthorize , PrePostAnnotationSecurityMetadataSource Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Method Security Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases).

As you practice Method Security, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Method Security inside Phase 7 — Spring Security. The next natural question is waiting in Episode 73 — CSRF.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 72 (*Method Security*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
