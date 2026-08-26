# Episode 25 — Sorting and Comparators

| Field | Value |
|---|---|
| Episode | 25 |
| Title | Sorting and Comparators |
| Catalog handbook column | 25 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Queues ordered things by arrival. Users often want a different order: alphabetical names, cheapest price first, newest message on top. Sorting is comparison policy — make that policy explicit and consistent.

Suppose you have a list of users. One screen sorts by name. Another sorts by age, then name. If `User` hard-codes one `compareTo`, every screen fights over the "natural" order. The natural question is: can the collection stay dumb while the sort rule stays swappable?

Java splits that responsibility. `Comparable` means natural order — the type itself knows how it compares. `Comparator` means an external strategy — a separate rule you pass into `sort` or into sorted collections.

```java
record User(String name, int age) {}

List<User> list = new ArrayList<>();
list.add(new User("Zoe", 30));
list.add(new User("Ada", 36));
list.add(new User("Ada", 20));

list.sort(Comparator.comparing(User::name).thenComparingInt(User::age));
```

Walk the policy. `comparing(User::name)` sorts by name. `thenComparingInt(User::age)` breaks ties by age. Two Adas end up with age twenty before thirty-six. The list changes in place. The `User` type did not need to implement `Comparable`. The strategy lived at the call site — exactly where the screen's requirement lived.

`thenComparing` chains are how real sorts grow without becoming unreadable nests of manual `compare` methods. Start with the primary key, chain the secondary, reverse when needed with `reversed()`. Keep each piece a pure comparison: given two elements, return a negative number, zero, or positive — and do not mutate the world while deciding.

Natural order still matters when a type truly has one obvious sequence — integers, strings, enums, timestamps.

```java
record Ranked(String id, int score) implements Comparable<Ranked> {
    public int compareTo(Ranked other) {
        return Integer.compare(other.score, this.score); // higher score first
    }
}
```

Now `TreeSet` or `Collections.sort` can use that order without a separate comparator. Choose `Comparable` when the order is intrinsic. Choose `Comparator` when the order is contextual. Many types offer both: a natural order plus extra comparators for special views.

Consistency with `equals` matters for sorted sets and maps. If two elements compare as zero — "equal for sorting" — a `TreeSet` will treat them as duplicates even when `equals` says they differ. That mismatch drops data silently. When you design a comparator for sorted collections, align "compare to zero" with equality, or document carefully why you are using sorting structures only as sorted sequences and not as sets of unique domain identities.

Java's object sort uses TimSort, a stable mergesort variant. Stability means equal elements keep their relative order from before the sort. If two users share a name and you only sorted by name, their previous relative order survives. That property matters when you sort in stages or when "equal under this comparator" should not scramble an earlier arrangement.

What if comparison policy stays implicit?

```java
// scattered if/else comparing fields differently in three screens
```

Each screen invents a slightly different rule. One treats null names as first; another crashes. Extracting a named `Comparator` — even a static final field — makes the policy reviewable and reusable.

```java
static final Comparator<User> BY_NAME_THEN_AGE =
    Comparator.comparing(User::name).thenComparingInt(User::age);

list.sort(BY_NAME_THEN_AGE);
```

The name documents intent. Tests can assert order against that single definition.


Null-friendly comparators are another production detail. Real data has missing names.

```java
Comparator<User> byName = Comparator.comparing(
    User::name,
    Comparator.nullsLast(String::compareToIgnoreCase));
```

You declare where nulls go instead of crashing mid-sort. The policy stays explicit — the theme of this episode.

When sorting arrays, `Arrays.sort` uses the same comparator ideas. For primitives there is no comparator object; the order is numeric. For objects, TimSort's stability lets you sort by department first, then by name, in two passes, and keep department groups intact. One-pass `thenComparing` chains are clearer when you can write them; staged sorts remain a useful mental model for why stability matters.

Never write a `compare` method that returns only -1 or 1 and uses 0 rarely if at all — or worse, subtract ints and risk overflow. Prefer `Integer.compare`, `Comparator.comparingInt`, and friends.


Reverse order is a one-liner that teams reimplement constantly:

```java
list.sort(Comparator.comparing(User::age).reversed());
```

Chain carefully: `reversed()` reverses the whole comparator so far. For multi-key sorts, reverse the specific key with `Comparator.comparing(...).reversed().thenComparing(...)` patterns you can read aloud.

Comparators should be transitive and antisymmetric. Clever shortcuts that break the contract produce `TreeMap` corruption and infinite loops in theory, subtle mis-sorts in practice. Keep them boring.



Product language often hides multiple comparators behind one screen: "default sort" versus "advanced sort." Implement both as named constants and select explicitly. Hidden sort rules in random utility methods become archaeology. Sorting is policy — keep the policy where humans can find it.

So let's reconnect the chain. Arrival order was not enough. `Comparable` covered intrinsic order; `Comparator` covered external strategy. `thenComparing` chains expressed multi-key sorts. Consistency with `equals` protected sorted sets and maps. TimSort's stability explained why staged sorts behave calmly.

Once we can filter, transform, and sort collections, another itch appears: expressing bulk operations as a pipeline — "keep these, transform those, collect the result" — without handwriting every loop. That style has a name in modern Java.

Named comparators belong next to the domain type or in a small `Comparators` companion. Scattering lambdas across controllers guarantees drift. When product asks "sort like the admin table," you want one definition to point to — not three similar lambdas.

When sorting maps by value, extract entries to a list and sort with a comparator on `Entry.getValue()`. Maps themselves are not "sorted by value" structures; `TreeMap` sorts keys. Knowing which axis you sort prevents awkward API misuse.

```java
entries.sort(Map.Entry.comparingByValue());
```

Episode Twenty-Six introduces Streams.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 25 (*Sorting and Comparators*).

Narration technique: multi-screen sort conflict → Comparable vs Comparator → thenComparing walkthrough → equals consistency → TimSort stability → next natural problem (bulk pipelines / streams). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Comparable = natural order.
- Comparator = external strategy.
- thenComparing chains.
- Consistency with equals matters for sorted sets/maps.
- TimSort is stable for objects.
