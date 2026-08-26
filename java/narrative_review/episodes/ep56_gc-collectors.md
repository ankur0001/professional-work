# Episode 56 — GC Collectors

| Field | Value |
|---|---|
| Episode | 56 |
| Title | GC Collectors |
| Catalog handbook column | 56 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Fifty-Five left us with a warmed-up JVM: hot methods become native code, and allocation keeps happening while that code runs. The heap fills. Something has to reclaim unreachable objects. The question is no longer "does Java have GC?" — it is which collector should we run, and what are we trading when we choose?

Imagine a checkout API under load. Requests allocate short-lived objects — DTOs, temporary lists, buffers — while some data lives longer: sessions, caches, pools. Your product owner does not ask for "GC." They ask for p99 latency under two hundred milliseconds, or for a nightly batch that finishes before the window closes. Those are different goals. Collectors answer different goals with different algorithms. Treat collector choice as fashion — "what is everyone using?" — and you skip the only question that matters: what does this service owe its users?

Speak the trade space plainly. Throughput is useful work over time. Latency is how long requests wait when the collector pauses threads or steals CPU. Footprint is how much memory and processor time the collector itself consumes. You rarely maximize all three. Tiny pauses often cost concurrent CPU; batch throughput often accepts harder pauses. Pick for service-level objectives, then measure. Goals first, flags second — otherwise tuning is superstition.

On modern server JDKs, G1 is a common default for a reason. It is region-based: the heap is divided into regions, and G1 collects sets of regions rather than treating the whole heap as one slab every time. That helps mixed workloads — lots of short-lived garbage plus some longer-lived data — without exotic configuration on day one. Starting with G1 and learning to read its logs is more honest than hunting for a "best" collector the night before launch.

When SLOs are about pause time, low-pause collectors enter. ZGC and Shenandoah chase short pauses by doing more work concurrently with the application. They are not free lunches — they shift cost into CPU and footprint. Latency-sensitive services with headroom can win. CPU-bound batch jobs on tight machines may lose: you paid for concurrency you did not need and slowed wall-clock completion.

Parallel and throughput-oriented collectors still exist for that reason. Batch jobs and offline pipelines often care more about finishing than about a pretty user-facing p99. A collector that pauses harder but reclaims efficiently can win on total time. "Newer" is not automatically better. "Lower pause" is not automatically better. Fit the tool to the SLO.

Region-based design is the mental model upgrade. The JVM tries to reclaim where garbage actually is instead of treating every collection as a full-heap emergency. Once you see regions, mixed collections and evacuation read as "work on the messy parts" rather than "boil the ocean."

Make the choice operational — evidence, not vibes:

```bash
java -XX:+UseG1GC -Xlog:gc*:file=gc.log -jar app.jar
```

`UseG1GC` selects the collector. `-Xlog:gc*` writes behavior you can inspect after a load test or incident. Without the log, choosing a collector is storytelling. With it, you see pause times, occupancy after collections, and whether young or mixed collections dominate — validated under production-like load, not a laptop idle heap.

People fall down when they copy blog flags for a different heap and allocation pattern, chase zero pauses for a nightly report nobody watches live, or switch collectors while an unbounded cache grows the live set forever. The collector performs on the stage set by allocation rate and live set size. Changing the orchestra does not fix a score that never ends.

If an interview asks how you choose a collector, answer under constraints: match pause and throughput goals to the workload, respect heap and CPU budget, then measure under realistic load. G1 for a solid server default; ZGC or Shenandoah when latency SLOs demand it and you can afford the cost; a throughput collector when batch wall-clock wins. Say what you will look at in the GC log — and what you will refuse to change until allocation behavior is understood.

Today we moved from "GC exists" to "GC is a product decision with algorithms behind it." The next pain usually arrives after you pick a collector and the heap still climbs: objects that should have died are still reachable. That is not a collector bug. That is a reference leak — and Episode Fifty-Seven is where we find those chains with dumps and profilers.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — GC Collectors curriculum mapping (Episode 56).

Narration technique: SLO situation → throughput/latency/footprint trade → G1 default → low-pause collectors → batch/throughput collectors → region-based idea → logged command → misconceptions → interview woven in → bridge to leaks.

Teaching points preserved: G1 default; ZGC/Shenandoah; Parallel/throughput for batch; region-based designs; validate with production-like load.
