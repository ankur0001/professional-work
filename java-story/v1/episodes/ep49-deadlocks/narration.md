# Episode 49 — Deadlocks

**Cut:** v1 (original)

## Transcript (from captions)

Episode Forty-Eight kept state private per thread. Shared resources still need locks — and locks can trap threads forever. Thread A holds lock one, waits for lock two. Thread B holds lock two, waits for lock one.

Neither can proceed — classic circular wait. Today — deadlock conditions, detection, avoidance, and lock ordering. Episode Forty-Nine. Deadlocks — Detection and Avoidance. Coffman conditions — all four must hold for a deadlock.

Mutual exclusion — at least one resource is non-sharable. Hold and wait — a thread holds a lock while waiting for another. No preemption — locks cannot be forcibly taken away. Circular wait — a cycle of threads each waiting on the next.

Break any one condition — and deadlocks cannot form. The dining philosophers — intuitive deadlock story. Five philosophers, five forks — need two forks to eat. Everyone picks left fork, then right — cycle forms.

In code — transfer between accounts locking in opposite order. Thread one locks account A then B. Thread two locks B then A — same circular pattern. Detection — find cycles in the wait-for graph.

Thread dump on JVM — jstack or kill minus three. Look for BLOCKED threads waiting on monitors held by each other. ThreadMXBean.findDeadlockedThreads returns deadlocked thread IDs. Detection is reactive — the system is already stuck.

Use in production monitoring — alert when deadlocks appear. Avoidance — design so deadlocks cannot happen. Lock ordering — always acquire locks in a global consistent order. Try-lock with timeout — back off and retry instead of waiting forever.

Lock fewer resources — coarser design or lock-free structures. Banker algorithm — theoretical resource allocation — rarely used in apps. Prevention beats detection — design locks in from the start.

Lock ordering in practice. Assign each lock a unique integer ID — always lock lower ID first. For account transfer — lock accounts by ascending hash or ID. ReentrantLock with tryLock and timeout — fail fast under contention.

synchronized blocks — same ordering rule applies. Document the order — code review catches violations early. Three common mistakes. One — nested locks in different orders across call paths.

Two — calling external code while holding a lock — hidden lock order. Three — ignoring try-lock timeouts — infinite BLOCKED in thread dumps. Also — fine-grained locks without a documented acquisition order.

Deadlocks are design bugs — not random runtime glitches. Interview question — what causes deadlock and how do you prevent it? Four Coffman conditions — mutual exclusion, hold-and-wait, no preemption, circular wait.

Prevention — consistent global lock ordering. Detection — thread dumps, ThreadMXBean, cycle in wait-for graph. tryLock with timeout — back off instead of blocking forever. Mention dining philosophers or account transfer example.

Platform threads block — and blocking under load gets expensive. Episode Fifty — Virtual Threads. Project Loom, pinning, and structured concurrency. See you there.
