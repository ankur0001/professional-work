# Episode 60 — Metaspace and Native Memory

| Field | Value |
|---|---|
| Episode | 60 |
| Title | Metaspace and Native Memory |
| Catalog handbook column | 60 |
| Narration source script | `make_episode_60.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Nine showed escape analysis eliminating heap allocations.
2. But JVM memory is more than the heap — classes and native buffers matter too.
3. Before Java 8, PermGen held class metadata with a fixed size limit.
4. Metaspace replaced PermGen — class metadata in native memory, auto-growing.
5. Direct ByteBuffers and JNI allocations live outside the heap entirely.
6. Today — metaspace, native memory, direct buffers, and NMT.

### Scene `title` (renderer: `title`)

1. Episode Sixty.
2. Metaspace and Native Memory.

### Scene `permgen_history` (renderer: `permgen_history`)

1. PermGen — Permanent Generation — stored class metadata until Java 7.
2. Fixed maximum size — PermGenSpace OutOfMemoryError on class-heavy apps.
3. Hot redeploy in app servers leaked class loaders into PermGen.
4. Java 8 removed PermGen — metadata moved to native metaspace.
5. Metaspace grows on demand — limited by MaxMetaspaceSize flag.
6. Understanding the history explains old PermGen tuning advice still online.

### Scene `metaspace_basics` (renderer: `metaspace_basics`)

1. Metaspace stores class metadata — method tables, constant pools, annotations.
2. Allocated from native OS memory — not counted in -Xmx heap limit.
3. Grows as classes load — shrinks when class loaders become unreachable.
4. MaxMetaspaceSize caps growth — default unlimited on 64-bit JVM.
5. Compressed class pointers — UseCompressedClassPointers saves space on 64-bit.
6. Class unloading requires collecting the defining ClassLoader — rare in long-lived apps.

### Scene `direct_buffers` (renderer: `direct_buffers`)

1. Direct ByteBuffers allocate memory outside the Java heap.
2. ByteBuffer.allocateDirect — native memory for zero-copy I/O with OS.
3. Not tracked by heap -Xmx — can exhaust process memory silently.
4. Cleaner or explicit free releases native memory when buffer is garbage collected.
5. Netty and NIO frameworks use direct buffers heavily — watch native usage.
6. MaxDirectMemorySize flag sets the cap — default is roughly max heap size.

### Scene `nmt_native_memory` (renderer: `nmt_native_memory`)

1. Native Memory Tracking — NMT — accounts for JVM native allocations.
2. Enable with -XX:NativeMemoryTracking=summary or detail at startup.
3. jcmd <pid> VM.native_memory summary — breakdown by category.
4. Categories include Java Heap, Metaspace, Code, Thread, and Internal.
5. Compare baseline versus after load test — spot metaspace or direct buffer growth.
6. Detail mode has overhead — use summary in production, detail in staging.

### Scene `sizing_tuning` (renderer: `sizing_tuning`)

1. Sizing native memory for production workloads.
2. Set MaxMetaspaceSize if class loaders leak or dynamic codegen runs wild.
3. Set MaxDirectMemorySize when using heavy NIO or off-heap caches.
4. Monitor RSS process size — heap plus metaspace plus code cache plus threads.
5. NMT diff before and after deployment catches class loader leaks early.
6. Native OOM kills the process — no catchable Java exception.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — sizing only -Xmx and ignoring metaspace and direct memory.
3. Two — assuming GC frees direct buffer memory immediately — Cleaner is async.
4. Three — enabling NMT detail in production — measurable overhead.
5. Also — redeploying without restarting — class loader leaks accumulate.
6. Watch RSS and NMT — heap metrics alone miss half the story.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is metaspace and how does it differ from the heap?
2. Metaspace holds class metadata in native memory — not Java objects.
3. Replaced PermGen in Java 8 — grows on demand, capped by MaxMetaspaceSize.
4. Direct buffers and code cache also live outside -Xmx heap.
5. NMT with jcmd VM.native_memory tracks native allocation categories.
6. RSS is the real process limit — heap plus all native JVM regions.

### Scene `teaser` (renderer: `teaser`)

1. Not all references are strong — the JVM offers softer cleanup contracts.
2. Episode Sixty-One — Soft, Weak, and Phantom References.
3. ReferenceQueue, caches, and cleanup patterns.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **60** — *JVM Memory Areas*.
- **Series catalog mapping:** Episode 60 / catalog column `60` / published title *Metaspace and Native Memory*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Nine showed escape analysis eliminating heap allocations._
- **`title`** — starts from: _Episode Sixty._
- **`permgen_history`** — starts from: _PermGen — Permanent Generation — stored class metadata until Java 7._
- **`metaspace_basics`** — starts from: _Metaspace stores class metadata — method tables, constant pools, annotations._
- **`direct_buffers`** — starts from: _Direct ByteBuffers allocate memory outside the Java heap._
- **`nmt_native_memory`** — starts from: _Native Memory Tracking — NMT — accounts for JVM native allocations._
- **`sizing_tuning`** — starts from: _Sizing native memory for production workloads._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is metaspace and how does it differ from the heap?_
- **`teaser`** — starts from: _Not all references are strong — the JVM offers softer cleanup contracts._
