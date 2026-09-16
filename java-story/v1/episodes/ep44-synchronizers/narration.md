# Episode 44 — Synchronizers

**Cut:** v1 (original)

## Transcript (from captions)

Threads often need to meet at a point — start together or wait for completion. Synchronizers coordinate thread arrival and departure without shared data structures. CountDownLatch — one thread waits until others finish a countdown.

CyclicBarrier — threads rendezvous at a barrier, then release together. Semaphore — limit how many threads access a resource at once. Today — the three core synchronizers and when each fits.

Episode Forty-Four. Synchronizers. CountDownLatch initializes with a count — typically the number of workers. Each worker calls countDown when finished — the latch decrements. await blocks until the count reaches zero — then all waiters proceed.

One-shot — cannot reset the count after it reaches zero. Classic pattern — main thread waits for parallel startup or shutdown. Example — wait for N services to finish initialization before accepting traffic.

CyclicBarrier sets a party count — the number of threads that must arrive. Each thread calls await — the barrier releases when all parties arrive. Reusable — after release, the barrier resets for the next cycle.

Optional barrier action runs once when the last thread arrives. Use for phased parallel computation — each phase ends at the barrier. BrokenBarrierException if a waiting thread is interrupted or times out.

Semaphore maintains a set of permits — acquire takes one, release returns one. new Semaphore of N allows up to N concurrent accessors. acquire blocks when no permits remain — release wakes a waiter.

tryAcquire with timeout avoids indefinite blocking. Binary semaphore with one permit acts like a mutex — but not reentrant. Use for connection pools, rate limiting, and bounded resource access.

Choosing the right synchronizer. CountDownLatch — wait for a fixed number of events — one direction. CyclicBarrier — threads meet repeatedly at the same point. Semaphore — cap concurrent access to a limited resource.

Phaser offers flexible phase-based coordination — advanced alternative. Exchanger swaps objects between two threads at a rendezvous point. When to use each synchronizer. Service startup gate — CountDownLatch until all workers ready.

Parallel matrix phases — CyclicBarrier between compute steps. Database connection cap — Semaphore with pool size permits. Fork-join style shutdown — latch counts completed tasks. When not — simple flag — volatile or AtomicBoolean may suffice.

Three common mistakes. One — reusing a CountDownLatch after count hits zero — it is one-shot. Two — wrong party count on CyclicBarrier — threads hang forever. Three — Semaphore acquire without matching release — permits leak.

Also — calling await on the only thread that should countDown. Synchronizers coordinate timing — they do not protect mutable state alone. Interview question — CountDownLatch versus CyclicBarrier?

CountDownLatch — one or more threads wait for others to finish events. Count is decremented — cannot reset after reaching zero. CyclicBarrier — threads rendezvous; all must arrive before any proceed.

Barrier resets and is reusable for the next cycle. Semaphore limits concurrent access — different problem entirely. Synchronizers coordinate arrival. What about passing work between threads?

Episode Forty-Five — BlockingQueue and Producer-Consumer. Bounded queues, backpressure, and the classic pattern. See you there.
