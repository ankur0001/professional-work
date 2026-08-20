# Episode 54 — Garbage Collection

| Field | Value |
|---|---|
| Episode | 54 |
| Title | Garbage Collection |
| Catalog handbook column | 54 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Three placed objects on the shared heap with references from stacks and fields.
2. Who frees memory when those objects are no longer needed?
3. Java has no free or delete — the garbage collector reclaims unreachable objects automatically.
4. GC traces from roots — stack locals, static fields, JNI references — anything strongly reachable stays live.
5. Generations exploit the observation that most objects die young — optimize for that reality.
6. Today — garbage collection basics, mark-sweep intuition, generations, and stop-the-world pauses.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Four.
2. Garbage Collection Intro.
3. We'll follow an object's lifecycle from allocation to collection and read what GC logs mean at a high level.

### Scene `gc_roots` (renderer: `gc_roots`)

1. GC roots are starting points for reachability analysis — where the trace begins.
2. Local variables and operand stacks in active frames are roots — your running methods hold references.
3. Static fields in loaded classes hold root references — singleton caches live here until nulled.
4. JNI global references and JVM internal structures are roots too — invisible but counted.
5. An object is live if reachable from any root through a chain of references.
6. Unreachable objects are garbage — eligible for collection on the next appropriate GC cycle.

```java
void process() {
    byte[] buffer = new byte[1_000_000];  // reachable while method runs
}  // buffer eligible after return if no other references exist
```

7. Eligible is not instant — GC runs when the collector decides, not the moment the last reference disappears.

### Scene `mark_sweep` (renderer: `mark_sweep`)

1. Mark-sweep is the foundational GC algorithm every collector variation builds on.
2. Mark phase — traverse from roots, flag every reachable object in the heap graph.
3. Sweep phase — walk the heap, reclaim unmarked objects — return memory to allocator pools.
4. Compact phase in some collectors — defragment live objects to reduce fragmentation over time.
5. Simple mark-sweep can fragment memory without compaction — free holes scattered between live objects.
6. Modern collectors extend this with copying young generations and concurrent marking for old regions.

### Scene `generations` (renderer: `generations`)

1. The generational hypothesis — most objects die young — short-lived temporaries dominate allocation rate.
2. Young generation — Eden plus Survivor spaces — frequent minor GC, fast because region is small.
3. Objects that survive several collections promote to old generation — tenured long-lived data.
4. Old generation collected less often — more expensive when it runs — major or full GC territory.
5. Minor GC is fast — scans primarily young region — stop-the-world but usually milliseconds on healthy heaps.
6. Major or full GC collects broader heap areas — longer pauses — the spikes users feel in P99 latency.

### Scene `stop_the_world` (renderer: `stop_the_world`)

1. Stop-the-world means all application threads pause during certain GC phases — safepoint synchronization.
2. Safepoints are bytecode locations where the JVM can safely halt threads — counted loops, method returns, some calls.
3. During STW phases, roots are scanned accurately — no mutator moving references underneath the collector.
4. Pause time is the metric users feel — latency spikes in production dashboards and SLA breaches.
5. Concurrent collectors reduce STW duration but add complexity — barriers, floating garbage, tuning knobs.
6. GC logs with -Xlog:gc* show pause durations — always monitor in production, not only after incidents.

### Scene `gc_triggers` (renderer: `gc_triggers`)

1. Minor GC triggers when Eden fills up — allocation failure in young gen kicks collection.
2. Major GC triggers when old generation is full or metaspace pressure indirectly forces broader collection — or explicit System.gc hint.
3. System.gc is a hint — JVM may ignore it depending on collector and -XX:+DisableExplicitGC.
4. OutOfMemoryError fires only after GC fails to reclaim enough space — not on first failed allocation attempt.
5. Heap flags Xms and Xmx control heap bounds — initial and maximum — collector manages internal generation ratios often automatically.
6. Tuning starts with understanding what triggers each collection — logs first, knobs second.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes I want burned into your brain.
2. Mistake one — calling System.gc expecting immediate cleanup — unreliable hint, may cause full STW pause at worst time.
3. Mistake two — setting heap huge without understanding GC pause trade-offs — big heap can mean big pauses on some collectors.
4. Mistake three — ignoring GC logs until production latency spikes — baseline logs make diffs obvious.
5. Also — assuming all unreachable objects collect instantly — GC is periodic, not reference-counted immediate.
6. Measure pause times and allocation rates before tuning — data beats GC folklore from blog posts.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this out loud like someone who has shipped code.
2. Question: How does Java GC work?
3. Answer: Trace from roots — stack locals, statics, JNI refs — mark reachable objects.
4. Sweep or copy unreachable ones — generational collectors focus on young objects that die fast.
5. Stop-the-world pauses application threads at safepoints for certain phases — concurrent collectors shorten but do not always eliminate STW.
6. Collector choice and heap sizing affect pause versus throughput — no free lunch.
7. Mention you read GC logs in incidents — practical credibility.

### Scene `teaser` (renderer: `teaser`)

1. GC reclaims objects — but bytecode still starts in the interpreter until hot paths compile.
2. Episode Fifty-Five — JIT Compilation.
3. Interpreter, C1, C2 tiers, hot methods, and deoptimization when assumptions break.
4. See you there.

_Total beats: expanded for ~10–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **65** — *GC Algorithms*.
- **Series catalog mapping:** Episode 54 / catalog column `54` / published title *Garbage Collection*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 65 → episode 54). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with reachability examples — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — automatic reclamation vs manual free
- **`title`** — episode title card
- **`gc_roots`** — reachability from roots
- **`mark_sweep`** — foundational GC algorithm
- **`generations`** — young vs old generation hypothesis
- **`stop_the_world`** — safepoints and pause impact
- **`gc_triggers`** — what kicks minor and major GC
- **`mistakes`** — System.gc, huge heap blind, ignoring logs
- **`interview`** — how Java GC works interview answer
- **`teaser`** — bridge to JIT Compilation
