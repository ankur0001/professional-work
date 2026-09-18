# Episode 79 — Schedulers

| Field | Value |
|---|---|
| Episode | 79 |
| Title | Schedulers |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 79 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`Mono` and `Flux` describe what happens. Schedulers describe where it happens. In Reactor, threads are not an afterthought you sprinkle with `new Thread` — you shift execution with `publishOn` and `subscribeOn`, backed by `Schedulers` factories.

Know the common pools by role. `Schedulers.parallel()` is for non-blocking CPU-ish work across cores. `Schedulers.single()` is one dedicated thread for tasks that must be serialized. `Schedulers.boundedElastic()` is for blocking or blocking-ish legacy calls — it grows elastically up to a bound so you do not invent unbounded thread creation. `Schedulers.immediate()` runs on the caller. Netty event loops in WebFlux are precious: blocking on them stalls unrelated requests.

```java
public Mono<Report> buildReport(String id) {
    return Mono.fromCallable(() -> legacyJdbc.loadReport(id)) // blocking JDBC
        .subscribeOn(Schedulers.boundedElastic())             // run callable on elastic pool
        .flatMap(raw ->
            enricher.enrich(raw)                              // reactive HTTP → Mono
                .publishOn(Schedulers.parallel())             // CPU transform off event loop if needed
                .map(this::toReport)
        );
}

// subscribeOn: influences where the subscription upstream begins (source side)
// publishOn: switches threads for downstream operators after it appears in the chain
```

Say the difference out loud until it sticks. `subscribeOn` affects the thread where the source is subscribed — useful when the source itself blocks. `publishOn` inserts a thread hop for operators below it in the chain. Stacking them without need adds latency and confusion. Prefer keeping pure reactive I/O on the event loop and isolating blocking adapters behind `boundedElastic`.

In WebFlux, you often never call `subscribeOn` because the framework and Netty already drive non-blocking I/O. You reach for schedulers when you must integrate a blocking library, when you deliberately parallelize CPU work, or when you time deferred tasks with `Mono.delay` and friends. `Schedulers.fromExecutor` wraps an executor you already size for your service.

A misconception is wrapping every operator in `publishOn(parallel())` "for performance." Thread hops cost; measure. Another is using `boundedElastic` for everything, including non-blocking Netty calls — you lose the point of the event loop. A third is spawning unbounded `elastic()` from older Reactor habits; prefer `boundedElastic` so overload becomes visible as queueing instead of silent thread explosion.

Pipelines now know what to emit and which threads may run stages. When a fast producer meets a slow consumer — network writer, browser, or downstream service — you still need a rule for how much data may be in flight.

That rule is backpressure.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 79 (*Schedulers*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
