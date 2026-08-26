# Episode 44 — Synchronizers

| Field | Value |
|---|---|
| Episode | 44 |
| Title | Synchronizers |
| Catalog handbook column | 44 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Atomics help when the problem is updating a value. Many concurrent designs are not about a value at all — they are about timing. Three workers must finish warming caches before the server accepts traffic. A parallel algorithm must wait until every thread reaches the end of a phase before any starts the next. At most five database connections may be checked out at once. Those are coordination problems. Reinventing them with bare `wait` and `notify` is possible and usually unwise.

Latches, barriers, and semaphores are the standard synchronizers for those shapes. Pick the simplest tool that matches the phase you mean.

`CountDownLatch` is a one-shot gate. You set a count. Workers call `countDown` when they finish a step. Waiters call `await` until the count reaches zero.

```java
CountDownLatch latch = new CountDownLatch(3);
// each worker:
latch.countDown();
// coordinator:
latch.await();
```

Walk the story. Three workers start. Each counts down once when ready. The coordinator blocks in `await` until all three have counted down. Then it opens the gate and continues. The latch does not reset. That one-shot nature is a feature when startup or a single rendezvous is the point. Forgetting to `countDown` on an error path is the classic hang: one worker throws, never counts down, and `await` waits forever. Use `try`/`finally` so the count moves even when work fails — or fail the whole startup explicitly instead of stalling.

`CyclicBarrier` is for recurring phases. Parties arrive, wait until all are present, then the barrier releases and can be reused for the next round. If you used a latch when you needed a barrier, you would rebuild the latch every phase — or worse, try to reset something that was not designed to reset. Latch versus barrier is a favorite interview contrast for exactly that reason: one-shot versus reusable multi-phase rendezvous.

`Semaphore` manages permits. Acquire a permit to enter; release when done. A semaphore of five is a clean way to limit concurrent access to a scarce resource without hand-rolling a counter and condition pair.

```java
Semaphore permits = new Semaphore(5);
permits.acquire();
try {
    talkToScarceService();
} finally {
    permits.release();
}
```

Leaking permits — acquiring and forgetting to release on exceptions — slowly starves the system. The `finally` release is the same ownership instinct as unlocking a `ReentrantLock`.

What if we skip these utilities and write our own wait/notify protocol for every gate?

You can, and you will relearn missed signals, spurious wakes, and forgotten notifies. The synchronizers exist so ordinary phase problems stay ordinary. Do not reinvent them casually. Prefer the named tool whose contract matches the story you are telling in the code review.

A startup narrative ties them together. Use a latch so initializer threads can finish before the acceptor starts. Use a semaphore so background jobs respect a concurrency budget toward a dependency. Use a barrier only if you truly have repeated parallel phases. Naming the synchronizer after the phase makes the design readable — and readability is part of concurrency safety.

A teaching contrast helps lock the vocabulary. Use a latch when the story is "wait until N one-time events happen." Use a barrier when the story is "N parties meet at the end of each phase, then repeat." Use a semaphore when the story is "at most N may enter." If you catch yourself explaining a custom wait/notify graph that matches one of those sentences, delete the custom graph and use the synchronizer.

Phasers and other advanced synchronizers exist for richer phase graphs. Curiosity is enough today. Most application code should get latches, barriers, and semaphores right before collecting exotic tools.

Error paths deserve one more beat. A worker that fails before `countDown` is indistinguishable from a worker that never existed — to the waiter. Decide whether failure counts down and records an error, or whether failure aborts the latch by other means. Silence is the worst policy; hangs are how silence presents itself.

Semaphores also model interesting fairness choices and draining permits for shutdown. You can acquire all permits to stop new entrants while existing work finishes — a cooperative quiescent state. That pattern shows up when a service wants to go idle before a config reload. Synchronizers are not only for startup; they are for controlled pauses and limited concurrency across a system's life.
When a teammate proposes wait/notify for a limit of five, offer a semaphore and save the review cycle.

Picture three initializer threads warming cache, connecting to a broker, and loading feature flags. A latch of three gates the HTTP acceptor. If flag loading fails, count down anyway and set a failed state the acceptor checks — or refuse to open the gate and crash the process loudly. Either policy beats a silent hang where nobody knows which initializer stuck.

Name the synchronizer after the phase in code reviews: `startupLatch`, `phaseBarrier`, `dbPermits`. Clear names prevent the next developer from using a latch where a barrier belonged simply because both "wait for others."

Hold the checklist when you design: one-shot event set → latch; repeating peer meetup → barrier; limited concurrent entry → semaphore. If none fit, maybe you need a queue or a lock — not a custom wait/notify clone of a semaphore.

So reconnect the chain. We needed phase and permit coordination, not only atomic updates. Latches gated one-shot readiness. Barriers reused rendezvous across phases. Semaphores limited concurrency with permits. Error-path countDown and permit leaks showed operational traps. Simplest matching tool beat clever wait/notify.

Once producers create work faster than consumers can take it, another coordination structure dominates: a queue that blocks, bounds memory, and carries jobs between stages.

Episode Forty-Five: `BlockingQueue`.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 44 (*Synchronizers*).

Narration technique: phase-timing situation → latch walkthrough → barrier contrast → semaphore permits → avoid wait/notify reinvention → startup story → next natural problem (blocking queues).
