# Episode 47 — ForkJoinPool

| Field | Value |
|---|---|
| Episode | 47 |
| Title | ForkJoinPool |
| Catalog handbook column | 47 |
| Narration source script | `make_episode_47.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Forty-Six showed CompletableFuture on the common pool.
2. That pool is a ForkJoinPool — built for divide-and-conquer parallelism.
3. Workers split big tasks into smaller pieces and join results.
4. Idle threads steal work from busy neighbors — work-stealing.
5. RecursiveTask and RecursiveAction model fork-join decomposition.
6. Today — ForkJoinPool, work-stealing, and when recursive parallelism pays off.

### Scene `title` (renderer: `title`)

1. Episode Forty-Seven.
2. ForkJoinPool and Work-Stealing.

### Scene `fork_join_basics` (renderer: `fork_join_basics`)

1. ForkJoinPool is an ExecutorService tuned for parallel decomposition.
2. fork splits a task into subtasks — join waits for subtask results.
3. invoke runs a single task and blocks until it completes.
4. submit returns a ForkJoinTask — use when you need a handle.
5. Pool size defaults to available processors — tune for your workload.
6. Think tree-shaped computation — split down, merge up.

### Scene `work_stealing` (renderer: `work_stealing`)

1. Each worker maintains a deque of tasks — LIFO for its own work.
2. When a worker runs dry, it steals from another worker deque — FIFO end.
3. Stealing balances load without a central coordinator bottleneck.
4. Fine-grained tasks keep workers busy — coarse tasks leave threads idle.
5. Work-stealing shines when task sizes are uneven or unpredictable.
6. Too many tiny tasks add overhead — batch until splits are worthwhile.

### Scene `recursive_task` (renderer: `recursive_task`)

1. RecursiveTask of V extends ForkJoinTask — compute returns a value.
2. Override compute — fork children, join them, combine results.
3. Example — parallel sum of a large array by halving ranges.
4. fork enqueues a subtask on the current pool.
5. join blocks the current worker until the child completes.
6. Use RecursiveTask when the result is a computed value.

### Scene `recursive_action` (renderer: `recursive_action`)

1. RecursiveAction extends ForkJoinTask of Void — side effects only.
2. Override compute — fork subtasks, join, no return value.
3. Example — parallel forEach over a tree or matrix in place.
4. Same fork-join pattern — split work, wait for children.
5. Choose RecursiveAction when you mutate shared structures carefully.
6. Or when each leaf performs independent I/O or logging.

### Scene `when_to_use` (renderer: `when_to_use`)

1. When ForkJoinPool fits.
2. CPU-bound divide-and-conquer — mergesort, matrix multiply, tree walks.
3. Parallel streams use the common pool under the hood.
4. Recursive decomposition with cheap merge steps.
5. When not — many blocking I/O tasks — use a cached thread pool.
6. When not — tiny uniform tasks — overhead beats parallelism.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — blocking inside compute — pins a worker and kills stealing.
3. Two — shared mutable state without coordination — data races.
4. Three — forking too deep — millions of tasks overwhelm the pool.
5. Also — using commonPool for blocking work — starves parallel streams.
6. Size tasks so fork overhead stays small relative to real work.

### Scene `interview` (renderer: `interview`)

1. Interview question — how does work-stealing work?
2. Each thread has a deque — processes own tasks LIFO.
3. Idle threads steal from the opposite end — FIFO — of another deque.
4. Balances load without a global queue lock on every operation.
5. RecursiveTask returns a value — RecursiveAction is void side effects.
6. Mention parallel streams and CompletableFuture common pool.

### Scene `teaser` (renderer: `teaser`)

1. Pools share threads across tasks. What about per-thread state?
2. Episode Forty-Eight — ThreadLocal.
3. Per-thread variables, inheritance, and leak hazards.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **47** — *ForkJoinPool*.
- **Series catalog:** Episode 47 ↔ handbook lesson 47 — *ForkJoinPool*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Forty-Six showed CompletableFuture on the common pool._
- **`title`** — starts from: _Episode Forty-Seven._
- **`fork_join_basics`** — starts from: _ForkJoinPool is an ExecutorService tuned for parallel decomposition._
- **`work_stealing`** — starts from: _Each worker maintains a deque of tasks — LIFO for its own work._
- **`recursive_task`** — starts from: _RecursiveTask of V extends ForkJoinTask — compute returns a value._
- **`recursive_action`** — starts from: _RecursiveAction extends ForkJoinTask of Void — side effects only._
- **`when_to_use`** — starts from: _When ForkJoinPool fits._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how does work-stealing work?_
- **`teaser`** — starts from: _Pools share threads across tasks. What about per-thread state?_
