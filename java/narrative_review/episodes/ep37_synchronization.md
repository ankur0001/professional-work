# Episode 37 — Synchronization

| Field | Value |
|---|---|
| Episode | 37 |
| Title | Synchronization |
| Catalog handbook column | 37 |
| Narration source script | `make_episode_37.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Two threads update the same counter. You expect two — you might get one.
2. Race conditions happen when shared mutable state is accessed without coordination.
3. Synchronization is how Java makes critical sections safe.
4. One thread at a time — mutual exclusion on shared data.
5. Locks, monitors, and the synchronized keyword — the first line of defense.
6. Today — synchronized methods, blocks, and intrinsic locks.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Seven.
2. Synchronization — safe access to shared data.

### Scene `race` (renderer: `race`)

1. A race condition — outcome depends on thread scheduling order.
2. count plus plus is not atomic — read, increment, write — three steps.
3. Two threads interleave those steps — updates can be lost.
4. The bug is intermittent — hardest kind to reproduce.
5. You need mutual exclusion — only one thread in the critical section.
6. Synchronization enforces that rule at the language level.

### Scene `sync_method` (renderer: `sync_method`)

1. synchronized on a method locks the instance — or the Class object for static.
2. Only one thread can execute that synchronized method at a time.
3. Other threads block until the lock is released.
4. Simple and readable for small critical sections.
5. The lock is automatically released when the method exits — even on exception.
6. Use synchronized methods when the whole method is the critical section.

### Scene `sync_block` (renderer: `sync_block`)

1. synchronized block — finer control over what is protected.
2. synchronized on this — locks the current instance.
3. synchronized on a dedicated lock object — often clearer intent.
4. Protect only the few lines that touch shared state.
5. Smaller critical sections mean less contention — better throughput.
6. Prefer blocks when only part of a method needs protection.

### Scene `monitor` (renderer: `monitor`)

1. Every Java object has an intrinsic lock — also called a monitor.
2. Entering synchronized acquires the monitor. Exiting releases it.
3. Reentrant — the same thread can acquire a lock it already holds.
4. wait and notify operate on the monitor — coordination beyond exclusion.
5. The JVM maps monitors to operating-system mutexes under the hood.
6. Understand monitors — they underpin every synchronized construct.

### Scene `when_sync` (renderer: `when_sync`)

1. When to synchronize.
2. Any read-modify-write on shared mutable fields.
3. Invariants that must hold while multiple fields are updated.
4. Compound actions — check-then-act on shared state.
5. When not — over-synchronizing everything kills performance.
6. Synchronize the minimum — but synchronize what matters.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — synchronizing on the wrong object — String literals or boxed integers.
3. Two — holding locks while doing slow I/O — blocks every waiter.
4. Three — nested locks on different objects — classic deadlock setup.
5. Also — assuming synchronized fixes visibility alone — see next episode.
6. Lock only what you must — for as short as possible.

### Scene `interview` (renderer: `interview`)

1. Interview question — synchronized method versus synchronized block?
2. Both acquire an intrinsic lock on an object.
3. Method form locks on this or the Class. Block form lets you choose the lock.
4. Blocks allow finer granularity — protect fewer lines.
5. Mention reentrancy and that locks release on exception.
6. That answer shows you understand monitors, not just keywords.

### Scene `teaser` (renderer: `teaser`)

1. Locks prevent races. But can every thread see your writes?
2. Episode Thirty-Eight — Memory Visibility.
3. volatile, happens-before, and the Java Memory Model.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **37** — *Synchronization*.
- **Series catalog:** Episode 37 ↔ handbook lesson 37 — *Synchronization*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Two threads update the same counter. You expect two — you might get one._
- **`title`** — starts from: _Episode Thirty-Seven._
- **`race`** — starts from: _A race condition — outcome depends on thread scheduling order._
- **`sync_method`** — starts from: _synchronized on a method locks the instance — or the Class object for static._
- **`sync_block`** — starts from: _synchronized block — finer control over what is protected._
- **`monitor`** — starts from: _Every Java object has an intrinsic lock — also called a monitor._
- **`when_sync`** — starts from: _When to synchronize._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — synchronized method versus synchronized block?_
- **`teaser`** — starts from: _Locks prevent races. But can every thread see your writes?_
