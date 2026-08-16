# Episode 54 — Garbage Collection

| Field | Value |
|---|---|
| Episode | 54 |
| Title | Garbage Collection |
| Catalog handbook column | 54 |
| Narration source script | `make_episode_54.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Three placed objects on the shared heap.
2. Who frees memory when those objects are no longer needed?
3. Java has no free or delete — the garbage collector reclaims unreachable objects.
4. GC traces from roots — stack locals, static fields, JNI references.
5. Generations exploit the observation that most objects die young.
6. Today — garbage collection basics, mark-sweep, and stop-the-world pauses.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Four.
2. Garbage Collection Intro.

### Scene `gc_roots` (renderer: `gc_roots`)

1. GC roots are starting points for reachability analysis.
2. Local variables and operand stacks in active frames are roots.
3. Static fields in loaded classes hold root references.
4. JNI global references and JVM internal structures are roots too.
5. An object is live if reachable from any root through references.
6. Unreachable objects are garbage — eligible for collection.

### Scene `mark_sweep` (renderer: `mark_sweep`)

1. Mark-sweep is the foundational GC algorithm.
2. Mark phase — traverse from roots, flag every reachable object.
3. Sweep phase — walk the heap, reclaim unmarked objects.
4. Compact phase in some collectors — defragment live objects.
5. Simple but can fragment memory without compaction.
6. Modern collectors extend this with copying and concurrent marking.

### Scene `generations` (renderer: `generations`)

1. The generational hypothesis — most objects die young.
2. Young generation — Eden plus Survivor spaces — frequent minor GC.
3. Objects that survive several collections promote to old generation.
4. Old generation — long-lived data — collected less often, more expensive.
5. Minor GC is fast — scans only the young region.
6. Major or full GC collects the entire heap — longer pauses.

### Scene `stop_the_world` (renderer: `stop_the_world`)

1. Stop-the-world means all application threads pause during GC.
2. Safepoints are locations where the JVM can safely halt threads.
3. During STW, roots are scanned and the heap is processed.
4. Pause time is the metric users feel — latency spikes in production.
5. Concurrent collectors reduce STW but add complexity.
6. GC logs show pause durations — always monitor in production.

### Scene `gc_triggers` (renderer: `gc_triggers`)

1. Minor GC triggers when Eden fills up.
2. Major GC triggers when old generation is full or explicitly requested.
3. System.gc is a hint — JVM may ignore it depending on collector.
4. OutOfMemoryError fires only after GC fails to reclaim enough space.
5. Heap flags like Xms and Xmx control generation sizes.
6. Tuning starts with understanding what triggers each collection.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — calling System.gc expecting immediate cleanup — unreliable hint.
3. Two — setting heap huge without understanding GC pause trade-offs.
4. Three — ignoring GC logs until production latency spikes.
5. Also — assuming all unreachable objects collect instantly — GC is periodic.
6. Measure pause times before tuning — data beats folklore.

### Scene `interview` (renderer: `interview`)

1. Interview question — how does Java GC work?
2. Trace from roots — stack locals, statics, JNI refs.
3. Mark reachable objects — sweep or compact unreachable ones.
4. Generational — young collected often, old collected rarely.
5. Stop-the-world pauses all threads at safepoints.
6. Collector choice and heap sizing affect pause versus throughput.

### Scene `teaser` (renderer: `teaser`)

1. Bytecode starts in the interpreter — hot code gets compiled.
2. Episode Fifty-Five — JIT Compilation.
3. Interpreter, C1, C2 tiers, hot methods, and deoptimization.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **65** — *GC Algorithms*.
- **Series catalog mapping:** Episode 54 / catalog column `54` / published title *Garbage Collection*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 65 → episode 54). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Three placed objects on the shared heap._
- **`title`** — starts from: _Episode Fifty-Four._
- **`gc_roots`** — starts from: _GC roots are starting points for reachability analysis._
- **`mark_sweep`** — starts from: _Mark-sweep is the foundational GC algorithm._
- **`generations`** — starts from: _The generational hypothesis — most objects die young._
- **`stop_the_world`** — starts from: _Stop-the-world means all application threads pause during GC._
- **`gc_triggers`** — starts from: _Minor GC triggers when Eden fills up._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how does Java GC work?_
- **`teaser`** — starts from: _Bytecode starts in the interpreter — hot code gets compiled._
