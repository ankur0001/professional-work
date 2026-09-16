# Episode 27 — Profiles

| Field | Value |
|---|---|
| Episode | 27 |
| Title | Profiles |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 27 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Boot inherits profiles, then makes them feel natural through application-*.yml and spring.profiles.active.

Here is the pain this lesson exists to remove. Without mastering Profiles (Spring Boot) , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Boot Profiles misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Profiles.

Profiles (Spring Boot) — application-{profile}.yml, spring.profiles.active, profile groups. This lesson is part of Phase 2 — SPRING BOOT . It builds on Phase 1 lessons. By Lesson 27, you should see how Boot Profiles fits into the container's definition → registration → instantiation → injection → initialization pipeline and the broader application architecture. Primary API spring.profiles.group Related classes Profile-specific PropertySource , spring.config.activate.on-profile Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Boot Profiles in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. spring.profiles.group , @Profile with Boot config files. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Boot Profiles to well-tested components: Profile-specific PropertySource , spring.config.activate.on-profile Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Boot Profiles Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Profiles, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Profiles inside Phase 2 — Spring Boot. The next natural question is waiting in Episode 28 — Packaging.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 27 (*Profiles*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
