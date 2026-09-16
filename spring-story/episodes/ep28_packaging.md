# Episode 28 — Packaging

| Field | Value |
|---|---|
| Episode | 28 |
| Title | Packaging |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 28 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

How you package the app decides how you deploy it. Executable JARs changed the default story for Spring services.

Here is the pain this lesson exists to remove. Without mastering Packaging , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Packaging misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Packaging.

Packaging — Executable fat JAR, WAR for external Tomcat, layered JAR, GraalVM native. This lesson is part of Phase 2 — SPRING BOOT . It builds on Phase 1 lessons. By Lesson 28, you should see how Packaging fits into the container's definition → registration → instantiation → injection → initialization pipeline and the broader application architecture. Primary API Spring-Boot-Jar-Launcher Related classes SpringBootJarLauncher , LayersIndex , native-maven-plugin Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Packaging in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. Spring-Boot-Jar-Launcher , BOOT-INF/classes , BOOT-INF/lib . This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Packaging to well-tested components: SpringBootJarLauncher , LayersIndex , native-maven-plugin Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Packaging Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Packaging, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Packaging inside Phase 2 — Spring Boot. The next natural question is waiting in Episode 29 — DispatcherServlet.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 28 (*Packaging*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
