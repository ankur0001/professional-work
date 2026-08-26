# Episode 40 — ExecutorService

| Field | Value |
|---|---|
| Episode | 40 |
| Title | ExecutorService |
| Catalog handbook column | 40 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We can start threads. We can synchronize them. We can lock with more control when we must. None of that excuses inventing a new thread for every piece of work that arrives.

Picture a burst of a thousand short tasks. Spawning a thousand platform threads can exhaust memory and scheduling capacity before the tasks finish doing anything useful. Unbounded thread creation is not a strategy. It is a load test you accidentally run in production. So the natural question is: how do we reuse workers and bound concurrency on purpose?

`ExecutorService` is Java's standard answer. Thread pools bound concurrency, reuse threads, and give you a place to attach queueing and rejection policy. Submit work; do not babysit thread lifecycles by hand for every task.

```java
try (var exec = Executors.newFixedThreadPool(4)) {
    exec.submit(() -> task());
}
```

Walk the shape. `newFixedThreadPool(4)` creates a pool with four worker threads. `submit` hands a task to that pool. Using try-with-resources (on modern executor APIs that are `AutoCloseable`) ties pool shutdown to scope exit so the pool does not outlive the method by accident. Even when you manage shutdown manually, the idea is the same: pools have a lifecycle, and ignoring that lifecycle leaks threads.

Pool flavors exist because workloads differ. A fixed pool caps the number of concurrent workers. A cached pool creates threads as needed and reuses idle ones — convenient, and dangerous if an unbounded burst arrives with no other limit. A scheduled pool runs delayed or periodic work. Choose the shape that matches the workload, not the factory method you memorized first.

Shutdown has two common verbs. `shutdown` lets submitted tasks finish and refuses new ones. `shutdownNow` attempts to cancel in-flight work and drains the queue, typically by interrupting workers. Neither is "the rude one" or "the polite one" in the abstract — they are different policies. Always have a failure and stop story: how does this pool die when the application stops, and what happens to tasks still waiting?

Bounded queues and rejection policies are how pools survive overload. If the queue can grow forever, you have not bounded anything meaningful — you have moved the OOM from threads to queue memory. When the queue is full and workers are busy, the rejection policy decides whether to run the task on the caller, discard it, abort with an exception, or follow another rule. Ignoring `RejectedExecutionException` is how overload becomes a mysterious lost task.

Virtual threads will later change some defaults for blocking workloads — cheap threads make "one task, one thread" sensible again in many servers. That does not erase pools for every case, especially CPU-bound work that still needs bounding. Hold the curiosity; we will get there. Today the lesson is older and still vital: manage concurrency as a resource.

Common mistakes are predictable. Using a cached pool for unbounded bursty work without another limit. Never shutting down pools in long-running processes. Treating rejection as an impossible edge instead of an expected pressure valve.

So reconnect the chain. Unbounded `new Thread` failed under burst. Executors reused workers and capped concurrency. Shutdown verbs and rejection policies made lifecycle and overload explicit. Different pool types matched different jobs.

Submitting work raises a new hunger immediately: many tasks produce a result, may fail with a checked exception, and must not be waited on forever. `Runnable` is not enough for that contract.

Episode Forty-One introduces `Callable` and `Future`.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 40 (*ExecutorService*).

Narration technique: burst-of-tasks situation → pools as answer → fixed pool walkthrough → pool flavors → shutdown → bounded queue/rejection → virtual-thread foreshadow → next natural problem (Callable/Future).
