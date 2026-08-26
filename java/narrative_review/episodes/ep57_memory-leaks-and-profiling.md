# Episode 57 — Memory Leaks and Profiling

| Field | Value |
|---|---|
| Episode | 57 |
| Title | Memory Leaks and Profiling |
| Catalog handbook column | 57 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

In the last episode we chose collectors and stared at GC logs. Sometimes those logs look healthy — short pauses, steady young collections — and yet the old generation keeps climbing until the process dies. People say "GC is broken." More often, GC is doing exactly what it should: it cannot reclaim objects that are still reachable. Your object graph is stubborn.

A classic C-style leak is "I forgot to free." A classic Java leak is "something still points at this." The object graph keeps a path from a GC root to memory you thought was temporary. Profilers and heap dumps exist to find that path. Until you see it, every theory about "maybe we need ZGC" is a distraction.

Picture an orders service that caches product details in a static map "for speed." Every SKU ever requested lands there. No maximum size. No time-to-live. After a week, the cache is the live set. GC finds the map from a static field — a GC root — and leaves everything alone. From the outside it looks like a memory leak. From the inside it is an unbounded cache — a reference leak with a product justification. The fix is bounds or eviction, not a new collector flag.

Listeners tell the same story differently. A domain event bus registers a listener and nobody unregisters it when the feature goes away. The listener closes over a service that closes over a repository. The bus lives for the life of the process, so does everything the listener can reach. ThreadLocal misuse on pools is another classic: request-scoped state stays on a worker thread until something clears it. The next request may see stale data; the heap may retain graphs that should have died with the request. Pooled threads are long-lived roots wearing short-lived costumes.

When the heap is climbing, guessing which pattern is guilty wastes hours. Capture evidence under load — while the problem is visible:

```bash
jcmd <pid> GC.heap_dump /tmp/app.hprof
```

That dump is a snapshot of the object graph. Open it in a profiler and resist staring only at total bytes. Look for dominator trees. A dominator owns a large retained set — if it became unreachable, a whole subgraph would go with it. The tree answers what is keeping this memory alive. Often the answer is a static collection, a cache, a registry, a ThreadLocal map, or a classloader that cannot unload. Paths to GC roots turn a vague "memory leak" into a sentence you can paste into a ticket.

Walk one concrete example. The dominator tree shows a `ConcurrentHashMap` retaining gigabytes. Expand it: `ProductCache.CACHE`, string keys, fat DTOs. Now you know the mechanism. The fix is a size limit, a TTL, explicit invalidation, or not caching that data in-process — not G1 versus Shenandoah. Profiling without a willingness to change retention policy is sightseeing.

Before you open the dump, notice what metrics already said. Heap used after full GC trends upward across hours. Allocation rate may look normal; pause times may look fine. That combination is retention, not a collector that forgot how to collect. Teams that only watch pause percentiles miss it until the process dies. Watch live set size and heap after collection. Another habit: compare two dumps — early climb and near danger. Diffing dominators shows what grew. A cache that was always large is a design choice; one that grew tenfold since morning is an incident.

Classloader leaks deserve a mention in hot-reload and plugin stories. If something in an old loader is still referenced from a longer-lived loader, the entire loader — classes and static fields — can stick around. Metaspace climbs. People retune GC. The real bug is a reference from the wrong lifetime.

War-room misunderstandings: guessing instead of dumping; fixating on GC settings when the leak is the reference graph; taking one dump after restart when the live set has already collapsed — you needed the dump under load, at the ugly moment.

If someone asks what a classic Java leak looks like, answer with mechanisms: unbounded caches, static collections, forgotten listeners, ThreadLocal values left on pooled threads. Then add how you would prove it — heap dump under load, dominator tree, retained size, path to GC roots. That second half separates vocabulary from on-call readiness.

We started from a climbing heap that GC could not save and arrived at reachability as the real subject. But production pain is not only memory. Sometimes the app is stuck, slow, or mysteriously idle-burning CPU. Episode Fifty-Eight puts jcmd, JFR, thread dumps, and profilers into one incident playbook.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Memory Leaks and Profiling (Episode 57).

Narration technique: healthy GC + climbing heap → reference-leak thesis → unbounded cache / listeners / ThreadLocal → heap dump → dominators → metrics + dump diffs → classloader leaks → misconceptions → interview woven → bridge to diagnostics.

Teaching points preserved: dominator trees; unbounded caches; listener leaks; ThreadLocal pool leaks; heap dumps under load.
