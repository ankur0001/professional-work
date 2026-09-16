# Episode 39 — Explicit Locks

**Cut:** v1 (original)

## Transcript (from captions)

synchronized is built in — but sometimes you need more control. What if you want to try acquiring a lock without blocking forever? What if you need multiple wait conditions on the same lock?

Explicit locks in java.util.concurrent give you those options. ReentrantLock, tryLock, and Condition — the flexible toolkit. Today — explicit locks beyond synchronized. Episode Thirty-Nine.

Explicit Locks — ReentrantLock and Condition. ReentrantLock is a mutual-exclusion lock with explicit API. lock acquires. unlock releases — you must unlock in a finally block. Reentrant — the same thread can lock again without deadlocking itself.

Fair mode optional — threads acquire in arrival order. Use try-finally — never forget unlock after lock. ReentrantLock provides the same exclusion as synchronized — with more features.

tryLock attempts acquisition without indefinite blocking. Returns true if the lock was acquired — false if not available. tryLock with timeout — wait up to a duration, then give up.

Useful for avoiding deadlocks — back off and retry or fail gracefully. lockInterruptibly responds to thread interruption while waiting. Explicit locks shine when blocking forever is not acceptable.

Condition replaces wait and notify with a clearer API. lock.newCondition creates a condition variable bound to that lock. await releases the lock and waits. signal wakes one waiter.

Multiple conditions per lock — separate queues for different events. Always await inside a loop checking the predicate — spurious wakeups happen. Condition variables enable producer-consumer patterns cleanly.

ReentrantLock versus synchronized. Both provide mutual exclusion and memory visibility. synchronized is simpler — automatic release, no forgotten unlock. ReentrantLock adds tryLock, fairness, interruptible waits, multiple conditions.

synchronized is fine for most cases — do not reach for locks by default. Use explicit locks when you need their specific capabilities. When to choose explicit locks. Timed or non-blocking lock attempts — tryLock with timeout.

Fair ordering when starvation is a real concern. Multiple condition variables on one lock object. When not — simple critical sections — synchronized is cleaner. Measure contention before optimizing lock strategy.

Three common mistakes. One — forgetting unlock in finally — lock leaked forever. Two — locking without holding the lock when calling await or signal. Three — using tryLock but not handling the false return path.

Also — fair locks cost throughput — enable only when needed. Explicit locks demand discipline — synchronized is harder to misuse. Interview question — ReentrantLock versus synchronized?

Both provide mutual exclusion and happens-before visibility. ReentrantLock offers tryLock, fairness, interruptible lock, multiple Conditions. synchronized is simpler — JVM-managed, always released on exit.

Prefer synchronized unless you need a specific ReentrantLock feature. Mention always unlocking in finally with explicit locks. Locks coordinate threads. Who manages the threads themselves?

Episode Forty — ExecutorService and Thread Pools. Submit tasks, reuse threads, and shut down gracefully. See you there.
