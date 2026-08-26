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

On tiny lists, the cost of splitting and joining dwarfs the work. You can make a sort slower by parallelizing it. Measure; don't hope. A microbenchmark or a realistic timer around the real dataset beats folklore.

Ordering and side effects get weird. Encounter order may differ. `forEach` on a parallel stream does not promise sequence. If you print inside a lambda for debugging, lines shuffle. If you mutate an external `ArrayList` from parallel threads, you corrupt it. Side-effecting lambdas that were "fine" sequentially become races.

```java
List<String> unsafe = new ArrayList<>();
list.parallelStream().forEach(unsafe::add);   // don't
```

Use a proper concurrent collector or keep the pipeline pure and collect at the end.

IO-bound work wants explicit executors or virtual threads, not the common fork-join pool. A parallel stream that blocks on network calls inside `map` can stall shared compute work for the whole JVM process — other unrelated parallel streams may wait. That surprise is why "just parallelize the stream" is dangerous in servers. Blocking queues and dedicated thread pools from later concurrency episodes are the better fit for IO pipelines.

```java
// CPU-bound, pure, large enough — candidate
list.parallelStream().map(this::score).toList();

// IO-bound — prefer structured concurrency / executors / virtual threads
// not the common ForkJoinPool via parallelStream
```

A fair interview-style check: when would you refuse parallel streams? Tiny data, IO inside the pipeline, need for strict encounter order with side effects, or already saturated cores. When would you consider them? Large in-memory data, pure CPU work, associative reductions, measured improvement.

What if we always call `parallel()` for fashion?

```java
List.of("a", "b", "c").parallelStream().map(String::toUpperCase).toList();
```

Three elements. No win. Harder debugging. You taught the team the wrong default. Keep sequential as the default; go parallel when evidence says so.


Reductions have associativity requirements under parallelism. Summing integers works. Building a string by repeatedly concatenating on the left in a non-associative way can scramble. Prefer `Collectors.joining` or concurrent collectors designed for the job.

```java
int sum = list.parallelStream().mapToInt(Integer::intValue).sum();
```

Primitive specialized streams avoid boxing and parallelize cleanly for numeric work. That is a better first parallel candidate than a stream of objects with heavy allocation inside `map`.

Also know the pool: the common ForkJoinPool size defaults around available processors. Saturating it with blocking tasks hurts unrelated parallel streams library-wide. Isolate blocking work elsewhere. That single operational fact prevents many "the app randomly stalled" incidents blamed on "Java streams."


Thread-safety of the source matters. Parallel streams over freshly built `ArrayList`s of immutable data are the happy path. Parallel streams over concurrent collections undergoing mutation are a research project you did not mean to start. Stabilize inputs first.

Naming tip: `processInParallel(data)` as a dedicated method signals intent and localizes the parallel boundary. Inline `.parallelStream()` in the middle of business logic hides a concurrency decision where reviewers least expect it.



Finally, remember that parallel streams do not replace architecture. Throughput problems may need better algorithms, caching, or batching — not just more cores on the same pipeline. Measure end-to-end. Local parallel wins that hurt tail latency are not wins.

Numbers first, parallel second: that ordering keeps the common pool healthy and the code honest.

If you cannot cite a measurement, leave the stream sequential. Parallelism is an optimization with a concurrency bill attached. Pay the bill only when the speedup is real. Hope is not a benchmark.

So let's reconnect the chain. Independent CPU work suggested parallelism. The common ForkJoinPool powered parallel streams. Purity and sizing constraints appeared. Ordering and shared mutation failed loudly. IO-bound work pointed elsewhere. Measurement closed the argument.

Pipelines and collectors still have one more everyday absence problem: a lookup that might not find a user, a parse that might not yield a number. Returning null works until it doesn't. Is there a type that makes absence explicit at the boundary?

A healthy team default: sequential streams in application code; parallel only behind a clearly named method with a comment pointing at a benchmark. Fashionable `.parallel()` in random service methods is how fork-join saturation becomes a production mystery.

If a parallel pipeline helps in benchmarks but complicates error handling — one element's failure should cancel others, for example — consider structured concurrency tools instead of stretching parallel streams past their design. Parallel streams are a concise parallel map/reduce, not a general workflow engine.

A quick lab: time a CPU-heavy map over 10 elements and over 10 million. Parallelism usually only pays in the second world. Keep that lab in mind whenever a pull request sprinkles `.parallel()` without numbers.

Episode Thirty — Optional.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 29 (*Parallel Streams*).

Narration technique: speed temptation → parallelStream/ForkJoinPool → CPU-bound fit → tiny/IO/side-effect failures → measure → next natural problem (explicit absence / Optional). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Uses common ForkJoinPool.
- Best for CPU-heavy independent work.
- Ordering and side effects get weird.
- IO-bound work wants explicit executors/virtual threads.
- Measure; don't hope.
