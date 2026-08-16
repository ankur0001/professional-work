# Episode 39 — Explicit Locks

| Field | Value |
|---|---|
| Episode | 39 |
| Title | Explicit Locks |
| Catalog handbook column | 39 |
| Narration source script | `make_episode_39.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. synchronized is built in — but sometimes you need more control.
2. What if you want to try acquiring a lock without blocking forever?
3. What if you need multiple wait conditions on the same lock?
4. Explicit locks in java.util.concurrent give you those options.
5. ReentrantLock, tryLock, and Condition — the flexible toolkit.
6. Today — explicit locks beyond synchronized.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Nine.
2. Explicit Locks — ReentrantLock and Condition.

### Scene `reentrant` (renderer: `reentrant`)

1. ReentrantLock is a mutual-exclusion lock with explicit API.
2. lock acquires. unlock releases — you must unlock in a finally block.
3. Reentrant — the same thread can lock again without deadlocking itself.
4. Fair mode optional — threads acquire in arrival order.
5. Use try-finally — never forget unlock after lock.
6. ReentrantLock provides the same exclusion as synchronized — with more features.

### Scene `trylock` (renderer: `trylock`)

1. tryLock attempts acquisition without indefinite blocking.
2. Returns true if the lock was acquired — false if not available.
3. tryLock with timeout — wait up to a duration, then give up.
4. Useful for avoiding deadlocks — back off and retry or fail gracefully.
5. lockInterruptibly responds to thread interruption while waiting.
6. Explicit locks shine when blocking forever is not acceptable.

### Scene `condition` (renderer: `condition`)

1. Condition replaces wait and notify with a clearer API.
2. lock.newCondition creates a condition variable bound to that lock.
3. await releases the lock and waits. signal wakes one waiter.
4. Multiple conditions per lock — separate queues for different events.
5. Always await inside a loop checking the predicate — spurious wakeups happen.
6. Condition variables enable producer-consumer patterns cleanly.

### Scene `compare` (renderer: `compare`)

1. ReentrantLock versus synchronized.
2. Both provide mutual exclusion and memory visibility.
3. synchronized is simpler — automatic release, no forgotten unlock.
4. ReentrantLock adds tryLock, fairness, interruptible waits, multiple conditions.
5. synchronized is fine for most cases — do not reach for locks by default.
6. Use explicit locks when you need their specific capabilities.

### Scene `when_locks` (renderer: `when_locks`)

1. When to choose explicit locks.
2. Timed or non-blocking lock attempts — tryLock with timeout.
3. Fair ordering when starvation is a real concern.
4. Multiple condition variables on one lock object.
5. When not — simple critical sections — synchronized is cleaner.
6. Measure contention before optimizing lock strategy.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — forgetting unlock in finally — lock leaked forever.
3. Two — locking without holding the lock when calling await or signal.
4. Three — using tryLock but not handling the false return path.
5. Also — fair locks cost throughput — enable only when needed.
6. Explicit locks demand discipline — synchronized is harder to misuse.

### Scene `interview` (renderer: `interview`)

1. Interview question — ReentrantLock versus synchronized?
2. Both provide mutual exclusion and happens-before visibility.
3. ReentrantLock offers tryLock, fairness, interruptible lock, multiple Conditions.
4. synchronized is simpler — JVM-managed, always released on exit.
5. Prefer synchronized unless you need a specific ReentrantLock feature.
6. Mention always unlocking in finally with explicit locks.

### Scene `teaser` (renderer: `teaser`)

1. Locks coordinate threads. Who manages the threads themselves?
2. Episode Forty — ExecutorService and Thread Pools.
3. Submit tasks, reuse threads, and shut down gracefully.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **39** — *Explicit Locks*.
- **Series catalog:** Episode 39 ↔ handbook lesson 39 — *Explicit Locks*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _synchronized is built in — but sometimes you need more control._
- **`title`** — starts from: _Episode Thirty-Nine._
- **`reentrant`** — starts from: _ReentrantLock is a mutual-exclusion lock with explicit API._
- **`trylock`** — starts from: _tryLock attempts acquisition without indefinite blocking._
- **`condition`** — starts from: _Condition replaces wait and notify with a clearer API._
- **`compare`** — starts from: _ReentrantLock versus synchronized._
- **`when_locks`** — starts from: _When to choose explicit locks._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — ReentrantLock versus synchronized?_
- **`teaser`** — starts from: _Locks coordinate threads. Who manages the threads themselves?_
