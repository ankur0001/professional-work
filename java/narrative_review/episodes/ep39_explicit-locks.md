# Episode 39 — Explicit Locks

| Field | Value |
|---|---|
| Episode | 39 |
| Title | Explicit Locks |
| Catalog handbook column | 39 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`synchronized` covers a huge amount of real Java. Then you meet a situation it cannot express cleanly, and the keyword starts to feel like a wall instead of a tool.

Suppose a worker must acquire a lock, but only if it can do so within a short timeout — otherwise it should abandon the attempt and try another path. Or suppose one lock protects a buffer, and you need two different wait conditions: "not empty" and "not full," signaled independently. Intrinsic locks give you one wait-set per object and no `tryLock`. When do we need a lock we control as an object, with methods we can call?

`ReentrantLock` answers that need. It adds `tryLock`, condition variables, and optional fairness when `synchronized` is not enough. Prefer `synchronized` unless you need those features. Explicit locks are power tools, not a stylish replacement for the keyword.

```java
private final ReentrantLock lock = new ReentrantLock();

void critical() {
    lock.lock();
    try {
        work();
    } finally {
        lock.unlock();
    }
}
```

You call `lock()` to acquire. You do the work inside `try`. You unlock in `finally` so that exceptions still release ownership. Forgetting unlock is the classic failure mode: one path throws, the lock stays held, and the rest of the system waits forever while CPU looks idle. The `finally` is the ownership contract. Reentrancy means the same thread can acquire the same lock again without deadlocking itself — useful when helper methods also need the lock — but it does not excuse messy ownership.

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

Now the thread can fail to acquire and choose another strategy. Timeouts turn "maybe stuck" into "definably abandoned." Combined with consistent lock ordering, try-lock-with-timeout is one of the practical ways out of circular-wait disasters.

Multiple conditions matter for monitors with more than one reason to wait. With `ReentrantLock`, you can create separate `Condition` objects — for example, `notFull` and `notEmpty` — and await or signal the one that matches the state change:

```java
private final Condition notEmpty = lock.newCondition();
private final Condition notFull = lock.newCondition();
```

Intrinsic `wait`/`notify` can emulate this with care and complexity; explicit conditions make the intent readable when the state machine has more than one waiting reason.

Fairness is a knob, not a virtue by default. A fair lock tends to grant acquisition in roughly arrival order. That can reduce some starvation scenarios and usually costs throughput under contention. Do not enable fairness because it sounds nicer in a design doc. Enable it when measurement and requirements say you need that scheduling behavior.

Ownership clarity matters as much as API features. Know which thread is supposed to unlock. Do not lock in one abstraction and unlock in another without a hard protocol. Do not hold an explicit lock while calling alien code that might acquire other locks — unless you have mapped the ordering story.

Compare the mental model to `synchronized` once more. With the keyword, acquisition and release are tied to a block boundary the compiler enforces. With `ReentrantLock`, you own the timeline — which means you can express try-lock and timed lock, and also means you can forget unlock. That trade is the entire episode in one sentence. Reach for the explicit lock when the keyword cannot say what you mean. Stay with the keyword when it can.

What if you need interruptible lock acquisition so shutdown can break a thread waiting forever on `lock()`? `lockInterruptibly()` exists for that. It is another reason explicit locks show up in frameworks and servers that care about clean stop behavior.

When an interviewer asks when to prefer `ReentrantLock`, answer with features — tryLock, timeouts, multiple conditions, fairness — not with "because it is newer." Prefer tests that assert timeout behavior and unlock-on-exception behavior explicitly. Explicit locks make those policies visible in code — take advantage of that visibility in tests, not only in production firefighting.

Once locking techniques are in hand, another production pressure dominates: creating a raw `Thread` for every task does not scale. We need bounded workers, queues, shutdown rules, and rejection policies.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 39 (*Explicit Locks*).

Narration technique: timeout/tryLock situation → ReentrantLock → unlock in finally → tryLock → conditions → fairness → next natural problem (thread pools).
