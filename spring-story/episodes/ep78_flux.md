# Episode 78 — Flux

| Field | Value |
|---|---|
| Episode | 78 |
| Title | Flux |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 78 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`Mono` was zero or one. `Flux<T>` is zero to many — a reactive sequence. Search results, event streams, Server-Sent Events, and chunked database reads live here. The mental model is still a publisher: assemble operators, subscribe to run, honor demand from downstream.

```java
public Flux<OrderView> streamOpenOrders(String tenantId) {
    return orderRepository.findOpenByTenant(tenantId)   // Flux<Order>
        .filter(Order::isOpen)
        .flatMap(order ->
            pricingClient.quote(order)                  // Mono<Money>
                .map(price -> OrderView.from(order, price))
        , 8) // concurrency hint: up to 8 in-flight quotes
        .limitRate(32)
        .doOnCancel(() -> log.info("client cancelled tenant {}", tenantId));
}

// WebFlux controller can return Flux for JSON array (buffered) or streaming media types
@GetMapping(value = "/orders/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
Flux<OrderView> stream(@RequestParam String tenantId) {
    return streamOpenOrders(tenantId);
}
```

`flatMap` on a `Flux` fans out async work per element. The concurrency parameter matters: unbounded fan-out can overwhelm a downstream API. `concatMap` preserves order and waits for each inner publisher to finish — slower, safer for ordered side effects. `map` stays synchronous per item. `buffer`, `window`, and `collectList` move between stream and aggregate shapes; `collectList()` turns a `Flux` into `Mono<List<T>>` when you truly need the whole collection in memory — know that cost.

Hot versus cold shows up more with `Flux`. A cold publisher — typical repository query — runs per subscriber. A hot publisher — a shared event bus — emits regardless of when you subscribe; late subscribers miss earlier signals. `share()` and `publish().refCount()` bridge those worlds carefully. For HTTP responses, cold pipelines tied to the request subscription are the usual story.

Cancellation is part of the API. When a browser closes an SSE connection, Reactor cancels the subscription. `doOnCancel` and operator cleanup release downstream work. Ignoring cancellation leaks subscriptions against remote systems. That is not optional polish in streaming endpoints.

A misconception is using `Flux` for a single optional entity because "reactive means Flux." Use `Mono` for 0..1. Another is `toStream()` or `blockLast()` in request code to get back to familiar loops — you just left the reactive model. A third is assuming `filter` plus `map` replaces SQL pushdown — filter early in the database when you can; reactive operators do not make wasted rows free.

We can now express sequences. The next practical question is where those operators run. CPU work, blocking legacy calls, and event-loop I/O should not all share one thread by accident.

That is the job of schedulers.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 78 (*Flux*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
