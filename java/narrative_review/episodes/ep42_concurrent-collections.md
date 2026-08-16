# Episode 42 — Concurrent Collections

| Field | Value |
|---|---|
| Episode | 42 |
| Title | Concurrent Collections |
| Catalog handbook column | 42 |
| Narration source script | `make_episode_42.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Multiple threads reading and writing the same HashMap can corrupt it.
2. Synchronized wrappers lock the entire collection — every operation blocks.
3. Concurrent collections offer finer-grained safety without one global lock.
4. ConcurrentHashMap scales reads and writes across internal segments.
5. CopyOnWriteArrayList snapshots the backing array on each mutation.
6. Today — thread-safe collections and when each design wins.

### Scene `title` (renderer: `title`)

1. Episode Forty-Two.
2. Concurrent Collections.

### Scene `concurrent_hashmap` (renderer: `concurrent_hashmap`)

1. ConcurrentHashMap is the go-to concurrent map in Java.
2. It never throws ConcurrentModificationException on concurrent access.
3. Internal locking is segment-based — not one lock for the whole map.
4. get is usually lock-free. put and remove lock only a segment.
5. null keys and null values are not permitted — unlike HashMap.
6. Use ConcurrentHashMap when many threads share a mutable map.

### Scene `copy_on_write` (renderer: `copy_on_write`)

1. CopyOnWriteArrayList copies the entire array on every write.
2. Reads iterate a stable snapshot — no locks during traversal.
3. Writes are expensive — copy plus replace the reference.
4. Perfect when reads vastly outnumber writes — listener lists, caches.
5. Iterator never throws ConcurrentModificationException.
6. Do not use for write-heavy workloads — copying dominates.

### Scene `thread_safe_queues` (renderer: `thread_safe_queues`)

1. ConcurrentLinkedQueue — lock-free linked nodes for high-throughput queues.
2. BlockingQueue variants add wait and notify semantics — covered next episode.
3. ConcurrentSkipListMap and ConcurrentSkipListSet offer sorted concurrent access.
4. Collections.synchronizedList wraps with a mutex — simple but coarse.
5. Prefer java.util.concurrent types over synchronized wrappers at scale.
6. Match the collection to your read-write ratio and ordering needs.

### Scene `vs_synchronized` (renderer: `vs_synchronized`)

1. Synchronized collections versus concurrent collections.
2. SynchronizedMap — one lock per operation — simple but contended.
3. ConcurrentHashMap — segmented or striped locking — scales better.
4. CopyOnWriteArrayList — no read locks — ideal for read-heavy lists.
5. Vector and synchronized ArrayList block every reader and writer.
6. Legacy wrappers still appear — know the modern replacements.

### Scene `when_use` (renderer: `when_use`)

1. When to choose each concurrent collection.
2. Shared cache or registry — ConcurrentHashMap.
3. Event listeners or config snapshots — CopyOnWriteArrayList.
4. High-throughput work queues — ConcurrentLinkedQueue.
5. Sorted concurrent map — ConcurrentSkipListMap.
6. When not — single-threaded code — plain HashMap is faster.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using HashMap from multiple threads without external locking.
3. Two — CopyOnWriteArrayList for write-heavy lists — copies explode.
4. Three — assuming compound actions are atomic — check-then-act needs care.
5. Also — iterating a synchronized list without holding its lock.
6. Concurrent collections help — but logical consistency is still your job.

### Scene `interview` (renderer: `interview`)

1. Interview question — ConcurrentHashMap versus synchronized HashMap?
2. ConcurrentHashMap uses finer locking — better scalability under contention.
3. No ConcurrentModificationException on concurrent iteration patterns.
4. Null keys and values forbidden — enforced at API level.
5. CopyOnWriteArrayList for read-heavy, rarely mutated lists.
6. Mention when synchronized wrappers are still acceptable — low contention.

### Scene `teaser` (renderer: `teaser`)

1. Collections protect shared structures. What about single counters?
2. Episode Forty-Three — Atomic Variables.
3. AtomicInteger, compare-and-swap, and lock-free updates.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **42** — *Concurrent Collections*.
- **Series catalog:** Episode 42 ↔ handbook lesson 42 — *Concurrent Collections*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Multiple threads reading and writing the same HashMap can corrupt it._
- **`title`** — starts from: _Episode Forty-Two._
- **`concurrent_hashmap`** — starts from: _ConcurrentHashMap is the go-to concurrent map in Java._
- **`copy_on_write`** — starts from: _CopyOnWriteArrayList copies the entire array on every write._
- **`thread_safe_queues`** — starts from: _ConcurrentLinkedQueue — lock-free linked nodes for high-throughput queues._
- **`vs_synchronized`** — starts from: _Synchronized collections versus concurrent collections._
- **`when_use`** — starts from: _When to choose each concurrent collection._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — ConcurrentHashMap versus synchronized HashMap?_
- **`teaser`** — starts from: _Collections protect shared structures. What about single counters?_
