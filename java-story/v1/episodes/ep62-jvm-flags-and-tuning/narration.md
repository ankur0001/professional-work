# Episode 62 — JVM Flags and Tuning

**Cut:** v1 (original)

## Transcript (from captions)

Episode Sixty-One covered soft, weak, and phantom references. Reference types shape object lifetime — JVM flags shape runtime behavior. Every production JVM starts with dozens of implicit defaults.

Heap size, collector choice, and logging flags change latency and stability. Copying flags from a blog post without measurement is a common failure mode. Today — JVM flags, heap sizing, GC switches, and a measurement-first mindset.

Episode Sixty-Two. JVM Flags and Tuning Basics. Heap sizing starts with -Xms and -Xmx. -Xms sets initial heap — -Xmx sets maximum heap the JVM may use. Matching Xms to Xmx avoids resize pauses during steady state.

Too small — frequent GC and OutOfMemoryError under load. Too large — long GC pauses and wasted RAM on shared hosts. Start from observed usage under realistic traffic — add headroom, not guesses.

Collector flags select the garbage collector implementation. -XX:+UseG1GC — default general-purpose collector since Java 9. -XX:+UseZGC — low-pause collector for large heaps and strict latency.

-XX:+UseParallelGC — throughput-oriented for batch workloads. MaxGCPauseMillis tunes G1 pause target — best effort, not a guarantee. Collector choice is empirical — validate with GC logs on your workload.

Diagnostic flags make invisible behavior visible. -Xlog:gc* enables unified GC logging in modern JDK releases. -XX:+HeapDumpOnOutOfMemoryError writes a heap dump on OOM. -XX:ErrorFile=path captures fatal JVM error details.

PrintFlagsFinal lists every flag and its effective value at startup. Flight Recorder and async profilers complement flags — use them before tuning blind. Tuning without measurement is guessing.

Establish a baseline — latency, throughput, GC pause times, heap usage. Change one variable at a time — flag, heap size, or collector. Replay production traffic or run load tests that match real patterns.

Compare before and after with the same dataset and duration. Document what you changed and why — future you will thank present you. A practical starter flag set for services. java -Xms4g -Xmx4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200.

Add -Xlog:gc*:file=gc.log:time,uptime,level,tags for GC analysis. Container deployments — respect cgroup memory limits with -XX:MaxRAMPercentage. Never set flags you cannot explain in an incident postmortem.

Flags are tools — the goal is reliable behavior under real load. Three common mistakes. One — copying another team's flags without matching workload or heap. Two — setting Xmx to all available RAM — no room for metaspace or OS cache.

Three — tuning GC before fixing allocation hotspots in application code. Also — changing five flags at once — impossible to attribute improvements. Measure first, tune second, verify third — always in that order.

Interview question — how do you tune JVM flags for a service? Start with baseline metrics — latency percentiles, GC logs, heap usage. Size heap from observed peak plus headroom — match Xms and Xmx when stable.

Choose collector for workload — G1 default, ZGC for strict pause goals. Enable GC logging and OOM heap dumps before changing anything. Change one knob, re-test, document — never tune from blog posts alone.

Flags control the JVM — object layout controls how much memory each instance uses. Episode Sixty-Three — Object Layout and Compressed Oops. Headers, padding, and pointer compression on 64-bit heaps.

See you there.
