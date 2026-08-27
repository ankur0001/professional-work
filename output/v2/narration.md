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

`toList`, `toSet`, and `toMap` are the first tools to reach for. Modern `stream.toList()` overlaps the list case with an unmodifiable result; `Collectors.toList()` remains common when you want a mutable list explicitly.

`toMap` needs a merge function when keys can collide:

```java
Map<String, Integer> scores = players.stream()
    .collect(Collectors.toMap(
        Player::name,
        Player::score,
        Integer::max));   // keep the best score on duplicate names
```

Without a merge function, duplicate keys throw. With one, collisions become a deliberate policy — sum, max, first-wins, or combine objects.

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

What if we finish every stream as a list and rebuild maps afterward? It works. It also stages an intermediate structure you may not need. Collectors let the terminal step be the real answer.

`Collectors.joining` is another everyday terminal for readable output:

```java
String csv = names.stream().collect(Collectors.joining(", "));
```

Pipelines needed richer endings. Collectors answered with `toList`/`toSet`/`toMap`, grouping and partitioning, downstream composition, merge functions for collisions, and unmodifiable results for safe returns.

Sometimes the stream elements contain collections of their own — a user with orders, an order with lines. Mapping then gives you a stream of lists, which is rarely what you wanted. How do you flatten nested structure inside a pipeline?

That is the pressure that brings flatMap.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 27 (*Stream Collectors*).

Narration technique: need richer terminals → collectors basics → toMap merge → grouping/partitioning → downstream → immutable collectors → next natural problem (nested data / flatMap). Continuity-checked transitions.
