# Episode 37 — Synchronization

**Cut:** v1 (original)

## Transcript (from captions)

Two threads update the same counter. You expect two — you might get one. Race conditions happen when shared mutable state is accessed without coordination. Synchronization is how Java makes critical sections safe.

One thread at a time — mutual exclusion on shared data. Locks, monitors, and the synchronized keyword — the first line of defense. Today — synchronized methods, blocks, and intrinsic locks.

Episode Thirty-Seven. Synchronization — safe access to shared data. A race condition — outcome depends on thread scheduling order. count plus plus is not atomic — read, increment, write — three steps.

Two threads interleave those steps — updates can be lost. The bug is intermittent — hardest kind to reproduce. You need mutual exclusion — only one thread in the critical section. Synchronization enforces that rule at the language level.

synchronized on a method locks the instance — or the Class object for static. Only one thread can execute that synchronized method at a time. Other threads block until the lock is released.

Simple and readable for small critical sections. The lock is automatically released when the method exits — even on exception. Use synchronized methods when the whole method is the critical section.

synchronized block — finer control over what is protected. synchronized on this — locks the current instance. synchronized on a dedicated lock object — often clearer intent. Protect only the few lines that touch shared state.

Smaller critical sections mean less contention — better throughput. Prefer blocks when only part of a method needs protection. Every Java object has an intrinsic lock — also called a monitor.

Entering synchronized acquires the monitor. Exiting releases it. Reentrant — the same thread can acquire a lock it already holds. wait and notify operate on the monitor — coordination beyond exclusion.

The JVM maps monitors to operating-system mutexes under the hood. Understand monitors — they underpin every synchronized construct. When to synchronize. Any read-modify-write on shared mutable fields.

Invariants that must hold while multiple fields are updated. Compound actions — check-then-act on shared state. When not — over-synchronizing everything kills performance. Synchronize the minimum — but synchronize what matters.

Three common mistakes. One — synchronizing on the wrong object — String literals or boxed integers. Two — holding locks while doing slow I/O — blocks every waiter. Three — nested locks on different objects — classic deadlock setup.

Also — assuming synchronized fixes visibility alone — see next episode. Lock only what you must — for as short as possible. Interview question — synchronized method versus synchronized block?

Both acquire an intrinsic lock on an object. Method form locks on this or the Class. Block form lets you choose the lock. Blocks allow finer granularity — protect fewer lines. Mention reentrancy and that locks release on exception.

That answer shows you understand monitors, not just keywords. Locks prevent races. But can every thread see your writes? Episode Thirty-Eight — Memory Visibility. volatile, happens-before, and the Java Memory Model.

See you there.
