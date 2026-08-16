# Episode 23 — Maps

| Field | Value |
|---|---|
| Episode | 23 |
| Title | Maps |
| Catalog handbook column | 23 |
| Narration source script | `make_episode_23.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Sets answer membership. Maps answer association.
2. Given this key — what value belongs with it?
3. Lookups, caches, indexes, configuration — maps are everywhere.
4. HashMap is the workhorse. Ordering variants exist for a reason.
5. Today — Map contracts, null rules, and modern helpers.
6. Keys find values. Contracts keep them honest.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Three.
2. Maps — key to value in java.util.

### Scene `contract` (renderer: `contract`)

1. Map is not a Collection — it is its own hierarchy.
2. Each key maps to at most one value.
3. put replaces. get returns null when absent — or when the value is null.
4. Views matter — keySet, values, and entrySet share the underlying map.
5. Mutating a view mutates the map. That surprise shows up in code reviews.
6. Model associations. Do not stuff pairs into a list forever.

### Scene `hashmap` (renderer: `hashmap`)

1. HashMap is the default map for single-threaded use.
2. Average constant-time put and get when hashing behaves.
3. Keys need equals and hashCode — same story as HashSet.
4. One null key is allowed. Many null values are allowed.
5. Prefer computeIfAbsent and merge over get-then-put races of logic.
6. For most application maps, start here.

### Scene `variants` (renderer: `variants`)

1. Ordering and specialized maps.
2. LinkedHashMap preserves insertion order — or access order for LRU-style caches.
3. TreeMap keeps keys sorted — natural order or Comparator.
4. EnumMap is compact and fast when keys are enum constants.
5. IdentityHashMap uses reference equality — rare, sharp tool.
6. Pick the variant that matches your iteration and key domain.

### Scene `nulls` (renderer: `nulls`)

1. Null rules are implementation-specific.
2. HashMap tolerates a null key. TreeMap does not.
3. Hashtable rejects nulls entirely — and brings legacy synchronization.
4. Never assume null policy from the Map interface alone.
5. In modern code, ConcurrentHashMap also rejects nulls.
6. Read the implementation before you lean on null as a signal.

### Scene `modern` (renderer: `modern`)

1. Modern Map APIs reduce boilerplate bugs.
2. getOrDefault avoids null checks for simple fallbacks.
3. computeIfAbsent builds values lazily and cleanly.
4. merge combines values with an explicit remapping function.
5. Map.of and Map.copyOf create unmodifiable maps for safer APIs.
6. Prefer these helpers over fragile get-then-mutate sequences.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — mutable keys whose equals fields change after insertion.
3. Two — modifying a map while iterating its keySet carelessly.
4. Three — reaching for Hashtable in new code out of habit.
5. Also — using null values as a secret third state without documenting it.
6. Maps amplify clear key design — and punish sloppy identity.

### Scene `interview` (renderer: `interview`)

1. Interview question — how does HashMap work, and when TreeMap?
2. HashMap — hash buckets, equals for collisions, average O(1).
3. TreeMap — red-black tree, sorted keys, logarithmic ops.
4. Call out mutable keys and null differences.
5. Mention LinkedHashMap if they ask about predictable order.
6. That answer is solid for junior and mid-level interviews.

### Scene `teaser` (renderer: `teaser`)

1. Associations are clear. Next — waiting lines and two-ended queues.
2. Episode Twenty-Four — Queues and Deques.
3. FIFO, stacks, and why ArrayDeque wins often.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **25** — *Map*.
- **Series catalog mapping:** Episode 23 / catalog column `23` / published title *Maps*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 25 → episode 23). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Sets answer membership. Maps answer association._
- **`title`** — starts from: _Episode Twenty-Three._
- **`contract`** — starts from: _Map is not a Collection — it is its own hierarchy._
- **`hashmap`** — starts from: _HashMap is the default map for single-threaded use._
- **`variants`** — starts from: _Ordering and specialized maps._
- **`nulls`** — starts from: _Null rules are implementation-specific._
- **`modern`** — starts from: _Modern Map APIs reduce boilerplate bugs._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how does HashMap work, and when TreeMap?_
- **`teaser`** — starts from: _Associations are clear. Next — waiting lines and two-ended queues._
