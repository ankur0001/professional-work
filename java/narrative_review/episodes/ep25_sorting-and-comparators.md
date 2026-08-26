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

Walk the policy. `comparing(User::name)` sorts by name. `thenComparingInt(User::age)` breaks ties by age. Two Adas end up with age twenty before thirty-six. The `User` type did not need to implement `Comparable`. The strategy lived at the call site — exactly where the screen's requirement lived.

`thenComparing` chains are how real sorts grow without becoming unreadable nests of manual `compare` methods. Start with the primary key, chain the secondary, reverse when needed with `reversed()`. Keep each piece a pure comparison: given two elements, return a negative number, zero, or positive — and do not mutate the world while deciding.

Natural order still matters when a type truly has one obvious sequence — integers, strings, enums, timestamps.

```java
record Ranked(String id, int score) implements Comparable<Ranked> {
    public int compareTo(Ranked other) {
        return Integer.compare(other.score, this.score); // higher score first
    }
}
```

Now `TreeSet` or `Collections.sort` can use that order without a separate comparator. Choose `Comparable` when the order is intrinsic. Choose `Comparator` when the order is contextual.

Consistency with `equals` matters for sorted sets and maps. If two elements compare as zero — "equal for sorting" — a `TreeSet` will treat them as duplicates even when `equals` says they differ. That mismatch drops data silently.

Java's object sort uses TimSort, a stable mergesort variant. Stability means equal elements keep their relative order from before the sort. That property matters when you sort in stages or when "equal under this comparator" should not scramble an earlier arrangement.

What if comparison policy stays implicit? Each screen invents a slightly different rule. Extracting a named `Comparator` makes the policy reviewable and reusable.

```java
static final Comparator<User> BY_NAME_THEN_AGE =
    Comparator.comparing(User::name).thenComparingInt(User::age);

list.sort(BY_NAME_THEN_AGE);
```

Null-friendly comparators are another production detail. Real data has missing names.

```java
Comparator<User> byName = Comparator.comparing(
    User::name,
    Comparator.nullsLast(String::compareToIgnoreCase));
```

You declare where nulls go instead of crashing mid-sort. Never write a `compare` method that subtracts ints and risk overflow — prefer `Integer.compare` and `Comparator.comparingInt`.

Reverse order is a one-liner:

```java
list.sort(Comparator.comparing(User::age).reversed());
```

Arrival order was not enough. `Comparable` covered intrinsic order; `Comparator` covered external strategy. `thenComparing` chains expressed multi-key sorts. Consistency with `equals` protected sorted sets and maps.

Once we can filter, transform, and sort collections, another itch appears: expressing bulk operations as a pipeline — "keep these, transform those, collect the result" — without handwriting every loop.

That style has a name in modern Java: streams.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 25 (*Sorting and Comparators*).

Narration technique: multi-screen sort conflict → Comparable vs Comparator → thenComparing walkthrough → equals consistency → TimSort stability → next natural problem (bulk pipelines / streams). Continuity-checked transitions.
