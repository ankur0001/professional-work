# Episode 41 — Callable and Future

**Cut:** v1 (original)

## Transcript (from captions)

Runnable says do this. But what if the task produces a result? Callable is Runnable with a return value — and checked exceptions. Submit a Callable, get a Future — a handle to the eventual result.

Block on get, cancel if needed, check if done. CompletableFuture takes it further — compose async pipelines. Today — Callable, Future, and an intro to CompletableFuture. Episode Forty-One.

Callable, Future, and CompletableFuture. Callable of T is a functional interface — T call throws Exception. Like Runnable but returns a value and can throw checked exceptions. Submit to an ExecutorService — the pool runs call on a worker thread.

Use lambdas — Callable task equals open paren close paren arrow compute. Callable fits any task that produces a result — fetch, parse, calculate. Separate the computation from where it runs.

Future of T represents a pending result of an asynchronous computation. get blocks until the result is ready — optionally with a timeout. get with timeout — wait up to a duration, then throw TimeoutException.

isDone checks completion without blocking. cancel attempts to stop. cancel with mayInterruptIfRunning — true interrupts a running task. Always handle ExecutionException — the real cause is in getCause.

CompletableFuture of T — a Future you can compose and complete manually. supplyAsync runs a supplier on the default ForkJoinPool. thenApply transforms the result. thenCompose chains dependent futures.

allOf and anyOf combine multiple futures. exceptionally handles failures in the pipeline. CompletableFuture is the modern way to build async workflows in Java. Runnable versus Callable versus Future.

Runnable — void, no checked exceptions, fire-and-forget. Callable — returns T, throws Exception, submitted for a Future. Future — read-only view of a pending result. CompletableFuture — writable, composable, chainable.

Choose based on whether you need a result and how you compose tasks. When to use Callable and Future. Parallel API calls — submit many, collect results with get. CPU work off the request thread — return Future to caller.

Batch processing where each unit produces output. CompletableFuture when you need chaining — thenApply, thenCombine. When not — simple fire-and-forget — Runnable and execute suffice.

Three common mistakes. One — calling get on the event loop thread — blocks the UI. Two — ignoring ExecutionException — swallowing the real error. Three — not setting timeouts on get — waits forever on hung tasks.

Also — chaining blocking gets instead of thenCompose. Async code needs async thinking — do not block what should stay free. Interview question — Callable versus Runnable? Runnable returns void, no checked exceptions.

Callable returns a value and can throw checked exceptions. Submit Callable to ExecutorService — receive Future of T. Future get blocks for result — use timeout in production. Mention CompletableFuture for composable async pipelines.

Tasks and futures coordinate work. What about shared data structures? Episode Forty-Two — Concurrent Collections. ConcurrentHashMap, CopyOnWriteArrayList, and thread-safe queues. See you there.
