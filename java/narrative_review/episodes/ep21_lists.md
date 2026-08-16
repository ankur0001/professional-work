# Episode 21 — Lists

| Field | Value |
|---|---|
| Episode | 21 |
| Title | Lists |
| Catalog handbook column | 21 |
| Narration source script | `make_episode_21.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Modules draw boundaries. Collections fill the day-to-day work.
2. Almost every Java program needs an ordered sequence of values.
3. That is the List interface — indexed, ordered, and everywhere.
4. ArrayList. LinkedList. When each one earns its keep.
5. Today we choose lists with intent — not habit.
6. Order with random access — or order with cheap inserts. Know the trade.

### Scene `title` (renderer: `title`)

1. Episode Twenty-One.
2. Lists — ordered collections in java.util.

### Scene `contract` (renderer: `contract`)

1. List is a contract in java.util.
2. Elements have positions — zero-based indexes.
3. Duplicates are allowed. Null may be allowed depending on the implementation.
4. add, get, set, remove, size, contains — the verbs you already know.
5. Prefer coding to List, not to a concrete class — until performance forces a choice.
6. The interface keeps your API flexible.

### Scene `arraylist` (renderer: `arraylist`)

1. ArrayList is the default workhorse.
2. Backed by a resizable array. Amortized constant-time append at the end.
3. Random access by index is fast — get and set are essentially array ops.
4. Inserts and removes in the middle shift elements — that can get expensive.
5. Give an initial capacity when you know the size roughly.
6. For most application lists, start here.

### Scene `linked` (renderer: `linked`)

1. LinkedList is a doubly linked structure.
2. Cheap inserts and removes when you already hold the right node position.
3. Random access by index walks the chain — do not pretend it is an array.
4. It also implements Queue and Deque — useful as a deque more than as a random-access list.
5. If you mainly get by index, LinkedList is usually the wrong tool.
6. Measure the access pattern before you romanticize pointers.

### Scene `choose` (renderer: `choose`)

1. How to choose.
2. Most reads by index, appends at the end — ArrayList.
3. Heavy middle inserts with sequential traversal — consider LinkedList, or rethink the model.
4. Often a better answer is a different structure — Queue, Deque, or a map.
5. Do not pick LinkedList because it sounds advanced.
6. Pick the structure that matches how you touch the data.

### Scene `pitfalls` (renderer: `pitfalls`)

1. List pitfalls that show up in reviews.
2. Modifying a list while iterating with a for-each — ConcurrentModificationException risk.
3. Use an Iterator remove, or collect changes and apply after.
4. Arrays.asList returns a fixed-size list backed by an array — not a fully mutable ArrayList.
5. List.of creates unmodifiable lists — great for constants, surprising if you call add.
6. Know whether your list is growable before you mutate it.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — LinkedList everywhere for inserts that never happen in the middle.
3. Two — raw types — List without generics — type safety thrown away.
4. Three — exposing a mutable ArrayList from an API that should return an unmodifiable view.
5. Also — ignoring equals contract when lists hold custom types.
6. Lists are simple. Careless APIs make them expensive.

### Scene `interview` (renderer: `interview`)

1. Interview question — ArrayList versus LinkedList?
2. ArrayList — array-backed, fast index access, costly middle inserts.
3. LinkedList — node-backed, weak random access, better as a deque sometimes.
4. Default choice in apps is almost always ArrayList.
5. Mention Big-O briefly, then talk about real access patterns.
6. That answer is practical — not textbook theater.

### Scene `teaser` (renderer: `teaser`)

1. Ordered sequences are clear. Next — uniqueness and hashing.
2. Episode Twenty-Two — Sets.
3. HashSet, LinkedHashSet, TreeSet — and when order matters.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **22** — *List*.
- **Series catalog mapping:** Episode 21 / catalog column `21` / published title *Lists*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 22 → episode 21). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Modules draw boundaries. Collections fill the day-to-day work._
- **`title`** — starts from: _Episode Twenty-One._
- **`contract`** — starts from: _List is a contract in java.util._
- **`arraylist`** — starts from: _ArrayList is the default workhorse._
- **`linked`** — starts from: _LinkedList is a doubly linked structure._
- **`choose`** — starts from: _How to choose._
- **`pitfalls`** — starts from: _List pitfalls that show up in reviews._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — ArrayList versus LinkedList?_
- **`teaser`** — starts from: _Ordered sequences are clear. Next — uniqueness and hashing._
