# Episode 37 — Synchronization

| Field | Value |
|---|---|
| Episode | 37 |
| Title | Synchronization |
| Catalog handbook column | 37 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Two threads update the same counter. You expect two increments — you might get one.
2. Race conditions happen when shared mutable state is accessed without coordination.
3. Synchronization is how Java makes critical sections safe — one thread at a time.
4. Mutual exclusion on shared data — locks, monitors, and the synchronized keyword.
5. Today — synchronized methods, synchronized blocks, and intrinsic locks explained plainly.
6. Shared memory is powerful. Synchronization keeps it honest.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Seven.
2. Synchronization — safe access to shared data.
3. Races, monitors, method versus block locking, and when to synchronize minimally.

### Scene `race` (renderer: `race`)

1. A race condition — outcome depends on thread scheduling order you don't control.
2. count++ is not atomic — read, increment, write — three separate steps at bytecode level.
3. Two threads interleave those steps — updates can be lost silently.
4. The bug is intermittent — hardest kind to reproduce in dev, nastiest in prod.
5. You need mutual exclusion — only one thread in the critical section at a time.
6. Synchronization enforces that rule at the language level — compiler and JVM cooperate.
7. AtomicInteger is an alternative for simple counters — we'll see atomics later in the series.

### Scene `sync_method` (renderer: `sync_method`)

1. synchronized on an instance method locks the instance — the object referenced by this.
2. synchronized on a static method locks the Class object — one lock for all instances.
3. Only one thread can execute that synchronized method on the same lock at a time.
4. Other threads block until the lock is released — park/unpark under the hood.
5. Simple and readable for small critical sections that fit entirely in one method.
6. The lock is automatically released when the method exits — even on exception. No forgotten unlock.
7. Use synchronized methods when the whole method is the critical section — nothing else needs the lock mid-method.

### Scene `sync_block` (renderer: `sync_block`)

1. synchronized block — finer control over exactly what is protected.
2. synchronized on this — locks the current instance, same as instance method form.
3. synchronized on a dedicated lock object — private final Object lock = new Object() — clearer intent.
4. Protect only the few lines that touch shared state — leave non-shared work outside.
5. Smaller critical sections mean less contention — better throughput under load.
6. Prefer blocks when only part of a method needs protection — most methods aren't 100% critical.
7. Never synchronize on String literals or boxed Integer cache values — shared accidental locks across code.

### Scene `monitor` (renderer: `monitor`)

1. Every Java object has an intrinsic lock — also called a monitor.
2. Entering synchronized acquires the monitor. Exiting releases it — bytecode monitorenter/monitorexit.
3. Reentrant — the same thread can acquire a lock it already holds without deadlocking itself.
4. wait, notify, and notifyAll operate on the monitor — coordination beyond mere exclusion.
5. The JVM maps monitors to operating-system mutexes under the hood — blocking has real cost.
6. Understand monitors — they underpin synchronized, wait/notify, and later explicit locks.
7. One monitor per object — choosing the right lock object is a design decision.

### Scene `when_sync` (renderer: `when_sync`)

1. When to synchronize — read-modify-write on shared mutable fields.
2. Invariants that must hold while multiple fields are updated together — transfer between accounts.
3. Compound actions — check-then-act on shared state — if balance sufficient then deduct.
4. When not — over-synchronizing everything kills performance and invites deadlocks.
5. Synchronize the minimum — but synchronize what matters. Missing lock is worse than slow lock.
6. Immutable objects and thread confinement reduce how much you synchronize — design first.
7. Concurrent collections help for data structures — not a replacement for all coordination needs.

### Scene `code` (renderer: `code`)

1. Fix a race with synchronized increment — watch the difference.

```java
public class Counter {
    private int count = 0;

    public synchronized void increment() {
        count++;
    }

    public synchronized int getCount() {
        return count;
    }

    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        Thread t1 = new Thread(() -> { for (int i = 0; i < 1000; i++) counter.increment(); });
        Thread t2 = new Thread(() -> { for (int i = 0; i < 1000; i++) counter.increment(); });
        t1.start(); t2.start();
        t1.join(); t2.join();
        System.out.println(counter.getCount());  // 2000 — with sync
    }
}
```

2. synchronized on increment makes read-modify-write atomic relative to other synchronized methods on same lock.
3. getCount synchronized too — otherwise another thread might read mid-update torn value on some architectures.
4. Without synchronized, result often below 2000 — lost updates from interleaving.
5. Two threads, one lock object — the Counter instance monitor.
6. swap increment body to synchronized block on private lock field — same semantics, clearer for large methods.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — synchronizing on the wrong object — String literals or Integer.valueOf(1) shared across classes.
3. Two — holding locks while doing slow I/O — blocks every other thread waiting on that lock.
4. Three — nested locks on different objects in different orders — classic deadlock setup.
5. Also — assuming synchronized fixes visibility alone for all patterns — volatile and JMM still matter.
6. Lock only what you must — for as short as possible. Measure contention under load.

### Scene `interview` (renderer: `interview`)

1. Interview question — synchronized method versus synchronized block?
2. Both acquire an intrinsic lock on an object — instance this or explicit lock reference.
3. Method form locks on this or the Class. Block form lets you choose the lock and scope.
4. Blocks allow finer granularity — protect fewer lines, less contention.
5. Mention reentrancy and that locks release on exception — unlike manual unlock forget.
6. Contrast with ReentrantLock when you need tryLock — preview next episodes.
7. That answer shows you understand monitors, not just keywords.

### Scene `amplify`

1. Let me press on point 1 a bit harder.
2. Intrinsic locks.
3. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
4. If you cannot explain the failure mode, you do not own the feature yet.
5. Let me press on point 2 a bit harder.
6. Happens-before via sync.
7. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
8. If you cannot explain the failure mode, you do not own the feature yet.
9. Let me press on point 3 a bit harder.
10. Lock on shared state, not on random objects.
11. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
12. If you cannot explain the failure mode, you do not own the feature yet.
13. Let me press on point 4 a bit harder.
14. Deadlocks from multiple locks.
15. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
16. If you cannot explain the failure mode, you do not own the feature yet.
17. Let me press on point 5 a bit harder.
18. Prefer higher-level concurrency utils when possible.
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
3. 1) Say out loud what Synchronization is for in one sentence.
4. 2) Write the example from memory — approximate is fine.
5. 3) Name one mistake from this episode and how you would catch it in review.
6. That three-step drill turns watching into learning.
### Scene `summary` (renderer: `summary`)

1. Races come from unsynchronized shared mutable state.
2. synchronized = intrinsic lock on object monitor.
3. Method lock for whole method; block lock for partial critical sections.
4. Same thread can reenter — reentrant monitors.
5. Sync minimally; never lock on String literals or boxed caches.

### Scene `teaser` (renderer: `teaser`)

1. Locks prevent races. But can every thread see your writes?
2. Episode Thirty-Eight — volatile and Happens-Before.
3. Memory visibility and the Java Memory Model.
4. See you there.

_Total beats: **102** — expanded for ~8–12 minute conversational delivery (4-minute floor, 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **37** — *Synchronization*.
- **Series catalog:** Episode 37 ↔ handbook lesson 37 — *Synchronization*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with a walked-through code example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — Threads → Synchronization bridge
- **`title`** — episode title card
- **`race`** — race conditions
- **`sync_method`** — synchronized methods
- **`sync_block`** — synchronized blocks
- **`monitor`** — intrinsic locks/monitors
- **`when_sync`** — when to synchronize
- **`code`** — synchronized counter walkthrough
- **`mistakes`** — common mistakes
- **`interview`** — method vs block sync
- **`summary`** — revision
- **`teaser`** — bridge to volatile/JMM
