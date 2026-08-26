# Episode 42 — Concurrent Collections

| Field | Value |
|---|---|
| Episode | 42 |
| Title | Concurrent Collections |
| Catalog handbook column | 42 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Futures gave us results from pools. Those results often land in shared structures — caches, metrics maps, work queues — touched by many threads. Synchronizing every access to an ordinary `HashMap` works until contention makes the whole map a single-file line. So a natural question appears: can the collection itself offer safe concurrent access without forcing us to lock the entire world?

Concurrent collections answer that need. They make shared structure access safer. They do not make every multi-step business operation automatically correct. That distinction is the whole episode.

Start with the map you will see most:

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.merge("a", 1, Integer::sum);
```

Walk it. `merge` atomically associates key `"a"` with `1` if absent, or applies `Integer::sum` if present. You did not write a check-then-act sequence that another thread could interleave. Single operations on `ConcurrentHashMap` are designed for concurrent use. The trap is pretending that two separate calls are one atomic story:

```java
// fragile under concurrency
if (!map.containsKey("a")) {
    map.put("a", 1);
}
```

Between `containsKey` and `put`, another thread can insert. Use `putIfAbsent`, `compute`, `merge`, and friends when the logic is compound. Interview form: is `ConcurrentHashMap` enough for multi-step logic? Single ops are safe; multi-step needs atomic APIs or additional coordination.

Copy-on-write structures trade a different cost. `CopyOnWriteArrayList` copies the underlying array on each mutation, then publishes the new array. Readers can iterate without locking and see a snapshot. That shines when reads dominate and writes are rare — listener lists are the classic example. It hurts when writes are frequent, because every write pays for a full copy. Using copy-on-write for a write-heavy workload is a performance foot-gun dressed as thread safety.

Blocking queues deserve a mention here even though they get their own deep episode soon. They are concurrent collections specialized for handoffs: producers put work in, consumers take work out, and blocking coordinates the tempo. Weakly consistent iterators on many concurrent collections mean an iterator may reflect some updates and not others — it will not throw `ConcurrentModificationException` the way a fail-fast `ArrayList` iterator might, but it also will not freeze a perfect point-in-time view unless the collection promises one.

What if we wrap every `ConcurrentHashMap` call in `synchronized (map)` "to be extra safe"?

Usually you add contention without adding meaning. The map already coordinates its single operations. External synchronization around it can be necessary for multi-map invariants — but then you are designing a higher-level lock protocol, not improving `ConcurrentHashMap`. Unnecessary outer locks are how people accidentally serialize a structure built to scale.

A small caching story ties the points together. Threads look up a computed value by key. If absent, they compute and insert. `computeIfAbsent` keeps that check-and-create atomic for the key. If computation is expensive and must not run twice, that atomic API is not a micro-optimization — it is correctness under load. If the value itself is mutable and shared, you still need a protocol for mutating it. The map's concurrency does not bless the object's interior.

Think about iteration while another thread mutates. On an `ArrayList`, a fail-fast iterator may throw if the structure changes. On many concurrent collections, iterators are weakly consistent: they reflect some updates made after the iterator was created and skip others, without throwing. That is not a bug — it is a throughput trade. If you need a true snapshot, copy under a protocol or use a structure that promises one. If you only need "visit what we can see without freezing writers," weak consistency is often exactly right.

Blocking queues sit in the same family tree: they are concurrent collections specialized for handoff and waiting. You will deepen them next. The important bridge is conceptual — shared structure access has many shapes, and "thread-safe collection" never meant "my multi-step business method is atomic."

A metrics counter map is a good weekly exercise. Increment with `merge`. Read with ordinary gets. Resist synchronizing around the whole map "just in case" unless you are composing a multi-key invariant the map cannot express. Let the collection do the job it was built for.

CopyOnWrite earns one concrete picture. A list of listeners is read on every event and updated when someone subscribes. Updates are rare; reads are constant. Copy-on-write makes reads cheap and lock-free at the cost of a copy on subscribe. Invert that workload — writes constantly, reads rare — and the copies dominate. The structure did not fail. The workload did not match the trade.
Concurrent collections are a menu of trades. Read the trade before you copy a type from a blog post into a hot path.

Picture a feature-flag map read on every request and updated by a rare admin call. `ConcurrentHashMap` fits. An admin update that changes three related keys under one logical "release" may still need a higher-level protocol — a single versioned immutable snapshot published atomically, for example. The collection keeps single-key operations honest; your product invariants may still need a wider story.

So reconnect the chain. Shared maps under pools created pressure for concurrent collections. `ConcurrentHashMap` atomic methods replaced fragile check-then-act. Copy-on-write fit rare writes. Iterators and blocking queues showed other shapes of concurrent structure. Outer locks and write-heavy COW showed misuse. Compound actions remain your responsibility even when the collection is "concurrent."

Sometimes the shared state is not a map of many keys — it is a single counter or flag updated constantly. Locking may be too heavy; check-then-act on a plain `int` is too racy. That hotspot shape is where atomics earn their keep.

Episode Forty-Three: atomics.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 42 (*Concurrent Collections*).

Narration technique: shared-map situation → CHM merge → check-then-act trap → COW tradeoff → iterators/queues foreshadow → outer lock mistake → cache story → next natural problem (atomics).
