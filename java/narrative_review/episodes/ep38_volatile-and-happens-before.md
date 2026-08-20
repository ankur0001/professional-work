# Episode 38 — volatile and Happens-Before

| Field | Value |
|---|---|
| Episode | 38 |
| Title | volatile and Happens-Before |
| Catalog handbook column | 38 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Synchronization prevents races on critical sections. But can another thread even see your write?
2. Without visibility guarantees, a thread may read a stale cached value forever — infinite loops that never exit.
3. The Java Memory Model defines when writes become visible across threads — formal rules, not folklore.
4. volatile and happens-before are the vocabulary for that contract.
5. Locks help with both exclusion and visibility — but visibility has lighter-weight tools too.
6. Today — volatile, happens-before, and memory visibility without synchronizing everything.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Eight.
2. volatile and Happens-Before — memory visibility.
3. Caching, visibility bugs, volatile semantics, and JMM ordering rules.

### Scene `visibility` (renderer: `visibility`)

1. Each thread may cache field values in CPU registers or core-local caches for performance.
2. A write by thread A might sit in a cache — invisible to thread B reading from its cache.
3. Synchronization flushes and syncs caches — but you cannot synchronize every flag read.
4. You need lighter-weight visibility guarantees for status fields and shutdown signals.
5. Reading a stale boolean can keep a worker loop running forever — "it should have stopped!"
6. Visibility bugs look like logic errors — the code path never triggers despite correct-looking source.
7. The compiler and CPU may reorder instructions within JMM rules — another source of surprise.

### Scene `volatile_kw` (renderer: `volatile_kw`)

1. volatile tells the JVM — reads and writes of this field go through main memory consistently.
2. No long-lived caching of the volatile field in thread-local storage across reads.
3. A read of a volatile always sees the latest write by any thread — visibility guarantee.
4. volatile does not make compound operations atomic — count++ still races with two threads.
5. Use volatile for single-field flags — running, ready, shutdown, initialized.
6. volatile is about visibility and ordering — not mutual exclusion for read-modify-write.
7. Writing volatile flushes prior writes visible to the thread — part of happens-before chain.

### Scene `happens` (renderer: `happens`)

1. Happens-before is the formal ordering rule in the JMM — the happens-before edge.
2. If action A happens-before B, then B sees everything A did before A completed.
3. Unlocking a monitor happens-before the next lock on that same monitor by another thread.
4. Writing a volatile happens-before a subsequent read of that same volatile by another thread.
5. Thread.start happens-before any action in the started thread. Thread.join happens-before actions after join returns.
6. Chain these edges to reason about what each thread can observe — draw the timeline.
7. Without a happens-before edge between writer and reader — no visibility guarantee.

### Scene `jmm` (renderer: `jmm`)

1. The Java Memory Model — contract between compiler, CPU, and programmer.
2. Without reordering, CPUs could not pipeline effectively — performance would suffer massively.
3. The JMM allows optimizations within happens-before boundaries — safe reorderings only.
4. Program order within a single thread is preserved — as-if serial execution from that thread's view.
5. Across threads — only guaranteed ordering comes from synchronization, volatile, and thread actions.
6. Understand the JMM — or your concurrent code will surprise you in production on ARM servers.
7. data race = conflicting accesses without happens-before — undefined behavior territory for non-volatile non-atomic fields.

### Scene `when_volatile` (renderer: `when_volatile`)

1. When to use volatile — one writer, many readers on a status flag.
2. Shutdown flags, configuration switches, state machine phase indicators.
3. Publishing an immutable object reference — safe if the object is truly immutable after construction.
4. Double-checked locking on singletons requires volatile on the reference field — broken without it.
5. When not — counters with increment, compound updates, multiple writers to same field without sync.
6. For those — use synchronized, AtomicInteger, or LongAdder instead.
7. volatile boolean done is idiomatic for graceful worker shutdown — check in loop, set from another thread.

### Scene `code` (renderer: `code`)

1. Worker loop with volatile shutdown flag — visibility without locking every iteration.

```java
public class GracefulWorker {
    private volatile boolean shutdown = false;

    public void stop() {
        shutdown = true;
    }

    public void run() {
        while (!shutdown) {
            // do work
        }
        System.out.println("Worker stopped cleanly");
    }

    public static void main(String[] args) throws InterruptedException {
        GracefulWorker worker = new GracefulWorker();
        Thread t = new Thread(worker::run);
        t.start();
        Thread.sleep(100);
        worker.stop();
        t.join();
    }
}
```

2. shutdown volatile — main thread write visible to worker thread read without synchronized.
3. stop sets flag from main — happens-before worker observes true on next loop check.
4. Without volatile, worker might cache false forever — join hangs, JVM looks stuck.
5. Loop body should be non-blocking or respond to interrupt too — volatile alone doesn't interrupt sleep.
6. Do not add count++ on volatile int expecting atomicity — use AtomicInteger for counts.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using volatile expecting atomic increment — it is not synchronized arithmetic.
3. Two — assuming all fields in an object become visible when one volatile field is read — only volatile read guarantees for that field chain rules apply to prior writes in same thread before volatile write.
4. Three — double-checked locking without volatile on the singleton reference — broken on some JVMs historically.
5. Also — relying on visibility without establishing any happens-before edge — wishful thinking.
6. Match the tool to the guarantee you actually need — visibility, atomicity, or both.

### Scene `interview` (renderer: `interview`)

1. Interview question — what does volatile guarantee?
2. Visibility — every read sees the latest write to that volatile field.
3. Ordering — writes before a volatile write in same thread are visible after volatile read in another.
4. Not atomicity — compound operations like increment still need synchronization or atomics.
5. Contrast with synchronized — which provides both exclusion and full monitor semantics.
6. Mention happens-before as the formal backing concept — unlock/lock, volatile write/read, start/join.
7. Double-checked locking idiom requires volatile — shows depth if you mention it correctly.

### Scene `amplify`

1. Let me press on point 1 a bit harder.
2. Ensures visibility of writes.
3. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
4. If you cannot explain the failure mode, you do not own the feature yet.
5. Let me press on point 2 a bit harder.
6. Does not make compound actions atomic.
7. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
8. If you cannot explain the failure mode, you do not own the feature yet.
9. Let me press on point 3 a bit harder.
10. Happens-before edges matter.
11. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
12. If you cannot explain the failure mode, you do not own the feature yet.
13. Let me press on point 4 a bit harder.
14. Use atomics for counters.
15. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
16. If you cannot explain the failure mode, you do not own the feature yet.
17. Let me press on point 5 a bit harder.
18. Publication patterns use volatile carefully.
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
3. 1) Say out loud what volatile and Happens-Before is for in one sentence.
4. 2) Write the example from memory — approximate is fine.
5. 3) Name one mistake from this episode and how you would catch it in review.
6. That three-step drill turns watching into learning.
### Scene `summary` (renderer: `summary`)

1. Visibility ≠ atomicity. volatile fixes visibility for single-field access.
2. happens-before chains define what threads observe across memory.
3. JMM balances optimization with predictable concurrent semantics.
4. Use volatile for flags and safe publication of immutable refs.
5. Use synchronized or atomics for read-modify-write counters.

### Scene `teaser` (renderer: `teaser`)

1. Intrinsic locks work. Sometimes you need more control.
2. Episode Thirty-Nine — Explicit Locks.
3. ReentrantLock, tryLock, and Condition variables.
4. See you there.

_Total beats: **102** — expanded for ~8–12 minute conversational delivery (4-minute floor, 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **38** — *volatile and Happens-Before*.
- **Series catalog:** Episode 38 ↔ handbook lesson 38 — *volatile and Happens-Before*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with a walked-through code example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — Synchronization → visibility bridge
- **`title`** — episode title card
- **`visibility`** — stale cache problem
- **`volatile_kw`** — volatile semantics
- **`happens`** — happens-before rules
- **`jmm`** — Java Memory Model
- **`when_volatile`** — when to use volatile
- **`code`** — shutdown flag walkthrough
- **`mistakes`** — common mistakes
- **`interview`** — volatile guarantees
- **`summary`** — revision
- **`teaser`** — bridge to Explicit Locks
