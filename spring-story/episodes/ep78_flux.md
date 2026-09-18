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

`Mono` was zero or one vessel. Harbor ops still need live maps: AIS position ticks for every ship on a quay, berth event feeds, Server-Sent Events to operator consoles, chunked file reads. That cardinality is `Flux<T>` — a reactive sequence of zero to many items. The mental model stays a publisher: assemble operators into a pipeline, subscribe (or return the publisher to WebFlux) to run, honor demand from downstream. Nothing in the chain runs until something subscribes.

```java
public Flux<PositionView> streamPositions(String quayId) {
    return aisFeed.positionsForQuay(quayId)              // Flux<AisFix>
        .filter(fix -> fix.isFresh(Duration.ofMinutes(2)))
        .flatMap(fix ->
            vesselDirectory.nameOf(fix.mmsi())          // Mono<String>
                .map(name -> PositionView.from(fix, name))
        , 8) // concurrency hint: up to 8 in-flight directory lookups
        .limitRate(32)
        .doOnCancel(() -> log.info("operator cancelled quay {}", quayId));
}

@GetMapping(value = "/positions/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
Flux<PositionView> stream(@RequestParam String quayId) {
    return streamPositions(quayId);
}
```

Walk an operator opening the quay map. WebFlux subscribes to the returned `Flux` when the SSE response starts. `aisFeed.positionsForQuay(quayId)` begins emitting `AisFix` items — each fix is one signal, not a buffered list handed over at once. `filter` drops stale fixes older than two minutes so the console does not paint ghosts. `flatMap` takes each remaining fix and starts an async `vesselDirectory.nameOf` lookup, merging results into `PositionView` as they complete. The concurrency argument `8` caps how many directory calls may be in flight; omit it and an AIS burst can open hundreds of lookups and melt the directory. `limitRate(32)` requests upstream in batches so a fast feed does not overwhelm the SSE write path. Each `PositionView` becomes an SSE event on the wire. When the operator closes the tab, the browser drops the connection, WebFlux cancels the subscription, `doOnCancel` logs, and upstream work should stop — if the AIS fan-in ignores cancellation, you leak subscriptions against the feed.

Operator vocabulary that differs from `Mono` mostly by cardinality. `map` stays synchronous per item. `flatMap` fans out async work per element and interleaves results; `concatMap` preserves order and waits for each inner publisher to finish — slower, safer for ordered side effects like writing berth audit rows. `flatMapSequential` keeps interleaving concurrency but emits in source order. `buffer`, `window`, and `collectList` move between stream and aggregate shapes; `collectList()` turns a `Flux` into `Mono<List<T>>` when you truly need the whole collection in memory — know that cost for AIS history, where a long quay window can blow the heap. `take`, `skip`, and `timeout` bound time and count for consoles that should not stream forever without a client heartbeat story.

Hot versus cold shows up harder with `Flux`. A cold publisher — a reactive repository query — runs its work per subscriber; two operators opening the same historical window hit the database twice. A hot publisher — a shared AIS multicast feed — emits regardless of when you subscribe; late operators miss earlier fixes and only see live ticks from join time forward. `share()` and `publish().refCount()` bridge those worlds carefully: first subscriber connects upstream, last cancel disconnects. For HTTP responses, cold pipelines tied to the request subscription are the usual story; live maps often sit on a hot feed with explicit join semantics so "why is my map empty for thirty seconds?" is explainable.

Failure mode symptoms on the ops floor. Unbounded `flatMap` without concurrency limits: directory latency climbs, event-loop threads busy, SSE clients time out while CPU looks "fine" on the wrong pool. Calling `blockLast()` or `toStream()` inside a WebFlux handler to "get a List": you left the reactive model and can stall Netty threads that other quay streams share. Using `Flux` for a single optional vessel because "reactive means Flux": wrong cardinality — WebFlux may serialize an array body where clients expected one object; use `Mono` for 0..1. Assuming `filter` plus `map` replaces pushdown at the AIS feed: reactive operators do not make wasted fixes free — filter at the source when the feed API allows. Ignoring cancellation: after tab close, logs still show directory lookups for that quayId for minutes — leaked work.

Trade-offs. `Flux` expresses push sequences and composes cancellation and backpressure hooks; it costs cognitive load and makes blocking libraries dangerous on shared event loops. Prefer `Mono` when the contract is one result. Prefer `Flux` when the product is a stream — live positions, event feeds, chunked download — and design hot/cold deliberately instead of discovering it in an incident.

Misconception unique to Flux: "Returning `Flux` means the work already started." Assembly is lazy; subscription starts it. Another: "`collectList()` is always fine for APIs." It is fine for small bounded sets; it is a memory incident for unbounded AIS history. A third: "hot and cold are academic." They decide whether a second subscriber replays or joins live — operator console bugs are often that distinction misread.

We can now express sequences. CPU work, blocking legacy PDF calls, and event-loop I/O still should not all share one thread by accident. Where those operators run is the next control surface.

That is the job of schedulers.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 78 (*Flux*).
