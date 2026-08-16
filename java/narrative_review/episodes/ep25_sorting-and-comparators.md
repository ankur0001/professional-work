# Episode 25 — Sorting and Comparators

| Field | Value |
|---|---|
| Episode | 25 |
| Title | Sorting and Comparators |
| Catalog handbook column | 25 |
| Narration source script | `make_episode_25.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Queues move work. Sorting decides presentation and priority.
2. Order is not decoration — it is a policy your types must support.
3. Comparable for natural order. Comparator for strategies.
4. Stability, equals consistency, and the APIs that actually sort.
5. Today — making order explicit and safe.
6. Sorted data is a contract — not a happy accident.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Five.
2. Sorting and Comparators.

### Scene `comparable` (renderer: `comparable`)

1. Comparable defines a type's natural order.
2. compareTo returns negative, zero, or positive.
3. Strings and numbers already have natural orders.
4. Domain types should only implement Comparable when one obvious order exists.
5. TreeSet and TreeMap rely on that ordering for structure.
6. Natural order is a product decision — treat it that way.

### Scene `comparator` (renderer: `comparator`)

1. Comparator lives outside the type.
2. Use it when many sort orders are valid — by name, by date, by score.
3. Comparator.comparing and thenComparing compose cleanly.
4. reversed flips direction without rewriting logic.
5. Pass comparators into sort, TreeMap, and PriorityQueue.
6. Strategy beats stuffing every order into compareTo.

### Scene `sortapi` (renderer: `sortapi`)

1. Know the sort entry points.
2. List.sort and Collections.sort sort lists in place.
3. Arrays.sort handles object arrays and primitives.
4. Stream.sorted sorts inside a pipeline — useful, not always cheapest.
5. Object sorts use TimSort — stable for equal elements.
6. Pick the API that matches where your data already lives.

### Scene `stable` (renderer: `stable`)

1. Stability matters when you sort by secondary keys.
2. A stable sort keeps equal elements in their prior relative order.
3. That lets you sort by last name, then by first name, in stages.
4. Object sorts in the JDK are stable. Primitive sorts may differ.
5. Do not assume stability without knowing the algorithm.
6. Multi-key Comparator.comparing chains make intent clearer anyway.

### Scene `consistency` (renderer: `consistency`)

1. compareTo should be consistent with equals when used in sorted sets and maps.
2. If compareTo says zero, equals should usually say true.
3. Break that and TreeSet may treat unequal business objects as duplicates.
4. If you must diverge, document it loudly and avoid sorted sets.
5. Hash-based collections still need equals and hashCode — sorting does not replace them.
6. Contracts stack. Respect all of them.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — compareTo that disagrees with equals without documentation.
3. Two — sorting by mutable fields that change after insertion into a TreeSet.
4. Three — giant compareTo methods instead of composed Comparators.
5. Also — assuming Stream.sorted is free on huge collections.
6. Clear ordering code is easier to trust than clever ordering code.

### Scene `interview` (renderer: `interview`)

1. Interview question — Comparable versus Comparator?
2. Comparable — natural order implemented by the class itself.
3. Comparator — external ordering strategy, often multiple per type.
4. Mention stability and equals consistency for bonus points.
5. Give a domain example — sort users by name versus by created date.
6. That answer is interview-ready.

### Scene `teaser` (renderer: `teaser`)

1. Ordering is explicit. Next — processing collections as pipelines.
2. Episode Twenty-Six — Streams introduction.
3. Map, filter, reduce — and laziness that matters.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- Series catalog lists this episode under handbook column **25** with title **Sorting and Comparators**.
- Recovered handbook TOC does **not** contain a matching lesson title for this slot (curriculum was remapped for 4–5 minute YouTube pacing).
- Narration was **authored for on-screen visuals** using the episode topic as the outline; concepts reflect standard Java curriculum covered by the handbook’s surrounding lessons, not a verbatim paste.
