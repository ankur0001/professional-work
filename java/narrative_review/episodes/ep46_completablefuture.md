# Episode 46 — CompletableFuture

| Field | Value |
|---|---|
| Episode | 46 |
| Title | CompletableFuture |
| Catalog handbook column | 46 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`Future` gave us one result with a timed get. Real services often need a pipeline: load something, transform it, combine it with another call, handle failure, enforce a timeout, then save. Blocking on each `get` in sequence works and throws away concurrency. Nesting callbacks by hand works and becomes unreadable. So the question becomes: how do we compose asynchronous work as a graph of stages?

`CompletableFuture` is Java's standard answer for that composition.

```java
CompletableFuture.supplyAsync(this::load)
    .thenApply(this::transform)
    .orTimeout(1, TimeUnit.SECONDS)
    .thenAccept(this::save);
```

Walk the graph. `supplyAsync` starts `load` on an async pool and yields a future of its result. `thenApply` maps the value through `transform` when load completes. `orTimeout` fails the stage if the pipeline takes too long. `thenAccept` consumes the final value in `save`. The code reads top to bottom like a happy-path story, while the machinery runs asynchronously. That readability is why the type earned its place.

`thenApply` versus `thenCompose` is the composition subtlety interviews love. `thenApply` maps a value to another value. `thenCompose` maps a value to another future and flattens the nesting — the async cousin of flatMap. If `transform` itself returns a `CompletableFuture`, `thenApply` gives you a future of a future; `thenCompose` keeps one layer. Choose the operator that matches the shape of the next step.

```java
.thenCompose(id -> loadDetailsAsync(id))
```

Error handling belongs in the graph. `exceptionally` recovers a value from a failure. `handle` sees success or failure together. Swallowing exceptions inside a stage without recovering or completing exceptionally is how pipelines die quietly. The same discipline from the exceptions episode applies: preserve causes, decide policy, do not erase failure.

Executor choice matters. `supplyAsync` without an executor uses the common Fork/Join pool. That pool is shared. Blocking on I/O inside common-pool stages can starve other async work on the JVM — including parallel streams. For blocking I/O, pass an executor sized for that workload. For CPU work, the common pool may be appropriate. The method signature makes the default easy; production makes the default consequential.

```java
CompletableFuture.supplyAsync(this::loadRemote, ioExecutor)
```

Timeouts and cancellation remain part of the story. `orTimeout` and `completeOnTimeout` define latency policy in the graph instead of hoping callers remember to wrap `get`. Cancellation still cooperates with interruptible work underneath. Composition does not remove the need for tasks that notice they should stop.

What if we use `thenApply` where `thenCompose` was needed, or block with `get` inside a common-pool stage to "keep it simple"?

Nested futures appear, or the common pool stalls. Both bugs look like "async is hard" when they are really operator mismatch and pool misuse. Pick operators for the data shape. Pick executors for the blocking shape.

`thenCombine` earns a mention once pipelines grow branches. You start two asynchronous loads, then combine their results when both complete. That is the graph thinking futures were missing: not only chains, but joins. Timeouts on the combined stage still matter; a slow sibling should not pin a request forever.

Debugging a composed future means reading the exception from the stage that failed and remembering which executor ran which lambda. Logging correlation ids inside stages helps. Silent `exceptionally` that returns null converts a loud failure into a null that explodes later — the same anti-pattern as swallowing checked exceptions, wearing async clothes.

What if the team bans `get` entirely inside services? That can be a healthy rule for request threads, forcing composition to stay asynchronous until the edge. At the edge — a test, a main method, a gateway that must return a value — timed `get` or `join` with policy still appears. Rules should target accidental blocking, not honesty about waiting.

Cancellation and timeouts should be tested, not assumed. A unit test that only checks happy-path `thenApply` will miss the stage that blocks the common pool. Inject a slow dependency and assert timeout behavior. Inject a failure and assert recovery. Async graphs fail in the branches people skip in demos.
`thenCombine` and sibling joins also need clear executor stories for each branch. Two blocking loads on the common pool are two chances to stall shared workers. Pass io executors into both supplies when the work is blocking.

Picture loading a user profile and a set of entitlements concurrently, then combining them into a view model with a one-second timeout on the join. `thenCombine` expresses the join; `orTimeout` expresses the budget; `exceptionally` maps failures to a safe fallback or an error type. The graph matches the product sentence. That alignment is the point of CompletableFuture.

Keep stages small and pure when you can: load, transform, save. Side effects in the middle of a graph make cancellation and retries harder. Composition is easiest when each stage has one job — the same method lesson from early episodes, resurfacing in async form.

Hold the checklist: operators match shapes (`thenApply` vs `thenCompose`); executors match blocking; timeouts sit on the graph; failures recover or surface with causes. Meet those four and CompletableFuture remains a clarity tool instead of a nesting maze.

 When in doubt, sketch the stage graph on paper before coding — boxes for loads, arrows for apply/compose/combine, notes for executors and timeouts. If the sketch is messy, the code will be messier.

So reconnect the chain. Single futures were not enough for pipelines. `CompletableFuture` composed stages with apply/compose/combine, error handlers, and timeouts. Executor choice protected the common pool. Misused operators and blocking stages showed the traps. The graph is the design.

Some workloads are not async I/O graphs — they are CPU-heavy divide-and-conquer over large arrays or trees. That shape has its own pool and its own recursion style.

Episode Forty-Seven: `ForkJoinPool`.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 46 (*CompletableFuture*).

Narration technique: pipeline situation → CompletableFuture graph → thenApply vs thenCompose → errors → executor choice → timeouts → mistakes → next natural problem (ForkJoin).
