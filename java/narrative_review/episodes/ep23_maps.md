# Episode 23 — Maps

| Field | Value |
|---|---|
| Episode | 23 |
| Title | Maps |
| Catalog handbook column | 23 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Sets answered uniqueness. They do not answer the everyday business question: given this key, what value sits beside it?

Imagine a phone book, a cache of user ids to profiles, a dictionary of sku to quantity. You can fake it with two lists — keys in one, values in the other — and pray the indexes stay aligned. Or you can search a list of pairs. Both get painful. The natural question is: where is the lookup engine?

Maps are that engine. A map stores key-to-value associations. Keys hash into buckets in a `HashMap`. A good key's `equals` and `hashCode` decide both placement and retrieval, just as they did for sets.

```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Ada", 36);
int v = ages.getOrDefault("Ada", 0);
```

Walk it. `put` associates `"Ada"` with `36`. `getOrDefault` returns the value if present, otherwise the default you supply — here `0`. That single method prevents a pile of null checks when missing keys are normal. Maps are the lookup engine of business logic because so many rules are "look up X, then decide."

Three workhorse methods show up constantly once you live in map-shaped code: `getOrDefault`, `computeIfAbsent`, and `merge`.

```java
Map<String, List<String>> index = new HashMap<>();
index.computeIfAbsent("java", k -> new ArrayList<>()).add("ep23");

Map<String, Integer> counts = new HashMap<>();
counts.merge("ada", 1, Integer::sum);
counts.merge("ada", 1, Integer::sum);   // ada → 2
```

`computeIfAbsent` builds a value only when the key is missing — perfect for multimap-style indexes. `merge` combines a new contribution with an existing value through a function; counting and aggregating become one readable line instead of get-null-check-put boilerplate.

Null rules depend on the implementation. `HashMap` allows one null key and null values. `Hashtable` and `ConcurrentHashMap` do not play the same null game. `TreeMap` rejects null keys under natural ordering. Do not assume "maps allow null" as a universal law — read the implementation you chose.

Order is another axis:

```java
Map<String, Integer> linked = new LinkedHashMap<>(); // insertion (or access) order
Map<String, Integer> tree = new TreeMap<>();         // sorted by key
```

`LinkedHashMap` preserves order — useful for stable iteration, LRU-style access-order caches, and predictable output. `TreeMap` sorts by key, with the same comparator-consistency caveats you met for `TreeSet`. Pick the map that matches the question you ask: fast unordered lookup, ordered iteration, or sorted keys.

A small inventory fragment shows why maps replace parallel lists:

```java
Map<String, Integer> stock = new HashMap<>();
stock.put("SKU-1", 10);
stock.put("SKU-2", 0);

int available = stock.getOrDefault("SKU-1", 0);
stock.merge("SKU-1", -1, Integer::sum);   // sell one
```

The sku is the key. Quantity is the value. There is no second list to keep in sync. Missing skus default safely. Updates speak in merge language.

What about concurrency? Concurrent maps come later for shared mutation. A plain `HashMap` is not safe for multi-threaded writes. If two threads resize or update together, you can corrupt the structure. For now, treat maps as single-threaded unless you reach for a concurrent variant on purpose. That warning is enough to stop a common production accident without derailing today's lesson.

What if we skip maps and search lists?

```java
for (User u : users) {
    if (u.id().equals(id)) return u;
}
```

Fine at dozens. Painful at hundreds of thousands. Maps exist so average lookup cost stays sensible when the key is known.


Hashing deserves a plain-language picture. A key's `hashCode` selects a bucket. Within the bucket, `equals` finds the exact entry. Bad hash distributions — every key hashing to the same value — turn a map into a slow list. You rarely write hash functions for strings, but for custom keys you inherit the same duty you saw with sets: equal objects, equal hashes.

```java
Map<String, Integer> ages = new HashMap<>();
ages.put("Ada", 36);
ages.put("Ada", 37);   // replaces, does not duplicate
System.out.println(ages.get("Ada")); // 37
```

Keys are unique. A second `put` with the same key replaces the value. That is different from a list of pairs that could hold Ada twice. If you need multi-values per key, use `computeIfAbsent` with a collection value — a multimap pattern — rather than expecting `HashMap` to keep duplicates.

When iterating, prefer `entrySet()` when you need both key and value, so you do not re-get by key on each step. Small habits like that keep map-heavy services honest under load.


`keySet`, `values`, and `entrySet` are views backed by the map. Remove from the key set and the map loses the entry. Clear that relationship in your mind before treating those collections as independent copies. When you need a snapshot for safe later mutation, copy deliberately.

For counting and histograms, `merge` with `Integer::sum` beats handwritten get-and-put. For indexes of lists, `computeIfAbsent` beats null checks. Learn those two deeply and a surprising fraction of map boilerplate disappears.


So let's reconnect the chain. Keyed lookup outgrew lists and sets. Maps answered with hashed associations. `getOrDefault`, `computeIfAbsent`, and `merge` removed boilerplate. Null and ordering rules depended on the implementation. Concurrent mutation was flagged for later.

Sometimes the problem is not lookup by key, but flow: work waiting to be processed, messages waiting to be handled, undo history waiting to rewind. That is a different shape — first-in-first-out, or double-ended access.

Caches, indexes, and configuration tables are map-shaped thoughts. When you catch yourself looping to find an object by id for the third time in a module, stop and build a map once. The collection choice documents the access pattern for the next reader — lookup, not scan.

That shape is Episode Twenty-Four — Queues and Deques.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 23 (*Maps*).

Narration technique: keyed-lookup need → HashMap basics → workhorse methods → null/order variants → concurrency caution → next natural problem (flow / queues). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Keys hash into buckets.
- getOrDefault/computeIfAbsent/merge are workhorses.
- null key/value rules depend on implementation.
- LinkedHashMap preserves order; TreeMap sorts.
- Concurrent maps come later for shared mutation.
