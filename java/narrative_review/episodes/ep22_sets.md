# Episode 22 — Sets

| Field | Value |
|---|---|
| Episode | 22 |
| Title | Sets |
| Catalog handbook column | 22 |
| Narration source script | `make_episode_22.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Lists keep order and duplicates. Sets answer a different question.
2. Is this value already in the collection — yes or no?
3. Uniqueness is the product. Membership is the verb.
4. HashSet. LinkedHashSet. TreeSet. Same contract — different trade-offs.
5. Today we pick the right Set for the job.
6. One of each — with rules you must respect.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Two.
2. Sets — uniqueness in java.util.

### Scene `contract` (renderer: `contract`)

1. Set is a Collection that forbids duplicates.
2. Whether two elements collide is decided by equals — not by ==.
3. There is no get by index. You ask contains.
4. Iteration order depends on the implementation you chose.
5. Prefer the Set interface in APIs until performance forces a concrete type.
6. Model membership. Do not pretend it is a list.

### Scene `hashset` (renderer: `hashset`)

1. HashSet is the default for most uniqueness needs.
2. It uses hashing for average constant-time add, remove, and contains.
3. Do not rely on iteration order — it is not a feature.
4. Your element type must honor equals and hashCode together.
5. Mutable fields that participate in equals make sets unstable.
6. For fast membership tests, start with HashSet.

### Scene `ordered` (renderer: `ordered`)

1. When order matters, reach for a sibling.
2. LinkedHashSet preserves insertion order while keeping hash performance.
3. TreeSet keeps elements sorted — natural order or a Comparator.
4. Tree operations are logarithmic — fine, until you pretend they are free.
5. Need sorted ranges or first and last — TreeSet earns its keep.
6. Need stable encounter order — LinkedHashSet is cleaner than sorting later.

### Scene `equals` (renderer: `equals`)

1. The silent dependency — equals and hashCode.
2. If two objects are equal, their hash codes must match.
3. Break that contract and HashSet will lose or duplicate your data.
4. TreeSet uses compareTo or a Comparator — consistency with equals still matters.
5. Immutable value types make safer set elements.
6. Identity is a design decision. Sets enforce it ruthlessly.

### Scene `choose` (renderer: `choose`)

1. How to choose.
2. Pure membership, order irrelevant — HashSet.
3. Need predictable iteration in insertion order — LinkedHashSet.
4. Need sorted traversal or range queries — TreeSet.
5. Set.of gives an unmodifiable set — great for constants.
6. Choose for access pattern, not for how advanced the class name sounds.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — putting mutable objects in a HashSet, then mutating their keys.
3. Two — implementing equals without hashCode — or the reverse.
4. Three — using TreeSet with types that have no natural ordering.
5. Also — expecting HashSet iteration to stay stable across JVMs.
6. Sets are simple. Contracts are not optional.

### Scene `interview` (renderer: `interview`)

1. Interview question — HashSet versus LinkedHashSet versus TreeSet?
2. HashSet — fastest typical membership, no order guarantees.
3. LinkedHashSet — hash performance with insertion-order iteration.
4. TreeSet — sorted, logarithmic, needs ordering rules.
5. Mention equals and hashCode — interviewers listen for that.
6. That answer shows judgment, not memorization.

### Scene `teaser` (renderer: `teaser`)

1. Uniqueness is clear. Next — associating keys with values.
2. Episode Twenty-Three — Maps.
3. HashMap realities, ordering variants, and null rules.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **23** — *Set*.
- **Series catalog mapping:** Episode 22 / catalog column `22` / published title *Sets*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 23 → episode 22). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Lists keep order and duplicates. Sets answer a different question._
- **`title`** — starts from: _Episode Twenty-Two._
- **`contract`** — starts from: _Set is a Collection that forbids duplicates._
- **`hashset`** — starts from: _HashSet is the default for most uniqueness needs._
- **`ordered`** — starts from: _When order matters, reach for a sibling._
- **`equals`** — starts from: _The silent dependency — equals and hashCode._
- **`choose`** — starts from: _How to choose._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — HashSet versus LinkedHashSet versus TreeSet?_
- **`teaser`** — starts from: _Uniqueness is clear. Next — associating keys with values._
