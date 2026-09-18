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

Servlet security assumed a familiar shape: a request arrives, a thread runs filters and controllers, blocking I/O waits on the database or HTTP client, then the thread returns to the pool. That model scales until waiting dominates — thousands of open connections each holding a thread hostage while something remote thinks.

Reactive programming flips the default. Instead of returning a finished value, you return a **publisher** that will emit values later. The thread that accepts the connection does not sit blocked on JDBC or a remote call; it schedules work and moves on. Subscribers pull or request data; operators transform streams; schedulers decide which threads run which stages. The goal is higher concurrency with fewer threads for I/O-bound workloads — not magic speed for CPU-bound math.

Project Reactor is the library Spring WebFlux builds on. The Reactive Streams specification sits underneath: `Publisher`, `Subscriber`, `Subscription`, and `Processor`, with **backpressure** as a first-class idea — subscribers request only what they can handle. Reactor’s `Mono` and `Flux` are publishers with a rich operator vocabulary. You compose pipelines declaratively; nothing runs until something subscribes.

```java
// Not servlet DI — a reactive pipeline
Mono<User> user = userClient.findById(id);           // Publisher of 0..1
Flux<Order> orders = orderClient.findByUser(id);     // Publisher of 0..n

Mono<UserOrders> page = user
    .zipWith(orders.collectList(), UserOrders::new)
    .timeout(Duration.ofSeconds(2))
    .doOnError(e -> log.warn("assembly failed: {}", e.toString()));

// Nothing hits the network until:
page.subscribe(
    result -> response.write(result),
    error -> response.error(error)
);
```

Read that as assembly, not as imperative steps that already executed. `zipWith` and `timeout` describe a graph. Subscription triggers demand. That laziness is why returning a `Mono` from a WebFlux controller works — the framework subscribes and wires the response when data arrives.

Reactive is not "async annotations on servlet code." A blocking `Thread.sleep` or JDBC call inside a reactive operator still blocks a thread — often an event-loop thread you cannot afford to stall. The discipline is end-to-end non-blocking I/O (R2DBC, reactive HTTP clients) or explicit offloading of blocking work onto bounded elastic schedulers. Mixing one blocking repository into a WebFlux app is a classic production footgun.

When do you reach for this model? Many concurrent slow I/O dependencies, streaming responses, or gateways that multiplex downstream calls. When do you stay on Spring MVC? Familiar blocking drivers, team expertise, and workloads that never needed tens of thousands of concurrent connections. Boot can run either stack; picking both without clear boundaries usually creates confusion.

A misconception is equating reactive with faster CPU-bound algorithms. Another is treating `subscribe()` inside business code as normal — in WebFlux you typically return the publisher and let the framework subscribe. A third is ignoring error and cancellation paths: when a client disconnects, subscriptions cancel; your pipeline should not ignore that.

Today we named the shift: publishers instead of eager values, subscription as the start gun, backpressure as part of the contract. The smallest publisher shape — zero or one element — is where most service calls live.

That shape is `Mono`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 76 (*Reactive Programming*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
