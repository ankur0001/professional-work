# Episode 47 — ForkJoinPool

| Field | Value |
|---|---|
| Episode | 47 |
| Title | ForkJoinPool |
| Catalog handbook column | 47 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

CompletableFuture composed asynchronous stages. Another family of problems looks different: take a large CPU-bound job, split it into pieces, solve the pieces, combine the results. Sorting, compressing, scanning huge arrays — divide and conquer. You could submit every piece to a fixed thread pool by hand. You would also reinvent work stealing poorly. What machinery is built for recursive splitting?

`ForkJoinPool` is divide-and-conquer with work stealing. Idle workers steal tasks from busy workers' queues so cores stay busy even when splits are uneven. Parallel streams use this machinery under the hood — which is why blocking the common pool hurt in the last episode too.

```java
ForkJoinPool.commonPool().invoke(new MyTask(range));
```

You define a task — typically a `RecursiveTask` that returns a value, or a `RecursiveAction` that does not. The task decides whether the range is small enough to solve directly, or should fork into subtasks and join their results. `invoke` runs the root task and waits for the answer.

```java
class SumTask extends RecursiveTask<Long> {
    final int[] data; final int lo; final int hi;
    SumTask(int[] data, int lo, int hi) { this.data = data; this.lo = lo; this.hi = hi; }

    protected Long compute() {
        if (hi - lo <= THRESHOLD) {
            long sum = 0;
            for (int i = lo; i < hi; i++) sum += data[i];
            return sum;
        }
        int mid = (lo + hi) >>> 1;
        SumTask left = new SumTask(data, lo, mid);
        SumTask right = new SumTask(data, mid, hi);
        left.fork();
        long rightAns = right.compute();
        long leftAns = left.join();
        return leftAns + rightAns;
    }
}
```

Small ranges add directly. Large ranges split, fork one side, compute the other, join, and add. The threshold matters: too large and you under-parallelize; too small and task overhead dominates. Unbalanced splits — always peeling one element — defeat the model. Aim for pieces that are meaningful work units.

Work stealing in interview language: idle workers steal tasks from busy workers' queues. That sentence explains why the pool tolerates uneven task sizes better than a naive global queue of giant chunks.

The common pool is shared across the JVM. Best for CPU-bound splitting. Do not block worker threads on I/O or locks held for long. A blocked worker cannot steal or run other tasks; under enough blocking, the pool's parallelism collapses. Submit blocking work to a separate executor. Keep Fork/Join for computation.

What if we treat Fork/Join as a general application executor for mixed I/O? You will contend with every parallel stream and many async defaults for the same workers, then block them. That is how "parallelism" becomes mysterious latency.

Parallel streams made Fork/Join popular even among developers who never wrote a `RecursiveTask`. A library that blocks inside `parallelStream` forbids other features from using the same common pool effectively. Prefer sequential streams for I/O-bound work; reserve parallel for measured CPU gains on large enough data.

Fork/Join task sizing is an empirical craft. Start with a threshold that does meaningful work — thousands of elements, not one — and measure. The steal scheduler is clever; it is not a substitute for sane task granularity.

A final caution: `invoke` on a huge task from a request thread still occupies that request thread until completion. Fork/Join parallelizes the work; it does not automatically make the caller asynchronous. Divide-and-conquer shines when subproblems are independent. Shared mutable accumulators without atomics or reduction discipline reintroduce races the pool cannot fix.

Picture summing sensor readings across a multi-million-element array on a batch box. A recursive task splits until chunks fit in cache-friendly sizes, then adds. Wall-clock time drops until you hit cores or memory bandwidth. Blocking on a database inside those tasks would waste the win.

Hold the checklist: CPU-bound splits; sane thresholds; no blocking on workers; measure before celebrating.

Sometimes the data you need is not shared through a queue or map — it is ambient per-thread context: a request id, a principal, a legacy formatter that is not thread-safe. That temptation has a name, and a leak story.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 47 (*ForkJoinPool*).

Narration technique: divide-and-conquer situation → ForkJoin/work stealing → RecursiveTask walkthrough → common pool caution → next natural problem (ThreadLocal).
