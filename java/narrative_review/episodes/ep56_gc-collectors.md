# Episode 56 — GC Collectors

| Field | Value |
|---|---|
| Episode | 56 |
| Title | GC Collectors |
| Catalog handbook column | 56 |
| Narration source script | `make_episode_56.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Five showed the JIT compiling hot bytecode to native code.
2. Garbage collection algorithms matter just as much for production latency.
3. Different collectors trade throughput against pause time differently.
4. Serial GC — one thread, simple, fine for tiny heaps.
5. G1 and ZGC target low pause times for large heaps.
6. Today — Serial, Parallel, G1, and ZGC — and when to choose each.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Six.
2. GC Collectors.

### Scene `serial_parallel` (renderer: `serial_parallel`)

1. Serial GC uses a single thread for all collection work.
2. Flag UseSerialGC — good for small client apps and single-core machines.
3. Parallel GC — formerly Parallel Old plus Parallel New — multi-threaded.
4. Flag UseParallelGC — maximizes throughput on batch workloads.
5. Parallel pauses all threads but uses multiple GC threads to finish faster.
6. Default before Java 9 — still valid for compute-heavy, pause-tolerant jobs.

### Scene `g1_collector` (renderer: `g1_collector`)

1. G1 — Garbage First — is the default collector since Java 9.
2. Divides heap into equal-sized regions instead of fixed generations.
3. Concurrent marking identifies regions with the most garbage.
4. Mixed collections reclaim both young and old regions together.
5. Target pause time via MaxGCPauseMillis — best-effort, not guaranteed.
6. Good general-purpose choice for heaps from hundreds of MB to tens of GB.

### Scene `zgc_overview` (renderer: `zgc_overview`)

1. ZGC targets sub-millisecond pauses on large heaps.
2. Uses colored pointers and load barriers for concurrent compaction.
3. Most work happens concurrently — STW phases are tiny.
4. Flag UseZGC — available since Java 15, production-ready in LTS releases.
5. Shenandoah is an alternative low-pause collector with similar goals.
6. Choose ZGC when pause latency is critical and heap is large.

### Scene `choosing_collector` (renderer: `choosing_collector`)

1. How to choose a collector for your workload.
2. Small heap, single core — Serial GC, minimal overhead.
3. Batch processing, throughput priority — Parallel GC.
4. General web services, moderate heaps — G1 default is a solid start.
5. Large heap, strict latency SLA — ZGC or Shenandoah.
6. Always validate with GC logs and load tests — not blog posts.

### Scene `flags_overview` (renderer: `flags_overview`)

1. Key GC flags to know.
2. UseG1GC, UseParallelGC, UseSerialGC, UseZGC — select the collector.
3. Xms and Xmx set initial and maximum heap size.
4. MaxGCPauseMillis tunes G1 pause target.
5. Xlog:gc* enables unified GC logging in modern JDK.
6. Print flags with java -XX:+PrintFlagsFinal -version for your JVM.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — switching to ZGC without measuring — adds overhead for small heaps.
3. Two — setting MaxGCPauseMillis to one millisecond — unrealistic expectation.
4. Three — copying GC flags from another app without matching workload.
5. Also — ignoring GC logs after a collector change.
6. Collector choice is empirical — profile your actual traffic patterns.

### Scene `interview` (renderer: `interview`)

1. Interview question — which GC collector would you choose?
2. Serial — tiny single-core apps. Parallel — throughput batch jobs.
3. G1 — default general purpose, region-based, pause-time target.
4. ZGC — large heap, sub-ms pause goals, concurrent compaction.
5. Trade throughput versus latency — no one-size-fits-all answer.
6. Tune with GC logs, heap sizing, and realistic load tests.

### Scene `teaser` (renderer: `teaser`)

1. Even the best collector cannot fix memory leaks.
2. Episode Fifty-Seven — Memory Leaks and Profiling.
3. Heap dumps, MAT, and finding what holds references alive.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **66** — *G1GC*.
- **Series catalog mapping:** Episode 56 / catalog column `56` / published title *GC Collectors*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 66 → episode 56). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Five showed the JIT compiling hot bytecode to native code._
- **`title`** — starts from: _Episode Fifty-Six._
- **`serial_parallel`** — starts from: _Serial GC uses a single thread for all collection work._
- **`g1_collector`** — starts from: _G1 — Garbage First — is the default collector since Java 9._
- **`zgc_overview`** — starts from: _ZGC targets sub-millisecond pauses on large heaps._
- **`choosing_collector`** — starts from: _How to choose a collector for your workload._
- **`flags_overview`** — starts from: _Key GC flags to know._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — which GC collector would you choose?_
- **`teaser`** — starts from: _Even the best collector cannot fix memory leaks._
