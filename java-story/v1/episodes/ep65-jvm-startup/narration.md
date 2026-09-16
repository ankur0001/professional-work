# Episode 65 — JVM Startup

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-Four explained safepoints and stop-the-world coordination. Runtime pauses matter — but so does the time before your service is ready. Cold JVM startup loads hundreds of classes, initializes JIT, and warms caches.

First requests after deploy are often slow — class loading and interpretation dominate. Class Data Sharing and warmup strategies shrink that cold-start penalty. Today — JVM startup phases, class loading cost, CDS, and warmup.

Episode Sixty-Five. JVM Startup and Warmup. JVM startup unfolds in distinct phases before your main method runs. VM initialization — memory regions, thread system, and core subsystems.

Class loading and linking — bootstrap classes, then application classpath. Interpreter executes bytecode until JIT identifies hot methods. JIT compilation kicks in — C1 quick compile, then C2 optimizing compile.

Steady state — most hot code runs compiled native instructions. Class loading is a major cold-start cost for large applications. Each class — parse bytecode, verify, create Class object in metaspace.

Spring and dependency injection frameworks load thousands of classes at boot. Fat JARs with many dependencies multiply class count and startup time. Lazy initialization defers loading — but first touch still pays the cost.

Measure with -Xlog:class+load or startup JFR events — know your baseline. Class Data Sharing — CDS — archives loaded classes for faster restart. JVM builds a shared archive of classes at training time.

Subsequent JVM instances memory-map the archive — skip parse and verify. AppCDS extends CDS to application classpath classes — not just bootstrap. java -Xshare:dump with classpath creates the archive — -Xshare:on uses it.

Container images can bake the archive in — significant startup improvement. Warmup brings the JVM to steady state before serving production traffic. Synthetic load — replay health checks or canary requests after deploy.

AOT compilation — GraalVM native image — trades flexibility for instant start. Tiered compilation — TieredStopAtLevel tunes how aggressively JIT compiles. Spring AOT and CRaC explore checkpoint-restore for sub-second restarts.

Warmup is workload-specific — exercise the code paths users actually hit. Measure startup like any other performance metric. Time from process start to ready — health endpoint responding.

JFR ApplicationStarted and ClassLoad events break down phases. Compare cold start versus warm restart — CDS impact is visible immediately. Track P99 latency for first N requests after deploy — the warmup window.

Set SLOs on startup time — regressions from new dependencies are common. Three common mistakes. One — measuring only steady-state latency — ignoring cold-start after deploy. Two — skipping warmup in staging — production first request pays the cost.

Three — adding dependencies without checking class count impact. Also — assuming GraalVM native image fits every service — reflection limits apply. Profile startup separately — it is a different problem than throughput tuning.

Interview question — how do you reduce JVM startup time? Identify class loading cost — log class load events, count classes. CDS and AppCDS — shared archives skip parse and verify on restart.

Warmup traffic before cutting over — JIT compiles hot paths. Lazy init and smaller classpath reduce classes loaded at boot. Measure time-to-ready — not just main method entry. Startup and warmup complete the internals picture — time to tie it together.

Episode Sixty-Six — JVM Interview Wrap-Up. Crisp explanations of heap, stack, GC, and JIT for interviews. See you there.
