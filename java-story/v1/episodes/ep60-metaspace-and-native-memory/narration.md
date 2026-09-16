# Episode 60 — Metaspace and Native Memory

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Nine showed escape analysis eliminating heap allocations. But JVM memory is more than the heap — classes and native buffers matter too. Before Java 8, PermGen held class metadata with a fixed size limit.

Metaspace replaced PermGen — class metadata in native memory, auto-growing. Direct ByteBuffers and JNI allocations live outside the heap entirely. Today — metaspace, native memory, direct buffers, and NMT.

Episode Sixty. Metaspace and Native Memory. PermGen — Permanent Generation — stored class metadata until Java 7. Fixed maximum size — PermGenSpace OutOfMemoryError on class-heavy apps.

Hot redeploy in app servers leaked class loaders into PermGen. Java 8 removed PermGen — metadata moved to native metaspace. Metaspace grows on demand — limited by MaxMetaspaceSize flag.

Understanding the history explains old PermGen tuning advice still online. Metaspace stores class metadata — method tables, constant pools, annotations. Allocated from native OS memory — not counted in -Xmx heap limit.

Grows as classes load — shrinks when class loaders become unreachable. MaxMetaspaceSize caps growth — default unlimited on 64-bit JVM. Compressed class pointers — UseCompressedClassPointers saves space on 64-bit.

Class unloading requires collecting the defining ClassLoader — rare in long-lived apps. Direct ByteBuffers allocate memory outside the Java heap. ByteBuffer.allocateDirect — native memory for zero-copy I/O with OS.

Not tracked by heap -Xmx — can exhaust process memory silently. Cleaner or explicit free releases native memory when buffer is garbage collected. Netty and NIO frameworks use direct buffers heavily — watch native usage.

MaxDirectMemorySize flag sets the cap — default is roughly max heap size. Native Memory Tracking — NMT — accounts for JVM native allocations. Enable with -XX:NativeMemoryTracking=summary or detail at startup.

jcmd <pid> VM.native_memory summary — breakdown by category. Categories include Java Heap, Metaspace, Code, Thread, and Internal. Compare baseline versus after load test — spot metaspace or direct buffer growth.

Detail mode has overhead — use summary in production, detail in staging. Sizing native memory for production workloads. Set MaxMetaspaceSize if class loaders leak or dynamic codegen runs wild.

Set MaxDirectMemorySize when using heavy NIO or off-heap caches. Monitor RSS process size — heap plus metaspace plus code cache plus threads. NMT diff before and after deployment catches class loader leaks early.

Native OOM kills the process — no catchable Java exception. Three common mistakes. One — sizing only -Xmx and ignoring metaspace and direct memory. Two — assuming GC frees direct buffer memory immediately — Cleaner is async.

Three — enabling NMT detail in production — measurable overhead. Also — redeploying without restarting — class loader leaks accumulate. Watch RSS and NMT — heap metrics alone miss half the story.

Interview question — what is metaspace and how does it differ from the heap? Metaspace holds class metadata in native memory — not Java objects. Replaced PermGen in Java 8 — grows on demand, capped by MaxMetaspaceSize.

Direct buffers and code cache also live outside -Xmx heap. NMT with jcmd VM.native_memory tracks native allocation categories. RSS is the real process limit — heap plus all native JVM regions.

Not all references are strong — the JVM offers softer cleanup contracts. Episode Sixty-One — Soft, Weak, and Phantom References. ReferenceQueue, caches, and cleanup patterns. See you there.
