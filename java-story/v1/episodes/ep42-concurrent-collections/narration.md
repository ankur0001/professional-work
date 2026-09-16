# Episode 42 — Concurrent Collections

**Cut:** v1 (original)

## Transcript (from captions)

Multiple threads reading and writing the same HashMap can corrupt it. Synchronized wrappers lock the entire collection — every operation blocks. Concurrent collections offer finer-grained safety without one global lock.

ConcurrentHashMap scales reads and writes across internal segments. CopyOnWriteArrayList snapshots the backing array on each mutation. Today — thread-safe collections and when each design wins.

Episode Forty-Two. Concurrent Collections. ConcurrentHashMap is the go-to concurrent map in Java. It never throws ConcurrentModificationException on concurrent access. Internal locking is segment-based — not one lock for the whole map.

get is usually lock-free. put and remove lock only a segment. null keys and null values are not permitted — unlike HashMap. Use ConcurrentHashMap when many threads share a mutable map.

CopyOnWriteArrayList copies the entire array on every write. Reads iterate a stable snapshot — no locks during traversal. Writes are expensive — copy plus replace the reference. Perfect when reads vastly outnumber writes — listener lists, caches.

Iterator never throws ConcurrentModificationException. Do not use for write-heavy workloads — copying dominates. ConcurrentLinkedQueue — lock-free linked nodes for high-throughput queues.

BlockingQueue variants add wait and notify semantics — covered next episode. ConcurrentSkipListMap and ConcurrentSkipListSet offer sorted concurrent access. Collections.synchronizedList wraps with a mutex — simple but coarse.

Prefer java.util.concurrent types over synchronized wrappers at scale. Match the collection to your read-write ratio and ordering needs. Synchronized collections versus concurrent collections.

SynchronizedMap — one lock per operation — simple but contended. ConcurrentHashMap — segmented or striped locking — scales better. CopyOnWriteArrayList — no read locks — ideal for read-heavy lists.

Vector and synchronized ArrayList block every reader and writer. Legacy wrappers still appear — know the modern replacements. When to choose each concurrent collection. Shared cache or registry — ConcurrentHashMap.

Event listeners or config snapshots — CopyOnWriteArrayList. High-throughput work queues — ConcurrentLinkedQueue. Sorted concurrent map — ConcurrentSkipListMap. When not — single-threaded code — plain HashMap is faster.

Three common mistakes. One — using HashMap from multiple threads without external locking. Two — CopyOnWriteArrayList for write-heavy lists — copies explode. Three — assuming compound actions are atomic — check-then-act needs care.

Also — iterating a synchronized list without holding its lock. Concurrent collections help — but logical consistency is still your job. Interview question — ConcurrentHashMap versus synchronized HashMap?

ConcurrentHashMap uses finer locking — better scalability under contention. No ConcurrentModificationException on concurrent iteration patterns. Null keys and values forbidden — enforced at API level.

CopyOnWriteArrayList for read-heavy, rarely mutated lists. Mention when synchronized wrappers are still acceptable — low contention. Collections protect shared structures. What about single counters?

Episode Forty-Three — Atomic Variables. AtomicInteger, compare-and-swap, and lock-free updates. See you there.
