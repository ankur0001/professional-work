# Episode 39 — Explicit Locks

| Field | Value |
|---|---|
| Episode | 39 |
| Title | Explicit Locks |
| Catalog handbook column | 39 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. synchronized is built in — simple, JVM-managed, hard to forget to release.
2. But sometimes you need more control than a keyword can offer.
3. What if you want to try acquiring a lock without blocking forever?
4. What if you need multiple wait conditions on the same lock — not one wait set?
5. Explicit locks in java.util.concurrent give you those options — ReentrantLock and Condition.
6. Today — explicit locks beyond synchronized, with the discipline they demand.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Nine.
2. Explicit Locks — ReentrantLock and Condition.
3. tryLock, fairness, interruptible waits, and when synchronized still wins.

### Scene `reentrant` (renderer: `reentrant`)

1. ReentrantLock is a mutual-exclusion lock with an explicit Java API.
2. lock acquires. unlock releases — you must unlock in a finally block every time. No exceptions.
3. Reentrant — the same thread can lock again without deadlocking itself — hold count tracked internally.
4. Fair mode optional — new ReentrantLock(true) — threads acquire in approximate arrival order.
5. Fair locks reduce starvation but cost throughput — measure before enabling globally.
6. ReentrantLock provides the same exclusion as synchronized — plus optional features synchronized lacks.
7. isHeldByCurrentThread helps assert lock ownership in complex refactors.

### Scene `trylock` (renderer: `trylock`)

1. tryLock attempts acquisition without indefinite blocking — returns boolean immediately or after timeout.
2. Returns true if the lock was acquired — false if not available right now.
3. tryLock with timeout — wait up to Duration or milliseconds, then give up gracefully.
4. Useful for avoiding deadlocks — back off, log, retry, or fail with user-visible error.
5. lockInterruptibly responds to thread interruption while waiting — shutdown-friendly blocking.
6. Explicit locks shine when blocking forever is not acceptable — UI threads, deadline-bound requests.
7. Always handle false return from tryLock — don't assume you hold the lock.

### Scene `condition` (renderer: `condition`)

1. Condition replaces Object wait and notify with a clearer, more flexible API.
2. lock.newCondition creates a condition variable bound to that specific lock instance.
3. await releases the lock and waits. signal wakes one waiter. signalAll wakes all waiters on that condition.
4. Multiple conditions per lock — separate queues for "not empty" and "not full" — producer-consumer clarity.
5. Always await inside a loop checking the predicate — spurious wakeups happen, Java allows them.
6. Condition variables enable producer-consumer patterns cleanly — BoundedBuffer textbook case.
7. awaitNanos and awaitUntil support timed waits — don't block past shutdown deadline.

### Scene `compare` (renderer: `compare`)

1. ReentrantLock versus synchronized — when does each win?
2. Both provide mutual exclusion and memory visibility via happens-before.
3. synchronized is simpler — automatic release on exit, no forgotten unlock, less boilerplate.
4. ReentrantLock adds tryLock, fairness, interruptible lock acquisition, multiple Conditions, lock polling.
5. synchronized is fine for most cases — do not reach for ReentrantLock by default in every service.
6. Use explicit locks when you need their specific capabilities — documented in code review.
7. StampedLock adds optimistic reads — even more specialized, easy to misuse — advanced topic.

### Scene `when_locks` (renderer: `when_locks`)

1. When to choose explicit locks — timed or non-blocking lock attempts with tryLock.
2. Fair ordering when starvation of low-priority threads is a real observed problem.
3. Multiple condition variables on one lock object — bounded queues with separate empty/full signals.
4. When not — simple critical sections protecting a few lines — synchronized is cleaner and safer for juniors.
5. Measure contention before optimizing lock strategy — premature ReentrantLock adds noise.
6. Always unlock in finally — treat lock like Closeable resource mentally.
7. Lock ordering across objects prevents deadlocks — same rule as synchronized nested locks.

### Scene `code` (renderer: `code`)

1. tryLock with timeout — fail gracefully instead of blocking forever.

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.ReentrantLock;

public class TryLockDemo {
    private final ReentrantLock lock = new ReentrantLock();

    public boolean tryUpdate() {
        boolean acquired = false;
        try {
            acquired = lock.tryLock(100, TimeUnit.MILLISECONDS);
            if (!acquired) {
                System.out.println("Could not acquire lock — skipping update");
                return false;
            }
            // critical section
            System.out.println("Update applied");
            return true;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return false;
        } finally {
            if (acquired) {
                lock.unlock();
            }
        }
    }

    public static void main(String[] args) {
        new TryLockDemo().tryUpdate();
    }
}
```

2. tryLock with timeout — waits up to 100ms then returns false — no infinite stall.
3. acquired flag tracks whether we hold lock — unlock only if we acquired — critical pattern.
4. finally unlock — even if critical section throws — same discipline as synchronized auto-release.
5. Interrupt during wait — restore interrupt flag, return false — don't swallow interruption.
6. Contrast with lock() — blocks until available — tryLock for degradable operations.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — forgetting unlock in finally — lock leaked forever, all other threads block eternally.
3. Two — calling await or signal without holding the lock — IllegalMonitorStateException at runtime.
4. Three — using tryLock but not handling the false return path — logic runs without holding lock, races return.
5. Also — enabling fair locks globally without measuring — throughput cliff on high-contention paths.
6. Explicit locks demand discipline — synchronized is harder to misuse for simple cases.

### Scene `interview` (renderer: `interview`)

1. Interview question — ReentrantLock versus synchronized?
2. Both provide mutual exclusion and happens-before visibility.
3. ReentrantLock offers tryLock, fairness option, interruptible lock, multiple Conditions per lock.
4. synchronized is simpler — JVM-managed, always released on exit including exceptions.
5. Prefer synchronized unless you need a specific ReentrantLock feature — justify in design review.
6. Mention always unlocking in finally with explicit locks — interviewers love hearing finally.
7. Condition.await loop checking predicate — shows producer-consumer understanding.

### Scene `amplify`

1. Let me press on point 1 a bit harder.
2. Always unlock in finally.
3. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
4. If you cannot explain the failure mode, you do not own the feature yet.
5. Let me press on point 2 a bit harder.
6. tryLock avoids dead waiting.
7. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
8. If you cannot explain the failure mode, you do not own the feature yet.
9. Let me press on point 3 a bit harder.
10. Multiple conditions.
11. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
12. If you cannot explain the failure mode, you do not own the feature yet.
13. Let me press on point 4 a bit harder.
14. Fairness costs throughput.
15. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
16. If you cannot explain the failure mode, you do not own the feature yet.
17. Let me press on point 5 a bit harder.
18. Prefer synchronized unless you need features.
19. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
20. If you cannot explain the failure mode, you do not own the feature yet.

### Scene `handbook_spine`

1. How this maps to the reference handbook mindset:
2. The handbook teaches concept, internal working, mistakes, and interview questions.
3. We are doing the same job in spoken form — compressed for video, but not reduced to headlines.
4. So if a section felt familiar, good: that means the curriculum spine is intact.

### Scene `practice`

1. Mini practice before you go.
2. Pause the video and do this without looking:
3. 1) Say out loud what Explicit Locks is for in one sentence.
4. 2) Write the example from memory — approximate is fine.
5. 3) Name one mistake from this episode and how you would catch it in review.
6. That three-step drill turns watching into learning.
### Scene `summary` (renderer: `summary`)

1. ReentrantLock = explicit synchronized with extras.
2. tryLock and timeouts avoid indefinite blocking and aid deadlock recovery.
3. Condition replaces wait/notify with multiple wait sets per lock.
4. unlock in finally — non-negotiable.
5. Default to synchronized; upgrade when features justify complexity.

### Scene `teaser` (renderer: `teaser`)

1. Locks coordinate threads. Who manages the threads themselves?
2. Episode Forty — ExecutorService and Thread Pools.
3. Submit tasks, reuse threads, and shut down gracefully.
4. See you there.

_Total beats: **102** — expanded for ~8–12 minute conversational delivery (4-minute floor, 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **39** — *Explicit Locks*.
- **Series catalog:** Episode 39 ↔ handbook lesson 39 — *Explicit Locks*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with a walked-through code example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — volatile → Explicit Locks bridge
- **`title`** — episode title card
- **`reentrant`** — ReentrantLock basics
- **`trylock`** — tryLock and timeouts
- **`condition`** — Condition variables
- **`compare`** — vs synchronized
- **`when_locks`** — when to choose explicit locks
- **`code`** — tryLock walkthrough
- **`mistakes`** — common mistakes
- **`interview`** — ReentrantLock vs synchronized
- **`summary`** — revision
- **`teaser`** — bridge to ExecutorService
