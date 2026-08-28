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

Here is a classic setup. One thread prepares a packet of data — fills several fields on a result object — then sets a `boolean ready` flag to true. Another thread loops until `ready` is true, then reads the data. Without a careful memory protocol, the reader can see `ready == true` and still observe stale fields. Or it can spin forever on a cached `false` that never updates in its view of memory. How do we publish "I am done writing" so another thread reliably sees both the flag and the data that came before it?

`volatile` is visibility tooling for that kind of publication story. It is not a magic atomic wand for every compound action.

```java
class Payload {
    int a;
    int b;
    volatile boolean ready;
}

// writer
payload.a = 1;
payload.b = 2;
payload.ready = true; // publish last

// reader
if (payload.ready) {
    use(payload.a, payload.b);
}
```

The writer fills the data fields first, then writes `ready = true`. The reader waits until it sees `ready == true`, then reads the data. The volatile write and later volatile read create a happens-before edge: actions before the write become visible to a thread that observed the read. Reverse the order — set ready first, then write the fields — and you reopen the window for a reader to see ready without seeing the data.

Happens-before is the language Java uses for these guarantees. You do not need to recite the entire Java Memory Model in one sitting. You need the habit of asking: which write is ordered before which read, and by what rule? Lock release happens-before a later acquire of the same lock. A volatile write happens-before a later read that sees that write. Starting a thread happens-before the first action in that thread. `join` completes after the dying thread's actions. These edges are why concurrency is more than "take turns on a CPU."

What volatile does not do is make compound actions atomic:

```java
volatile int count;
count++; // still a race under contention
```

`count++` is still read-modify-write. Two threads can both read 10, both write 11, and lose an increment. Volatility may make each individual read or write more visible; it does not merge three steps into one atomic update. For counters, prefer atomics — which we will treat properly soon — or locking when the invariant spans more than one variable.

Another publication pattern: a volatile reference to an immutable object. The writer builds a complete immutable snapshot, then assigns it to a volatile field in one write. Readers read the reference once and use the snapshot without further locking:

```java
volatile Config snapshot;

void publish(Config next) {
    snapshot = next; // next must not be mutated after this
}
```

This pattern fails if the object is mutable and still being changed after publication — because then you are back to sharing mutable state without a protocol.

Using volatile on every field "for safety" adds cost and still fails to protect multi-step invariants like "transfer money between two accounts." Overuse is not caution. It is a sign the protocol was never designed.

Does volatile make `++` atomic? No. Use atomics or locks for that. Use volatile when the need is visibility and ordered publication — not when the need is "update this counter safely under contention."

One more boundary: `volatile` is about one variable's reads and writes. It does not freeze an entire object graph. If you publish a volatile reference to a mutable object and then keep mutating that object from the writer thread, readers can still see torn state inside. Immutability after publication — or locking for ongoing mutation — remains part of the design.

Sometimes `synchronized` is almost enough, but you need try-lock, timed waits, multiple wait-sets, or fairness knobs the intrinsic lock does not offer. That is when explicit locks enter — not as a replacement for thinking, but as a richer toolbox for ownership you must manage yourself.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 38 (*volatile and Happens-Before*).

Narration technique: ready-flag publication → volatile as visibility tool → happens-before → ++ still racy → immutable snapshot → next natural problem (explicit locks).
