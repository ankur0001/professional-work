# Episode 54 — Garbage Collection

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Three placed objects on the shared heap. Who frees memory when those objects are no longer needed? Java has no free or delete — the garbage collector reclaims unreachable objects.

GC traces from roots — stack locals, static fields, JNI references. Generations exploit the observation that most objects die young. Today — garbage collection basics, mark-sweep, and stop-the-world pauses.

Episode Fifty-Four. Garbage Collection Intro. GC roots are starting points for reachability analysis. Local variables and operand stacks in active frames are roots. Static fields in loaded classes hold root references.

JNI global references and JVM internal structures are roots too. An object is live if reachable from any root through references. Unreachable objects are garbage — eligible for collection.

Mark-sweep is the foundational GC algorithm. Mark phase — traverse from roots, flag every reachable object. Sweep phase — walk the heap, reclaim unmarked objects. Compact phase in some collectors — defragment live objects.

Simple but can fragment memory without compaction. Modern collectors extend this with copying and concurrent marking. The generational hypothesis — most objects die young. Young generation — Eden plus Survivor spaces — frequent minor GC.

Objects that survive several collections promote to old generation. Old generation — long-lived data — collected less often, more expensive. Minor GC is fast — scans only the young region.

Major or full GC collects the entire heap — longer pauses. Stop-the-world means all application threads pause during GC. Safepoints are locations where the JVM can safely halt threads.

During STW, roots are scanned and the heap is processed. Pause time is the metric users feel — latency spikes in production. Concurrent collectors reduce STW but add complexity. GC logs show pause durations — always monitor in production.

Minor GC triggers when Eden fills up. Major GC triggers when old generation is full or explicitly requested. System.gc is a hint — JVM may ignore it depending on collector. OutOfMemoryError fires only after GC fails to reclaim enough space.

Heap flags like Xms and Xmx control generation sizes. Tuning starts with understanding what triggers each collection. Three common mistakes. One — calling System.gc expecting immediate cleanup — unreliable hint.

Two — setting heap huge without understanding GC pause trade-offs. Three — ignoring GC logs until production latency spikes. Also — assuming all unreachable objects collect instantly — GC is periodic.

Measure pause times before tuning — data beats folklore. Interview question — how does Java GC work? Trace from roots — stack locals, statics, JNI refs. Mark reachable objects — sweep or compact unreachable ones.

Generational — young collected often, old collected rarely. Stop-the-world pauses all threads at safepoints. Collector choice and heap sizing affect pause versus throughput. Bytecode starts in the interpreter — hot code gets compiled.

Episode Fifty-Five — JIT Compilation. Interpreter, C1, C2 tiers, hot methods, and deoptimization. See you there.
