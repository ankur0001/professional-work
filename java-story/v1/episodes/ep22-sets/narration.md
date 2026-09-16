# Episode 22 — Sets

**Cut:** v1 (original)

## Transcript (from captions)

Lists keep order and duplicates. Sets answer a different question. Is this value already in the collection — yes or no? Uniqueness is the product. Membership is the verb. HashSet. LinkedHashSet. TreeSet. Same contract — different trade-offs.

Today we pick the right Set for the job. One of each — with rules you must respect. Episode Twenty-Two. Sets — uniqueness in java.util. Set is a Collection that forbids duplicates. Whether two elements collide is decided by equals — not by ==.

There is no get by index. You ask contains. Iteration order depends on the implementation you chose. Prefer the Set interface in APIs until performance forces a concrete type. Model membership. Do not pretend it is a list.

HashSet is the default for most uniqueness needs. It uses hashing for average constant-time add, remove, and contains. Do not rely on iteration order — it is not a feature. Your element type must honor equals and hashCode together.

Mutable fields that participate in equals make sets unstable. For fast membership tests, start with HashSet. When order matters, reach for a sibling. LinkedHashSet preserves insertion order while keeping hash performance.

TreeSet keeps elements sorted — natural order or a Comparator. Tree operations are logarithmic — fine, until you pretend they are free. Need sorted ranges or first and last — TreeSet earns its keep.

Need stable encounter order — LinkedHashSet is cleaner than sorting later. The silent dependency — equals and hashCode. If two objects are equal, their hash codes must match. Break that contract and HashSet will lose or duplicate your data.

TreeSet uses compareTo or a Comparator — consistency with equals still matters. Immutable value types make safer set elements. Identity is a design decision. Sets enforce it ruthlessly.

How to choose. Pure membership, order irrelevant — HashSet. Need predictable iteration in insertion order — LinkedHashSet. Need sorted traversal or range queries — TreeSet. Set.of gives an unmodifiable set — great for constants.

Choose for access pattern, not for how advanced the class name sounds. Three common mistakes. One — putting mutable objects in a HashSet, then mutating their keys. Two — implementing equals without hashCode — or the reverse.

Three — using TreeSet with types that have no natural ordering. Also — expecting HashSet iteration to stay stable across JVMs. Sets are simple. Contracts are not optional. Interview question — HashSet versus LinkedHashSet versus TreeSet?

HashSet — fastest typical membership, no order guarantees. LinkedHashSet — hash performance with insertion-order iteration. TreeSet — sorted, logarithmic, needs ordering rules. Mention equals and hashCode — interviewers listen for that.

That answer shows judgment, not memorization. Uniqueness is clear. Next — associating keys with values. Episode Twenty-Three — Maps. HashMap realities, ordering variants, and null rules.

See you there.
