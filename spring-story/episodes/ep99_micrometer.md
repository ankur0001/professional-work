# Episode 99 — Micrometer

| Field | Value |
|---|---|
| Episode | 99 |
| Title | Micrometer |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 99 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You cannot improve what you do not measure. Micrometer is Spring's facade for application metrics.

Here is the pain this lesson exists to remove. Without metrics: blind in production — "is it slow?" answered only by user complaints. Ad-hoc JMX or custom logging counters don't aggregate across 50 pods.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Micrometer.

Micrometer is the application metrics facade for Spring — a vendor-neutral API for counters, gauges, timers, and distribution summaries. Spring Boot Actuator auto-configures Micrometer and exports to Prometheus, CloudWatch, Datadog, and more. Three Pillars of Observability

A little context helps the idea stick. Micrometer created by Pivotal (2017) to unify metrics across Spring projects, replacing Spring Boot 1.x direct Dropwizard metrics. Now the standard for Boot 2.x/3.x observability.

Spring's design choice here is deliberate. Single MeterRegistry bean; @Timed / @Observed annotations; auto HTTP/JVM/DB metrics; pluggable exporters via classpath.

Once you accept the feature, the next honest question is how it works under the hood. CompositeMeterRegistry holds child registries. MeterFilter common tags (app, env, pod). Actuator MetricsEndpoint exposes snapshot; Prometheus registry formats for scrape.

As you practice Micrometer, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Micrometer inside Phase 11 — Observability. The next natural question is waiting in Episode 100 — Prometheus.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 99 (*Micrometer*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
