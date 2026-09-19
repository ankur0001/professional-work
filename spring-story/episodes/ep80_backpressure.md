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

Flux<AisFix> toMapUi = incoming
        .onBackpressureLatest()              // map gauge: newest fix wins
        .doOnRequest(n -> log.debug("UI requested {}", n));

Flux<AisFix> toArchive = incoming
        .onBackpressureBuffer(256)           // short bursts OK; bound the queue
        .flatMap(this::persistAsync, 4);     // also cap in-flight persists
```

Those two chains are different policies for the same producer/consumer mismatch — not interchangeable knobs.

Buffering with `onBackpressureBuffer(n)` keeps up to *n* fixes when the consumer hiccups, then applies an overflow policy (error, drop oldest, and so on). Use it for short bursts you cannot afford to lose — a brief UI freeze while archiving still wants those positions. Always bound the buffer; unbounded buffer is a deferred OOM.

Dropping with `onBackpressureDrop()` discards new signals when demand is zero. Use it when a missed AIS tick is acceptable and crashing is not — some telemetry fits here. It is wrong for ledger-like persistence.

Latest-value with `onBackpressureLatest()` keeps only the newest unread fix; older pending values lose. That fits operator map gauges, where a stale ship position is worse than a skipped intermediate one. It is wrong when every event must be processed.

Rate shaping — `limitRate`, or `flatMap` concurrency — controls how demand is requested upstream or how many inner publishers run at once. That is still backpressure: you are limiting outstanding work, even when the method name does not start with `onBackpressure`.

Prefetch is part of the same story. Many operators request a batch ahead for throughput. That helps until the batch is larger than the consumer can absorb — then you are back to choosing buffer, drop, latest, or fail. There is no universal default that saves you from naming the product policy.

In WebFlux, the HTTP response and Netty watermarks participate in demand. If you return a `Flux` as SSE for `/positions/stream`, a slow client should slow generation when the pipeline is wired correctly. If you assemble an in-memory list with `collectList()` first, you already opted out of streaming backpressure for that payload — fine for small pages, dangerous for unbounded AIS history.

A misconception is “reactive automatically prevents OOM.” It prevents OOM only when operators and sources honor bounded demand. A blocking JDBC `Flux` created by hammering a cursor without limits can still blow memory. Another misconception is using unbounded `onBackpressureBuffer()` and calling it production-ready. Name the bound. A third is confusing backpressure with circuit breaking — related resilience themes, different mechanisms.

We now have publishers, thread control, and demand control. The missing piece in the Spring stack is the web layer that speaks HTTP with these types end to end — routers, annotated controllers returning `Mono`/`Flux`, and a runtime that is not `DispatcherServlet`.

That layer is Spring WebFlux.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 80 (*Backpressure*).
