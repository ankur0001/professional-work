# Episode 61 — Reference Types

| Field | Value |
|---|---|
| Episode | 61 |
| Title | Reference Types |
| Catalog handbook column | 61 |
| Narration source script | `make_episode_61.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty covered metaspace and native memory beyond the heap.
2. Strong references keep objects alive until nothing points to them.
3. But Java offers weaker reference types with different GC contracts.
4. Soft, Weak, and Phantom references let you build caches and cleanup hooks.
5. ReferenceQueue notifies you when the referent is collected.
6. Today — soft, weak, and phantom references, caches, and cleanup patterns.

### Scene `title` (renderer: `title`)

1. Episode Sixty-One.
2. Soft, Weak, and Phantom References.

### Scene `reference_hierarchy` (renderer: `reference_hierarchy`)

1. Four reference strengths from strongest to weakest.
2. Strong reference — normal variable assignment — never collected while reachable.
3. Soft reference — collected only when memory is tight — good for caches.
4. Weak reference — collected at next GC regardless of memory pressure.
5. Phantom reference — collected after finalization — for native resource cleanup.
6. Each type extends Reference<T> with different enqueue behavior.

### Scene `soft_weak_use` (renderer: `soft_weak_use`)

1. SoftReference — ideal for memory-sensitive caches.
2. JVM keeps soft referents until heap is nearly full, then clears them.
3. LinkedHashMap plus SoftReference — simple image or parsed-data cache.
4. WeakReference — canonical mappings that should not prevent GC.
5. WeakHashMap uses weak keys — entries vanish when key is only weakly reachable.
6. Do not rely on reference clearing for correctness — always have a fallback.

### Scene `phantom_cleanup` (renderer: `phantom_cleanup`)

1. PhantomReference — referent is not accessible through the reference itself.
2. Used with ReferenceQueue to run cleanup after object is finalized.
3. Pattern — allocate native handle, wrap in PhantomReference, enqueue on GC.
4. Cleaner thread polls queue and releases native memory or file handles.
5. Alternative to finalize — no resurrection risk, predictable ordering.
6. java.lang.ref.Cleaner in Java 9 — modern API built on phantom references.

### Scene `reference_queue` (renderer: `reference_queue`)

1. ReferenceQueue receives enqueued references when referent is cleared.
2. Poll or remove blocks until a reference is ready — background cleanup thread.
3. Soft and weak references optionally register with a queue.
4. Phantom references require a queue — referent is never directly accessible.
5. Do not do heavy work in the GC thread — poll from a dedicated thread.
6. Missed queue processing can leak native resources even after GC.

### Scene `cache_patterns` (renderer: `cache_patterns`)

1. Practical cache patterns with reference types.
2. SoftReference cache — keep parsed objects while memory allows.
3. WeakReference intern pool — deduplicate without pinning strings forever.
4. Caffeine and Guava caches use smarter eviction — often better than raw SoftReference.
5. Combine size limits with soft references — unbounded soft caches still risk OOM.
6. Measure hit rate and memory — reference caches are a tuning tool, not a default.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using SoftReference as a leak fix — masks the real strong reference.
3. Two — no ReferenceQueue consumer thread — phantom cleanup never runs.
4. Three — expecting immediate weak reference clearing — GC must run first.
5. Also — storing large objects only in soft refs without size cap.
6. Prefer explicit cache libraries with eviction policies for production.

### Scene `interview` (renderer: `interview`)

1. Interview question — explain soft, weak, and phantom references.
2. Soft — cleared under memory pressure — cache use case.
3. Weak — cleared at next GC — WeakHashMap canonical keys.
4. Phantom — post-finalization cleanup — native resources via ReferenceQueue.
5. ReferenceQueue delivers notification — poll from background thread.
6. Strong refs dominate — weak types only affect GC reachability, not magic.

### Scene `teaser` (renderer: `teaser`)

1. Reference types shape object lifetime — JVM flags shape runtime behavior.
2. Episode Sixty-Two — JVM Flags and Tuning Basics.
3. Heap sizing, GC flags, and diagnostic switches.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **61** — *Heap*.
- **Series catalog mapping:** Episode 61 / catalog column `61` / published title *Reference Types*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty covered metaspace and native memory beyond the heap._
- **`title`** — starts from: _Episode Sixty-One._
- **`reference_hierarchy`** — starts from: _Four reference strengths from strongest to weakest._
- **`soft_weak_use`** — starts from: _SoftReference — ideal for memory-sensitive caches._
- **`phantom_cleanup`** — starts from: _PhantomReference — referent is not accessible through the reference itself._
- **`reference_queue`** — starts from: _ReferenceQueue receives enqueued references when referent is cleared._
- **`cache_patterns`** — starts from: _Practical cache patterns with reference types._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — explain soft, weak, and phantom references._
- **`teaser`** — starts from: _Reference types shape object lifetime — JVM flags shape runtime behavior._
