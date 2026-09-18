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

The AIS feed publishes dozens of fixes per second. The operator UI on a congested laptop paints one map update at a time. Without a demand signal, the reactive chain buffers until memory hurts, latency spikes, then the console collapses. Schedulers placed work on threads. Backpressure answers how much work is allowed to be outstanding.

In Reactive Streams, the subscriber tells the publisher how many items it requests through the `Subscription`. Publishers should respect that demand. That conversation is backpressure. Classic imperative code hides the same problem behind thread pools and blocking queues; reactive makes the demand signal explicit.

```java
Flux<AisFix> incoming = aisFeed.live(); // potentially high-rate source

Flux<AisFix> protectedFlow = incoming
    .onBackpressureLatest()                 // UI gauges: newest fix wins
    .flatMap(this::persistAsync, 4)         // limit in-flight persists
    .doOnRequest(n -> log.debug("UI requested {}", n));

// Alternative strategies (pick deliberately):
// onBackpressureBuffer(256)  — bounded buffer for short bursts
// onBackpressureDrop()       — drop when consumer is slow (telemetry sometimes OK)
// onBackpressureBuffer(n, overflowHandler) — bounded + explicit overflow
// limitRate(32)              — prefetch / request in chunks toward upstream
```

Prefetch matters. Many operators request a batch ahead of time for throughput. `limitRate` helps shape how demand is propagated upstream. `flatMap` concurrency caps how many inner publishers run at once — that is also a backpressure-related control, even though it is not named `onBackpressure*`.

Strategies are product decisions. Buffering smooths bursts until memory hurts — always bound the buffer. Dropping suits metrics where staleness beats crash. Latest suits operator map gauges — a stale position is worse than a skipped one when the UI is slow. Erroring on overflow makes failure visible when silent loss is unacceptable. There is no universal default that saves you from thinking.

In WebFlux, the HTTP response and Netty watermarks participate in demand. If you return a `Flux` as SSE for `/positions/stream`, a slow client should slow generation when the pipeline is wired correctly. If you assemble an in-memory list with `collectList()` first, you already opted out of streaming backpressure for that payload — fine for small pages, dangerous for unbounded AIS history.

A misconception is “reactive automatically prevents OOM.” It prevents OOM only when operators and sources honor bounded demand. A blocking JDBC `Flux` created by hammering a cursor without limits can still blow memory. Another misconception is using unbounded `onBackpressureBuffer()` and calling it production-ready. Name the bound. A third is confusing backpressure with circuit breaking — related resilience themes, different mechanisms.

We now have publishers, thread control, and demand control. The missing piece in the Spring stack is the web layer that speaks HTTP with these types end to end — routers, annotated controllers returning `Mono`/`Flux`, and a runtime that is not `DispatcherServlet`.

That layer is Spring WebFlux.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 80 (*Backpressure*).
