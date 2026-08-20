# Episode 57 — Memory Leaks and Profiling

| Field | Value |
|---|---|
| Episode | 57 |
| Title | Memory Leaks and Profiling |
| Catalog handbook column | 57 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Six compared GC collectors that reclaim unreachable objects efficiently.
2. But what if objects stay reachable when they should not — held by references you forgot?
3. A memory leak in Java means live references pin objects that belong in the garbage — not missing free calls.
4. The heap grows until OutOfMemoryError — no collector fixes strong references you still maintain.
5. Profiling and heap dumps reveal what keeps objects alive — dominator trees and paths to GC roots.
6. Today — memory leaks, heap dumps, retained sets, and leak patterns that repeat across codebases.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Seven.
2. Memory Leaks and Profiling.
3. We'll capture a dump, read MAT reports, and fix the static map that never evicts.

### Scene `heap_dumps` (renderer: `heap_dumps`)

1. A heap dump is a snapshot of every object on the heap at one instant — HPROF format.
2. Trigger with jmap, jcmd GC.heap_dump, or -XX:+HeapDumpOnOutOfMemoryError for automatic capture on OOM.
3. Open in Eclipse MAT or VisualVM — indexed analysis, dominator tree, leak suspects.
4. Capture during high memory or right after OOM for best signal — not immediately after restart when heap is empty.
5. Never dump production without a plan — files can be many gigabytes, disk and privacy matter.
6. Compare two dumps from the same workload version — diff growth implicates new code paths.

```bash
jcmd <pid> GC.heap_dump /tmp/heap.hprof
```

7. Histogram first with jcmd GC.class_histogram — confirms suspect class before full dump weight.

### Scene `retained_sets` (renderer: `retained_sets`)

1. Retained set — all objects kept alive only because a given object references them — domination analysis.
2. MAT computes retained heap size — memory you would free if one reference disappeared.
3. Dominator tree sorts objects by retained size — big retained blocks scream leak suspects.
4. Leak suspects report highlights collections growing without bound — ArrayList or HashMap entries dominating.
5. Follow reference chains from GC roots — path to GC roots, exclude weak references when hunting strong leaks.
6. Shallow size versus retained size — shallow is the object alone, retained is the whole subgraph it pins.

### Scene `leak_patterns` (renderer: `leak_patterns`)

1. Common leak patterns in Java applications — recognize before you grep blindly.
2. Static collections that never remove entries — caches without eviction policy or TTL.
3. Listeners registered but never unregistered — event buses, UI frameworks, JMX notifications.
4. ThreadLocal values not cleared after request — pool thread carries last user's context and data graph.
5. ClassLoader leaks in redeployed web apps — old WAR classes pinned by singleton references.
6. Unclosed resources held in fields — streams and connections indirectly retain buffers.

```java
private static final Map<String, byte[]> CACHE = new HashMap<>();  // grows forever
void handle(String key, byte[] data) {
    CACHE.put(key, data);  // no remove, no bounds — classic leak
}
```

7. Fix — bounded cache, WeakReference values, or Caffeine with eviction — not unbounded static HashMap.

### Scene `profiling_overview` (renderer: `profiling_overview`)

1. Profiling complements heap dumps for live diagnosis before the heap explodes.
2. Async Profiler — low-overhead CPU and allocation sampling attachable in production carefully.
3. JFR allocation events show which methods allocate the most bytes over time — hot allocators.
4. jcmd VM.native_memory summary tracks native and heap together — metaspace and direct buffer growth.
5. VisualVM connects live — watch heap trend during load test — slope tells leak from traffic spike.
6. Profile under realistic sustained load — idle apps hide leaks that appear only under steady traffic.

### Scene `mat_workflow` (renderer: `mat_workflow`)

1. A practical MAT workflow for leak hunting — repeatable, not panic-driven.
2. Open HPROF — run Leak Suspects and Top Consumers reports first pass.
3. Inspect dominator tree — sort by retained heap, click largest suspicious collection.
4. Right-click suspect — Path to GC Roots, exclude weak and soft references initially.
5. Identify the static field, cache, or listener holder keeping unexpected objects alive.
6. Fix code — remove reference, add eviction, use WeakReference, or clear ThreadLocal in finally — verify with second dump under same workload.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes I want burned into your brain.
2. Mistake one — restarting the JVM before capturing a heap dump — evidence gone, mystery returns next week.
3. Mistake two — chasing shallow size of many tiny objects instead of retained heap of one big map.
4. Mistake three — assuming GC logs alone prove a leak — you need object graph proof of unexpected retention.
5. Also — comparing dumps from different application versions or different traffic shapes — false leads.
6. Leaks are reference problems — find what still points at garbage, then break that edge.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this out loud like someone who has shipped code.
2. Question: How do you diagnose a memory leak?
3. Answer: Confirm heap grows under steady load — not just a traffic spike — GC cannot keep up despite collections.
4. Capture heap dump — MAT retained set, dominator tree, leak suspects report.
5. Path to GC roots — find unexpected strong reference chain — static map, listener, ThreadLocal, class loader.
6. Fix and verify with another dump under the same workload — retained size should stabilize.
7. Mention JFR allocation profiling for live triage — operational depth interviewers notice.

### Scene `teaser` (renderer: `teaser`)

1. Heap dumps answer what is alive at a snapshot — command-line tools answer what is running right now.
2. Episode Fifty-Eight — Diagnostic Tools.
3. jcmd, jmap, jstack, and JFR for live JVM inspection on call.
4. See you there.

_Total beats: expanded for ~10–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **57** — *Bytecode*.
- **Series catalog mapping:** Episode 57 / catalog column `57` / published title *Memory Leaks and Profiling*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with leak pattern code example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — reachable garbage vs GC failure
- **`title`** — episode title card
- **`heap_dumps`** — capture and analyze HPROF
- **`retained_sets`** — dominator tree and retained size
- **`leak_patterns`** — static caches, listeners, ThreadLocal
- **`profiling_overview`** — JFR and allocation profiling
- **`mat_workflow`** — step-by-step leak hunt
- **`mistakes`** — restart before dump, shallow size chase
- **`interview`** — leak diagnosis interview answer
- **`teaser`** — bridge to Diagnostic Tools
