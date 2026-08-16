# Episode 65 — JVM Startup

| Field | Value |
|---|---|
| Episode | 65 |
| Title | JVM Startup |
| Catalog handbook column | 65 |
| Narration source script | `make_episode_65.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Sixty-Four explained safepoints and stop-the-world coordination.
2. Runtime pauses matter — but so does the time before your service is ready.
3. Cold JVM startup loads hundreds of classes, initializes JIT, and warms caches.
4. First requests after deploy are often slow — class loading and interpretation dominate.
5. Class Data Sharing and warmup strategies shrink that cold-start penalty.
6. Today — JVM startup phases, class loading cost, CDS, and warmup.

### Scene `title` (renderer: `title`)

1. Episode Sixty-Five.
2. JVM Startup and Warmup.

### Scene `startup_phases` (renderer: `startup_phases`)

1. JVM startup unfolds in distinct phases before your main method runs.
2. VM initialization — memory regions, thread system, and core subsystems.
3. Class loading and linking — bootstrap classes, then application classpath.
4. Interpreter executes bytecode until JIT identifies hot methods.
5. JIT compilation kicks in — C1 quick compile, then C2 optimizing compile.
6. Steady state — most hot code runs compiled native instructions.

### Scene `class_loading_cost` (renderer: `class_loading_cost`)

1. Class loading is a major cold-start cost for large applications.
2. Each class — parse bytecode, verify, create Class object in metaspace.
3. Spring and dependency injection frameworks load thousands of classes at boot.
4. Fat JARs with many dependencies multiply class count and startup time.
5. Lazy initialization defers loading — but first touch still pays the cost.
6. Measure with -Xlog:class+load or startup JFR events — know your baseline.

### Scene `cds_appcds` (renderer: `cds_appcds`)

1. Class Data Sharing — CDS — archives loaded classes for faster restart.
2. JVM builds a shared archive of classes at training time.
3. Subsequent JVM instances memory-map the archive — skip parse and verify.
4. AppCDS extends CDS to application classpath classes — not just bootstrap.
5. java -Xshare:dump with classpath creates the archive — -Xshare:on uses it.
6. Container images can bake the archive in — significant startup improvement.

### Scene `warmup_strategies` (renderer: `warmup_strategies`)

1. Warmup brings the JVM to steady state before serving production traffic.
2. Synthetic load — replay health checks or canary requests after deploy.
3. AOT compilation — GraalVM native image — trades flexibility for instant start.
4. Tiered compilation — TieredStopAtLevel tunes how aggressively JIT compiles.
5. Spring AOT and CRaC explore checkpoint-restore for sub-second restarts.
6. Warmup is workload-specific — exercise the code paths users actually hit.

### Scene `measurement_startup` (renderer: `measurement_startup`)

1. Measure startup like any other performance metric.
2. Time from process start to ready — health endpoint responding.
3. JFR ApplicationStarted and ClassLoad events break down phases.
4. Compare cold start versus warm restart — CDS impact is visible immediately.
5. Track P99 latency for first N requests after deploy — the warmup window.
6. Set SLOs on startup time — regressions from new dependencies are common.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — measuring only steady-state latency — ignoring cold-start after deploy.
3. Two — skipping warmup in staging — production first request pays the cost.
4. Three — adding dependencies without checking class count impact.
5. Also — assuming GraalVM native image fits every service — reflection limits apply.
6. Profile startup separately — it is a different problem than throughput tuning.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you reduce JVM startup time?
2. Identify class loading cost — log class load events, count classes.
3. CDS and AppCDS — shared archives skip parse and verify on restart.
4. Warmup traffic before cutting over — JIT compiles hot paths.
5. Lazy init and smaller classpath reduce classes loaded at boot.
6. Measure time-to-ready — not just main method entry.

### Scene `teaser` (renderer: `teaser`)

1. Startup and warmup complete the internals picture — time to tie it together.
2. Episode Sixty-Six — JVM Interview Wrap-Up.
3. Crisp explanations of heap, stack, GC, and JIT for interviews.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **65** — *GC Algorithms*.
- **Series catalog mapping:** Episode 65 / catalog column `65` / published title *JVM Startup*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Sixty-Four explained safepoints and stop-the-world coordination._
- **`title`** — starts from: _Episode Sixty-Five._
- **`startup_phases`** — starts from: _JVM startup unfolds in distinct phases before your main method runs._
- **`class_loading_cost`** — starts from: _Class loading is a major cold-start cost for large applications._
- **`cds_appcds`** — starts from: _Class Data Sharing — CDS — archives loaded classes for faster restart._
- **`warmup_strategies`** — starts from: _Warmup brings the JVM to steady state before serving production traffic._
- **`measurement_startup`** — starts from: _Measure startup like any other performance metric._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you reduce JVM startup time?_
- **`teaser`** — starts from: _Startup and warmup complete the internals picture — time to tie it together._
