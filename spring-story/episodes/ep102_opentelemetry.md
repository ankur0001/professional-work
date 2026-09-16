# Episode 102 — OpenTelemetry

| Field | Value |
|---|---|
| Episode | 102 |
| Title | OpenTelemetry |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 102 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Logs, metrics, and traces should not be three disconnected worlds. OpenTelemetry aims at one instrumentation story.

Here is the pain this lesson exists to remove. Without mastering OpenTelemetry , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in OpenTelemetry misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is OpenTelemetry.

OpenTelemetry — Unified traces, metrics, logs — W3C tracecontext propagation. This lesson is part of Phase 11 — OBSERVABILITY & PERFORMANCE . It builds on Phase 1–10 (complete Spring development and testing stack). By Lesson 102, you should see how OpenTelemetry fits into the observability, performance, and production operations layer and the broader application architecture. Core Ideas Idea Explanation Purpose Unified traces, metrics, logs — W3C tracecontext propagation. Primary API Micrometer Tracing bridge Related classes OpenTelemetry , Tracer , Span , OtlpGrpcSpanExporter Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes OpenTelemetry in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. Micrometer Tracing bridge, OTel Java agent, OTLP export. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates OpenTelemetry to well-tested components: OpenTelemetry , Tracer , Span , OtlpGrpcSpanExporter Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for OpenTelemetry Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice OpenTelemetry, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through OpenTelemetry inside Phase 11 — Observability. The next natural question is waiting in Episode 103 — Performance Tuning.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 102 (*OpenTelemetry*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
