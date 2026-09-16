# Episode 40 — ExecutorService

**Cut:** v1 (original)

## Transcript (from captions)

Creating a new Thread per request does not scale — creation is expensive. Thread pools reuse a fixed set of worker threads for many tasks. ExecutorService is the standard abstraction for submitting work.

Submit a Runnable, get back control — the pool handles scheduling. Shutdown gracefully — in-flight tasks deserve a clean finish. Today — ExecutorService, thread pools, and task submission.

Episode Forty. ExecutorService and Thread Pools. ExecutorService decouples task submission from thread management. You describe what to run — the executor decides how and when. Factories in Executors create common pool configurations.

newFixedThreadPool — bounded pool, unbounded queue. newCachedThreadPool — grows on demand, reclaims idle threads. Prefer factory methods — they encode sensible defaults. A thread pool maintains a queue of tasks and a set of worker threads.

Workers pull tasks from the queue and execute them. Bounded pools cap resource usage — critical for server applications. Too few threads — tasks wait. Too many — context-switch overhead.

Size pools based on workload — CPU-bound versus I/O-bound. Thread pools turn unbounded thread creation into managed concurrency. submit takes a Runnable or Callable and returns a Future.

execute is fire-and-forget — no result handle. shutdown stops accepting new tasks — existing tasks still run. shutdownNow attempts to cancel pending and interrupt running tasks. awaitTermination waits for the pool to finish — with optional timeout.

Always shut down executors — leaked pools keep JVM threads alive. Common executor types. Fixed thread pool — predictable concurrency for steady workloads. Cached thread pool — bursty short tasks, grows and shrinks.

Single-thread executor — sequential execution, ordered results. ScheduledThreadPoolExecutor — delayed and periodic tasks. ForkJoinPool — work-stealing for divide-and-conquer parallelism.

When to use thread pools. Server request handling — bound concurrent work. Background processing — logging, indexing, notifications. Batch jobs with many independent units of work. When not — trivial one-off tasks — maybe just start one thread.

Always size and monitor — blind defaults cause outages. Three common mistakes. One — never calling shutdown — threads leak, JVM hangs on exit. Two — unbounded queue with fixed pool — memory grows forever.

Three — submitting blocking tasks to a small CPU-bound pool. Also — ignoring rejected execution when the queue is full. Treat the executor as a managed resource — lifecycle matters.

Interview question — why use ExecutorService over raw Thread? Decouples task logic from thread lifecycle management. Reuses threads — avoids creation overhead per task. Provides bounded concurrency — protects system resources.

Returns Future for results — supports graceful shutdown. Mention shutdown and awaitTermination in production code. Pools run tasks. What about tasks that return values? Episode Forty-One — Callable and Future.

Typed results, blocking get, and CompletableFuture intro. See you there.
