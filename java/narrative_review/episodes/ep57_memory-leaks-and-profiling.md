# Episode 57 — Memory Leaks and Profiling

| Field | Value |
|---|---|
| Episode | 57 |
| Title | Memory Leaks and Profiling |
| Catalog handbook column | 57 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

In the last episode we chose collectors and stared at GC logs. Sometimes those logs look healthy — short pauses, steady young collections — and yet the old generation keeps climbing until the process dies. That is a confusing night. People say "GC is broken." More often, GC is doing exactly what it should: it cannot reclaim objects that are still reachable. The collector is not lost. Your object graph is stubborn.

So here is the Java-shaped truth. A classic C-style leak is "I forgot to free." A classic Java leak is "something still points at this." The object graph keeps a path from a GC root to memory you thought was temporary. Profilers and heap dumps exist to find that path. Until you see the path, every theory about "maybe we need ZGC" is a distraction dressed as expertise.

Picture an orders service that caches product details in a static map "for speed." Every SKU ever requested lands in the map. There is no maximum size. There is no time-to-live. After a week of traffic, the cache is the live set. GC runs. GC finds the map from a static field — a GC root. GC leaves everything alone. From the outside it looks like a memory leak. From the inside it is an unbounded cache — a reference leak with a product justification. The fix is bounds or eviction, not a new collector flag.

Listeners tell the same story in a different costume. A domain event bus registers a listener and nobody unregisters it when the feature goes away. The listener closes over a service that closes over a repository that closes over a connection pool wrapper. The bus lives for the life of the process. So does everything the listener can reach. ThreadLocal misuse on thread pools is another classic: you put request-scoped state into a ThreadLocal, the worker thread returns to the pool, and the value stays until something clears it. The next request may see stale data. The heap may retain graphs that should have died with the request. Pooled threads are long-lived roots wearing short-lived costumes.

When the heap is climbing, guessing which of those patterns is guilty wastes hours. Capture evidence under load — while the problem is visible:

```bash
jcmd <pid> GC.heap_dump /tmp/app.hprof
```

That dump is a snapshot of the object graph. Open it in a profiler or heap analyzer and resist the urge to stare only at total bytes. Look for dominator trees. A dominator is an object that owns a large retained set — if that object became unreachable, a whole subgraph would go with it. The dominator tree answers the question you actually have: what is keeping this memory alive? Often the answer is a static collection, a cache, a registry, a ThreadLocal map, or a classloader that cannot unload. Paths to GC roots turn a vague "memory leak" into a sentence you can paste into a ticket.

Walk a concrete mental example. You dump the heap. The dominator tree shows a `ConcurrentHashMap` retaining gigabytes. You expand it. The map is `ProductCache.CACHE`. Keys are strings; values are fat DTOs with nested collections. Now you know the mechanism. The fix is not G1 versus Shenandoah. The fix is a size limit, a TTL, explicit invalidation, or not caching that data in-process at all. Profiling without a willingness to change retention policy is sightseeing.

Classloader leaks deserve a special mention in hot-reload and plugin stories. If something in an old loader is still referenced from a longer-lived loader, the entire loader — and all its classes and static fields — can stick around. Metaspace climbs. Heaps look weird across redeploys. People retune GC. The real bug is a reference from the wrong lifetime. Ignoring classloader leaks in hot reload is how teams fight the same outage every Friday afternoon deploy.

Common misunderstandings show up in the war room. First: guessing instead of dumping. "It must be the new feature" without a dump is storytelling. Second: fixating on GC settings when the leak is the reference graph. Tuning G1 will not shrink an unbounded static map. Third: taking one dump after restart when the live set has already collapsed — you needed the dump under load, at the ugly moment.

If someone asks in an interview what a classic Java leak looks like, answer with mechanisms: unbounded caches, static collections, forgotten listeners, ThreadLocal values left on pooled threads. Then add how you would prove it — heap dump under load, dominator tree, retained size, path to GC roots. That second half is what separates vocabulary from on-call readiness.

We started from a climbing heap that GC could not save and arrived at reachability as the real subject. Dumps and dominators are the microscope. But production pain is not only memory. Sometimes the app is stuck, slow, or mysteriously idle-burning CPU. For that you need a wider toolkit — and Episode Fifty-Eight is where we put jcmd, JFR, thread dumps, and profilers into one incident playbook.

Before you even open the dump, notice what the metrics should have told you. Heap used after full GC trends upward across hours. Allocation rate may look normal. Pause times may look fine. That combination is the signature of retention, not of a collector that forgot how to collect. Teams that only watch pause percentiles miss retention until the process dies. Watch live set size and heap after collection, not only pause duration.

Before you even open the dump, notice what the metrics should have told you. Heap used after full GC trends upward across hours. Allocation rate may look normal. Pause times may look fine. That combination is the signature of retention, not of a collector that forgot how to collect. Teams that only watch pause percentiles miss retention until the process dies. Watch live set size and heap after collection, not only pause duration.

Another practical habit: compare two dumps. One early in the climb, one near the danger zone. Diffing dominators across time shows what grew, not only what is large. A large cache that was always large is a design choice. A cache that grew tenfold since morning is an incident. Profilers make that comparison possible when you treat dumps as a time series instead of a single panic artifact.

Another practical habit: compare two dumps. One early in the climb, one near the danger zone. Diffing dominators across time shows what grew, not only what is large. A large cache that was always large is a design choice. A cache that grew tenfold since morning is an incident. Profilers make that comparison possible when you treat dumps as a time series instead of a single panic artifact.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Memory Leaks and Profiling (Episode 57).

Narration technique: healthy GC + climbing heap → reference-leak thesis → unbounded cache / listeners / ThreadLocal → heap dump command → dominator trees → worked example → classloader leaks → misconceptions → interview woven → bridge to diagnostics.

Teaching points preserved: dominator trees; unbounded caches; listener leaks; ThreadLocal pool leaks; heap dumps under load.
