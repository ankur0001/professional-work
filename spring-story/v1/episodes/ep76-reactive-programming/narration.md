# Episode 76 — Reactive Programming

| Field | Value |
|---|---|
| Episode | 76 |
| Title | Reactive Programming |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 76 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

AIS feeds do not wait politely for your thread pool. Hundreds of vessels report positions; operators open live maps; each connection holds a servlet thread while blocking I/O waits on the next read. Under fan-in, the thread-per-request model collapses — not because the CPU is busy computing, but because every open socket owns a worker sitting idle on the network.

Reactive programming flips the default. Instead of returning a finished value, you return a **publisher** that will emit values later. The thread that accepts the connection does not sit blocked on JDBC or a remote call; it schedules work and moves on. Subscribers request data; operators transform streams; schedulers decide which threads run which stages. The goal is higher concurrency with fewer threads for I/O-bound workloads — not magic speed for CPU-bound math.

Project Reactor is the library Spring WebFlux builds on. The Reactive Streams specification sits underneath: `Publisher`, `Subscriber`, `Subscription`, and `Processor`, with **backpressure** as a first-class idea — subscribers request only what they can handle. Reactor’s `Mono` and `Flux` are publishers with a rich operator vocabulary. You compose pipelines declaratively; nothing runs until something subscribes.

```java
// Reactive publishers for AIS — not servlet DI wiring
Mono<Vessel> vessel = vesselClient.findByMmsi(mmsi);     // 0..1
Flux<Position> positions = aisFeed.streamFor(mmsi);      // 0..n

Mono<VesselTrack> track = vessel
    .zipWith(positions.take(50).collectList(), VesselTrack::new)
    .timeout(Duration.ofSeconds(2))
    .doOnError(e -> log.warn("AIS assembly failed: {}", e.toString()));

// Nothing hits the network until subscribe:
track.subscribe(
    result -> response.write(result),
    error -> response.error(error)
);
```

Read that as assembly, not as imperative steps that already executed. `zipWith` and `timeout` describe a graph. Subscription triggers demand. That laziness is why returning a `Mono` from a WebFlux controller works — the framework subscribes and wires the response when data arrives.

Reactive is not “async annotations on servlet code.” A blocking `Thread.sleep` or JDBC call inside a reactive operator still blocks a thread — often an event-loop thread you cannot afford to stall under AIS load. The discipline is end-to-end non-blocking I/O (R2DBC, reactive HTTP clients) or explicit offloading of blocking work onto bounded elastic schedulers. Mixing one blocking repository into a WebFlux app is a classic production footgun.

When do you reach for this model? Many concurrent slow I/O dependencies, streaming AIS positions, or gateways that multiplex downstream calls. When do you stay on Spring MVC? Familiar blocking drivers, team expertise, and workloads that never needed tens of thousands of concurrent connections. Boot can run either stack; picking both without clear boundaries usually creates confusion.

A misconception is equating reactive with faster CPU-bound algorithms. Another is treating `subscribe()` inside business code as normal — in WebFlux you typically return the publisher and let the framework subscribe. A third is ignoring cancellation: when an operator closes a map, subscriptions cancel; your pipeline should not ignore that.

Today we named the shift: publishers instead of eager values, subscription as the start gun, backpressure as part of the contract. The smallest publisher shape — zero or one element — is where most vessel lookups live.

That shape is `Mono`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 76 (*Reactive Programming*).
