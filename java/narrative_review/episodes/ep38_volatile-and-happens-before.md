# Episode 38 — volatile and Happens-Before

| Field | Value |
|---|---|
| Episode | 38 |
| Title | volatile and Happens-Before |
| Catalog handbook column | 38 |
| Narration source script | `make_episode_38.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Synchronization prevents races. But can another thread even see your write?
2. Without visibility guarantees, a thread may read a stale cached value forever.
3. The Java Memory Model defines when writes become visible across threads.
4. volatile and happens-before are the vocabulary for that contract.
5. Locks help — but visibility has its own rules.
6. Today — volatile, happens-before, and memory visibility in Java.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Eight.
2. volatile and Happens-Before — memory visibility.

### Scene `visibility` (renderer: `visibility`)

1. Each thread may cache field values in CPU registers or local caches.
2. A write by thread A might sit in a cache — invisible to thread B.
3. Synchronization flushes caches — but you cannot synchronize everything.
4. You need lighter-weight visibility guarantees for flags and status fields.
5. Reading a stale boolean can keep a worker loop running forever.
6. Visibility bugs look like logic errors — the code path never triggers.

### Scene `volatile_kw` (renderer: `volatile_kw`)

1. volatile tells the JVM — reads and writes go directly to main memory.
2. No caching of the volatile field in thread-local storage.
3. A read of a volatile always sees the latest write by any thread.
4. volatile does not make compound operations atomic — count plus plus still races.
5. Use volatile for single-field flags — running, ready, shutdown.
6. volatile is about visibility — not mutual exclusion.

### Scene `happens` (renderer: `happens`)

1. Happens-before is the formal ordering rule in the JMM.
2. If action A happens-before B, then B sees everything A did.
3. Unlocking a monitor happens-before the next lock on that monitor.
4. Writing a volatile happens-before a subsequent read of that volatile.
5. Thread start and join establish happens-before edges too.
6. Chain these edges to reason about what each thread can observe.

### Scene `jmm` (renderer: `jmm`)

1. The Java Memory Model — the contract between compiler, CPU, and programmer.
2. Without reordering, CPUs could not pipeline — performance would suffer.
3. The JMM allows optimizations within happens-before boundaries.
4. Program order within a single thread is preserved — as-if serial.
5. Across threads — only guaranteed ordering comes from synchronization.
6. Understand the JMM — or your concurrent code will surprise you.

### Scene `when_volatile` (renderer: `when_volatile`)

1. When to use volatile.
2. One writer, many readers — status flags and configuration switches.
3. Publishing an immutable object reference — safe if object is truly immutable.
4. Double-checked locking requires volatile on the reference field.
5. When not — counters, compound updates, or multiple writers.
6. For those — use synchronized or atomic classes instead.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using volatile on a non-volatile field inside a volatile read context.
3. Two — assuming volatile makes increment atomic — it does not.
4. Three — relying on visibility without establishing happens-before.
5. Also — double-checked locking without volatile — broken on some JVMs.
6. Match the tool to the guarantee you actually need.

### Scene `interview` (renderer: `interview`)

1. Interview question — what does volatile guarantee?
2. Visibility — every read sees the latest write to that field.
3. Ordering — writes before a volatile read are visible to that reader.
4. Not atomicity — compound operations still need synchronization.
5. Contrast with synchronized — which provides both exclusion and visibility.
6. Mention happens-before as the formal backing concept.

### Scene `teaser` (renderer: `teaser`)

1. Intrinsic locks work. Sometimes you need more control.
2. Episode Thirty-Nine — Explicit Locks.
3. ReentrantLock, tryLock, and Condition variables.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **38** — *volatile and Happens-Before*.
- **Series catalog:** Episode 38 ↔ handbook lesson 38 — *volatile and Happens-Before*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Synchronization prevents races. But can another thread even see your write?_
- **`title`** — starts from: _Episode Thirty-Eight._
- **`visibility`** — starts from: _Each thread may cache field values in CPU registers or local caches._
- **`volatile_kw`** — starts from: _volatile tells the JVM — reads and writes go directly to main memory._
- **`happens`** — starts from: _Happens-before is the formal ordering rule in the JMM._
- **`jmm`** — starts from: _The Java Memory Model — the contract between compiler, CPU, and programmer._
- **`when_volatile`** — starts from: _When to use volatile._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what does volatile guarantee?_
- **`teaser`** — starts from: _Intrinsic locks work. Sometimes you need more control._
