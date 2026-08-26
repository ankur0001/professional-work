# Episode 61 — Reference Types

| Field | Value |
|---|---|
| Episode | 61 |
| Title | Reference Types |
| Catalog handbook column | 61 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Ordinary Java references are strong. If a GC root can reach an object through strong references, that object stays. Episode Fifty-Seven's leaks were mostly strong-reference accidents: maps, listeners, ThreadLocals that never let go. But sometimes you want a different contract with memory. You want a cache that may give up entries under pressure. You want cleanup when an object becomes unreachable. You want to cooperate with GC instead of fighting it with forever-strong maps. That is why Java offers soft, weak, and phantom references alongside strong ones.

Start from a practical itch. You have a byte array that is expensive to rebuild and nice to keep, but not mandatory for correctness:

```java
SoftReference<byte[]> soft = new SoftReference<>(data);
byte[] again = soft.get(); // may be null after GC pressure
```

A soft reference lets the GC clear the referent under memory pressure. `get()` may return `null` later even though you never assigned null yourself. Soft refs are the traditional "keep until you need the memory" tool. They are not a promise that the value lives forever until you say otherwise. Assuming soft references never clear is how caches surprise you in production after a quiet staging environment with a huge heap. Staging lied because it never got hungry.

Weak references are cleared more eagerly once the object is no longer strongly reachable. If only weak references point at an object, it is eligible for clearing. That makes weak references useful for canonical mappings and certain observer-style structures where you do not want the map alone to keep the key alive. `WeakHashMap` uses weak keys: entries can disappear when keys are otherwise unused. The caveat is important — values can strongly reference keys and pin lifetimes in confusing ways, and `WeakHashMap` is not a complete cache product. It is a specialized map with weak-key semantics, not a substitute for a bounded cache with eviction policy, metrics, and explicit invalidation.

Phantom references are about cleanup signaling more than about retrieving the object. You do not use them to revive data. You use them with a reference queue to learn that an object has become phantom-reachable so post-mortem cleanup can run. In modern Java, prefer `Cleaner` over finalizers. Relying on `finalize` is a historical mistake: unpredictable timing, risks around resurrection, and painful interactions under load. Cleaner and reference queues give a clearer lifecycle for "run this cleanup when the object is gone." If you are still writing `finalize` in new code, you are carrying a museum piece into a production kitchen.

Notice the theme across all of these: cooperation with GC, not replacement for policy. Caches need bounds anyway — size limits, TTLs, explicit invalidation. A soft-reference cache without a size or TTL policy can still grow until pressure is extreme, and then clear in awkward bursts that stampede rebuilds. Using weak or soft caches as the only control knob is how teams rediscover Episode Fifty-Seven with fancier types and the same outage graph.

Reference queues close the loop. When the GC clears a reference, it can enqueue that reference so your code can remove bookkeeping entries, release native resources, or update metrics. Without the queue, you only discover clearance when `get()` returns null — fine for some caches, insufficient for native resource cleanup. Strong, soft, weak, phantom is not a trivia list. It is a ladder of how tightly you insist the object remain.

If an interview asks weak versus soft, answer with reachability policy: weak references are cleared when the object is only weakly reachable; soft references are retained longer and cleared under memory pressure according to the collector's policy. Then add: neither replaces an explicit eviction policy for a serious cache, and `finalize` is not your cleanup plan.

We learned that reachability is not only strong-or-gone; Java lets you express softer attachments and cleanup hooks. Next the conversation turns operational again: which JVM flags you set, how you change them without cargo-culting, and how evidence beats folklore. Episode Sixty-Two is JVM flags and tuning.

Put soft and weak references next to the unbounded cache from Episode Fifty-Seven. Someone "fixes" the static map by wrapping values in `SoftReference` and ships. Under mild load the cache grows. Under memory pressure it clears abruptly, then every request rebuilds, allocates hard, and pressure returns — a soft-reference stampede. Soft references changed the failure mode; they did not install a product-quality cache. Size bounds, TTL, and single-flight loading still belong in the design.

WeakHashMap surprises deserve a concrete picture too. You store metadata about an object using the object as a weak key, but the value holds a strong reference back to the key. The entry cannot clear as you expected. The map looks "weak" in the type name and strong in the graph. Reading the caveat before production is cheaper than learning it from a dump.

Put soft and weak references next to the unbounded cache from Episode Fifty-Seven. Someone "fixes" the static map by wrapping values in `SoftReference` and ships. Under mild load the cache grows. Under memory pressure it clears abruptly, then every request rebuilds, allocates hard, and pressure returns — a soft-reference stampede. Soft references changed the failure mode; they did not install a product-quality cache. Size bounds, TTL, and single-flight loading still belong in the design.

WeakHashMap surprises deserve a concrete picture too. You store metadata about an object using the object as a weak key, but the value holds a strong reference back to the key. The entry cannot clear as you expected. The map looks "weak" in the type name and strong in the graph. Reading the caveat before production is cheaper than learning it from a dump.

When cleanup must release a native resource — a file descriptor, an off-heap buffer you own — phantom reachability plus a cleaner or reference queue is the honest tool. Trying to recover the object and use it again is not the point. The point is a signal that the Java wrapper is gone and native cleanup may proceed.

When cleanup must release a native resource — a file descriptor, an off-heap buffer you own — phantom reachability plus a cleaner or reference queue is the honest tool. Trying to recover the object and use it again is not the point. The point is a signal that the Java wrapper is gone and native cleanup may proceed.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Reference Types (Episode 61).

Narration technique: strong refs & leaks → need softer contracts → soft example → weak / WeakHashMap caveats → phantom + Cleaner vs finalize → bounds still required → reference queues → interview woven → bridge to flags.

Teaching points preserved: strong/soft/weak/phantom; WeakHashMap caveats; Cleaner vs finalize; caches need bounds; reference queues.
