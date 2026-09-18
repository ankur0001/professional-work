# Episode 77 — Mono

| Field | Value |
|---|---|
| Episode | 77 |
| Title | Mono |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 77 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Reactive programming introduced publishers. Most harbor lookups are not streams of thousands of rows — they are “give me this vessel by MMSI,” “load this berth assignment,” “call this registry once.” Reactor’s type for that is `Mono<T>`: a publisher that completes with zero or one item, or with an error.

Think of `Mono` as a lazy asynchronous `Optional` with operators — but do not implement it by wrapping blocking calls in `Mono.just`. `Mono.just(repo.findByMmsi(mmsi))` still blocks the caller thread before the Mono even exists. Prefer sources that are non-blocking, or defer blocking work explicitly.

```java
public Mono<Vessel> findVessel(String mmsi) {
    return vesselRepository.findByMmsi(mmsi)           // reactive repo → Mono<Vessel>
        .switchIfEmpty(Mono.error(new VesselNotFoundException(mmsi)))
        .flatMap(vessel ->
            registryClient.enrich(vessel.imo())        // Mono<RegistryFacts>
                .map(facts -> vessel.withRegistry(facts))
        )
        .timeout(Duration.ofSeconds(3))
        .doOnNext(v -> log.info("loaded vessel {}", v.mmsi()));
}

// Cold: nothing runs until subscribe / WebFlux returns this Mono to the framework
// Empty → VesselNotFoundException
// Downstream registry error → error signal to subscriber
// Success → one Vessel emitted, then onComplete
```

Operator vocabulary you should say out loud. `map` transforms the item synchronously. `flatMap` chains another `Mono` or `Flux` when each item needs an async call — the reactive replacement for nested callbacks. `switchIfEmpty` handles the zero-item case. `timeout`, `retry`, `onErrorResume` shape time and failure. `zipWhen` / `zipWith` combine parallel lookups. `then` ignores the payload and waits for completion — useful for deletes.

Cardinality is the contract. If you accidentally emit two items into a `Mono`, Reactor signals an error. If your repository can return many positions, you wanted `Flux`. Choosing `Mono` documents intent: WebFlux treats `Mono` as a single JSON object body, not an array.

Empty is not null. A completed empty `Mono` means “no value.” Mapping without guarding empty keeps emptiness. Turning empty into an error with `switchIfEmpty(Mono.error(...))` is how you express 404-style vessel misses at the reactive layer. Returning `Mono.justOrEmpty(optional)` bridges imperative code carefully; returning `null` from a reactive adapter is not the same and usually breaks callers.

A misconception is calling `.block()` on a `Mono` inside WebFlux request handling to “make it simple.” That reintroduces thread blocking on the event loop. Blocking belongs at edges you control — tests sometimes, or a narrow adapter — not in the hot path. Another misconception is nesting `subscribe` inside `map` instead of `flatMap` — that breaks backpressure and error propagation. A third is treating `Mono` as a servlet-style injected dependency rather than a publisher you compose and return.

Today we treated `Mono` as the 0..1 reactive publisher: compose with `flatMap`, handle empty, signal errors, return it to the web layer instead of blocking. Live AIS maps need 0..n.

That publisher is `Flux`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 77 (*Mono*).
