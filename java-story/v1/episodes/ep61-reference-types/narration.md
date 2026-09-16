# Episode 61 — Reference Types

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty covered metaspace and native memory beyond the heap. Strong references keep objects alive until nothing points to them. But Java offers weaker reference types with different GC contracts.

Soft, Weak, and Phantom references let you build caches and cleanup hooks. ReferenceQueue notifies you when the referent is collected. Today — soft, weak, and phantom references, caches, and cleanup patterns.

Episode Sixty-One. Soft, Weak, and Phantom References. Four reference strengths from strongest to weakest. Strong reference — normal variable assignment — never collected while reachable.

Soft reference — collected only when memory is tight — good for caches. Weak reference — collected at next GC regardless of memory pressure. Phantom reference — collected after finalization — for native resource cleanup.

Each type extends Reference<T> with different enqueue behavior. SoftReference — ideal for memory-sensitive caches. JVM keeps soft referents until heap is nearly full, then clears them.

LinkedHashMap plus SoftReference — simple image or parsed-data cache. WeakReference — canonical mappings that should not prevent GC. WeakHashMap uses weak keys — entries vanish when key is only weakly reachable.

Do not rely on reference clearing for correctness — always have a fallback. PhantomReference — referent is not accessible through the reference itself. Used with ReferenceQueue to run cleanup after object is finalized.

Pattern — allocate native handle, wrap in PhantomReference, enqueue on GC. Cleaner thread polls queue and releases native memory or file handles. Alternative to finalize — no resurrection risk, predictable ordering.

java.lang.ref.Cleaner in Java 9 — modern API built on phantom references. ReferenceQueue receives enqueued references when referent is cleared. Poll or remove blocks until a reference is ready — background cleanup thread.

Soft and weak references optionally register with a queue. Phantom references require a queue — referent is never directly accessible. Do not do heavy work in the GC thread — poll from a dedicated thread.

Missed queue processing can leak native resources even after GC. Practical cache patterns with reference types. SoftReference cache — keep parsed objects while memory allows. WeakReference intern pool — deduplicate without pinning strings forever.

Caffeine and Guava caches use smarter eviction — often better than raw SoftReference. Combine size limits with soft references — unbounded soft caches still risk OOM. Measure hit rate and memory — reference caches are a tuning tool, not a default.

Three common mistakes. One — using SoftReference as a leak fix — masks the real strong reference. Two — no ReferenceQueue consumer thread — phantom cleanup never runs. Three — expecting immediate weak reference clearing — GC must run first.

Also — storing large objects only in soft refs without size cap. Prefer explicit cache libraries with eviction policies for production. Interview question — explain soft, weak, and phantom references.

Soft — cleared under memory pressure — cache use case. Weak — cleared at next GC — WeakHashMap canonical keys. Phantom — post-finalization cleanup — native resources via ReferenceQueue.

ReferenceQueue delivers notification — poll from background thread. Strong refs dominate — weak types only affect GC reachability, not magic. Reference types shape object lifetime — JVM flags shape runtime behavior.

Episode Sixty-Two — JVM Flags and Tuning Basics. Heap sizing, GC flags, and diagnostic switches. See you there.
