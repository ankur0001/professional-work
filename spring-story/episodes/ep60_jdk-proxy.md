# Episode 60 — JDK Proxy

| Field | Value |
|---|---|
| Episode | 60 |
| Title | JDK Proxy |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 60 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

If your class implements an interface, Spring can often wrap it with a JDK dynamic proxy.

Here is the pain this lesson exists to remove. Without mastering JDK Proxy , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in JDK Proxy misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is JDK Proxy.

JDK Proxy — java.lang.reflect.Proxy — interface-based proxies only. This lesson is part of Phase 6 — SPRING AOP . By Lesson 60, you should see how JDK Proxy fits into the cross-cutting concern interception layer and the broader application architecture. Core Ideas Idea Explanation Purpose java.lang.reflect.Proxy — interface-based proxies only. Primary API InvocationHandler.invoke() Related classes JdkDynamicAopProxy , Proxy.newProxyInstance() Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes JDK Proxy in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. InvocationHandler.invoke(), requires interface on target. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates JDK Proxy to well-tested components: JdkDynamicAopProxy , Proxy.newProxyInstance() Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for JDK Proxy Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice JDK Proxy, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through JDK Proxy inside Phase 6 — Spring AOP. The next natural question is waiting in Episode 61 — CGLIB.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 60 (*JDK Proxy*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
