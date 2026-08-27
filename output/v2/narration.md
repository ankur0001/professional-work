# Episode 21 — Lists

| Field | Value |
|---|---|
| Episode | 21 |
| Title | Lists |
| Catalog handbook column | 21 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Platform boundaries can now be declared. That does not shrink the data inside a feature. Arrays still give us fixed length; real carts, search hits, and timelines rarely promise one.

Suppose you are collecting tags a user adds to a post. They might add three, then delete one, then add five more. With an array you allocate, copy, allocate again. The natural question becomes: is there a resizable, ordered collection that still lets me talk about "the first item" and "insert here"?

That collection is a `List`. A list is ordered and allows duplicates. Position matters. The same value can appear twice and mean two entries.

```java
List<String> list = new ArrayList<>();
list.add("a");
list.add(0, "b");
System.out.println(list.get(0));
```

Walk the lines. We program to the `List` interface and construct an `ArrayList` — the default workhorse for most application code. `add("a")` appends. `add(0, "b")` inserts at the front, shifting what was there. `get(0)` reads by index and prints `b`. The list now holds `[b, a]`.

Why `ArrayList` by default? Under the hood it uses a resizable array: fast random access by index, fast append at the end amortized, slower inserts at the front because elements shift. That profile matches how most business code actually uses lists.

What about `LinkedList`? It is a doubly linked structure. Inserts and removals at known nodes can be cheap, but getting the nth element means walking links. In practice, `LinkedList` rarely wins for typical access patterns. Prefer the boring default until a profiler argues otherwise.

Programming to the `List` interface matters: callers depend on list behavior, not on a concrete class.

```java
void printAll(List<String> items) {
    for (String item : items) {
        System.out.println(item);
    }
}
```

`printAll` does not care how the list is stored. It cares that iteration and order behave like a list.

Now the failure mode that bites during iteration: structural modification while an iterator is live.

```java
List<String> tags = new ArrayList<>(List.of("java", "jvm", "gc"));
for (String tag : tags) {
    if (tag.equals("jvm")) {
        tags.remove(tag);   // ConcurrentModificationException risk
    }
}
```

The enhanced for-loop uses an iterator. Removing directly from the list during that iteration can throw `ConcurrentModificationException`. The safe habits are: use the iterator's own `remove`, collect removals and apply them after, or use `removeIf`.

What if we skip lists and keep resizing arrays by hand? It works until the copy logic drifts, or someone forgets to update a length variable. Lists exist so resizable ordered sequences stop being a DIY project.

A small product-shaped fragment ties it together:

```java
List<String> cart = new ArrayList<>();
cart.add("keyboard");
cart.add("cable");
cart.add("cable");              // duplicates allowed
String first = cart.get(0);
cart.removeIf(item -> item.equals("cable"));
```

The cart is ordered. Duplicate cables are two lines until we remove them. That is list thinking: sequence, not uniqueness, not key lookup.

Also watch aliasing: `subList` views share structure with the backing list. When you need a true independent snapshot, copy into a new `ArrayList`. Prefer `List.of` and `List.copyOf` when the collection should not grow — fixed lists fail fast on `add`, which is better than a mutable list that callers mutate by accident.

Growing sequences outgrew arrays. `List` answered with ordered, duplicate-friendly collections. `ArrayList` became the default workhorse. Programming to `List` kept APIs flexible. Iteration-modification rules kept us from surprising exceptions.

But sometimes duplicates are exactly what you do not want. A set of roles, a set of visited ids, a set of tags where "java" should appear once. How does Java say "unique membership"?

That question opens sets.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 21 (*Lists*).

Narration technique: resizable sequence need → List/ArrayList → LinkedList rarity → program to interface → ConcurrentModification → next natural problem (uniqueness / sets). Continuity-checked transitions.
