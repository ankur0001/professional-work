# Episode 41 — Callable and Future

| Field | Value |
|---|---|
| Episode | 41 |
| Title | Callable and Future |
| Catalog handbook column | 41 |
| Narration source script | `make_episode_41.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Runnable says do this. But what if the task produces a result?
2. Callable is Runnable with a return value — and checked exceptions.
3. Submit a Callable, get a Future — a handle to the eventual result.
4. Block on get, cancel if needed, check if done.
5. CompletableFuture takes it further — compose async pipelines.
6. Today — Callable, Future, and an intro to CompletableFuture.

### Scene `title` (renderer: `title`)

1. Episode Forty-One.
2. Callable, Future, and CompletableFuture.

### Scene `callable` (renderer: `callable`)

1. Callable of T is a functional interface — T call throws Exception.
2. Like Runnable but returns a value and can throw checked exceptions.
3. Submit to an ExecutorService — the pool runs call on a worker thread.
4. Use lambdas — Callable task equals open paren close paren arrow compute.
5. Callable fits any task that produces a result — fetch, parse, calculate.
6. Separate the computation from where it runs.

### Scene `future` (renderer: `future`)

1. Future of T represents a pending result of an asynchronous computation.
2. get blocks until the result is ready — optionally with a timeout.
3. get with timeout — wait up to a duration, then throw TimeoutException.
4. isDone checks completion without blocking. cancel attempts to stop.
5. cancel with mayInterruptIfRunning — true interrupts a running task.
6. Always handle ExecutionException — the real cause is in getCause.

### Scene `completable` (renderer: `completable`)

1. CompletableFuture of T — a Future you can compose and complete manually.
2. supplyAsync runs a supplier on the default ForkJoinPool.
3. thenApply transforms the result. thenCompose chains dependent futures.
4. allOf and anyOf combine multiple futures.
5. exceptionally handles failures in the pipeline.
6. CompletableFuture is the modern way to build async workflows in Java.

### Scene `vs_runnable` (renderer: `vs_runnable`)

1. Runnable versus Callable versus Future.
2. Runnable — void, no checked exceptions, fire-and-forget.
3. Callable — returns T, throws Exception, submitted for a Future.
4. Future — read-only view of a pending result.
5. CompletableFuture — writable, composable, chainable.
6. Choose based on whether you need a result and how you compose tasks.

### Scene `when_async` (renderer: `when_async`)

1. When to use Callable and Future.
2. Parallel API calls — submit many, collect results with get.
3. CPU work off the request thread — return Future to caller.
4. Batch processing where each unit produces output.
5. CompletableFuture when you need chaining — thenApply, thenCombine.
6. When not — simple fire-and-forget — Runnable and execute suffice.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — calling get on the event loop thread — blocks the UI.
3. Two — ignoring ExecutionException — swallowing the real error.
4. Three — not setting timeouts on get — waits forever on hung tasks.
5. Also — chaining blocking gets instead of thenCompose.
6. Async code needs async thinking — do not block what should stay free.

### Scene `interview` (renderer: `interview`)

1. Interview question — Callable versus Runnable?
2. Runnable returns void, no checked exceptions.
3. Callable returns a value and can throw checked exceptions.
4. Submit Callable to ExecutorService — receive Future of T.
5. Future get blocks for result — use timeout in production.
6. Mention CompletableFuture for composable async pipelines.

### Scene `teaser` (renderer: `teaser`)

1. Tasks and futures coordinate work. What about shared data structures?
2. Episode Forty-Two — Concurrent Collections.
3. ConcurrentHashMap, CopyOnWriteArrayList, and thread-safe queues.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **41** — *Callable and Future*.
- **Series catalog:** Episode 41 ↔ handbook lesson 41 — *Callable and Future*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Runnable says do this. But what if the task produces a result?_
- **`title`** — starts from: _Episode Forty-One._
- **`callable`** — starts from: _Callable of T is a functional interface — T call throws Exception._
- **`future`** — starts from: _Future of T represents a pending result of an asynchronous computation._
- **`completable`** — starts from: _CompletableFuture of T — a Future you can compose and complete manually._
- **`vs_runnable`** — starts from: _Runnable versus Callable versus Future._
- **`when_async`** — starts from: _When to use Callable and Future._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Callable versus Runnable?_
- **`teaser`** — starts from: _Tasks and futures coordinate work. What about shared data structures?_
