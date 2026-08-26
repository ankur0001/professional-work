# Episode 41 — Callable and Future

| Field | Value |
|---|---|
| Episode | 41 |
| Title | Callable and Future |
| Catalog handbook column | 41 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

ExecutorService taught us to submit work to a pool instead of inventing threads by hand. That solves concurrency budgeting. It does not yet answer a hunger that appears the moment the task computes something you need: how do I get a result back, wait with a timeout, and cancel when the caller no longer cares?

`Runnable` returns nothing and cannot throw checked exceptions. Many real tasks need both. That is why `Callable` exists — and why `Future` is the handle you hold while the pool does the work.

```java
ExecutorService exec = Executors.newFixedThreadPool(2);
Future<Integer> f = exec.submit(() -> compute());
int v = f.get(1, TimeUnit.SECONDS);
```

`submit` accepts a `Callable` that returns an `Integer`. The method returns a `Future` immediately; the computation may still be running. `get(1, TimeUnit.SECONDS)` blocks for at most one second. If the task finishes in time, you receive the value. If it does not, you get a timeout instead of hanging forever. Always prefer timeouts on `get` in server code. A bare `get()` with no limit is how one stuck worker becomes a stuck request thread — and then a stuck thread pool.

Cancellation is cooperative, not magical:

```java
boolean requested = f.cancel(true);
```

`cancel(true)` asks the pool to interrupt the running task if it has already started, or to prevent it from starting if it is still queued. "Cooperative" means the task must notice the interrupt — by exiting a blocking call that throws `InterruptedException`, or by checking interrupted status in a loop. Assuming cancel instantly stops arbitrary CPU work is a common production disappointment. Cancellation is a request. Well-behaved tasks honor it; stubborn tight loops ignore it.

`Callable` versus `Runnable` is the short form of today's design choice. `Callable` returns a value and may throw checked exceptions wrapped by the future machinery. `Runnable` is for fire-and-forget side effects. If you find yourself stuffing results into a shared mutable field from a `Runnable`, you are reinventing `Future` badly.

Exceptions from the task surface when you call `get`. They arrive wrapped — typically as `ExecutionException` with the original cause inside. Your wait site is also your failure-handling site. Ignoring the cause and only logging "execution failed" throws away the forensic trail we fought to keep in the exceptions episode.

What if we skip futures and only use shared variables?

```java
AtomicReference<Integer> box = new AtomicReference<>();
exec.submit(() -> box.set(compute()));
// now what — spin? sleep? guess?
```

You still need a completion protocol. `Future` is that protocol with timeouts and cancellation already designed.

A practical pattern in services is "submit, then wait with timeout, then cancel on timeout." The timeout protects the caller. The cancel attempt protects the pool from continuing useless work. Neither alone is a complete story; together they are the minimum polite concurrent call.

Picture a payment authorization callable that hits a slow bank link. The request thread waits with a two-second `get`. On timeout it cancels and returns "try again." On success it continues the order. On `ExecutionException` it unwraps the cause and maps it to an API error. That three-branch wait site is the everyday craft — not the lambda syntax, but the policy around waiting.

Composition pressure appears even with one future. You might wish the transformation happened asynchronously too. That wish is how teams graduate to `CompletableFuture`. For now, keep the contract crisp: submit returns a handle; the handle offers timed wait, cancel, and exception delivery.

What if every task is fire-and-forget logging? Then `Runnable` and `execute` may be enough. Futures are for results and failure delivery. Matching the tool to the need keeps APIs honest.

Always shut down the executor with a defined owner. Futures do not excuse leaked executors. The result handle and the worker pool are partners; lifecycle belongs to the pool's owner, while the future belongs to the caller waiting for a value. Prefer timeouts at every boundary where a peer can stall.

Once many threads share maps and queues, another question appears: can the collections themselves participate in thread safety, or must every access sit inside our own locks?

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 41 (*Callable and Future*).

Narration technique: need-a-result situation → Callable/Future → timed get → cooperative cancel → vs Runnable → exception wrapping → next natural problem (concurrent collections).
