# Episode 28 — flatMap & Composition

| Field | Value |
|---|---|
| Episode | 28 |
| Title | flatMap & Composition |
| Catalog handbook column | 28 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Collectors taught us to finish pipelines into maps and groups. Domain models still nest: a customer has orders, an order has line items, a team has members who have skills. If you `map` each customer to their orders, you get a stream of lists — a nested world. flatMap flattens nested worlds — lists of lists, optional chains, effect pipelines.

Suppose you want every order across all users.

```java
List<Order> orders = users.stream()
    .map(user -> user.orders())      // Stream<List<Order>>
    .toList();                       // still nested: a list of lists
```

That is not a list of orders. It is a list of lists. The natural question: how do we flatten one level?

```java
List<Order> orders = users.stream()
    .flatMap(user -> user.orders().stream())
    .toList();
```

Walk the difference. `map` would wrap each user's orders as one element of type `List<Order>`. `flatMap` expects each element to produce a stream, then concatenates those streams into one. Map nests; flatMap flattens. Domain models often nest collections — flatMap is how pipelines stay honest about that shape.

Composition beats manual nested loops when the pipeline stays readable:

```java
List<String> skus = users.stream()
    .flatMap(user -> user.orders().stream())
    .flatMap(order -> order.lines().stream())
    .map(Line::sku)
    .distinct()
    .toList();
```

Each flatMap removes one nesting level. The final map extracts skus. Distinct uniquifies. You can say the sentence out loud: "all skus from all lines from all orders from all users." When the pipeline becomes a puzzle, stop — nested loops with clear names may be kinder.

The same flattening idea appears with `Optional`. Multi-step lookups often return empty at any stage.

```java
Optional<String> city = findUser(id)
    .flatMap(User::address)
    .flatMap(Address::city);
```

`Optional.flatMap` for multi-step absence avoids nested `isPresent` pyramids. If `findUser` is empty, the chain short-circuits to empty. `map` would have produced `Optional<Optional<City>>` shaped confusion; `flatMap` keeps a single optional layer.

When a function already returns `Optional`, flatMap is the join you want:

```java
Optional<Optional<String>> nested = findUser(id).map(User::nickname); // if nickname is Optional
Optional<String> flat = findUser(id).flatMap(User::nickname);
```

What if we flatten with hand-rolled loops every time? Clear for two levels. At three levels with filters in between, the loop version grows braces while the stream version grows steps. Choose the form your teammates can amend safely next month.

Another flattening pattern: turning optional fields into zero-or-one streams.

```java
List<String> nicknames = users.stream()
    .flatMap(u -> u.nickname().stream())  // Optional.stream()
    .toList();
```

Empty optionals contribute nothing; present ones contribute one element. When composition grows, extract named methods for each nesting level — `ordersOf`, `linesOf`, `skuOf` — so the pipeline reads as business vocabulary.

Flattening is fundamentally about shape. Each time you are unsure whether to map or flatMap, ask: does my function return an element, or a collection/optional/stream of elements? Element → map. Collection of elements → flatMap. That question alone removes most guesswork.

Nested collections made `map` produce the wrong shape. `flatMap` flattened streams of streams. Optional flatMap handled multi-step absence. Readability set the limit on how far to push pipeline style.

Once sequential pipelines feel comfortable, someone asks the speed question: can we run this in parallel and use more cores? Sometimes yes. Often not for the reason people hope.

That caution is parallel streams.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 28 (*flatMap & Composition*).

Narration technique: nested collections problem → flatMap vs map → deeper composition → Optional.flatMap → readability limit → next natural problem (parallelism). Continuity-checked transitions.
