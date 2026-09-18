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

An operator clicks "export gate pass PDF" on a reactive harbor console. The chain that streamed AIS positions is non-blocking. The PDF library is not — it hammers CPU and filesystem APIs that block. Drop that callable on a Netty event-loop thread and unrelated position streams stutter: SSE ticks pause, quay maps freeze, and on-call sees "WebFlux is slow" when the real culprit is one blocking render on the wrong thread. `Mono` and `Flux` describe what happens. Schedulers describe where it happens.

In Reactor, you shift execution with `publishOn` and `subscribeOn`, backed by `Schedulers` factories — not with ad-hoc `new Thread` in handlers.

Know the common pools by role. `Schedulers.parallel()` is for non-blocking CPU-ish work across a fixed pool sized around core count — pure transforms, not blocking I/O. `Schedulers.single()` is one dedicated thread for tasks that must be serialized (a single-writer sequence). `Schedulers.boundedElastic()` is for blocking or blocking-ish legacy calls — it grows elastically up to a bound so you do not invent unbounded thread creation under an AIS storm. `Schedulers.immediate()` runs on the caller. Netty event loops in WebFlux are precious: blocking on them stalls unrelated AIS subscribers that share the loop.

```java
public Mono<byte[]> gatePassPdf(CargoId cargoId) {
    return cargoRepository.findById(cargoId)                    // reactive
        .flatMap(cargo ->
            Mono.fromCallable(() -> legacyPdf.render(cargo))    // blocking PDF
                .subscribeOn(Schedulers.boundedElastic())       // off event loop
        )
        .flatMap(bytes ->
            stampClient.watermark(bytes)                        // reactive HTTP
                .publishOn(Schedulers.parallel())               // CPU transform if needed
                .map(this::toDownload)
        );
}

// subscribeOn: influences where the subscription upstream begins (source side)
// publishOn: switches threads for downstream operators after it appears in the chain
```

Walk the export click. WebFlux subscribes on an event-loop thread. `cargoRepository.findById` should be a non-blocking reactive driver — it stays on the loop. When a `Cargo` arrives, `flatMap` builds `Mono.fromCallable(legacyPdf.render)`. Without `subscribeOn(boundedElastic)`, that callable would run on the same thread that subscribed the inner Mono — often the event loop — and hold it for the whole PDF render. With `subscribeOn(Schedulers.boundedElastic())`, subscription of that callable is scheduled onto the elastic pool; the event loop is free to service AIS SSE while PDF threads grind. After bytes return, `stampClient.watermark` is reactive HTTP again; `publishOn(Schedulers.parallel())` hops only the downstream `map(this::toDownload)` CPU work onto the parallel pool if that transform is heavy. Stacking hops without need adds latency and confusion. Prefer keeping pure reactive I/O on the event loop and isolating blocking adapters behind `boundedElastic`.

Say the difference until it sticks under pressure. `subscribeOn` affects the thread where the source is subscribed — useful when the source itself blocks, like the PDF callable or a JDBC wrapper wrongly placed in a Mono. Multiple `subscribeOn` calls — the closest to the source usually wins for that source. `publishOn` inserts a thread hop for operators below it in the assembly order; everything above keeps the previous thread. Putting `publishOn` before a blocking call does not protect the event loop if subscription of the blocking work still happens on the loop — you needed `subscribeOn` on the blocking wrapper.

Failure mode symptoms. PDF export without a scheduler: p99 on `/positions/stream` climbs whenever someone exports a gate pass; thread dumps show event-loop threads inside `legacyPdf.render` or `FileOutputStream`. Using `Schedulers.parallel()` for the PDF callable: parallel pool threads block, CPU work queues behind renders, and you still did not isolate blocking the way `boundedElastic` intends. Wrapping every operator in `publishOn(parallel())` "for performance": thread hops dominate; latency rises; flame graphs show park/unpark noise. Older `Schedulers.elastic()` habits under AIS load: thread count explodes until the host groans — prefer `boundedElastic` so overload becomes visible as queueing and rejection behavior instead of silent thread creation. Calling `block()` on the event loop "just for this admin export": one export freezes neighbors.

In WebFlux, you often never call `subscribeOn` because Netty already drives non-blocking I/O. Reach for schedulers when you integrate a blocking library, parallelize CPU work, or time deferred tasks with `Mono.delay`. `Schedulers.fromExecutor` wraps a pool you already size — use it when the platform owns that pool (named PDF pool with metrics) and you want Reactor to hop onto it.

Trade-offs. Schedulers make mixed blocking/reactive systems operable; they do not make blocking free. Cap elastic size to what the host can bear. Measure before adding hops. Keep AIS streaming on the event loop; put gate-pass PDF on bounded elastic; put heavy pure CPU on parallel when profiling says the transform matters.

Misconception unique to schedulers: "`subscribeOn` and `publishOn` are interchangeable." They are not — one biases source subscription, the other switches downstream execution at a point in the chain. Another: "boundedElastic is the default for everything." Using it for non-blocking Netty calls throws away the event-loop model. A third: "Reactor always picks the right thread." It picks what you configured; wrong configuration is a production incident.

Pipelines now know what to emit and which threads may run stages. When a fast AIS publisher meets a slow operator UI, you still need a rule for how much data may be in flight.

That rule is backpressure.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 79 (*Schedulers*).
