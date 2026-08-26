# Episode 39 — Explicit Locks

| Field | Value |
|---|---|
| Episode | 39 |
| Title | Explicit Locks |
| Catalog handbook column | 39 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`synchronized` covers a huge amount of real Java. Then you meet a situation it cannot express cleanly.

Suppose a worker must acquire a lock, but only if it can do so within a short timeout — otherwise it should abandon the attempt and try another path. Or suppose one lock protects a buffer, and you need two different wait conditions: "not empty" and "not full," signaled independently. Intrinsic locks give you one wait-set per object and no `tryLock`. The question becomes: when do we need a lock we control as an object?

`ReentrantLock` answers that need. It adds `tryLock`, conditions, and optional fairness when `synchronized` is not enough. Prefer `synchronized` unless you need those features. Explicit locks are power tools, not a stylish replacement for the keyword.

```java
lock.lock();
try {
    work();
} finally {
    lock.unlock();
}
```

Walk the discipline. You call `lock()` to acquire. You do the work inside `try`. You unlock in `finally` so that exceptions still release ownership. Forgetting unlock is the classic failure mode: one path throws, the lock stays held, and the rest of the system waits forever. The `finally` is not style. It is the ownership contract.

`tryLock` avoids dead waiting when waiting forever is the wrong policy:

```java
if (lock.tryLock(100, TimeUnit.MILLISECONDS)) {
    try {
        work();
    } finally {
        lock.unlock();
    }
} else {
    // take a backup path — do not pretend you hold the lock
}
```

Now the thread can fail to acquire and choose another strategy. That single ability changes how you design deadlock avoidance and responsive services. Timeouts turn "maybe stuck" into "definably abandoned."

Multiple conditions matter for monitors with more than one reason to wait. With `ReentrantLock`, you can create separate `Condition` objects — for example, `notFull` and `notEmpty` — and await or signal the one that matches the state change. Intrinsic `wait`/`notify` can emulate this with care and complexity; explicit conditions make the intent readable.

Fairness is a knob, not a virtue by default. A fair lock tends to grant acquisition in roughly arrival order. That can reduce some starvation scenarios and usually costs throughput under contention. Do not enable fairness because it sounds nicer. Enable it when measurement and requirements say you need that scheduling behavior.

Ownership clarity matters as much as API features. Know which thread is supposed to unlock. Do not lock in one abstraction and unlock in another without a hard protocol. Do not hold an explicit lock while calling alien code that might acquire other locks — unless you have mapped the ordering story. Features do not remove the need for a locking policy.

So reconnect the chain. We hit limits of `synchronized` — timeouts, try-acquire, multiple conditions, fairness. `ReentrantLock` provided those features with a strict unlock-in-finally discipline. Prefer the simpler intrinsic lock when it fits. Reach for explicit locks when the problem statement actually needs them.

Once locking techniques are in hand, another production pressure dominates: creating a raw `Thread` for every task does not scale. We need bounded workers, queues, shutdown rules, and rejection policies.

That pressure is Episode Forty: `ExecutorService`.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 39 (*Explicit Locks*).

Narration technique: timeout/tryLock situation → ReentrantLock as answer → unlock in finally → tryLock → conditions → fairness cost → ownership → next natural problem (thread pools).
