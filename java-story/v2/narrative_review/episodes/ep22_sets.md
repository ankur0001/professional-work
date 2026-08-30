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

Suppose you store roles in a list and check membership with `contains` before every `add`. It works for tiny data and becomes awkward as rules grow. The natural question is: is there a collection whose whole point is uniqueness?

That collection is a `Set`. Set means uniqueness — and uniqueness means `equals`/`hashCode` discipline.

```java
Set<String> set = new HashSet<>();
set.add("a");
set.add("a");
System.out.println(set.size());   // 1
```

Walk it. The first `add` inserts `"a"`. The second `add` sees an equal element already present and leaves the set unchanged. Size stays one. If you needed two entries, you wanted a list.

Under a `HashSet`, uniqueness is decided by hashing into buckets, then confirming with `equals`. If two objects are equal, they must share a hash code. If you break that contract, a set can hold what looks like duplicates, or fail to find what you just inserted. For your own classes, implementing `equals` and `hashCode` together is not optional decoration.

Different set implementations trade properties:

```java
Set<String> hash = new HashSet<>();           // fast, no order promise
Set<String> linked = new LinkedHashSet<>();   // keeps insertion order
Set<String> sorted = new TreeSet<>();         // sorted order
```

`HashSet` is the common default when you only care about membership. `LinkedHashSet` preserves insertion order. `TreeSet` keeps elements sorted, which means it needs a consistent ordering — natural `Comparable` order or an explicit `Comparator`. If the comparator says two elements are equal for ordering purposes, the set treats them as duplicates even if `equals` would disagree.

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

`removeAll`, `retainAll`, and `addAll` express difference, intersection, and union. Permission checks and feature flag merges sound like set talk once you stop forcing lists to pretend.

One sharp edge: do not mutate fields used in hashing while an object sits in a set.

```java
Set<User> users = new HashSet<>();
User u = new User("ada");   // equals/hashCode based on name
users.add(u);
u.setName("grace");         // hash bucket is now wrong
users.contains(u);          // may fail mysteriously
```

After mutation, the object may live in the wrong bucket. Treat elements as effectively immutable while they are set members, or remove, mutate, and re-add.

What if we skip sets and keep unique lists by hand? Fine for one call site. Then five call sites forget the check. A set makes the rule structural instead of ceremonial.

Equality discipline with a domain type:

```java
record Role(String name) {}  // equals/hashCode from components

Set<Role> roles = new HashSet<>();
roles.add(new Role("ADMIN"));
roles.add(new Role("ADMIN"));
System.out.println(roles.size()); // 1
```

Because `Role` is a record, equal names compare equal and hash alike. A hand-written class that compares names in `equals` but forgets `name` in `hashCode` would break `HashSet` membership.

Iteration order stories cause flaky tests. A `HashSet` may print elements in different orders across runs. If a test asserts a stringified set, prefer `LinkedHashSet`, a sorted set, or compare as sets without relying on order.

Lists allowed duplicates; many domains forbid them. Sets answered with uniqueness via `equals`/`hashCode`. `HashSet`, `LinkedHashSet`, and `TreeSet` traded speed, insertion order, and sorted order. Mutating hashed fields showed a classic foot-gun.

Uniqueness of elements is still not lookup by key. Often you need "given a user id, find the user" or "given a sku, find the price." Searching a list linearly gets old fast. How does Java give us keyed lookup?

That is the pressure that brings maps.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 22 (*Sets*).

Narration technique: duplicate-pain situation → Set/hash contract → implementation trade-offs → set algebra → mutation foot-gun → next natural problem (keyed lookup / maps). Continuity-checked transitions.
