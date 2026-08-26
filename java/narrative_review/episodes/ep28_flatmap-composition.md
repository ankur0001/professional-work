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

Each flatMap removes one nesting level. The final map extracts skus. Distinct uniquifies. You can say the sentence out loud: "all skus from all lines from all orders from all users." When the pipeline becomes a puzzle, stop — nested loops with clear names may be kinder. Keep pipelines readable; composition is a tool, not a purity contest.

The same flattening idea appears with `Optional`. Multi-step lookups often return empty at any stage.

```java
Optional<String> city = findUser(id)
    .flatMap(User::address)
    .flatMap(Address::city);
```

`Optional.flatMap` for multi-step absence avoids nested `isPresent` pyramids. If `findUser` is empty, the chain short-circuits to empty. If address is missing, same. `map` would have produced `Optional<Optional<City>>` shaped confusion; `flatMap` keeps a single optional layer.

Compare map versus flatMap on optionals quickly:

```java
Optional<Optional<String>> nested = findUser(id).map(User::nickname); // if nickname is Optional
Optional<String> flat = findUser(id).flatMap(User::nickname);
```

When a function already returns `Optional`, flatMap is the join you want.

What if we flatten with hand-rolled loops every time?

```java
List<Order> orders = new ArrayList<>();
for (User u : users) {
    for (Order o : u.orders()) {
        orders.add(o);
    }
}
```

Clear for two levels. At three levels with filters in between, the loop version grows braces while the stream version grows steps. Choose the form your teammates can amend safely next month.

A practical habit: name helpers when lambdas get heavy.

```java
flatMap(this::ordersOf)  // vs a long lambda inline
```

Composition stays readable when each function does one transformation. FlatMap is not an excuse for a novel in a lambda.


Another flattening pattern: turning optional fields into zero-or-one streams.

```java
List<String> nicknames = users.stream()
    .flatMap(u -> u.nickname().stream())  // Optional.stream()
    .toList();
```

Empty optionals contribute nothing; present ones contribute one element. That replaces filter-plus-get patterns with a single flatMap.

When composition grows, extract named methods for each nesting level — `ordersOf`, `linesOf`, `skuOf` — so the pipeline reads as business vocabulary. The goal is not fewer lines; it is fewer surprises for the next reader.

If you find yourself flatMapping more than two or three levels with filters interleaved, consider whether a small dedicated domain method should hide the traversal. Pipelines should reveal intent, not become the place all navigation lives.


Files and lines offer a classic flatMap story: a stream of paths flatMapped to lines of each file. Nested collections in memory follow the same shape. Once you see it, you start spotting flatten opportunities — and also spotting when a nested for-loop with early continues is less magical and more maintainable.

Avoid flatMapping into huge intermediate cardinalities without filters. Cartesian-style explosions hide in innocent looking pipelines. Estimate sizes. Keep limits close to the source when exploring.



When teaching teammates, draw the shapes: `Stream<List<T>>` versus `Stream<T>`. The picture does more than another definition. Once the shape is visible, flatMap stops feeling like magic syntax and starts feeling like the only honest operator for that shape.

That judgment call is the real skill this episode trains — not the spelling of flatMap.

Prefer that shape question over memorizing snippets. When the types line up, the operator choice usually becomes obvious.

So let's reconnect the chain. Nested collections made `map` produce the wrong shape. `flatMap` flattened streams of streams. Optional flatMap handled multi-step absence. Readability set the limit on how far to push pipeline style.

Once sequential pipelines feel comfortable, someone asks the speed question: can we run this in parallel and use more cores? Sometimes yes. Often not for the reason people hope.

Flattening is fundamentally about shape. Each time you are unsure whether to map or flatMap, ask: does my function return an element, or a collection/optional/stream of elements? Element → map. Collection of elements → flatMap. That question alone removes most guesswork.

Optional and stream flatMap share a name because they share a shape problem: nested wrappers. Once you are comfortable in both places, composition across APIs feels less like trivia and more like one idea. That unity is worth practicing with small examples until the map/flatMap choice becomes automatic.

Nested loops are not morally inferior. They are often the right tool when each level needs complex local control flow. Reach for flatMap when the story is "expand each element into zero or more contributions" and the steps stay pure. Judgment beats ideology.

That caution is Episode Twenty-Nine — Parallel Streams.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 28 (*flatMap & Composition*).

Narration technique: nested collections problem → flatMap vs map → deeper composition → Optional.flatMap → readability limit → next natural problem (parallelism). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- map nests; flatMap flattens.
- Optional.flatMap for multi-step absence.
- Domain models often nest collections.
- Keep pipelines readable.
- Composition beats manual nested loops when clear.
