# Episode 36 — Threads Intro

**Cut:** v1 (original)

## Transcript (from captions)

One CPU core can only do one thing at a time — unless you switch fast enough. Threads let a program do multiple tasks concurrently within one process. Download a file while updating the UI. Process requests while logging metrics.

Concurrency is about structure — parallelism is about simultaneous execution. Threads share memory — powerful, but dangerous without coordination. Today — the thread model in Java and how to start your first concurrent task.

Episode Thirty-Six. Threads Introduction — concurrency in Java. A Thread is a lightweight unit of execution inside a JVM process. The JVM maps Java threads to OS threads — one-to-one on most platforms.

Every Java program starts with a main thread — the one running main. Creating more threads lets work proceed on separate call stacks. Threads share the heap — instance fields are visible across threads.

Each thread has its own stack — local variables are thread-confined. Runnable is a functional interface — void run with no arguments. Pass a Runnable to a Thread constructor, then call start.

Callable is like Runnable but returns a value and can throw. ExecutorService is the modern way — submit tasks to a thread pool. Prefer Runnable lambdas over subclassing Thread directly.

Separate task logic from thread management. Thread states — NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED. NEW until start is called — then RUNNABLE when eligible to run.

BLOCKED waiting for a monitor lock. WAITING until notified. The scheduler decides which RUNNABLE thread runs on which core. You do not control scheduling — design for unpredictability.

Understanding states helps you debug stuck and starving threads. Never call run directly — that executes on the current thread. Call start to launch a new thread that invokes run. join waits for another thread to finish — useful for coordination.

sleep pauses the current thread for a duration — does not release locks. yield hints the scheduler to let other threads run — rarely needed. Start threads deliberately — unbounded thread creation exhausts memory.

Threads share the heap — all threads see the same object fields. Local variables live on each thread stack — no sharing by default. Mutable shared state without coordination causes race conditions.

Two threads reading and writing the same field — unpredictable results. Visibility matters — changes by one thread may not be seen by another. Shared memory is the reason synchronization exists — next episode.

Three common mistakes. One — calling run instead of start — no new thread created. Two — sharing mutable state without synchronization — race conditions. Three — spawning unlimited threads — one per request does not scale.

Also — assuming operations are atomic when they are not — count plus plus. Concurrency bugs are intermittent — design defensively from the start. Interview question — start versus run on a Thread?

start creates a new thread and schedules run on it. run called directly — executes synchronously on the caller thread. Mention Runnable, shared heap, and thread-local stacks. Note race conditions when sharing mutable state.

That answer opens the door to synchronization next episode. Threads share memory. Next — making that safe. Episode Thirty-Seven — Synchronization. synchronized, locks, and coordinating access to shared data.

See you there.
