# Episode 56 — GC Collectors

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Five showed the JIT compiling hot bytecode to native code. Garbage collection algorithms matter just as much for production latency. Different collectors trade throughput against pause time differently.

Serial GC — one thread, simple, fine for tiny heaps. G1 and ZGC target low pause times for large heaps. Today — Serial, Parallel, G1, and ZGC — and when to choose each. Episode Fifty-Six.

GC Collectors. Serial GC uses a single thread for all collection work. Flag UseSerialGC — good for small client apps and single-core machines. Parallel GC — formerly Parallel Old plus Parallel New — multi-threaded.

Flag UseParallelGC — maximizes throughput on batch workloads. Parallel pauses all threads but uses multiple GC threads to finish faster. Default before Java 9 — still valid for compute-heavy, pause-tolerant jobs.

G1 — Garbage First — is the default collector since Java 9. Divides heap into equal-sized regions instead of fixed generations. Concurrent marking identifies regions with the most garbage.

Mixed collections reclaim both young and old regions together. Target pause time via MaxGCPauseMillis — best-effort, not guaranteed. Good general-purpose choice for heaps from hundreds of MB to tens of GB.

ZGC targets sub-millisecond pauses on large heaps. Uses colored pointers and load barriers for concurrent compaction. Most work happens concurrently — STW phases are tiny. Flag UseZGC — available since Java 15, production-ready in LTS releases.

Shenandoah is an alternative low-pause collector with similar goals. Choose ZGC when pause latency is critical and heap is large. How to choose a collector for your workload. Small heap, single core — Serial GC, minimal overhead.

Batch processing, throughput priority — Parallel GC. General web services, moderate heaps — G1 default is a solid start. Large heap, strict latency SLA — ZGC or Shenandoah. Always validate with GC logs and load tests — not blog posts.

Key GC flags to know. UseG1GC, UseParallelGC, UseSerialGC, UseZGC — select the collector. Xms and Xmx set initial and maximum heap size. MaxGCPauseMillis tunes G1 pause target. Xlog:gc* enables unified GC logging in modern JDK.

Print flags with java -XX:+PrintFlagsFinal -version for your JVM. Three common mistakes. One — switching to ZGC without measuring — adds overhead for small heaps. Two — setting MaxGCPauseMillis to one millisecond — unrealistic expectation.

Three — copying GC flags from another app without matching workload. Also — ignoring GC logs after a collector change. Collector choice is empirical — profile your actual traffic patterns.

Interview question — which GC collector would you choose? Serial — tiny single-core apps. Parallel — throughput batch jobs. G1 — default general purpose, region-based, pause-time target.

ZGC — large heap, sub-ms pause goals, concurrent compaction. Trade throughput versus latency — no one-size-fits-all answer. Tune with GC logs, heap sizing, and realistic load tests.

Even the best collector cannot fix memory leaks. Episode Fifty-Seven — Memory Leaks and Profiling. Heap dumps, MAT, and finding what holds references alive. See you there.
