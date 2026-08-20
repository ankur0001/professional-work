# Episode 56 — GC Collectors

| Field | Value |
|---|---|
| Episode | 56 |
| Title | GC Collectors |
| Catalog handbook column | 56 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Five showed the JIT compiling hot bytecode to native code in the code cache.
2. Garbage collection algorithms matter just as much for production latency — different collectors, different pause stories.
3. Serial GC — one thread, simple, fine for tiny heaps and client tools.
4. Parallel GC maximizes throughput for batch jobs that tolerate pauses.
5. G1 and ZGC target manageable or sub-millisecond pauses on large heaps.
6. Today — Serial, Parallel, G1, and ZGC — and how to choose with evidence, not hype.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Six.
2. GC Collectors.
3. We'll map collectors to workloads and the flags you actually type on the command line.

### Scene `serial_parallel` (renderer: `serial_parallel`)

1. Serial GC uses a single thread for all young and old generation collection work.
2. Flag -XX:+UseSerialGC — good for small client apps, embedded tools, single-core containers.
3. Parallel GC — formerly Parallel Scavenge plus Parallel Old — multi-threaded throughput collector.
4. Flag -XX:+UseParallelGC — maximizes aggregate throughput on batch ETL and compute farms.
5. Parallel pauses all application threads but uses multiple GC threads to finish faster — still STW, just shorter wall clock.
6. Default before Java 9 on server-class machines — still valid for pause-tolerant batch workloads today.

### Scene `g1_collector` (renderer: `g1_collector`)

1. G1 — Garbage First — default collector since Java 9 on most deployments.
2. Divides heap into equal-sized regions instead of rigid contiguous young and old spaces.
3. Concurrent marking identifies regions with the most garbage — collect those first for efficiency.
4. Mixed collections reclaim both young and selected old regions together — incremental old gen reclamation.
5. Target pause time via -XX:MaxGCPauseMillis — best-effort goal, not a hard SLA guarantee.
6. Good general-purpose choice for heaps from hundreds of MB to tens of GB on web services.

```bash
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xms4g -Xmx4g -jar app.jar
```

7. Equal -Xms and -Xmx avoids resize churn — common production baseline before fine tuning.

### Scene `zgc_overview` (renderer: `zgc_overview`)

1. ZGC targets sub-millisecond pause times on large heaps — latency-sensitive services.
2. Uses colored pointers and load barriers for concurrent compaction — most work while app runs.
3. Stop-the-world phases shrink to tiny synchronization points — not zero, but small on modern JDK.
4. Flag -XX:+UseZGC — production-ready in LTS releases — pair with adequate heap headroom.
5. Shenandoah is an alternative low-pause collector with similar goals — Red Hat lineage, also concurrent.
6. Choose ZGC or Shenandoah when pause latency is critical and heap is large — validate with your object allocation pattern.

### Scene `choosing_collector` (renderer: `choosing_collector`)

1. How to choose a collector for your workload — decision flow without religion.
2. Small heap, single core — Serial GC, minimal footprint and threads.
3. Batch processing, throughput priority, pauses acceptable — Parallel GC.
4. General web services, moderate heaps — G1 default is a solid starting point before exotic switches.
5. Large heap, strict latency SLA, allocation rate you can measure — ZGC or Shenandoah with load tests.
6. Always validate with GC logs and realistic traffic — not blog posts from different hardware eras.

### Scene `flags_overview` (renderer: `flags_overview`)

1. Key GC flags to know — the ones ops teams actually grep in startup scripts.
2. UseG1GC, UseParallelGC, UseSerialGC, UseZGC — select the collector explicitly when default is wrong.
3. -Xms and -Xmx set initial and maximum heap size — container limits must leave headroom for native memory.
4. MaxGCPauseMillis tunes G1 pause target — millisecond fantasies without heap budget fail disappointingly.
5. -Xlog:gc* enables unified GC logging on modern JDK — replace ancient PrintGCDetails habits.
6. Print final flags with java -XX:+PrintFlagsFinal -version | grep GC — know what the JVM actually picked.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes I want burned into your brain.
2. Mistake one — switching to ZGC for a 256 MB heap without measuring — overhead may exceed benefit.
3. Mistake two — setting MaxGCPauseMillis to one millisecond — unrealistic, JVM cannot violate physics on huge live sets.
4. Mistake three — copying GC flags from another app with different allocation rate and object lifetime.
5. Also — ignoring GC logs after a collector change — regressions hide until peak traffic season.
6. Collector choice is empirical — profile your actual traffic patterns under failure scenarios.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this out loud like someone who has shipped code.
2. Question: Which GC collector would you choose?
3. Answer: Serial — tiny single-core apps. Parallel — throughput batch jobs tolerating pauses.
4. G1 — default general purpose, region-based, pause-time target knob — good web service starting point.
5. ZGC or Shenandoah — large heap, sub-ms pause goals, concurrent compaction — validate with load tests.
6. Trade throughput versus latency — no one-size-fits-all — mention you read GC logs and tune with data.
7. Container memory limits and native overhead — bonus points for production awareness.

### Scene `teaser` (renderer: `teaser`)

1. Even the best collector cannot fix memory leaks — live references beat every algorithm.
2. Episode Fifty-Seven — Memory Leaks and Profiling.
3. Heap dumps, MAT dominator trees, and finding what holds references alive.
4. See you there.

_Total beats: expanded for ~10–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **66** — *G1GC*.
- **Series catalog mapping:** Episode 56 / catalog column `56` / published title *GC Collectors*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 66 → episode 56). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with collector flags example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — collector choice affects latency
- **`title`** — episode title card
- **`serial_parallel`** — Serial and Parallel GC roles
- **`g1_collector`** — G1 regions and pause target
- **`zgc_overview`** — ZGC and Shenandoah low pause
- **`choosing_collector`** — workload-based selection
- **`flags_overview`** — command-line GC flags
- **`mistakes`** — wrong collector for heap size, fantasy pause targets
- **`interview`** — collector choice interview answer
- **`teaser`** — bridge to Memory Leaks and Profiling
