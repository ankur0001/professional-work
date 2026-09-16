# Episode 38 — volatile and Happens-Before

**Cut:** v1 (original)

## Transcript (from captions)

Synchronization prevents races. But can another thread even see your write? Without visibility guarantees, a thread may read a stale cached value forever. The Java Memory Model defines when writes become visible across threads.

volatile and happens-before are the vocabulary for that contract. Locks help — but visibility has its own rules. Today — volatile, happens-before, and memory visibility in Java. Episode Thirty-Eight.

volatile and Happens-Before — memory visibility. Each thread may cache field values in CPU registers or local caches. A write by thread A might sit in a cache — invisible to thread B.

Synchronization flushes caches — but you cannot synchronize everything. You need lighter-weight visibility guarantees for flags and status fields. Reading a stale boolean can keep a worker loop running forever.

Visibility bugs look like logic errors — the code path never triggers. volatile tells the JVM — reads and writes go directly to main memory. No caching of the volatile field in thread-local storage.

A read of a volatile always sees the latest write by any thread. volatile does not make compound operations atomic — count plus plus still races. Use volatile for single-field flags — running, ready, shutdown.

volatile is about visibility — not mutual exclusion. Happens-before is the formal ordering rule in the JMM. If action A happens-before B, then B sees everything A did. Unlocking a monitor happens-before the next lock on that monitor.

Writing a volatile happens-before a subsequent read of that volatile. Thread start and join establish happens-before edges too. Chain these edges to reason about what each thread can observe.

The Java Memory Model — the contract between compiler, CPU, and programmer. Without reordering, CPUs could not pipeline — performance would suffer. The JMM allows optimizations within happens-before boundaries.

Program order within a single thread is preserved — as-if serial. Across threads — only guaranteed ordering comes from synchronization. Understand the JMM — or your concurrent code will surprise you.

When to use volatile. One writer, many readers — status flags and configuration switches. Publishing an immutable object reference — safe if object is truly immutable. Double-checked locking requires volatile on the reference field.

When not — counters, compound updates, or multiple writers. For those — use synchronized or atomic classes instead. Three common mistakes. One — using volatile on a non-volatile field inside a volatile read context.

Two — assuming volatile makes increment atomic — it does not. Three — relying on visibility without establishing happens-before. Also — double-checked locking without volatile — broken on some JVMs.

Match the tool to the guarantee you actually need. Interview question — what does volatile guarantee? Visibility — every read sees the latest write to that field. Ordering — writes before a volatile read are visible to that reader.

Not atomicity — compound operations still need synchronization. Contrast with synchronized — which provides both exclusion and visibility. Mention happens-before as the formal backing concept.

Intrinsic locks work. Sometimes you need more control. Episode Thirty-Nine — Explicit Locks. ReentrantLock, tryLock, and Condition variables. See you there.
