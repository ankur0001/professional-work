# Episode 22 — Sets

| Field | Value |
|---|---|
| Episode | 22 |
| Title | Sets |
| Catalog handbook column | 22 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Lists proudly allow duplicates and remember order. The next product requirement often flips that pride into a bug: a user should have each role only once, a crawler should not visit the same url twice, a tag cloud should not print "java" three times.

Suppose you store roles in a list and check membership with `contains` before every `add`. It works for tiny data and becomes awkward as rules grow — intersections of permissions, differences of feature flags. The natural question is: is there a collection whose whole point is uniqueness?

That collection is a `Set`. Set means uniqueness — and uniqueness means `equals`/`hashCode` discipline.

```java
Set<String> set = new HashSet<>();
set.add("a");
set.add("a");
System.out.println(set.size());   // 1
```

Walk it. The first `add` inserts `"a"`. The second `add` sees an equal element already present and leaves the set unchanged. Size stays one. There is no "second slot" for the same value. If you needed two entries, you wanted a list.

Under a `HashSet`, uniqueness is decided by hashing into buckets, then confirming with `equals`. If two objects are equal, they must share a hash code. If you break that contract, a set can hold what looks like duplicates, or fail to find what you just inserted. For strings and other well-behaved library types you inherit good behavior. For your own classes, implementing `equals` and `hashCode` together is not optional decoration.

Different set implementations trade properties:

```java
Set<String> hash = new HashSet<>();           // fast, no order promise
Set<String> linked = new LinkedHashSet<>();   // keeps insertion order
Set<String> sorted = new TreeSet<>();         // sorted order
```

`HashSet` is the common default when you only care about membership. `LinkedHashSet` preserves insertion order — useful for "unique, but still stable when I iterate." `TreeSet` keeps elements sorted, which means it needs a consistent ordering — natural `Comparable` order or an explicit `Comparator`. Sorted order needs consistent comparators: if the comparator says two elements are equal for ordering purposes, the set treats them as duplicates even if `equals` would disagree. That inconsistency creates subtle bugs in sorted sets and maps.

Here is a domain-shaped example where set algebra shows up in real rules:

```java
Set<String> required = Set.of("READ", "WRITE");
Set<String> granted = new HashSet<>();
granted.add("READ");
granted.add("WRITE");
granted.add("EXECUTE");

Set<String> missing = new HashSet<>(required);
missing.removeAll(granted);   // empty → all required present

Set<String> extra = new HashSet<>(granted);
extra.removeAll(required);    // {"EXECUTE"}
```

`removeAll`, `retainAll`, and `addAll` express difference, intersection, and union. Permission checks, feature flag merges, and tag cleanup all sound like set talk once you stop forcing lists to pretend.

One sharp edge: do not mutate fields used in hashing while an object sits in a set.

```java
Set<User> users = new HashSet<>();
User u = new User("ada");   // equals/hashCode based on name
users.add(u);
u.setName("grace");         // hash bucket is now wrong
users.contains(u);          // may fail mysteriously
```

After mutation, the object may live in the wrong bucket. Membership checks become roulette. Treat elements as effectively immutable while they are set members, or remove, mutate, and re-add.

What if we skip sets and keep unique lists by hand?

```java
if (!roles.contains(role)) {
    roles.add(role);
}
```

Fine for one call site. Then five call sites forget the check. A set makes the rule structural instead of ceremonial.


Equality discipline deserves one more concrete walk-through with a domain type.

```java
record Role(String name) {}  // equals/hashCode from components

Set<Role> roles = new HashSet<>();
roles.add(new Role("ADMIN"));
roles.add(new Role("ADMIN"));
System.out.println(roles.size()); // 1
```

Because `Role` is a record, equal names compare equal and hash alike. A hand-written class that compares names in `equals` but forgets `name` in `hashCode` would break `HashSet` membership. When a set "sometimes contains" an object you just added, inspect the contract before blaming the collection.

`TreeSet` without a comparator requires elements to be `Comparable`. Dropping a non-comparable object in throws at runtime. If your sorted unique collection uses a comparator that ignores a field `equals` cares about, you can lose elements that were distinct by equality. Keep ordering and equality stories aligned when the structure is a set, not merely a sorted list substitute.


Iteration order stories cause flaky tests. A `HashSet` may print elements in different orders across JDK versions or runs. If a test asserts a stringified set, prefer `LinkedHashSet`, a sorted set, or compare as sets without relying on order. Flaky tests are often unordered-iteration tests in disguise.

Immutable sets from `Set.of` reject nulls and duplicates at creation — another way the platform pushes uniqueness early. Use them for fixed vocabularies of allowed values when an enum is too heavy.


So let's reconnect the chain. Lists allowed duplicates; many domains forbid them. Sets answered with uniqueness via `equals`/`hashCode`. `HashSet`, `LinkedHashSet`, and `TreeSet` traded speed, insertion order, and sorted order. Set algebra matched real permission and tag rules. Mutating hashed fields showed a classic foot-gun.

Uniqueness of elements is still not lookup by key. Often you need "given a user id, find the user" or "given a sku, find the price." Searching a list linearly gets old fast. How does Java give us keyed lookup?

In reviews, a `List` used only for membership tests is a smell pointing at a set. Linear `contains` on a growing list silently becomes a performance bug. Sets make the membership intent obvious and the average cost sensible. That clarity is as valuable as the uniqueness rule itself.

Set views from map key sets are a related trap: mutating them mutates the map. When you need an independent set of keys, copy. Shared views are powerful and easy to misuse — the same lesson as list `subList`, now in set clothing.

That is Episode Twenty-Three — Maps.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 22 (*Sets*).

Narration technique: duplicate-pain situation → Set/hash contract → implementation trade-offs → set algebra → mutation foot-gun → next natural problem (keyed lookup / maps). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Uniqueness via equals/hashCode.
- HashSet/LinkedHashSet/TreeSet trade-offs.
- Sorted order needs consistent comparators.
- Don't mutate fields used in hashing while in a set.
- Set algebra shows up in real domain rules.
