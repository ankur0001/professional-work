# Episode 48 — ThreadLocal

**Cut:** v1 (original)

## Transcript (from captions)

Episode Forty-Seven split work across a ForkJoinPool. Each thread needs its own context — request ID, formatter, database connection. Passing context through every method signature gets noisy fast.

ThreadLocal gives each thread a private copy of a variable. SimpleLocal.get on thread A never sees thread B value. Today — ThreadLocal, inheritance, common patterns, and leak traps.

Episode Forty-Eight. ThreadLocal — Per-Thread State. ThreadLocal of T stores a value per calling thread. Internally a map from Thread to T — invisible to your code. set assigns the value for the current thread.

get returns the current thread value — or the initial value. remove clears the entry for the current thread. No synchronization needed for reads and writes on the same thread. Typical usage — static final ThreadLocal of DateFormat.

withInitial supplies a factory — lazy per-thread creation. First get on a thread calls the supplier once. Subsequent gets return the same instance for that thread. DateFormat is not thread-safe — ThreadLocal avoids locking.

Same pattern for SimpleDateFormat, Random, StringBuilder scratch buffers. InheritableThreadLocal propagates values to child threads. When you new Thread or pool creates a worker, child inherits parent value.

Useful for tracing context — correlation IDs across async handoffs. Child gets a copy at creation time — not live updates from parent. ThreadLocal does not inherit — child starts with initial value only.

Modern alternative — pass context explicitly or use scoped values in newer JDKs. Common ThreadLocal uses in production. Per-request user or tenant context in servlet containers. Security principal or locale without method parameter drilling.

Transaction or connection context in older frameworks. Diagnostic MDC in logging — map diagnostic context per thread. Keep the scope narrow — set at entry, remove at exit. ThreadLocal leak risk — the classic thread-pool trap.

Pool threads live forever — their ThreadLocal map never garbage-collected. If the value references a large object graph, memory grows each request. Always remove in a finally block when borrowing from a pool.

Weak references in some implementations help — but do not rely on them. Prefer try-finally or try-with-resources wrappers around ThreadLocal scope. Three common mistakes. One — forgetting remove on pooled threads — slow memory leak.

Two — storing heavy mutable singletons — defeats per-thread isolation. Three — assuming InheritableThreadLocal updates propagate — they do not. Also — using ThreadLocal where explicit parameters are clearer.

ThreadLocal is convenience — not a substitute for good API design. Interview question — what is ThreadLocal and when is it dangerous? Per-thread variable — each thread has its own copy via get and set.

Use for non-thread-safe helpers — formatters, buffers, request context. Danger — thread pools reuse threads — stale values and memory leaks. Always remove after use on pooled threads.

Mention InheritableThreadLocal for child-thread propagation at creation. Per-thread state avoids sharing. What when threads block each other forever? Episode Forty-Nine — Deadlocks.

Four conditions, detection, avoidance, and lock ordering. See you there.
