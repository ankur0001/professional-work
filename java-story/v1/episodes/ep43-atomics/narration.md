# Episode 43 — Atomics

**Cut:** v1 (original)

## Transcript (from captions)

Incrementing a shared counter with a lock works — but locks block threads. For a single variable, atomics offer lock-free updates. AtomicInteger wraps an int with hardware-supported compare-and-swap.

CAS reads the current value, computes a new one, swaps only if unchanged. AtomicReference applies the same idea to object references. Today — atomic variables, CAS, and when lock-free beats locking.

Episode Forty-Three. Atomic Variables. AtomicInteger lives in java.util.concurrent.atomic. get and set are atomic — no external synchronization needed. incrementAndGet and addAndGet combine read-modify-write atomically.

compareAndSet expects the current value — swaps only on a match. Use for counters, sequence numbers, and shared tallies. One atomic variable — one contention point — still cheaper than a lock.

Compare-and-swap is the foundation of lock-free algorithms. Read the current value. Compute the desired new value. Atomically swap only if the current value still matches what you read.

If another thread changed it — retry with the fresh value. Hardware guarantees the swap is atomic — no mutex required. CAS loops power AtomicInteger, AtomicLong, and concurrent queues.

AtomicReference of T holds a reference updated atomically. compareAndSet swaps the reference when the expected match holds. getAndSet returns the old reference and stores a new one.

Useful for lazy initialization and swapping configuration objects. AtomicStampedReference adds a stamp to detect ABA problems. AtomicMarkableReference tracks a boolean mark alongside the reference.

Atomics versus locks for simple shared state. Locks — block threads, risk deadlock, heavier under contention. Atomics — optimistic retries, no blocking on the fast path. Best for single variables — counters, flags, reference swaps.

Not for protecting arbitrary multi-step invariants across fields. Combine atomics with careful design — not a blanket lock replacement. When to use atomic variables. Shared counters and metrics — AtomicInteger or AtomicLong.

One-shot initialization flags — AtomicBoolean. Swapping immutable config snapshots — AtomicReference. Building lock-free data structures — CAS loops internally. When not — complex multi-field updates — use locks or synchronized.

Three common mistakes. One — using volatile int plus manual increment — not atomic as a unit. Two — AtomicReference for mutable objects — reference swap does not deep-copy. Three — infinite CAS retry loops without backoff under extreme contention.

Also — assuming compareAndSet alone fixes logical races across fields. Atomics solve atomicity — your algorithm must still be correct. Interview question — what is compare-and-swap?

Hardware-supported atomic read-compare-write on a single location. Swap succeeds only if the current value equals the expected value. Failed CAS means another thread won — retry with updated value.

AtomicInteger incrementAndGet uses CAS internally. Contrast with synchronized — blocking versus optimistic retry. Atomics update single variables. What about coordinating many threads?

Episode Forty-Four — Synchronizers. CountDownLatch, CyclicBarrier, and Semaphore. See you there.
