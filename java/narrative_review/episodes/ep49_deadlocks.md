# Episode 49 — Deadlocks

| Field | Value |
|---|---|
| Episode | 49 |
| Title | Deadlocks |
| Catalog handbook column | 49 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We have locked, tried locks, queued work, and coordinated phases. Nest enough of those tools without a policy and you can freeze a process while every thread looks busy waiting. The CPU is idle. The health check fails. Nobody is making progress. That shape has a name.

Deadlocks are circular waits. Prevent them with ordering, smaller critical sections, and timeouts. Detect them with thread dumps when prevention fails.

The classic story is two locks, two threads, opposite orders:

```java
// T1: lock A then B
// T2: lock B then A
// That ordering risk is the story
```

Thread One holds A and waits for B. Thread Two holds B and waits for A. Each will wait forever. No exception is thrown. The bug is a schedule that eventually happens in production and rarely in a single-threaded test.

The four classic conditions for deadlock are worth knowing as a checklist: mutual exclusion, hold-and-wait, no preemption, and circular wait. Prevention usually attacks circular wait and hold-and-wait — by imposing a global lock order, by avoiding nested locks, or by using tryLock with timeouts so threads can back off instead of waiting forever.

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

Detection via thread dumps is the operational skill. When a system hangs, capture threads — `jcmd Thread.print`, jstack, or your platform's dump. Look for threads blocked on monitors or owning locks another thread wants. Deadlock detection messages sometimes appear directly. Learning to read that dump is as important as knowing the theory; we will deepen diagnostic tooling later, but the hunger should start now.

What if tests never deadlock and production does?

Because deadlock depends on timing. Two opposite orders can run for days until a rare interleaving appears. Testing helps when you stress nested paths; it cannot prove absence. Design prevention beats hopeful testing.

Inconsistent lock ordering across modules is how cycles sneak in through "clean" abstractions. Document order for shared locks. Prefer confinement and concurrent collections when they remove the need to lock at all.

Shrink the story to design rules you can enforce in review. One: document lock order for any pair that can nest. Two: never call unknown code while holding a lock. Three: prefer tryLock with timeout when nesting is unavoidable and order cannot be globally guaranteed. Four: keep critical sections small so you need fewer nests. These rules do not eliminate deadlock, but they remove the common factories that produce it.

Database deadlocks and distributed deadlocks follow similar circular-wait intuition with different detectors. Today stays in-process. The habit of thinking in cycles transfers.

When a dump shows a deadlock, fix the order or remove a lock — do not "retry the request" as the only strategy unless you also understand you are masking a design bug that will return under load.

Resource ordering extends beyond mutexes: lock files, connection checkouts, and remote leases can deadlock across processes. The in-process story trains your eye. When you later design distributed systems, circular wait will feel familiar — and so will the value of timeouts and ordering.
Keep a "lock ranking" note in modules that share locks across packages. Unwritten rankings drift. Written rankings can be reviewed.

Picture transfer locks on two accounts acquired in random order under load. One night the interleaving appears; support sees a hung JVM; the dump shows the cycle. The fix is sorted lock order by account id — a one-line policy that removes the cycle. Most deadlock stories end with a boring ordering rule that should have been written first.

Prefer ordering and confinement over cleverness. Deadlocks are not a badge of advanced concurrency — they are usually a missing policy. Write the policy early; let the dump be a last resort.

Hold the checklist: ordered locks; no alien calls while holding; timeouts when nesting; dumps when hung. Meet those four and you will prevent most homemade deadlocks and recognize the rest quickly when an incident starts.

 When in doubt, remove a lock or sort acquisition order. Clever deadlock recovery is not a substitute for a cycle-free design. Prevention is the craft; dumps are the safety net.

A deadlock is a design smell that became a schedule. Treat it that way in postmortems: change the design, then verify with dumps under stress — not the other way around.

So reconnect the chain. Opposite lock orders showed circular wait. The classic conditions framed prevention. Global ordering, smaller sections, and tryLock timeouts gave practical exits. Alien code and dumps showed how deadlocks hide and how you find them. Concurrency features without an ordering policy remain incomplete.

After platform-thread concurrency, a modern twist changes the economics of blocking: virtual threads make the thread-per-request style scalable again for blocking I/O — with new pitfalls of their own.

Episode Fifty: virtual threads.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 49 (*Deadlocks*).

Narration technique: hang situation → circular wait example → four conditions → tryLock/order → alien code → dumps → next natural problem (virtual threads).
