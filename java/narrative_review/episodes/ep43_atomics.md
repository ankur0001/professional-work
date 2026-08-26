# Episode 43 — Atomics

| Field | Value |
|---|---|
| Episode | 43 |
| Title | Atomics |
| Catalog handbook column | 43 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Concurrent maps helped when many keys were the shared story. Counters and flags are a narrower hotspot: one variable, updated constantly, where a full lock feels heavy and `volatile++` is still a race. We already learned that visibility is not atomicity. So the question becomes: how do we update one value safely without necessarily taking a monitor every time?

Atomics give lock-free updates for focused hotspots. Under the hood they lean on compare-and-set — CAS — loops: read the current value, compute the next, and install it only if the current value is still what you expect. If another thread won the race, you retry.

```java
AtomicInteger n = new AtomicInteger();
int after = n.incrementAndGet();
```

Walk it. `incrementAndGet` atomically adds one and returns the new value. Two threads calling it will not lose increments the way they can with `count++` on a plain or even volatile `int`. `AtomicLong` and `AtomicReference` play the same role for other shapes. Good uses are counters, sequence numbers, and simple state flags where the entire invariant fits in one value.

CAS in interview language: compare-and-set updates only if the current value matches expectation. That single sentence explains both the power and the limitation. If your invariant spans two fields — balance and version, or head and size — one atomic variable may not be enough. You might need an atomic reference to an immutable pair, or a lock, or a specialized concurrent structure. Using atomics for complex multi-field invariants is how people invent subtle races while feeling modern.

Contention still costs. Lock-free does not mean free. Under extreme contention, many threads can spin retrying CAS on the same hot counter. Sometimes a lock with less wasted spinning wins. Sometimes you shard counters. Sometimes you accept approximate counts. Atomics are a tool for a hotspot, not a personality trait for every field in the class.

```java
AtomicReference<Config> ref = new AtomicReference<>(Config.defaults());

boolean ok = ref.compareAndSet(oldConfig, newConfig);
```

Here the atomic unit is a reference. Publishing a new immutable `Config` with CAS lets readers see either the old or the new complete snapshot. That pattern pairs well with the volatile publication ideas from earlier — now with an atomic swap instead of only a volatile write.

Advanced cases reach for `VarHandle` when you need more control over memory ordering and shaped updates. You do not need to master VarHandles today. You need curiosity: atomics are the friendly face of a deeper memory and CPU toolkit the JDK exposes as you grow.

What if we replace every `synchronized` counter with an atomic and call it a day?

For a lone counter, good. For "transfer from account A to account B without observing intermediate states," not enough. Atomics shrink critical sections when the section is truly one variable. They do not delete the need for protocols around compound business operations.

Busy CAS without backoff under extreme contention can burn CPU while making little progress. That is another reason measurement matters. If a profiler shows a hot atomic under fifty threads, ask whether the design should shard, batch, or lock.

Slow down on CAS so it feels mechanical, not magical. Thread A reads 41. Thread B reads 41. Both add one and try to write 42. Only one CAS succeeds; the loser rereads — now 42 — and writes 43. Progress happens without a mutual-exclusion lock, but progress can still thrash when many threads fight over one address. That is why sharding hot counters — one atomic per stripe, summed rarely — shows up in high-throughput systems.

`AtomicInteger` methods like `getAndUpdate` and `accumulateAndGet` let you express richer single-variable transitions without writing your own CAS loop incorrectly. Prefer those helpers when they fit. Hand-rolled loops are easy to get almost right and miss a retry path.

What if the "atomic" value is a reference to a mutable object you keep editing? Then only the reference swap was atomic. The interior mutations need their own story — immutability after publish, or locking, or another concurrent structure. Atomics are precise tools. Precision includes knowing what, exactly, is atomic.

Pair atomics with the volatile lesson explicitly. Volatile publish can announce a completed immutable snapshot. Atomic update can advance a counter all threads share. Different problems, related memory stories. If you catch yourself using an atomic boolean only as a flag with no CAS retry needs, volatile might have been enough — or a lock if the flag gates a larger invariant. Name the operation: publish, or update under contention, or protect a compound invariant. The name guides the tool.

Picture a hit counter on a public API. `AtomicLong` increments on each call. A separate reporter thread samples `get` periodically. No lock ties them together; the atomic carries the updates. When product asks for "top three endpoints," you suddenly need a concurrent map of atomics or a merge strategy — and you feel the boundary where one atomic stops being the model.

Atomics shine when the invariant is one word wide. The moment product language needs two fields to stay coherent, widen the tool — immutable pair, lock, or concurrent structure — instead of forcing two CAS operations to pretend they are one transaction.

So reconnect the chain. Volatile taught visibility. Counters needed atomicity. Atomics provided CAS-based updates for single-value hotspots. Multi-field invariants and heavy contention showed the edges. VarHandles wait as a later power tool.

Not every coordination problem is "update a value." Sometimes threads must wait for a phase to finish, wait for peers to arrive, or limit how many may enter a section. Those phase and permit problems are the world of latches, barriers, and semaphores.

Episode Forty-Four: synchronizers.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 43 (*Atomics*).

Narration technique: hot-counter situation → atomics/CAS → increment walkthrough → multi-field limit → contention → AtomicReference publish → what-if overuse → next natural problem (synchronizers).
