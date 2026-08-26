# Episode 56 — GC Collectors

| Field | Value |
|---|---|
| Episode | 56 |
| Title | GC Collectors |
| Catalog handbook column | 56 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Fifty-Five left us with a warmed-up JVM: hot methods become native code, and allocation keeps happening while that code runs. Garbage collection is not optional in that world. The heap fills. Something has to reclaim unreachable objects. The question that follows is not "does Java have GC?" — we already know it does. The question is: which collector should we run, and what are we trading when we choose?

Imagine a checkout API under load. Requests allocate short-lived objects — DTOs, temporary lists, buffers. Some objects live longer: session data, caches, pooled resources. Your product owner does not ask for "GC." They ask for p99 latency under two hundred milliseconds, or for a nightly batch that finishes before the window closes. Those are different goals. Collectors are how the JVM answers different goals with different algorithms. If you treat collector choice as fashion — "what is everyone using?" — you skip the only question that matters: what does this service owe its users?

So start with the trade space, spoken plainly. Throughput means how much useful work the process gets done over time. Latency means how long individual requests wait when the collector pauses threads or steals CPU. Footprint means how much memory and processor time the collector itself consumes to do its job. You rarely maximize all three at once. A collector that chases tiny pauses may spend more concurrent CPU. A collector that maximizes batch throughput may pause harder. You pick for service-level objectives, then you measure. Without that order — goals first, flags second — tuning becomes superstition.

On modern server JDKs, G1 is a common default for a reason. It is region-based: the heap is divided into regions, and G1 collects sets of regions rather than treating the whole heap as one monolithic slab every time. That design helps mixed workloads — lots of short-lived garbage plus some longer-lived data — without forcing an exotic configuration on day one. For many services, starting with G1 and learning to read its logs is more honest than hunting for a "best" collector on a blog the night before a launch.

But what if your SLOs are about pause time, not about squeezing every last unit of throughput? That is where low-pause collectors enter the story. ZGC and Shenandoah chase very short pause times by doing more work concurrently with the application. They are not magic free lunches. They shift cost into CPU and footprint. If your app is a latency-sensitive interactive service and you have the headroom, they can be the right answer. If you are a CPU-bound batch transformer on a tight machine, they may be the wrong answer — you paid for concurrency you did not need and slowed the only metric that mattered: wall-clock completion.

That last sentence matters. Parallel and throughput-oriented collectors still exist for a reason. Batch jobs, offline analytics, and some offline pipelines care more about finishing the work than about keeping a user-facing p99 pretty. A collector that pauses harder but reclaims efficiently can win on total time for those workloads. "Newer" is not automatically better. "Lower pause" is not automatically better. Fit the tool to the SLO.

Hold the region idea a moment longer, because it explains more than G1's marketing name. Region-based designs let the collector focus on where garbage actually is. You stop imagining one giant "stop the world and scan everything" story as the only mental model. Concurrent marking, evacuating regions, remembering cross-region references — the vocabulary can grow — but the learner-facing point stays simple: the JVM tries to reclaim memory without treating every collection as a full-heap emergency. Once you see regions, mixed collections and evacuation make more sense as "work on the messy parts" rather than "boil the ocean."

Now make the choice operational. Suppose you decide to run with G1 and you want evidence, not vibes:

```bash
java -XX:+UseG1GC -Xlog:gc*:file=gc.log -jar app.jar
```

Read that command as a contract with yourself. `UseG1GC` selects the collector. `-Xlog:gc*` writes GC behavior somewhere you can inspect after a load test or an incident. Without the log, choosing a collector is mostly storytelling. With the log, you can see pause times, heap occupancy after collections, and whether young collections or mixed collections dominate. That is how you validate against production-like load — not against a laptop idle heap with one user clicking slowly.

And that validation step is where people fall down. Someone copies a flag list from a blog that tuned ZGC for a different heap size and a different allocation pattern. Someone else chases zero pauses for a nightly report that nobody watches live. Someone else switches collectors while ignoring that the real pressure is an unbounded cache allocating like a fire hose. The collector cannot save you from an allocation pattern that never stops growing reachable data. Allocation rate and live set size still set the stage; the collector only performs on that stage. Changing the orchestra does not fix a score that never ends.

So if an interview asks how you choose a collector, answer like an engineer under constraints: match pause and throughput goals to the workload, respect heap size and CPU budget, then measure under realistic load. Say G1 when you mean a solid server default. Say ZGC or Shenandoah when latency SLOs demand it and you can afford the cost. Say a throughput collector when batch wall-clock wins. Then say what you will look at in the GC log to defend the choice — and what you will refuse to change until allocation behavior is understood.

Today we moved from "GC exists" to "GC is a product decision with algorithms behind it." The next pain usually arrives after you pick a collector and the heap still climbs: objects that should have died are still reachable. That is not a collector bug. That is a reference leak — and Episode Fifty-Seven is where we learn to find those chains with dumps and profilers.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — GC Collectors curriculum mapping (Episode 56).

Narration technique: SLO situation → throughput/latency/footprint trade → G1 default → low-pause collectors → batch/throughput collectors → region-based idea → logged command → misconceptions → interview woven in → bridge to leaks.

Teaching points preserved: G1 default; ZGC/Shenandoah; Parallel/throughput for batch; region-based designs; validate with production-like load.
