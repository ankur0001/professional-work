# Episode 43 — Atomics

| Field | Value |
|---|---|
| Episode | 43 |
| Title | Atomics |
| Catalog handbook column | 43 |
| Narration source script | `make_episode_43.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Incrementing a shared counter with a lock works — but locks block threads.
2. For a single variable, atomics offer lock-free updates.
3. AtomicInteger wraps an int with hardware-supported compare-and-swap.
4. CAS reads the current value, computes a new one, swaps only if unchanged.
5. AtomicReference applies the same idea to object references.
6. Today — atomic variables, CAS, and when lock-free beats locking.

### Scene `title` (renderer: `title`)

1. Episode Forty-Three.
2. Atomic Variables.

### Scene `atomic_integer` (renderer: `atomic_integer`)

1. AtomicInteger lives in java.util.concurrent.atomic.
2. get and set are atomic — no external synchronization needed.
3. incrementAndGet and addAndGet combine read-modify-write atomically.
4. compareAndSet expects the current value — swaps only on a match.
5. Use for counters, sequence numbers, and shared tallies.
6. One atomic variable — one contention point — still cheaper than a lock.

### Scene `cas` (renderer: `cas`)

1. Compare-and-swap is the foundation of lock-free algorithms.
2. Read the current value. Compute the desired new value.
3. Atomically swap only if the current value still matches what you read.
4. If another thread changed it — retry with the fresh value.
5. Hardware guarantees the swap is atomic — no mutex required.
6. CAS loops power AtomicInteger, AtomicLong, and concurrent queues.

### Scene `atomic_reference` (renderer: `atomic_reference`)

1. AtomicReference of T holds a reference updated atomically.
2. compareAndSet swaps the reference when the expected match holds.
3. getAndSet returns the old reference and stores a new one.
4. Useful for lazy initialization and swapping configuration objects.
5. AtomicStampedReference adds a stamp to detect ABA problems.
6. AtomicMarkableReference tracks a boolean mark alongside the reference.

### Scene `vs_locks` (renderer: `vs_locks`)

1. Atomics versus locks for simple shared state.
2. Locks — block threads, risk deadlock, heavier under contention.
3. Atomics — optimistic retries, no blocking on the fast path.
4. Best for single variables — counters, flags, reference swaps.
5. Not for protecting arbitrary multi-step invariants across fields.
6. Combine atomics with careful design — not a blanket lock replacement.

### Scene `when_atomics` (renderer: `when_atomics`)

1. When to use atomic variables.
2. Shared counters and metrics — AtomicInteger or AtomicLong.
3. One-shot initialization flags — AtomicBoolean.
4. Swapping immutable config snapshots — AtomicReference.
5. Building lock-free data structures — CAS loops internally.
6. When not — complex multi-field updates — use locks or synchronized.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using volatile int plus manual increment — not atomic as a unit.
3. Two — AtomicReference for mutable objects — reference swap does not deep-copy.
4. Three — infinite CAS retry loops without backoff under extreme contention.
5. Also — assuming compareAndSet alone fixes logical races across fields.
6. Atomics solve atomicity — your algorithm must still be correct.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is compare-and-swap?
2. Hardware-supported atomic read-compare-write on a single location.
3. Swap succeeds only if the current value equals the expected value.
4. Failed CAS means another thread won — retry with updated value.
5. AtomicInteger incrementAndGet uses CAS internally.
6. Contrast with synchronized — blocking versus optimistic retry.

### Scene `teaser` (renderer: `teaser`)

1. Atomics update single variables. What about coordinating many threads?
2. Episode Forty-Four — Synchronizers.
3. CountDownLatch, CyclicBarrier, and Semaphore.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **48** — *Atomic Classes*.
- **Series catalog mapping:** Episode 43 / catalog column `43` / published title *Atomics*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 48 → episode 43). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Incrementing a shared counter with a lock works — but locks block threads._
- **`title`** — starts from: _Episode Forty-Three._
- **`atomic_integer`** — starts from: _AtomicInteger lives in java.util.concurrent.atomic._
- **`cas`** — starts from: _Compare-and-swap is the foundation of lock-free algorithms._
- **`atomic_reference`** — starts from: _AtomicReference of T holds a reference updated atomically._
- **`vs_locks`** — starts from: _Atomics versus locks for simple shared state._
- **`when_atomics`** — starts from: _When to use atomic variables._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is compare-and-swap?_
- **`teaser`** — starts from: _Atomics update single variables. What about coordinating many threads?_
