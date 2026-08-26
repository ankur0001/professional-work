# Episode 26 — Streams Intro

| Field | Value |
|---|---|
| Episode | 26 |
| Title | Streams Intro |
| Catalog handbook column | 26 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Sorting taught us to declare comparison policy. Many loops still look like the same story told with different field names: take a collection, keep some elements, transform what remains, produce a result. Streams let you describe bulk operations — laziness included — instead of micromanaging each iteration.

Suppose you have a list of words and you want the long ones uppercased. The classic loop builds a result list by hand.

```java
List<String> result = new ArrayList<>();
for (String s : list) {
    if (s.length() > 3) {
        result.add(s.toUpperCase());
    }
}
```

It works. It also mixes three concerns — filtering, mapping, collecting — into one mutable scratchpad. The natural question is: can we name those steps as a pipeline?

```java
List<String> result = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .toList();
```

Walk the pipeline. `list.stream()` is the source. `filter` and `map` are intermediate operations — they describe what to do, and they are lazy. `toList()` is a terminal operation that triggers work and produces a result. Until a terminal runs, the intermediate steps wait. That laziness means you can build a pipeline and still short-circuit with `findFirst` without transforming every element.

Pipelines always have that shape: source, intermediate ops, terminal op. Forget the terminal and you have a description that never runs — a common beginner surprise when they expect `map` alone to print something.

Prefer purity in lambdas. A filter should decide, not update a database. A map should transform, not quietly mutate a shared list. Side effects inside stream lambdas make order, laziness, and later parallelism hard to reason about. If you need a side effect, an ordinary loop is often clearer.

```java
long count = list.stream()
    .filter(s -> s.startsWith("A"))
    .count();
```

Here the terminal is `count`. No intermediate list required. The pipeline expresses the question: how many strings start with A?

Modern Java's `toList()` collector (from the stream itself) returns an unmodifiable list — handy for returning results safely. Older code uses `collect(Collectors.toList())`, which is mutable. Know which one you are calling when a caller later tries to `add`.

Streams are not always faster. They shine for clarity on bulk data transformations. On tiny lists, a simple loop can be easier to read and cheaper to run. On hot paths, measure. Do not rewrite every for-loop into a stream for fashion. Prefer the form that makes the intent obvious and the cost acceptable.

What if we treat streams as magic speed buttons?

```java
// tiny list, complex parallel stream, harder stack traces — no win
```

You pay abstraction cost without gaining clarity or performance. Use streams when the pipeline reads closer to the problem than the loop does.

A slightly richer example shows composition without nesting:

```java
List<String> names = users.stream()
    .filter(User::active)
    .sorted(Comparator.comparing(User::name))
    .map(User::name)
    .toList();
```

Filter, sort, map, collect — each step one idea. Comparators from the previous episode drop in naturally. The result list is the answer to a sentence you could say out loud.


Laziness becomes tangible with short-circuit terminals.

```java
Optional<String> first = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .findFirst();
```

If the first element already qualifies, later elements need not be mapped. A handwritten loop that always uppercases everything before finding does extra work. Streams can skip that when the terminal allows it.

Debugging tip: intermediate `peek` exists for observation, but leave it out of production pipelines. It encourages side effects. Prefer unit-testing the functions you pass to `map` and `filter` as ordinary methods.

Also remember streams are single-use. Call a terminal, and the stream is consumed. A second terminal throws. If you need two results, collect once or stream from the source twice.


Infinite streams exist — `Stream.iterate`, `Stream.generate` — and they make the terminal's role unmistakable. Without `limit` or a short-circuit terminal, they never finish. That extreme case teaches the everyday rule: intermediate ops describe; terminals decide.

```java
Stream.iterate(0, n -> n + 1).limit(5).toList(); // 0..4
```

Method references keep pipelines tidy when a lambda would only call one method. When logic grows beyond a line, extract a named method and reference it — readability beats inline cleverness.



Exception handling inside lambdas is deliberately awkward — checked exceptions do not pass through Functional interfaces cleanly. That friction pushes you to keep stream bodies simple and to handle awkward I/O outside the pipeline or with wrapping helpers. It is another quiet reminder that streams favor pure transformations.

So let's reconnect the chain. Hand-built loops mixed filter, map, and collect. Streams named those steps as a lazy pipeline. Purity kept lambdas honest. `toList()` modernized collection of results. Performance humility kept us from cargo-culting.

Once pipelines feel natural, the terminal step gets more interesting: sometimes you need a `Set`, a `Map`, or groups of elements. How do you collect into richer structures?

Think of a stream as a view over a computation, not as a stored collection. The source list is still the data. The stream is the recipe. That mental model explains laziness, single-use rules, and why mutating the source while streaming is a bad idea.

Primitive streams — `IntStream`, `LongStream`, `DoubleStream` — avoid boxing when you map to numbers and sum or average. They are part of the same pipeline idea with less wrapper traffic. Reach for them when the payload is numeric end to end.

```java
int sum = list.stream().mapToInt(String::length).sum();
```

When a pipeline is hard to name in one sentence, it is probably doing too much. Split it. Streams amplify clear steps; they punish kitchen-sink lambdas.

That is Episode Twenty-Seven — Stream Collectors.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 26 (*Streams Intro*).

Narration technique: loop-as-pipeline situation → stream source/intermediate/terminal → laziness → purity → toList → not always faster → next natural problem (richer collection / collectors). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Pipelines: source, intermediate ops, terminal op.
- Lazy until terminal.
- Prefer purity in lambdas.
- toList() modern collectors.
- Streams aren't always faster.
