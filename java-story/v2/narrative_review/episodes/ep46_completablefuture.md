# Episode 46 — CompletableFuture

| Field | Value |
|---|---|
| Episode | 46 |
| Title | CompletableFuture |
| Catalog handbook column | 46 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`Future` gave us one result with a timed get. Real services often need a pipeline: load something, transform it, combine it with another call, handle failure, enforce a timeout, then save. Blocking on each `get` in sequence works and throws away concurrency. Nesting callbacks by hand works and becomes unreadable. How do we compose asynchronous work as a graph of stages?

`CompletableFuture` is Java's standard answer for that composition.

```java
CompletableFuture.supplyAsync(this::load)
    .thenApply(this::transform)
    .orTimeout(1, TimeUnit.SECONDS)
    .thenAccept(this::save);
```

`supplyAsync` starts `load` on an async pool and yields a future of its result. `thenApply` maps the value through `transform` when load completes. `orTimeout` fails the stage if the pipeline takes too long. `thenAccept` consumes the final value in `save`. The code reads top to bottom like a happy-path story, while the machinery runs asynchronously.

`thenApply` versus `thenCompose` is the composition subtlety interviews love. `thenApply` maps a value to another value. `thenCompose` maps a value to another future and flattens the nesting — the async cousin of flatMap. If `transform` itself returns a `CompletableFuture`, `thenApply` gives you a future of a future; `thenCompose` keeps one layer:

```java
.thenCompose(id -> loadDetailsAsync(id))
```

Error handling belongs in the graph. `exceptionally` recovers a value from a failure. `handle` sees success or failure together. Swallowing exceptions inside a stage without recovering or completing exceptionally is how pipelines die quietly. Preserve causes, decide policy, do not erase failure.

Executor choice matters. `supplyAsync` without an executor uses the common Fork/Join pool. That pool is shared. Blocking on I/O inside common-pool stages can starve other async work on the JVM — including parallel streams. For blocking I/O, pass an executor sized for that workload:

```java
CompletableFuture.supplyAsync(this::loadRemote, ioExecutor)
```

Timeouts and cancellation remain part of the story. `orTimeout` and `completeOnTimeout` define latency policy in the graph instead of hoping callers remember to wrap `get`. Cancellation still cooperates with interruptible work underneath.

What if we use `thenApply` where `thenCompose` was needed, or block with `get` inside a common-pool stage to "keep it simple"? Nested futures appear, or the common pool stalls. Both bugs look like "async is hard" when they are really operator mismatch and pool misuse.

`thenCombine` earns a mention once pipelines grow branches. You start two asynchronous loads, then combine their results when both complete. That is the graph thinking single futures were missing: not only chains, but joins. Timeouts on the combined stage still matter; a slow sibling should not pin a request forever.

Debugging a composed future means reading the exception from the stage that failed and remembering which executor ran which lambda. Silent `exceptionally` that returns null converts a loud failure into a null that explodes later — the same anti-pattern as swallowing checked exceptions, wearing async clothes.

Picture loading a user profile and a set of entitlements concurrently, then combining them into a view model with a one-second timeout on the join. `thenCombine` expresses the join; `orTimeout` expresses the budget; `exceptionally` maps failures to a safe fallback or an error type. The graph matches the product sentence.

Keep stages small and pure when you can: load, transform, save. Side effects in the middle of a graph make cancellation and retries harder. Composition is easiest when each stage has one job.

Hold the checklist: operators match shapes (`thenApply` vs `thenCompose`); executors match blocking; timeouts sit on the graph; failures recover or surface with causes.

Some workloads are not async I/O graphs — they are CPU-heavy divide-and-conquer over large arrays or trees. That shape has its own pool and its own recursion style.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 46 (*CompletableFuture*).

Narration technique: pipeline situation → CompletableFuture graph → thenApply vs thenCompose → errors → executor choice → next natural problem (ForkJoin).
