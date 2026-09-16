# Episode 25 — Sorting and Comparators

**Cut:** v1 (original)

## Transcript (from captions)

Queues move work. Sorting decides presentation and priority. Order is not decoration — it is a policy your types must support. Comparable for natural order. Comparator for strategies.

Stability, equals consistency, and the APIs that actually sort. Today — making order explicit and safe. Sorted data is a contract — not a happy accident. Episode Twenty-Five. Sorting and Comparators.

Comparable defines a type's natural order. compareTo returns negative, zero, or positive. Strings and numbers already have natural orders. Domain types should only implement Comparable when one obvious order exists.

TreeSet and TreeMap rely on that ordering for structure. Natural order is a product decision — treat it that way. Comparator lives outside the type. Use it when many sort orders are valid — by name, by date, by score.

Comparator.comparing and thenComparing compose cleanly. reversed flips direction without rewriting logic. Pass comparators into sort, TreeMap, and PriorityQueue. Strategy beats stuffing every order into compareTo.

Know the sort entry points. List.sort and Collections.sort sort lists in place. Arrays.sort handles object arrays and primitives. Stream.sorted sorts inside a pipeline — useful, not always cheapest.

Object sorts use TimSort — stable for equal elements. Pick the API that matches where your data already lives. Stability matters when you sort by secondary keys. A stable sort keeps equal elements in their prior relative order.

That lets you sort by last name, then by first name, in stages. Object sorts in the JDK are stable. Primitive sorts may differ. Do not assume stability without knowing the algorithm.

Multi-key Comparator.comparing chains make intent clearer anyway. compareTo should be consistent with equals when used in sorted sets and maps. If compareTo says zero, equals should usually say true.

Break that and TreeSet may treat unequal business objects as duplicates. If you must diverge, document it loudly and avoid sorted sets. Hash-based collections still need equals and hashCode — sorting does not replace them.

Contracts stack. Respect all of them. Three common mistakes. One — compareTo that disagrees with equals without documentation. Two — sorting by mutable fields that change after insertion into a TreeSet.

Three — giant compareTo methods instead of composed Comparators. Also — assuming Stream.sorted is free on huge collections. Clear ordering code is easier to trust than clever ordering code.

Interview question — Comparable versus Comparator? Comparable — natural order implemented by the class itself. Comparator — external ordering strategy, often multiple per type. Mention stability and equals consistency for bonus points.

Give a domain example — sort users by name versus by created date. That answer is interview-ready. Ordering is explicit. Next — processing collections as pipelines. Episode Twenty-Six — Streams introduction.

Map, filter, reduce — and laziness that matters. See you there.
