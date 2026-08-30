# Episode 49 — Deadlocks

| Field | Value |
|---|---|
| Episode | 49 |
| Title | Deadlocks |
| Catalog handbook column | 49 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

ThreadLocal taught us ambient state can leak across borrowed threads. Locks create a different freeze: nest them without a global order and the process can wait forever while every thread looks busy. The CPU is idle. The health check fails. Nobody is making progress. That shape has a name.

Deadlocks are circular waits. Prevent them with ordering, smaller critical sections, and timeouts. Detect them with thread dumps when prevention fails.

The classic story is two locks, two threads, opposite orders:

```java
// T1: lock A then B
// T2: lock B then A
```

Thread One holds A and waits for B. Thread Two holds B and waits for A. Each will wait forever. No exception is thrown. The bug is a schedule that eventually happens in production and rarely in a single-threaded test.

The four classic conditions for deadlock are worth knowing as a checklist: mutual exclusion, hold-and-wait, no preemption, and circular wait. Prevention usually attacks circular wait and hold-and-wait — by imposing a global lock order, by avoiding nested locks, or by using tryLock with timeouts so threads can back off instead of waiting forever:

```java
if (lockA.tryLock(100, TimeUnit.MILLISECONDS)) {
    try {
        if (lockB.tryLock(100, TimeUnit.MILLISECONDS)) {
            try {
                work();
            } finally {
                lockB.unlock();
            }
        }
    } finally {
        lockA.unlock();
    }
}
```

Timed tryLock does not magically make nested locking free of design. It gives you an exit when the order goes wrong or contention spikes. Global lock order — always acquire account locks by ascending account id, for example — removes the cycle before it starts. Shrink nested locking: if you can redesign so one lock protects the invariant, do that. Holding locks while calling alien code is how you nest locks you did not even see — the alien code acquires something else, and your order story dies offstage.

Detection via thread dumps is the operational skill. When a system hangs, capture threads — `jcmd Thread.print`, jstack, or your platform's dump. Look for threads blocked on monitors or owning locks another thread wants. Learning to read that dump is as important as knowing the theory.

What if tests never deadlock and production does? Because deadlock depends on timing. Two opposite orders can run for days until a rare interleaving appears. Testing helps when you stress nested paths; it cannot prove absence. Design prevention beats hopeful testing.

Shrink the story to design rules you can enforce in review. One: document lock order for any pair that can nest. Two: never call unknown code while holding a lock. Three: prefer tryLock with timeout when nesting is unavoidable and order cannot be globally guaranteed. Four: keep critical sections small so you need fewer nests.

When a dump shows a deadlock, fix the order or remove a lock — do not "retry the request" as the only strategy unless you also understand you are masking a design bug that will return under load.

Picture transfer locks on two accounts acquired in random order under load. One night the interleaving appears; support sees a hung JVM; the dump shows the cycle. The fix is sorted lock order by account id — a one-line policy that removes the cycle. Most deadlock stories end with a boring ordering rule that should have been written first.

Prefer ordering and confinement over cleverness. Deadlocks are not a badge of advanced concurrency — they are usually a missing policy. Write the policy early; let the dump be a last resort.

After platform-thread concurrency, a modern twist changes the economics of blocking: virtual threads make the thread-per-request style scalable again for blocking I/O — with new pitfalls of their own.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 49 (*Deadlocks*).

Narration technique: hang situation → circular wait → four conditions → tryLock/order → alien code → dumps → next natural problem (virtual threads).
