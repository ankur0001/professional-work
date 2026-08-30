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

Prefer purity in lambdas. A filter should decide, not update a database. A map should transform, not quietly mutate a shared list. Side effects inside stream lambdas make order, laziness, and later parallelism hard to reason about.

```java
long count = list.stream()
    .filter(s -> s.startsWith("A"))
    .count();
```

Here the terminal is `count`. No intermediate list required. Modern Java's `toList()` returns an unmodifiable list — handy for returning results safely. Older code uses `collect(Collectors.toList())`, which is mutable.

Streams are not always faster. They shine for clarity on bulk data transformations. On tiny lists, a simple loop can be easier to read and cheaper to run. Do not rewrite every for-loop into a stream for fashion.

A slightly richer example shows composition without nesting:

```java
List<String> names = users.stream()
    .filter(User::active)
    .sorted(Comparator.comparing(User::name))
    .map(User::name)
    .toList();
```

Filter, sort, map, collect — each step one idea. Comparators from the previous episode drop in naturally.

Laziness becomes tangible with short-circuit terminals.

```java
Optional<String> first = list.stream()
    .filter(s -> s.length() > 3)
    .map(String::toUpperCase)
    .findFirst();
```

If the first element already qualifies, later elements need not be mapped. Also remember streams are single-use. Call a terminal, and the stream is consumed. If you need two results, collect once or stream from the source twice.

Infinite streams exist — `Stream.iterate`, `Stream.generate` — and they make the terminal's role unmistakable. Without `limit` or a short-circuit terminal, they never finish.

```java
Stream.iterate(0, n -> n + 1).limit(5).toList(); // 0..4
```

Primitive streams — `IntStream`, `LongStream`, `DoubleStream` — avoid boxing when you map to numbers and sum or average:

```java
int sum = list.stream().mapToInt(String::length).sum();
```

Hand-built loops mixed filter, map, and collect. Streams named those steps as a lazy pipeline. Purity kept lambdas honest. Performance humility kept us from cargo-culting.

Once pipelines feel natural, the terminal step gets more interesting: sometimes you need a `Set`, a `Map`, or groups of elements. How do you collect into richer structures?

That is the pressure that brings stream collectors.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 26 (*Streams Intro*).

Narration technique: loop-as-pipeline situation → stream source/intermediate/terminal → laziness → purity → toList → not always faster → next natural problem (richer collection / collectors). Continuity-checked transitions.
