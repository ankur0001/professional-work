# Episode 29 — Parallel Streams

| Field | Value |
|---|---|
| Episode | 29 |
| Title | Parallel Streams |
| Catalog handbook column | 29 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Sequential streams made bulk work declarative. Looking at a long CPU-heavy map, a temptation appears: add `.parallel()` and wait for a speedup. Parallel streams are a power tool — and a foot-gun on IO and tiny data.

Suppose you transform a large list of in-memory records with a pure, expensive function — compress a buffer, score a document, compute a hash. The work is independent: one element's result does not depend on another's. That is the profile where parallel streams can help.

```java
List<Result> results = list.parallelStream()
    .map(this::cpuHeavy)
    .toList();
```

Walk the claim carefully. `parallelStream()` splits the source and runs pieces concurrently. Under the hood it uses the common `ForkJoinPool`. Your lambdas must tolerate running on multiple threads. Prefer purity — no unsynchronized mutation of shared collections inside the map. Best for CPU-heavy independent work on sizable data.

What goes wrong when the problem is smaller or messier?

On tiny lists, the cost of splitting and joining dwarfs the work. You can make a sort slower by parallelizing it. Measure; don't hope.

Ordering and side effects get weird. Encounter order may differ. `forEach` on a parallel stream does not promise sequence. If you mutate an external `ArrayList` from parallel threads, you corrupt it.

```java
List<String> unsafe = new ArrayList<>();
list.parallelStream().forEach(unsafe::add);   // don't
```

Use a proper concurrent collector or keep the pipeline pure and collect at the end.

IO-bound work wants explicit executors or virtual threads, not the common fork-join pool. A parallel stream that blocks on network calls inside `map` can stall shared compute work for the whole JVM process — other unrelated parallel streams may wait.

```java
// CPU-bound, pure, large enough — candidate
list.parallelStream().map(this::score).toList();

// IO-bound — prefer structured concurrency / executors / virtual threads
// not the common ForkJoinPool via parallelStream
```

A fair check: when would you refuse parallel streams? Tiny data, IO inside the pipeline, need for strict encounter order with side effects, or already saturated cores. When would you consider them? Large in-memory data, pure CPU work, associative reductions, measured improvement.

What if we always call `parallel()` for fashion?

```java
List.of("a", "b", "c").parallelStream().map(String::toUpperCase).toList();
```

Three elements. No win. Harder debugging. Keep sequential as the default; go parallel when evidence says so.

Reductions have associativity requirements under parallelism. Summing integers works. Prefer `Collectors.joining` or concurrent collectors designed for the job.

```java
int sum = list.parallelStream().mapToInt(Integer::intValue).sum();
```

Primitive specialized streams avoid boxing and parallelize cleanly for numeric work. Also know the pool: the common ForkJoinPool size defaults around available processors. Saturating it with blocking tasks hurts unrelated parallel streams library-wide.

Thread-safety of the source matters. Parallel streams over freshly built `ArrayList`s of immutable data are the happy path. Stabilize inputs first. Naming tip: `processInParallel(data)` as a dedicated method signals intent and localizes the parallel boundary.

Independent CPU work suggested parallelism. The common ForkJoinPool powered parallel streams. Purity and sizing constraints appeared. Ordering and shared mutation failed loudly. IO-bound work pointed elsewhere. Measurement closed the argument.

Pipelines and collectors still have one more everyday absence problem: a lookup that might not find a user, a parse that might not yield a number. Returning null works until it doesn't. Is there a type that makes absence explicit at the boundary?

That type is Optional.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 29 (*Parallel Streams*).

Narration technique: speed temptation → parallelStream/ForkJoinPool → CPU-bound fit → tiny/IO/side-effect failures → measure → next natural problem (explicit absence / Optional). Continuity-checked transitions.
