# Episode 29 — Parallel Streams

**Cut:** v1 (original)

## Transcript (from captions)

flatMap flattened pipelines. Parallelism multiplies throughput — sometimes. parallelStream splits work across threads automatically. ForkJoinPool common pool backs most parallel streams.

Speedups are not free — coordination has a cost. Today — parallel streams with measurement, not hope. Parallel when it pays. Sequential when it does not. Episode Twenty-Nine. Parallel Streams — fork-join in practice.

Parallel streams build on the fork-join framework. Work splits into chunks. Threads process chunks concurrently. Results combine when chunks finish. Java uses a shared ForkJoinPool for parallel streams.

You do not manage threads manually — the pool does. Understand the pool before you trust the speedup. Call parallel or parallelStream to enable parallelism. The same pipeline runs — but elements may process concurrently.

Intermediate operations can run in parallel on sub-splits. Terminal operations coordinate the merge. Sequential is the default — parallelism is opt-in. One method call does not guarantee a faster program.

Ordering changes under parallelism. Sequential streams preserve encounter order when required. Parallel streams may process out of order for speed. forEachOrdered restores order at a cost.

sorted still produces a sorted result — but work may shuffle internally. If order matters for correctness, design for it explicitly. The common pool is shared across the JVM. Blocking tasks in parallel streams can starve other work.

Custom ForkJoinPool wrapping is possible for isolation — advanced topic. Do not nest parallel streams on the same pool blindly. IO-bound work usually belongs elsewhere — not parallel streams.

CPU-bound, large, independent chunks are the sweet spot. When parallelism helps. Large collections. Pure transformations. Minimal shared state. When it hurts. Small collections — overhead dominates.

Shared mutable accumulators without thread-safe collectors. Measure on real hardware — micro-benchmarks lie easily. Three common mistakes. One — parallel by default without profiling.

Two — mutating shared fields inside map or forEach. Three — assuming encounter order in parallel forEach. Also — running blocking IO inside parallel streams. Parallel code must still be correct code first.

Interview question — when would you use parallel streams? Large in-memory data, CPU-heavy pure transforms, few side effects. Mention ForkJoinPool and measurement before and after. Contrast with sequential — default until proven otherwise.

Note ordering and thread-safety requirements. That answer shows engineering judgment, not buzzwords. Parallelism needs safe absence handling. Next — Optional. Episode Thirty — Optional.

Present, empty, and chained without null checks everywhere. See you there.
