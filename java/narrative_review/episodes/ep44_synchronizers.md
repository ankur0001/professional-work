# Episode 44 — Synchronizers

| Field | Value |
|---|---|
| Episode | 44 |
| Title | Synchronizers |
| Catalog handbook column | 44 |
| Narration source script | `make_episode_44.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Threads often need to meet at a point — start together or wait for completion.
2. Synchronizers coordinate thread arrival and departure without shared data structures.
3. CountDownLatch — one thread waits until others finish a countdown.
4. CyclicBarrier — threads rendezvous at a barrier, then release together.
5. Semaphore — limit how many threads access a resource at once.
6. Today — the three core synchronizers and when each fits.

### Scene `title` (renderer: `title`)

1. Episode Forty-Four.
2. Synchronizers.

### Scene `countdown_latch` (renderer: `countdown_latch`)

1. CountDownLatch initializes with a count — typically the number of workers.
2. Each worker calls countDown when finished — the latch decrements.
3. await blocks until the count reaches zero — then all waiters proceed.
4. One-shot — cannot reset the count after it reaches zero.
5. Classic pattern — main thread waits for parallel startup or shutdown.
6. Example — wait for N services to finish initialization before accepting traffic.

### Scene `cyclic_barrier` (renderer: `cyclic_barrier`)

1. CyclicBarrier sets a party count — the number of threads that must arrive.
2. Each thread calls await — the barrier releases when all parties arrive.
3. Reusable — after release, the barrier resets for the next cycle.
4. Optional barrier action runs once when the last thread arrives.
5. Use for phased parallel computation — each phase ends at the barrier.
6. BrokenBarrierException if a waiting thread is interrupted or times out.

### Scene `semaphore` (renderer: `semaphore`)

1. Semaphore maintains a set of permits — acquire takes one, release returns one.
2. new Semaphore of N allows up to N concurrent accessors.
3. acquire blocks when no permits remain — release wakes a waiter.
4. tryAcquire with timeout avoids indefinite blocking.
5. Binary semaphore with one permit acts like a mutex — but not reentrant.
6. Use for connection pools, rate limiting, and bounded resource access.

### Scene `coordination` (renderer: `coordination`)

1. Choosing the right synchronizer.
2. CountDownLatch — wait for a fixed number of events — one direction.
3. CyclicBarrier — threads meet repeatedly at the same point.
4. Semaphore — cap concurrent access to a limited resource.
5. Phaser offers flexible phase-based coordination — advanced alternative.
6. Exchanger swaps objects between two threads at a rendezvous point.

### Scene `when_sync` (renderer: `when_sync`)

1. When to use each synchronizer.
2. Service startup gate — CountDownLatch until all workers ready.
3. Parallel matrix phases — CyclicBarrier between compute steps.
4. Database connection cap — Semaphore with pool size permits.
5. Fork-join style shutdown — latch counts completed tasks.
6. When not — simple flag — volatile or AtomicBoolean may suffice.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — reusing a CountDownLatch after count hits zero — it is one-shot.
3. Two — wrong party count on CyclicBarrier — threads hang forever.
4. Three — Semaphore acquire without matching release — permits leak.
5. Also — calling await on the only thread that should countDown.
6. Synchronizers coordinate timing — they do not protect mutable state alone.

### Scene `interview` (renderer: `interview`)

1. Interview question — CountDownLatch versus CyclicBarrier?
2. CountDownLatch — one or more threads wait for others to finish events.
3. Count is decremented — cannot reset after reaching zero.
4. CyclicBarrier — threads rendezvous; all must arrive before any proceed.
5. Barrier resets and is reusable for the next cycle.
6. Semaphore limits concurrent access — different problem entirely.

### Scene `teaser` (renderer: `teaser`)

1. Synchronizers coordinate arrival. What about passing work between threads?
2. Episode Forty-Five — BlockingQueue and Producer-Consumer.
3. Bounded queues, backpressure, and the classic pattern.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **44** — *Synchronizers*.
- **Series catalog:** Episode 44 ↔ handbook lesson 44 — *Synchronizers*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Threads often need to meet at a point — start together or wait for completion._
- **`title`** — starts from: _Episode Forty-Four._
- **`countdown_latch`** — starts from: _CountDownLatch initializes with a count — typically the number of workers._
- **`cyclic_barrier`** — starts from: _CyclicBarrier sets a party count — the number of threads that must arrive._
- **`semaphore`** — starts from: _Semaphore maintains a set of permits — acquire takes one, release returns one._
- **`coordination`** — starts from: _Choosing the right synchronizer._
- **`when_sync`** — starts from: _When to use each synchronizer._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — CountDownLatch versus CyclicBarrier?_
- **`teaser`** — starts from: _Synchronizers coordinate arrival. What about passing work between threads?_
