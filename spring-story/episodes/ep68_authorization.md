# Episode 68 — Authorization

| Field | Value |
|---|---|
| Episode | 68 |
| Title | Authorization |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 68 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Identity alone is not permission. Authorization decides what that identity is allowed to do.

Here is the pain this lesson exists to remove. Without mastering Authorization , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Authorization misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Authorization.

Authorization — Access control: authorizeHttpRequests, roles, authorities, expressions. This lesson is part of Phase 7 — SPRING SECURITY . By Lesson 68, you should see how Authorization fits into the authentication and authorization security layer and the broader application architecture. Core Ideas Idea Explanation Purpose Access control: authorizeHttpRequests, roles, authorities, expressions. Primary API hasRole Related classes AuthorizationManager , SecurityExpressionRoot , RequestAuthorizationManager Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Authorization in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. hasRole, hasAuthority, @PreAuthorize, AuthorizationManager. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Authorization to well-tested components: AuthorizationManager , SecurityExpressionRoot , RequestAuthorizationManager Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Authorization Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases).

As you practice Authorization, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Authorization inside Phase 7 — Spring Security. The next natural question is waiting in Episode 69 — JWT.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 68 (*Authorization*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
