# Episode 54 — Garbage Collection

| Field | Value |
|---|---|
| Episode | 54 |
| Title | Garbage Collection |
| Catalog handbook column | 54 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Heap and stack showed where objects live and where locals keep references. The next pressure is automatic: we are not calling `free()`. So who reclaims memory, and what makes an object reclaimable?

Garbage collection reclaims unreachable objects. Your allocation rate sets the pace. Treat GC as a partner that responds to how fast you allocate and how long you retain — not as an enemy that randomly pauses your app for sport.

```java
// Object becomes collectible when nothing reachable can touch it
List<byte[]> tmp = new ArrayList<>();
tmp.add(new byte[1024 * 1024]);
tmp = null; // if no other refs, GC may reclaim
```

Walk the reachability idea. While `tmp` points at the list, and the list points at the big array, those objects are reachable from a stack local — a GC root. When you set `tmp = null` (or the frame ends), if nothing else references that list, the list and its array become unreachable. They are then eligible for collection. "Eligible" is not "collected this millisecond." The collector runs according to its strategy and heap pressure. Correctness is reachability; timing is policy.

GC roots include stack references, static fields, JNI references, and a few other anchors. Mentally graph from roots downward. Anything not in that graph can go. Caching forever — static maps that only ever grow — keeps objects reachable on purpose and then surprises you when the heap fills. The GC is not leaking. Your retention policy is.

The generational hypothesis says most objects die young. Collectors exploit that: concentrate effort on young generations where most garbage appears, and promote survivors to older spaces. You will meet specific collectors later. Today, hold the why: allocation patterns that create many short-lived objects play to generational strengths; gigantic mid-life retention patterns stress them differently.

Pauses versus concurrent work is the latency story. Some collection work stops application threads briefly; some runs concurrently with them. Different collectors balance throughput, pause goals, and footprint differently. Tuning without metrics is superstition. Before you flip flags, measure allocation rate, pause times, heap occupancy, and promotion. The flags exist to respond to evidence.

```text
allocate fast → young collections more often
retain long → more old-generation pressure
cache forever → eventual OutOfMemory or endless full collections
```

What if we allocate insanely in tight loops — building strings with `+` in a hot path, creating temporary objects per packet — and then blame GC for "too many pauses"?

GC is responding to the trash you produce. Reduce allocation, reuse buffers carefully, or change the algorithm. Treating GC as the villain while ignoring allocation rate is backwards. Profiling allocation is often the real performance move.

Tuning without metrics deserves a second scolding. Copying a blog's `-Xmx` and collector choice from a different workload can make things worse. Start with defaults, measure, change one thing, measure again. Collector-specific episodes will expand the menu; curiosity should already be tied to evidence.

Allocation rate is the heartbeat GC hears. A service allocating hundreds of megabytes per second will collect frequently even with a huge heap. A service allocating modestly but retaining everything in a static cache will promote and fill old space until a painful collection or OOM. Two different pathologies; both show up as "GC problem" in chat until you measure.

Young collections being frequent is not automatically bad if pauses are tiny and throughput is fine. Full collections thrashing is bad. Learn to read the difference in logs before you retune. Collector-specific episodes will name G1, ZGC, and friends — for now, demand metrics first, logos second.

What if we "fix" a leak by increasing `-Xmx` every week? We delay the incident and grow the blast radius. Retention bugs deserve graphs and heap dumps, not larger handbags for the same junk.

Hold a practical checklist: collectibility is reachability; retention is a product decision; allocation rate drives pace; generational behavior explains young vs old pressure; measure before tuning. Meet those and GC stops being a superstition contest.

When you open logs, look for frequency of collections, pause times, and whether the heap recovers after a collection. A heap that never frees after full GC is a retention problem wearing a collector costume.

Picture two services with identical heap sizes. One allocates temporary buffers per request and discards them; young GC is busy and pauses stay small. The other accumulates session state forever; old generation grows until a long pause or OOM. Same `-Xmx`, opposite outcomes. GC policy cannot save a retention strategy that never forgets.

When product asks for a bigger heap as the first move, ask for allocation and occupancy charts first. Bigger heaps can mean rarer but longer pauses on some collectors — another reason evidence beats folklore.

 Prefer reducing retention and allocation waste before exotic collector flags. Collectors differ, but none thrive on infinite caches and pointless object churn. Partner with GC by making less garbage and keeping less junk.

 That partnership mindset — measure, reduce churn, then tune — is the entire skill this episode is trying to install before collector deep-dives begin.

So reconnect the chain. Unreachable objects become collectible. Roots and retention explain why. Generational behavior explains common patterns. Pauses and concurrency explain latency trade-offs. Allocation rate and metrics-first tuning keep you honest. The next runtime curiosity is how hot code stops being interpreted and becomes optimized native code — and why the first requests after startup feel slower.

Episode Fifty-Five: JIT compilation.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 54 (*Garbage Collection*).

Narration technique: who-reclaims situation → reachability walkthrough → roots/caching → generational hypothesis → pauses vs concurrent → allocation rate → next natural problem (JIT).
