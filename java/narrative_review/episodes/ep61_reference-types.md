# Episode 61 — Reference Types

| Field | Value |
|---|---|
| Episode | 61 |
| Title | Reference Types |
| Catalog handbook column | 61 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Ordinary Java references are strong. If a GC root can reach an object through strong references, that object stays. Episode Fifty-Seven's leaks were mostly strong-reference accidents: maps, listeners, ThreadLocals that never let go. Sometimes you want a different contract. You want a cache that may give up entries under pressure. You want cleanup when an object becomes unreachable. You want to cooperate with GC instead of fighting it with forever-strong maps. That is why Java offers soft, weak, and phantom references alongside strong ones.

Start from a practical itch — a byte array expensive to rebuild and nice to keep, but not mandatory for correctness:

```java
SoftReference<byte[]> soft = new SoftReference<>(data);
byte[] again = soft.get(); // may be null after GC pressure
```

A soft reference lets the GC clear the referent under memory pressure. `get()` may return `null` later even though you never assigned null yourself. Soft refs are the traditional "keep until you need the memory" tool — not a promise the value lives forever. Assuming they never clear is how caches surprise you in production after a quiet staging environment with a huge heap.

Put soft references next to the unbounded cache from Episode Fifty-Seven. Someone "fixes" the static map by wrapping values in `SoftReference` and ships. Under mild load the cache grows. Under pressure it clears abruptly, then every request rebuilds, allocates hard, and pressure returns — a soft-reference stampede. Soft references changed the failure mode; they did not install a product-quality cache. Size bounds, TTL, and single-flight loading still belong in the design.

Weak references are cleared more eagerly once the object is no longer strongly reachable. That makes them useful for canonical mappings and certain observer-style structures where you do not want the map alone to keep the key alive. `WeakHashMap` uses weak keys: entries can disappear when keys are otherwise unused. The caveat matters — values can strongly reference keys and pin lifetimes in confusing ways. You store metadata with the object as a weak key, but the value holds a strong reference back to the key: the entry cannot clear as expected. The map looks "weak" in the type name and strong in the graph. `WeakHashMap` is a specialized map with weak-key semantics, not a substitute for a bounded cache with eviction, metrics, and explicit invalidation.

Phantom references are about cleanup signaling more than retrieving the object. You do not use them to revive data. You use them with a reference queue to learn that an object has become phantom-reachable so post-mortem cleanup can run — a file descriptor, an off-heap buffer you own. In modern Java, prefer `Cleaner` over finalizers. Relying on `finalize` is a historical mistake: unpredictable timing, resurrection risks, and painful interactions under load. Cleaner and reference queues give a clearer lifecycle for "run this cleanup when the object is gone."

Notice the theme: cooperation with GC, not replacement for policy. Caches need bounds anyway. A soft-reference cache without size or TTL can still grow until pressure is extreme, then clear in awkward bursts. Using weak or soft caches as the only control knob is how teams rediscover Episode Fifty-Seven with fancier types and the same outage graph.

Reference queues close the loop. When the GC clears a reference, it can enqueue that reference so your code can remove bookkeeping entries, release native resources, or update metrics. Without the queue, you only discover clearance when `get()` returns null — fine for some caches, insufficient for native resource cleanup. Strong, soft, weak, phantom is not a trivia list. It is a ladder of how tightly you insist the object remain.

If an interview asks weak versus soft, answer with reachability policy: weak references clear when the object is only weakly reachable; soft references are retained longer and cleared under memory pressure according to the collector's policy. Neither replaces an explicit eviction policy for a serious cache, and `finalize` is not your cleanup plan.

We learned that reachability is not only strong-or-gone. Next the conversation turns operational again: which JVM flags you set, how you change them without cargo-culting, and how evidence beats folklore. Episode Sixty-Two is JVM flags and tuning.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Reference Types (Episode 61).

Narration technique: strong refs & leaks → softer contracts → soft example + stampede → weak / WeakHashMap caveats → phantom + Cleaner → bounds still required → reference queues → interview woven → bridge to flags.

Teaching points preserved: strong/soft/weak/phantom; WeakHashMap caveats; Cleaner vs finalize; caches need bounds; reference queues.
