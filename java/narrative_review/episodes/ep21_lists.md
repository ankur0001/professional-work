# Episode 21 — Lists

| Field | Value |
|---|---|
| Episode | 21 |
| Title | Lists |
| Catalog handbook column | 21 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Modules drew stronger boundaries around packages. Inside those boundaries, everyday programs still need a workhorse for sequences: shopping carts, search hits, timeline events, lines of a file. Arrays gave us fixed length. Real features rarely promise a fixed length.

Suppose you are collecting tags a user adds to a post. They might add three, then delete one, then add five more. With an array you allocate, copy, allocate again. The natural question becomes: is there a resizable, ordered collection that still lets me talk about "the first item" and "insert here"?

That collection is a `List`. A list is ordered and allows duplicates. Position matters. The same value can appear twice and mean two entries.

```java
List<String> list = new ArrayList<>();
list.add("a");
list.add(0, "b");
System.out.println(list.get(0));
```

Walk the lines. We program to the `List` interface and construct an `ArrayList` — the default workhorse for most application code. `add("a")` appends. `add(0, "b")` inserts at the front, shifting what was there. `get(0)` reads by index and prints `b`. The list now holds `[b, a]`. Order is part of the meaning; duplicates would be allowed if we added `"a"` again.

Why `ArrayList` by default? Under the hood it uses a resizable array: fast random access by index, fast append at the end amortized, slower inserts at the front because elements shift. That profile matches how most business code actually uses lists — build them, then read by index or iterate.

What about `LinkedList`? It is a doubly linked structure. Inserts and removals at known nodes can be cheap, but getting the nth element means walking links. In practice, `LinkedList` rarely wins for typical access patterns beginners expect. If you chose it because "linked lists are classic," measure. Often `ArrayList` still wins. Prefer the boring default until a profiler argues otherwise.

Programming to the `List` interface matters for the same reason we program to interfaces elsewhere: callers depend on list behavior, not on a concrete class. You can change `ArrayList` to another `List` implementation behind a factory without rewriting every method signature.

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

The enhanced for-loop uses an iterator. Removing directly from the list during that iteration can throw `ConcurrentModificationException`. The safe habits are: use the iterator's own `remove`, collect removals and apply them after, or use `removeIf`. Watch concurrent modification during iteration — even on a single thread — because "concurrent" here means conflicting modifications of the collection's structure, not necessarily multiple threads.

What if we skip lists and keep resizing arrays by hand?

```java
String[] tags = new String[2];
// ... copy into a larger array every time the user adds a tag
```

It works until the copy logic drifts, or someone forgets to update a length variable. Lists exist so resizable ordered sequences stop being a DIY project.

A small product-shaped fragment ties it together:

```java
List<String> cart = new ArrayList<>();
cart.add("keyboard");
cart.add("cable");
cart.add("cable");              // duplicates allowed
String first = cart.get(0);
cart.removeIf(item -> item.equals("cable"));
```

The cart is ordered. Duplicate cables are two lines until we remove them. Index zero is still the first added item that remains. That is list thinking: sequence, not uniqueness, not key lookup.


Let's linger on the interface versus implementation choice with a method you might actually ship.

```java
public List<String> recentTags(int limit) {
    List<String> tags = new ArrayList<>(this.tags);
    Collections.reverse(tags);
    return tags.subList(0, Math.min(limit, tags.size()));
}
```

Callers receive a `List`. They do not need to know you used `ArrayList` internally. Tomorrow you might wrap with `Collections.unmodifiableList` or return `List.copyOf`. The contract stays "ordered sequence." That is what programming to `List` protects.

Index-heavy algorithms — binary search on a sorted list, jumping to the middle — favor `ArrayList` because `get` is constant time. If your code mostly walks from the ends and rarely jumps by index, you might revisit `LinkedList`, but only with measurements in hand. Most business services are index-and-iterate heavy, which is why the workhorse advice exists.

Also watch aliasing: `subList` views share structure with the backing list. Structural edits through the view or the parent can surprise you. When you need a true independent snapshot, copy into a new `ArrayList`.


Capacity tuning is optional knowledge, not day-one ceremony. `new ArrayList<>(200)` pre-sizes when you know an approximate count and want fewer internal copies. Premature capacity fiddling rarely matters next to clear code. Prefer clarity, then profile.

Duplicates in lists are not always accidents. Two identical order lines can be two units. Sets would collapse them wrongly. Choosing list versus set is choosing whether position and multiplicity matter. That product question comes before the import statement.


So let's reconnect the chain. Growing sequences outgrew arrays. `List` answered with ordered, duplicate-friendly collections. `ArrayList` became the default workhorse. `LinkedList` stayed a specialty tool. Programming to `List` kept APIs flexible. Iteration-modification rules kept us from surprising exceptions.

But sometimes duplicates are exactly what you do not want. A set of roles, a set of visited ids, a set of tags where "java" should appear once. How does Java say "unique membership"?

One more operational habit: prefer `List.of` and `List.copyOf` when the collection should not grow. Fixed lists fail fast on `add`, which is better than a mutable list that callers mutate by accident. Use `ArrayList` when growth is part of the feature. Choosing mutability on purpose is part of choosing a list.

That question opens Episode Twenty-Two — Sets.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 21 (*Lists*).

Narration technique: resizable sequence need → List/ArrayList → LinkedList rarity → program to interface → ConcurrentModification → next natural problem (uniqueness / sets). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- List is ordered and allows duplicates.
- ArrayList is the default workhorse.
- LinkedList rarely wins for typical access.
- Program to the List interface.
- Watch ConcurrentModification during iteration.
