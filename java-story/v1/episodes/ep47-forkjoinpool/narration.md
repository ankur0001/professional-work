# Episode 47 — ForkJoinPool

**Cut:** v1 (original)

## Transcript (from captions)

Episode Forty-Six showed CompletableFuture on the common pool. That pool is a ForkJoinPool — built for divide-and-conquer parallelism. Workers split big tasks into smaller pieces and join results.

Idle threads steal work from busy neighbors — work-stealing. RecursiveTask and RecursiveAction model fork-join decomposition. Today — ForkJoinPool, work-stealing, and when recursive parallelism pays off.

Episode Forty-Seven. ForkJoinPool and Work-Stealing. ForkJoinPool is an ExecutorService tuned for parallel decomposition. fork splits a task into subtasks — join waits for subtask results.

invoke runs a single task and blocks until it completes. submit returns a ForkJoinTask — use when you need a handle. Pool size defaults to available processors — tune for your workload.

Think tree-shaped computation — split down, merge up. Each worker maintains a deque of tasks — LIFO for its own work. When a worker runs dry, it steals from another worker deque — FIFO end.

Stealing balances load without a central coordinator bottleneck. Fine-grained tasks keep workers busy — coarse tasks leave threads idle. Work-stealing shines when task sizes are uneven or unpredictable.

Too many tiny tasks add overhead — batch until splits are worthwhile. RecursiveTask of V extends ForkJoinTask — compute returns a value. Override compute — fork children, join them, combine results.

Example — parallel sum of a large array by halving ranges. fork enqueues a subtask on the current pool. join blocks the current worker until the child completes. Use RecursiveTask when the result is a computed value.

RecursiveAction extends ForkJoinTask of Void — side effects only. Override compute — fork subtasks, join, no return value. Example — parallel forEach over a tree or matrix in place.

Same fork-join pattern — split work, wait for children. Choose RecursiveAction when you mutate shared structures carefully. Or when each leaf performs independent I/O or logging. When ForkJoinPool fits.

CPU-bound divide-and-conquer — mergesort, matrix multiply, tree walks. Parallel streams use the common pool under the hood. Recursive decomposition with cheap merge steps. When not — many blocking I/O tasks — use a cached thread pool.

When not — tiny uniform tasks — overhead beats parallelism. Three common mistakes. One — blocking inside compute — pins a worker and kills stealing. Two — shared mutable state without coordination — data races.

Three — forking too deep — millions of tasks overwhelm the pool. Also — using commonPool for blocking work — starves parallel streams. Size tasks so fork overhead stays small relative to real work.

Interview question — how does work-stealing work? Each thread has a deque — processes own tasks LIFO. Idle threads steal from the opposite end — FIFO — of another deque. Balances load without a global queue lock on every operation.

RecursiveTask returns a value — RecursiveAction is void side effects. Mention parallel streams and CompletableFuture common pool. Pools share threads across tasks. What about per-thread state?

Episode Forty-Eight — ThreadLocal. Per-thread variables, inheritance, and leak hazards. See you there.
