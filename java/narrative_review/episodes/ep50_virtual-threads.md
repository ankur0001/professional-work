# Episode 50 — Virtual Threads

| Field | Value |
|---|---|
| Episode | 50 |
| Title | Virtual Threads |
| Catalog handbook column | 50 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

For many episodes we treated threads as expensive OS-backed workers you must pool and bound. That model still matters. It is no longer the only model. Modern Java can run a huge number of lightweight virtual threads scheduled onto a smaller set of platform carrier threads. The programming style that feels natural for servers — one thread per request, blocking I/O that reads like straight-line code — becomes scalable again for blocking workloads.

Virtual threads make that style practical. They are cheap to create in large numbers. Do not pool them like platform threads. Watch pinning cases. They shine with blocking I/O and structured concurrency. CPU-bound work still needs bounding.

```java
try (var exec = Executors.newVirtualThreadPerTaskExecutor()) {
    exec.submit(() -> handle(req));
}
```

Walk the shift. Instead of a fixed pool of eight platform threads, you create an executor that starts a new virtual thread per task. Blocking inside `handle` parks the virtual thread without permanently occupying a carrier the way a blocked platform thread occupies an OS thread. Thousands of in-flight requests can wait on I/O without forcing you into reactive callback mazes — when the libraries and code cooperate.

Why not pool them like before? Platform pools existed because platform threads were scarce. Virtual threads are plentiful; a pool that caps them can reintroduce scarcity without the old benefit. Prefer starting one per task for blocking request work, and use semaphores or other limits when you must bound access to a scarce dependency — bound the resource, not the virtual thread count by habit.

Pinning is the sharp edge. Certain operations — notably some `synchronized` blocks and native calls — can pin a virtual thread to its carrier, preventing the carrier from scheduling other virtual threads while blocked. Hot pinning in a frequent path undermines the scalability story. You do not need every pinning detail today; you need the habit of noticing synchronized/native hotspots when virtual threads underperform expectations. Prefer `ReentrantLock` in some hot paths, keep synchronized sections tiny, and measure.

CPU-bound work still needs bounding. Virtual threads do not create more cores. A stampede of CPU-heavy tasks on virtual threads can still oversubscribe the machine. Use a limited pool or semaphore for pure computation. Virtual threads optimize the economics of waiting, not the laws of arithmetic throughput.

```java
// still bound CPU work
Semaphore cpu = new Semaphore(Runtime.getRuntime().availableProcessors());
cpu.acquire();
try {
    heavyCompute();
} finally {
    cpu.release();
}
```

Structured concurrency — keeping related tasks in a clear scope with cancellation — pairs naturally with virtual threads. Hold that as curiosity for APIs evolving in the JDK; the theme is already clear: cheap threads invite many tasks, and many tasks need clear lifetimes.

What if we assume virtual threads make everything faster, including tight math loops?

They will not invent cores. Mis-pooling them, pinning in hot sections, or expecting CPU miracles are the three classic misunderstandings. Use them where blocking I/O and high concurrency meet. Keep the older lessons — atomics, queues, deadlock order, interrupt discipline — because correctness did not become optional when threads became cheap.

Migrate a mental model carefully. Old advice said "never block a request thread on slow I/O without an async design." Virtual threads revise that advice for many servers: blocking is fine if the thread is virtual and the stack is not pinned. Old advice said "always use a pool." Virtual threads revise that for task threads: pool the scarce resource, not the cheap thread. Old advice about shared mutability, interrupts, and deadlocks does not revise. Cheap threads make races easier to schedule, not harder.

Measure pinning and carrier utilization when adopting virtual threads on a hot service. The first win is often simpler code. The first surprise is often a synchronized block in a library you did not write. Adoption is an ecosystem conversation, not only a language feature flip.

With concurrency's main tools in hand, we are ready to look under the runtime — how classes appear, what bytecode is, where objects live, how GC reclaims, and how JIT warms. That JVM arc starts next.

Libraries matter as much as your code. A JDBC driver, logger, or metrics client that pins under synchronized blocks can limit the benefit of virtual threads until updated. Adoption plans should include dependency versions, not only a language level bump.
For learning, rewrite a small blocking server from a fixed pool to virtual threads and compare readability under the same correctness rules you already know. The win should be simplicity under load — not a license to ignore races.

Picture a server that used to maintain a pool of 200 platform threads and still queued during I/O spikes. Switching handlers to virtual threads per request collapses the queueing story for blocking I/O waits, while a semaphore still protects a database that can only handle 50 concurrent queries. Threads became plentiful; the database did not. Bound what is scarce.

Prefer virtual threads for many blocking tasks; prefer bounded concurrency for scarce dependencies and CPU. The combination is the modern default for many servers — simple code, honest limits.

So reconnect the chain. Expensive platform threads forced pools. Virtual threads revived thread-per-request for blocking I/O. Per-task executors replaced habitual pooling. Pinning and CPU bounding marked the edges. The concurrency arc from Episode Thirty-Six to here was progressive on purpose: start timelines, then safety, then structure, then scale.

When the language story stabilizes, another curiosity rises: how does the JVM even find and prepare the classes we have been running? That runtime machinery begins with class loading.

Episode Fifty-One opens the JVM internals arc.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 50 (*Virtual Threads*).

Narration technique: expensive-thread pressure → virtual threads → per-task executor → no habitual pooling → pinning → CPU bound → structured concurrency curiosity → next natural problem (class loading).
