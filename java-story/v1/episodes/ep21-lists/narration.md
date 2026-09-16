# Episode 21 — Lists

**Cut:** v1 (original)

## Transcript (from captions)

Modules draw boundaries. Collections fill the day-to-day work. Almost every Java program needs an ordered sequence of values. That is the List interface — indexed, ordered, and everywhere.

ArrayList. LinkedList. When each one earns its keep. Today we choose lists with intent — not habit. Order with random access — or order with cheap inserts. Know the trade. Episode Twenty-One.

Lists — ordered collections in java.util. List is a contract in java.util. Elements have positions — zero-based indexes. Duplicates are allowed. Null may be allowed depending on the implementation.

add, get, set, remove, size, contains — the verbs you already know. Prefer coding to List, not to a concrete class — until performance forces a choice. The interface keeps your API flexible.

ArrayList is the default workhorse. Backed by a resizable array. Amortized constant-time append at the end. Random access by index is fast — get and set are essentially array ops. Inserts and removes in the middle shift elements — that can get expensive.

Give an initial capacity when you know the size roughly. For most application lists, start here. LinkedList is a doubly linked structure. Cheap inserts and removes when you already hold the right node position.

Random access by index walks the chain — do not pretend it is an array. It also implements Queue and Deque — useful as a deque more than as a random-access list. If you mainly get by index, LinkedList is usually the wrong tool.

Measure the access pattern before you romanticize pointers. How to choose. Most reads by index, appends at the end — ArrayList. Heavy middle inserts with sequential traversal — consider LinkedList, or rethink the model.

Often a better answer is a different structure — Queue, Deque, or a map. Do not pick LinkedList because it sounds advanced. Pick the structure that matches how you touch the data. List pitfalls that show up in reviews.

Modifying a list while iterating with a for-each — ConcurrentModificationException risk. Use an Iterator remove, or collect changes and apply after. Arrays.asList returns a fixed-size list backed by an array — not a fully mutable ArrayList.

List.of creates unmodifiable lists — great for constants, surprising if you call add. Know whether your list is growable before you mutate it. Three common mistakes. One — LinkedList everywhere for inserts that never happen in the middle.

Two — raw types — List without generics — type safety thrown away. Three — exposing a mutable ArrayList from an API that should return an unmodifiable view. Also — ignoring equals contract when lists hold custom types.

Lists are simple. Careless APIs make them expensive. Interview question — ArrayList versus LinkedList? ArrayList — array-backed, fast index access, costly middle inserts. LinkedList — node-backed, weak random access, better as a deque sometimes.

Default choice in apps is almost always ArrayList. Mention Big-O briefly, then talk about real access patterns. That answer is practical — not textbook theater. Ordered sequences are clear. Next — uniqueness and hashing.

Episode Twenty-Two — Sets. HashSet, LinkedHashSet, TreeSet — and when order matters. See you there.
