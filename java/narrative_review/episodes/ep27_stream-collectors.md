# Episode 27 — Stream Collectors

| Field | Value |
|---|---|
| Episode | 27 |
| Title | Stream Collectors |
| Catalog handbook column | 27 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Streams taught us to describe bulk work as a pipeline. The last step still has to answer a practical question: what structure do we actually return to the rest of the program?

Sometimes a list is enough. Often you need a set of unique ids, a map of name to user, or a map of department to employees. Collectors turn streams into the structures you actually return.

```java
List<String> list = List.of("ada", "ada", "grace");

Map<String, Long> counts = list.stream()
    .collect(Collectors.groupingBy(s -> s, Collectors.counting()));
```

Walk it. `groupingBy` builds a map keyed by the classifier — here the string itself. The downstream collector `counting()` tallies how many elements fell into each group. Result: `ada → 2`, `grace → 1`. That is a whole nested loop and map-merge story expressed as one terminal thought.

The basic collectors cover everyday destinations:

```java
List<String> names = stream.collect(Collectors.toList());
Set<String> unique = stream.collect(Collectors.toSet());
Map<String, User> byId = users.stream()
    .collect(Collectors.toMap(User::id, u -> u));
```

`toList`, `toSet`, and `toMap` are the first tools to reach for. Modern `stream.toList()` overlaps the list case with an unmodifiable result; `Collectors.toList()` remains common in older code and when you want a mutable list explicitly.

`toMap` needs a merge function when keys can collide:

```java
Map<String, Integer> scores = players.stream()
    .collect(Collectors.toMap(
        Player::name,
        Player::score,
        Integer::max));   // keep the best score on duplicate names
```

Without a merge function, duplicate keys throw. With one, collisions become a deliberate policy — sum, max, first-wins, or combine objects. That merge parameter is not ceremony; it is where you admit duplicates might exist.

Grouping and partitioning split streams into buckets:

```java
Map<Boolean, List<User>> parts = users.stream()
    .collect(Collectors.partitioningBy(User::active));

Map<String, List<User>> byDept = users.stream()
    .collect(Collectors.groupingBy(User::department));
```

`partitioningBy` is grouping on a boolean — two buckets, true and false. `groupingBy` takes any classifier. Downstream collectors deepen both:

```java
Map<String, Long> sizeByDept = users.stream()
    .collect(Collectors.groupingBy(User::department, Collectors.counting()));

Map<String, Set<String>> namesByDept = users.stream()
    .collect(Collectors.groupingBy(
        User::department,
        Collectors.mapping(User::name, Collectors.toSet())));
```

Downstream collectors are how you avoid building a map of lists and then post-processing. You say the final shape in the terminal operation: counts, sets of names, summed salaries.

Immutable collection collectors matter when you return values from APIs:

```java
List<String> frozen = stream.collect(Collectors.toUnmodifiableList());
```

Callers cannot `add` later. That failure is a feature when the method's contract is "here is a snapshot."

What if we finish every stream as a list and rebuild maps afterward?

```java
List<User> all = users.stream().filter(User::active).toList();
Map<String, List<User>> byDept = new HashMap<>();
for (User u : all) {
    byDept.computeIfAbsent(u.department(), k -> new ArrayList<>()).add(u);
}
```

It works. It also stages an intermediate structure you may not need. Collectors let the terminal step be the real answer.


`Collectors.joining` is another everyday terminal for readable output:

```java
String csv = names.stream().collect(Collectors.joining(", "));
```

Grouping with downstream averaging or summing shows up in reporting features:

```java
Map<String, Double> avgAge = users.stream()
    .collect(Collectors.groupingBy(
        User::department,
        Collectors.averagingInt(User::age)));
```

The map's values are already the statistic you wanted — no second pass. When key collisions in `toMap` are programming errors rather than merge cases, omitting the merge function is correct: fail fast on duplicates. When duplicates are data, supply the merge. That choice is domain knowledge expressed in the collector.


`Collectors.teeing` (newer JDKs) can compute two results in one pass when needed, but most code stays with grouping, mapping, and reducing. Master the common collectors before collecting curiosities.

Reducing with `Collectors.reducing` or stream `reduce` overlaps. Prefer collectors when the result is a collection or grouped structure; prefer `reduce` for a single combined value when that reads clearer. The goal is the obvious terminal, not a favorite API.

When returning maps from public methods, unmodifiable copies prevent callers from corrupting your internal indexes. Collectors that produce unmodifiable results help enforce that boundary.



Empty streams still produce empty lists, empty maps, or zero counts depending on the collector — usually what you want. Confirm the empty behavior when grouping: you get an empty map, not a map with empty buckets for unseen keys. If you need all keys present, seed them deliberately.

So let's reconnect the chain. Pipelines needed richer endings. Collectors answered with `toList`/`toSet`/`toMap`, grouping and partitioning, downstream composition, merge functions for collisions, and unmodifiable results for safe returns.

Sometimes the stream elements contain collections of their own — a user with orders, an order with lines. Mapping then gives you a stream of lists, which is rarely what you wanted. How do you flatten nested structure inside a pipeline?

Collectors are also where parallel friendliness shows up later: some collectors are concurrent, some are not. Even in sequential code, choosing the collector that matches the return type keeps methods honest — return a `Map` when you built a map, not a list you immediately re-index.

A collecting habit for APIs: if the method name says `groupedByDepartment`, return the map from a collector, do not return a list and force the caller to group again. The collector belongs next to the question the method answers. That keeps stream terminals aligned with domain language.

`Collectors.mapping` inside grouping is the usual way to project values before they land in the per-key collection. Learn that nesting and most "I need a map of sets of names" tasks become mechanical.

Practice exercise for your own codebase: find a handwritten nested loop that builds a `Map<K, List<V>>` and replace it with `groupingBy`. Then find a counting loop and replace it with `groupingBy(..., counting())`. The repetitions you remove are the point of collectors.

That is Episode Twenty-Eight — flatMap and Composition.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 27 (*Stream Collectors*).

Narration technique: need richer terminals → collectors basics → toMap merge → grouping/partitioning → downstream → immutable collectors → next natural problem (nested data / flatMap). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- toList/toSet/toMap.
- groupingBy and partitioningBy.
- Downstream collectors.
- toMap merge functions for collisions.
- Immutable collection collectors.
