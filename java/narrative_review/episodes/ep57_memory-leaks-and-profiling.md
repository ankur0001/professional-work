# Episode 57 — Memory Leaks and Profiling

| Field | Value |
|---|---|
| Episode | 57 |
| Title | Memory Leaks and Profiling |
| Catalog handbook column | 57 |
| Narration source script | `make_episode_57.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Six showed how GC collectors reclaim unreachable objects.
2. But what if objects stay reachable when they should not?
3. A memory leak means live references hold objects you forgot about.
4. The heap grows until OutOfMemoryError — no collector can fix that.
5. Profiling and heap dumps reveal what keeps objects alive.
6. Today — memory leaks, heap dumps, retained sets, and leak patterns.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Seven.
2. Memory Leaks and Profiling.

### Scene `heap_dumps` (renderer: `heap_dumps`)

1. A heap dump is a snapshot of every object on the heap.
2. Trigger with jmap, jcmd, or -XX:+HeapDumpOnOutOfMemoryError.
3. HPROF format — open in Eclipse MAT or VisualVM.
4. Capture during high memory or right after an OOM for best signal.
5. Never dump production without a plan — files can be gigabytes.
6. One dump at a time — compare before and after a suspected leak.

### Scene `retained_sets` (renderer: `retained_sets`)

1. Retained set — objects kept alive only through a given object.
2. MAT computes retained heap size — the memory you free by removing one reference.
3. Dominator tree shows which objects hold the most retained memory.
4. Leak suspects report highlights collections growing without bound.
5. Follow reference chains from GC roots to find the holder.
6. Shallow size versus retained size — retained size is what matters.

### Scene `leak_patterns` (renderer: `leak_patterns`)

1. Common leak patterns in Java applications.
2. Static collections that never remove entries — caches without eviction.
3. Listeners registered but never unregistered — event bus leaks.
4. ThreadLocal values not cleared after request — pool thread reuse.
5. ClassLoader leaks in redeployed web apps — old classes pinned.
6. Closing resources late — streams and connections held open.

### Scene `profiling_overview` (renderer: `profiling_overview`)

1. Profiling complements heap dumps for live diagnosis.
2. Async Profiler — low-overhead CPU and allocation sampling.
3. JFR allocation events show which methods allocate the most.
4. jcmd VM.native_memory summary tracks native and heap together.
5. VisualVM connects live — watch heap trend during load test.
6. Profile under realistic load — idle apps hide leaks.

### Scene `mat_workflow` (renderer: `mat_workflow`)

1. A practical MAT workflow for leak hunting.
2. Open HPROF — run Leak Suspects and Top Consumers reports.
3. Inspect dominator tree — sort by retained heap size.
4. Right-click suspect — Path to GC Roots, exclude weak references.
5. Identify the collection or cache holding unexpected objects.
6. Fix code — remove reference, add eviction, or use WeakReference.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — restarting the JVM before capturing a heap dump.
3. Two — chasing shallow size instead of retained heap.
4. Three — assuming GC logs alone prove a leak — you need object graphs.
5. Also — comparing dumps from different application versions.
6. Leaks are reference problems — find what still points at the garbage.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you diagnose a memory leak?
2. Confirm heap grows under steady load — not just a traffic spike.
3. Capture heap dump — MAT retained set and dominator tree.
4. Path to GC roots — find the unexpected strong reference chain.
5. Common culprits — static maps, listeners, ThreadLocal, class loaders.
6. Fix and verify with another dump under the same workload.

### Scene `teaser` (renderer: `teaser`)

1. Heap dumps answer what is alive — command-line tools answer what is running now.
2. Episode Fifty-Eight — Diagnostic Tools.
3. jcmd, jmap, jstack, and JFR for live JVM inspection.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **57** — *Bytecode*.
- **Series catalog mapping:** Episode 57 / catalog column `57` / published title *Memory Leaks and Profiling*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Six showed how GC collectors reclaim unreachable objects._
- **`title`** — starts from: _Episode Fifty-Seven._
- **`heap_dumps`** — starts from: _A heap dump is a snapshot of every object on the heap._
- **`retained_sets`** — starts from: _Retained set — objects kept alive only through a given object._
- **`leak_patterns`** — starts from: _Common leak patterns in Java applications._
- **`profiling_overview`** — starts from: _Profiling complements heap dumps for live diagnosis._
- **`mat_workflow`** — starts from: _A practical MAT workflow for leak hunting._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you diagnose a memory leak?_
- **`teaser`** — starts from: _Heap dumps answer what is alive — command-line tools answer what is running now._
