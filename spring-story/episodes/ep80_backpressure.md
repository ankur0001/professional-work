# Episode 80 — Backpressure

| Field | Value |
|---|---|
| Episode | 80 |
| Title | Backpressure |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 80 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Schedulers place work on threads. Backpressure answers how much work is allowed to be outstanding. In Reactive Streams, the subscriber tells the publisher how many items it requests through the `Subscription`. Publishers should respect that demand. That conversation is backpressure.

Without it, a fast source can overwhelm a slow sink: unbounded queues, memory growth, latency spikes, then collapse. Classic imperative code hides the same problem behind thread pools and blocking queues; reactive makes the demand signal explicit.

```java
Flux<Event> incoming = eventSource.stream(); // potentially high-rate cold/hot source

Flux<Event> protectedFlow = incoming
    .onBackpressureBuffer(256)                 // bounded buffer strategy
    .flatMap(this::persistAsync, 4)            // limit in-flight persists
    .doOnRequest(n -> log.debug("downstream requested {}", n));

// Alternative strategies (pick deliberately):
// onBackpressureDrop()     — drop when consumer is slow (telemetry sometimes OK)
// onBackpressureLatest()   — keep only newest (UI gauges)
// onBackpressureBuffer(n, overflowHandler) — bounded + explicit overflow behavior
// limitRate(32)            — prefetch / request in chunks toward upstream
```

Prefetch matters. Many operators request a batch ahead of time for throughput. `limitRate` helps shape how demand is propagated upstream. `flatMap` concurrency caps how many inner publishers run at once — that is also a backpressure-related control, even though it is not named `onBackpressure*`.

Strategies are product decisions. Buffering smooths bursts until memory hurts — always bound the buffer. Dropping suits metrics where staleness beats crash. Latest suits dashboards. Erroring on overflow makes failure visible when silent loss is unacceptable. There is no universal default that saves you from thinking.

In WebFlux, the HTTP response and Netty watermarks participate in demand. If you return a `Flux` as SSE, a slow client should slow generation when the pipeline is wired correctly. If you assemble an in-memory list with `collectList()` first, you already opted out of streaming backpressure for that payload — fine for small pages, dangerous for unbounded queries.

A misconception is "reactive automatically prevents OOM." It prevents OOM only when operators and sources honor bounded demand. A blocking JDBC `Flux` created by hammering a cursor without limits can still blow memory. Another misconception is using unbounded `onBackpressureBuffer()` and calling it production-ready. Name the bound. A third is confusing backpressure with circuit breaking — related resilience themes, different mechanisms.

We now have publishers, thread control, and demand control. The missing piece in the Spring stack is the web layer that speaks HTTP with these types end to end — routers, annotated controllers returning `Mono`/`Flux`, and a runtime that is not `DispatcherServlet`.

That layer is Spring WebFlux.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 80 (*Backpressure*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
