# Episode 40 — ExecutorService

| Field | Value |
|---|---|
| Episode | 40 |
| Title | ExecutorService |
| Catalog handbook column | 40 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We can start threads. We can synchronize them. We can lock with more control when we must. None of that excuses inventing a new thread for every piece of work that arrives at the door.

Picture a burst of a thousand short tasks — thumbnails, notifications, webhook deliveries. Spawning a thousand platform threads can exhaust memory and scheduling capacity before the tasks finish doing anything useful. Unbounded thread creation is not a strategy. It is a load test you accidentally run in production. How do we reuse workers and bound concurrency on purpose?

`ExecutorService` is Java's standard answer. Thread pools bound concurrency, reuse threads, and give you a place to attach queueing and rejection policy. Submit work; do not babysit thread lifecycles by hand for every task.

```java
try (var exec = Executors.newFixedThreadPool(4)) {
    exec.submit(() -> task());
    exec.submit(() -> anotherTask());
}
```

`newFixedThreadPool(4)` creates a pool with four worker threads. `submit` hands tasks to that pool. Using try-with-resources (on modern executor APIs that are `AutoCloseable`) ties pool shutdown to scope exit. Even when you manage shutdown manually in a long-running server, the idea is the same: pools have a lifecycle, and ignoring that lifecycle leaks threads for the life of the process.

Pool flavors exist because workloads differ. A fixed pool caps concurrent workers — good when you know how much parallelism the machine and the downstream dependency can absorb. A cached pool creates threads as needed and reuses idle ones — convenient for bursty work, and dangerous if an unbounded burst arrives with no other limit. A scheduled pool runs delayed or periodic work. Choose the shape that matches the workload, not the factory method you memorized first.

Shutdown has two common verbs. `shutdown` lets submitted tasks finish and refuses new ones. `shutdownNow` attempts to cancel in-flight work and drains the queue, typically by interrupting workers. Always have a stop story: how does this pool die when the application stops, and what happens to tasks still waiting? A pool that never shuts down is a quiet resource leak.

Bounded queues and rejection policies are how pools survive overload. If the queue can grow forever, you have moved the out-of-memory risk from threads to queue memory. When the queue is full and workers are busy, the rejection policy decides whether to run the task on the caller thread, discard it, or abort with an exception. Ignoring `RejectedExecutionException` is how overload becomes a mysterious lost task that never ran.

```java
ExecutorService exec = new ThreadPoolExecutor(
    2, 4, 60, TimeUnit.SECONDS,
    new ArrayBlockingQueue<>(100),
    new ThreadPoolExecutor.CallerRunsPolicy());
```

That sketch shows the knobs: core size, max size, keep-alive, a bounded queue, and a policy that pushes work back to the caller when saturated. `newFixedThreadPool` hid decisions you will eventually want to own.

Virtual threads will later change some defaults for blocking workloads — cheap threads make "one task, one thread" sensible again in many servers. That does not erase pools for every case, especially CPU-bound work that still needs bounding. Today the lesson is older and still vital: manage concurrency as a resource with a budget.

Common mistakes are predictable. Using a cached pool for unbounded bursty work without another limit. Never shutting down pools in long-running processes. Treating rejection as an impossible edge instead of an expected pressure valve.

Think about ownership across an application. A web framework may own a pool for request tasks. A batch module may own another for CPU-heavy jobs. Sharing one giant unbounded pool for everything couples unrelated workloads: a flood of IO tasks can starve CPU work. Separating pools is blast-radius control — the same instinct as bounded queues, applied at architecture scale.

What if every library quietly creates its own cached thread pool and never shuts it down? You get thread leaks that are hard to attribute. Prefer passing an `Executor` in, or documenting lifecycle clearly. Pools are resources. Resources need owners.

Instrument pools when you can: active threads, queue depth, rejected tasks. Without metrics, "the pool feels slow" is superstition. The factory methods get you started; observability keeps you honest once traffic is real.

Submitting work raises a new hunger immediately: many tasks produce a result, may fail with a checked exception, and must not be waited on forever. `Runnable` is not enough for that contract.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 40 (*ExecutorService*).

Narration technique: burst-of-tasks situation → pools → fixed pool walkthrough → flavors → shutdown → bounded queue/rejection → next natural problem (Callable/Future).
