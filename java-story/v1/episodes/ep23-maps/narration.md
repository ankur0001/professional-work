# Episode 23 — Maps

**Cut:** v1 (original)

## Transcript (from captions)

Sets answer membership. Maps answer association. Given this key — what value belongs with it? Lookups, caches, indexes, configuration — maps are everywhere. HashMap is the workhorse. Ordering variants exist for a reason.

Today — Map contracts, null rules, and modern helpers. Keys find values. Contracts keep them honest. Episode Twenty-Three. Maps — key to value in java.util. Map is not a Collection — it is its own hierarchy.

Each key maps to at most one value. put replaces. get returns null when absent — or when the value is null. Views matter — keySet, values, and entrySet share the underlying map. Mutating a view mutates the map. That surprise shows up in code reviews.

Model associations. Do not stuff pairs into a list forever. HashMap is the default map for single-threaded use. Average constant-time put and get when hashing behaves. Keys need equals and hashCode — same story as HashSet.

One null key is allowed. Many null values are allowed. Prefer computeIfAbsent and merge over get-then-put races of logic. For most application maps, start here. Ordering and specialized maps.

LinkedHashMap preserves insertion order — or access order for LRU-style caches. TreeMap keeps keys sorted — natural order or Comparator. EnumMap is compact and fast when keys are enum constants.

IdentityHashMap uses reference equality — rare, sharp tool. Pick the variant that matches your iteration and key domain. Null rules are implementation-specific. HashMap tolerates a null key. TreeMap does not.

Hashtable rejects nulls entirely — and brings legacy synchronization. Never assume null policy from the Map interface alone. In modern code, ConcurrentHashMap also rejects nulls. Read the implementation before you lean on null as a signal.

Modern Map APIs reduce boilerplate bugs. getOrDefault avoids null checks for simple fallbacks. computeIfAbsent builds values lazily and cleanly. merge combines values with an explicit remapping function.

Map.of and Map.copyOf create unmodifiable maps for safer APIs. Prefer these helpers over fragile get-then-mutate sequences. Three common mistakes. One — mutable keys whose equals fields change after insertion.

Two — modifying a map while iterating its keySet carelessly. Three — reaching for Hashtable in new code out of habit. Also — using null values as a secret third state without documenting it.

Maps amplify clear key design — and punish sloppy identity. Interview question — how does HashMap work, and when TreeMap? HashMap — hash buckets, equals for collisions, average O(1).

TreeMap — red-black tree, sorted keys, logarithmic ops. Call out mutable keys and null differences. Mention LinkedHashMap if they ask about predictable order. That answer is solid for junior and mid-level interviews.

Associations are clear. Next — waiting lines and two-ended queues. Episode Twenty-Four — Queues and Deques. FIFO, stacks, and why ArrayDeque wins often. See you there.
