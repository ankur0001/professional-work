# Episode 57 — Memory Leaks and Profiling

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Six showed how GC collectors reclaim unreachable objects. But what if objects stay reachable when they should not? A memory leak means live references hold objects you forgot about.

The heap grows until OutOfMemoryError — no collector can fix that. Profiling and heap dumps reveal what keeps objects alive. Today — memory leaks, heap dumps, retained sets, and leak patterns.

Episode Fifty-Seven. Memory Leaks and Profiling. A heap dump is a snapshot of every object on the heap. Trigger with jmap, jcmd, or -XX:+HeapDumpOnOutOfMemoryError. HPROF format — open in Eclipse MAT or VisualVM.

Capture during high memory or right after an OOM for best signal. Never dump production without a plan — files can be gigabytes. One dump at a time — compare before and after a suspected leak.

Retained set — objects kept alive only through a given object. MAT computes retained heap size — the memory you free by removing one reference. Dominator tree shows which objects hold the most retained memory.

Leak suspects report highlights collections growing without bound. Follow reference chains from GC roots to find the holder. Shallow size versus retained size — retained size is what matters.

Common leak patterns in Java applications. Static collections that never remove entries — caches without eviction. Listeners registered but never unregistered — event bus leaks. ThreadLocal values not cleared after request — pool thread reuse.

ClassLoader leaks in redeployed web apps — old classes pinned. Closing resources late — streams and connections held open. Profiling complements heap dumps for live diagnosis. Async Profiler — low-overhead CPU and allocation sampling.

JFR allocation events show which methods allocate the most. jcmd VM.native_memory summary tracks native and heap together. VisualVM connects live — watch heap trend during load test.

Profile under realistic load — idle apps hide leaks. A practical MAT workflow for leak hunting. Open HPROF — run Leak Suspects and Top Consumers reports. Inspect dominator tree — sort by retained heap size.

Right-click suspect — Path to GC Roots, exclude weak references. Identify the collection or cache holding unexpected objects. Fix code — remove reference, add eviction, or use WeakReference.

Three common mistakes. One — restarting the JVM before capturing a heap dump. Two — chasing shallow size instead of retained heap. Three — assuming GC logs alone prove a leak — you need object graphs.

Also — comparing dumps from different application versions. Leaks are reference problems — find what still points at the garbage. Interview question — how do you diagnose a memory leak?

Confirm heap grows under steady load — not just a traffic spike. Capture heap dump — MAT retained set and dominator tree. Path to GC roots — find the unexpected strong reference chain.

Common culprits — static maps, listeners, ThreadLocal, class loaders. Fix and verify with another dump under the same workload. Heap dumps answer what is alive — command-line tools answer what is running now.

Episode Fifty-Eight — Diagnostic Tools. jcmd, jmap, jstack, and JFR for live JVM inspection. See you there.
