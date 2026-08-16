# Episode 62 — JVM Flags and Tuning

| Field | Value |
|---|---|
| Episode | 62 |
| Title | JVM Flags and Tuning |
| Catalog handbook column | 62 |
| Narration source script | `make_episode_62.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-One covered soft, weak, and phantom references.
2. Reference types shape object lifetime — JVM flags shape runtime behavior.
3. Every production JVM starts with dozens of implicit defaults.
4. Heap size, collector choice, and logging flags change latency and stability.
5. Copying flags from a blog post without measurement is a common failure mode.
6. Today — JVM flags, heap sizing, GC switches, and a measurement-first mindset.

### Scene `title` (renderer: `title`)

1. Episode Sixty-Two.
2. JVM Flags and Tuning Basics.

### Scene `heap_sizing` (renderer: `heap_sizing`)

1. Heap sizing starts with -Xms and -Xmx.
2. -Xms sets initial heap — -Xmx sets maximum heap the JVM may use.
3. Matching Xms to Xmx avoids resize pauses during steady state.
4. Too small — frequent GC and OutOfMemoryError under load.
5. Too large — long GC pauses and wasted RAM on shared hosts.
6. Start from observed usage under realistic traffic — add headroom, not guesses.

### Scene `gc_flags` (renderer: `gc_flags`)

1. Collector flags select the garbage collector implementation.
2. -XX:+UseG1GC — default general-purpose collector since Java 9.
3. -XX:+UseZGC — low-pause collector for large heaps and strict latency.
4. -XX:+UseParallelGC — throughput-oriented for batch workloads.
5. MaxGCPauseMillis tunes G1 pause target — best effort, not a guarantee.
6. Collector choice is empirical — validate with GC logs on your workload.

### Scene `diagnostic_flags` (renderer: `diagnostic_flags`)

1. Diagnostic flags make invisible behavior visible.
2. -Xlog:gc* enables unified GC logging in modern JDK releases.
3. -XX:+HeapDumpOnOutOfMemoryError writes a heap dump on OOM.
4. -XX:ErrorFile=path captures fatal JVM error details.
5. PrintFlagsFinal lists every flag and its effective value at startup.
6. Flight Recorder and async profilers complement flags — use them before tuning blind.

### Scene `measurement_mindset` (renderer: `measurement_mindset`)

1. Tuning without measurement is guessing.
2. Establish a baseline — latency, throughput, GC pause times, heap usage.
3. Change one variable at a time — flag, heap size, or collector.
4. Replay production traffic or run load tests that match real patterns.
5. Compare before and after with the same dataset and duration.
6. Document what you changed and why — future you will thank present you.

### Scene `common_flags` (renderer: `common_flags`)

1. A practical starter flag set for services.
2. java -Xms4g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200.
3. Add -Xlog:gc*:file=gc.log:time,uptime,level,tags for GC analysis.
4. Container deployments — respect cgroup memory limits with -XX:MaxRAMPercentage.
5. Never set flags you cannot explain in an incident postmortem.
6. Flags are tools — the goal is reliable behavior under real load.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — copying another team's flags without matching workload or heap.
3. Two — setting Xmx to all available RAM — no room for metaspace or OS cache.
4. Three — tuning GC before fixing allocation hotspots in application code.
5. Also — changing five flags at once — impossible to attribute improvements.
6. Measure first, tune second, verify third — always in that order.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you tune JVM flags for a service?
2. Start with baseline metrics — latency percentiles, GC logs, heap usage.
3. Size heap from observed peak plus headroom — match Xms and Xmx when stable.
4. Choose collector for workload — G1 default, ZGC for strict pause goals.
5. Enable GC logging and OOM heap dumps before changing anything.
6. Change one knob, re-test, document — never tune from blog posts alone.

### Scene `teaser` (renderer: `teaser`)

1. Flags control the JVM — object layout controls how much memory each instance uses.
2. Episode Sixty-Three — Object Layout and Compressed Oops.
3. Headers, padding, and pointer compression on 64-bit heaps.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **68** — *JVM Tuning*.
- **Series catalog mapping:** Episode 62 / catalog column `62` / published title *JVM Flags and Tuning*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 68 → episode 62). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-One covered soft, weak, and phantom references._
- **`title`** — starts from: _Episode Sixty-Two._
- **`heap_sizing`** — starts from: _Heap sizing starts with -Xms and -Xmx._
- **`gc_flags`** — starts from: _Collector flags select the garbage collector implementation._
- **`diagnostic_flags`** — starts from: _Diagnostic flags make invisible behavior visible._
- **`measurement_mindset`** — starts from: _Tuning without measurement is guessing._
- **`common_flags`** — starts from: _A practical starter flag set for services._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you tune JVM flags for a service?_
- **`teaser`** — starts from: _Flags control the JVM — object layout controls how much memory each instance uses._
