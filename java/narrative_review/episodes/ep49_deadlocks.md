# Episode 49 — Deadlocks

| Field | Value |
|---|---|
| Episode | 49 |
| Title | Deadlocks |
| Catalog handbook column | 49 |
| Narration source script | `make_episode_49.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Forty-Eight kept state private per thread.
2. Shared resources still need locks — and locks can trap threads forever.
3. Thread A holds lock one, waits for lock two.
4. Thread B holds lock two, waits for lock one.
5. Neither can proceed — classic circular wait.
6. Today — deadlock conditions, detection, avoidance, and lock ordering.

### Scene `title` (renderer: `title`)

1. Episode Forty-Nine.
2. Deadlocks — Detection and Avoidance.

### Scene `four_conditions` (renderer: `four_conditions`)

1. Coffman conditions — all four must hold for a deadlock.
2. Mutual exclusion — at least one resource is non-sharable.
3. Hold and wait — a thread holds a lock while waiting for another.
4. No preemption — locks cannot be forcibly taken away.
5. Circular wait — a cycle of threads each waiting on the next.
6. Break any one condition — and deadlocks cannot form.

### Scene `classic_example` (renderer: `classic_example`)

1. The dining philosophers — intuitive deadlock story.
2. Five philosophers, five forks — need two forks to eat.
3. Everyone picks left fork, then right — cycle forms.
4. In code — transfer between accounts locking in opposite order.
5. Thread one locks account A then B.
6. Thread two locks B then A — same circular pattern.

### Scene `detection` (renderer: `detection`)

1. Detection — find cycles in the wait-for graph.
2. Thread dump on JVM — jstack or kill minus three.
3. Look for BLOCKED threads waiting on monitors held by each other.
4. ThreadMXBean.findDeadlockedThreads returns deadlocked thread IDs.
5. Detection is reactive — the system is already stuck.
6. Use in production monitoring — alert when deadlocks appear.

### Scene `avoidance` (renderer: `avoidance`)

1. Avoidance — design so deadlocks cannot happen.
2. Lock ordering — always acquire locks in a global consistent order.
3. Try-lock with timeout — back off and retry instead of waiting forever.
4. Lock fewer resources — coarser design or lock-free structures.
5. Banker algorithm — theoretical resource allocation — rarely used in apps.
6. Prevention beats detection — design locks in from the start.

### Scene `lock_ordering` (renderer: `lock_ordering`)

1. Lock ordering in practice.
2. Assign each lock a unique integer ID — always lock lower ID first.
3. For account transfer — lock accounts by ascending hash or ID.
4. ReentrantLock with tryLock and timeout — fail fast under contention.
5. synchronized blocks — same ordering rule applies.
6. Document the order — code review catches violations early.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — nested locks in different orders across call paths.
3. Two — calling external code while holding a lock — hidden lock order.
4. Three — ignoring try-lock timeouts — infinite BLOCKED in thread dumps.
5. Also — fine-grained locks without a documented acquisition order.
6. Deadlocks are design bugs — not random runtime glitches.

### Scene `interview` (renderer: `interview`)

1. Interview question — what causes deadlock and how do you prevent it?
2. Four Coffman conditions — mutual exclusion, hold-and-wait, no preemption, circular wait.
3. Prevention — consistent global lock ordering.
4. Detection — thread dumps, ThreadMXBean, cycle in wait-for graph.
5. tryLock with timeout — back off instead of blocking forever.
6. Mention dining philosophers or account transfer example.

### Scene `teaser` (renderer: `teaser`)

1. Platform threads block — and blocking under load gets expensive.
2. Episode Fifty — Virtual Threads.
3. Project Loom, pinning, and structured concurrency.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **49** — *Deadlocks*.
- **Series catalog:** Episode 49 ↔ handbook lesson 49 — *Deadlocks*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Forty-Eight kept state private per thread._
- **`title`** — starts from: _Episode Forty-Nine._
- **`four_conditions`** — starts from: _Coffman conditions — all four must hold for a deadlock._
- **`classic_example`** — starts from: _The dining philosophers — intuitive deadlock story._
- **`detection`** — starts from: _Detection — find cycles in the wait-for graph._
- **`avoidance`** — starts from: _Avoidance — design so deadlocks cannot happen._
- **`lock_ordering`** — starts from: _Lock ordering in practice._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what causes deadlock and how do you prevent it?_
- **`teaser`** — starts from: _Platform threads block — and blocking under load gets expensive._
