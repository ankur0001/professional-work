# Episode 48 — ThreadLocal

| Field | Value |
|---|---|
| Episode | 48 |
| Title | ThreadLocal |
| Catalog handbook column | 48 |
| Narration source script | `make_episode_48.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Forty-Seven split work across a ForkJoinPool.
2. Each thread needs its own context — request ID, formatter, database connection.
3. Passing context through every method signature gets noisy fast.
4. ThreadLocal gives each thread a private copy of a variable.
5. SimpleLocal.get on thread A never sees thread B value.
6. Today — ThreadLocal, inheritance, common patterns, and leak traps.

### Scene `title` (renderer: `title`)

1. Episode Forty-Eight.
2. ThreadLocal — Per-Thread State.

### Scene `per_thread_state` (renderer: `per_thread_state`)

1. ThreadLocal of T stores a value per calling thread.
2. Internally a map from Thread to T — invisible to your code.
3. set assigns the value for the current thread.
4. get returns the current thread value — or the initial value.
5. remove clears the entry for the current thread.
6. No synchronization needed for reads and writes on the same thread.

### Scene `get_set` (renderer: `get_set`)

1. Typical usage — static final ThreadLocal of DateFormat.
2. withInitial supplies a factory — lazy per-thread creation.
3. First get on a thread calls the supplier once.
4. Subsequent gets return the same instance for that thread.
5. DateFormat is not thread-safe — ThreadLocal avoids locking.
6. Same pattern for SimpleDateFormat, Random, StringBuilder scratch buffers.

### Scene `inheritance` (renderer: `inheritance`)

1. InheritableThreadLocal propagates values to child threads.
2. When you new Thread or pool creates a worker, child inherits parent value.
3. Useful for tracing context — correlation IDs across async handoffs.
4. Child gets a copy at creation time — not live updates from parent.
5. ThreadLocal does not inherit — child starts with initial value only.
6. Modern alternative — pass context explicitly or use scoped values in newer JDKs.

### Scene `common_patterns` (renderer: `common_patterns`)

1. Common ThreadLocal uses in production.
2. Per-request user or tenant context in servlet containers.
3. Security principal or locale without method parameter drilling.
4. Transaction or connection context in older frameworks.
5. Diagnostic MDC in logging — map diagnostic context per thread.
6. Keep the scope narrow — set at entry, remove at exit.

### Scene `leaks` (renderer: `leaks`)

1. ThreadLocal leak risk — the classic thread-pool trap.
2. Pool threads live forever — their ThreadLocal map never garbage-collected.
3. If the value references a large object graph, memory grows each request.
4. Always remove in a finally block when borrowing from a pool.
5. Weak references in some implementations help — but do not rely on them.
6. Prefer try-finally or try-with-resources wrappers around ThreadLocal scope.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — forgetting remove on pooled threads — slow memory leak.
3. Two — storing heavy mutable singletons — defeats per-thread isolation.
4. Three — assuming InheritableThreadLocal updates propagate — they do not.
5. Also — using ThreadLocal where explicit parameters are clearer.
6. ThreadLocal is convenience — not a substitute for good API design.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is ThreadLocal and when is it dangerous?
2. Per-thread variable — each thread has its own copy via get and set.
3. Use for non-thread-safe helpers — formatters, buffers, request context.
4. Danger — thread pools reuse threads — stale values and memory leaks.
5. Always remove after use on pooled threads.
6. Mention InheritableThreadLocal for child-thread propagation at creation.

### Scene `teaser` (renderer: `teaser`)

1. Per-thread state avoids sharing. What when threads block each other forever?
2. Episode Forty-Nine — Deadlocks.
3. Four conditions, detection, avoidance, and lock ordering.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **48** — *Atomic Classes*.
- **Series catalog mapping:** Episode 48 / catalog column `48` / published title *ThreadLocal*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Forty-Seven split work across a ForkJoinPool._
- **`title`** — starts from: _Episode Forty-Eight._
- **`per_thread_state`** — starts from: _ThreadLocal of T stores a value per calling thread._
- **`get_set`** — starts from: _Typical usage — static final ThreadLocal of DateFormat._
- **`inheritance`** — starts from: _InheritableThreadLocal propagates values to child threads._
- **`common_patterns`** — starts from: _Common ThreadLocal uses in production._
- **`leaks`** — starts from: _ThreadLocal leak risk — the classic thread-pool trap._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is ThreadLocal and when is it dangerous?_
- **`teaser`** — starts from: _Per-thread state avoids sharing. What when threads block each other forever?_
