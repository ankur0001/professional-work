# Episode 38 — volatile and Happens-Before

| Field | Value |
|---|---|
| Episode | 38 |
| Title | volatile and Happens-Before |
| Catalog handbook column | 38 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Synchronization taught us that locks give both exclusion and visibility. That is a strong tool. It is also heavier than some problems need — and easy to misunderstand as the only visibility story Java has.

Here is a classic setup. One thread prepares a packet of data, then sets a `boolean ready` flag to true. Another thread loops until `ready` is true, then reads the data. Without a careful memory protocol, the reader can see `ready == true` and still observe stale fields from before the write — or spin forever on a cached `false`. The question is sharp: how do we publish "I am done writing" so another thread reliably sees both the flag and the data that came before it?

`volatile` is visibility tooling for that kind of publication story. It is not a magic atomic wand for every compound action.

```java
volatile boolean ready;
// writer publishes data then sets ready = true
```

In the safe pattern, the writer fills in the data fields first, then writes `ready = true`. The reader waits until it sees `ready == true`, then reads the data. The volatile write and later volatile read create a happens-before edge: actions before the write become visible to a thread that observed the read. That is the mechanism. The flag is not decorative. It is the publication signal.

Happens-before is the language Java uses for these guarantees. You do not need to recite the entire memory model. You need the habit of asking: which write is ordered before which read, and by what rule — lock release/acquire, volatile write/read, thread start/join, and so on? Synchronization gave you one family of edges. Volatile gives another. Starting a thread happens-before the code that runs in that thread. These edges are why concurrency is more than "take turns."

What volatile does not do is make compound actions atomic.

```java
volatile int count;
count++; // still a race under contention
```

`count++` is still read-modify-write. Two threads can interleave. Volatility may make each individual read or write more visible; it does not merge three steps into one atomic update. For counters and similar hotspots, prefer atomics — which we will treat properly soon — or locking when the invariant spans more than one variable.

Publication patterns use volatile carefully: a volatile reference to an immutable object, or a volatile flag that gates reading previously written state, can be elegant. Using volatile on every field "for safety" adds cost and still fails to protect multi-step invariants. Overuse is not caution. It is a sign the protocol was never designed.

Interviewers love the short form of today's lesson: does volatile make `++` atomic? No. Use atomics or locks for that. Use volatile when the need is visibility and ordered publication, not when the need is "update this counter safely under contention."

So reconnect the chain. We had a ready-flag race between preparing data and announcing it. Volatile plus happens-before explained safe publication. Compound actions reminded us visibility is not atomicity. Atomics and locks wait as the right tools for different shapes of problem.

Sometimes `synchronized` is almost enough, but you need try-lock, timed waits, multiple wait-sets, or fairness knobs the intrinsic lock does not offer. That is when explicit locks enter — not as a replacement for thinking, but as a richer toolbox.

Episode Thirty-Nine: explicit locks.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 38 (*volatile and Happens-Before*).

Narration technique: ready-flag publication situation → volatile as visibility tool → happens-before → ++ still racy → overuse → next natural problem (explicit locks).
