# Episode 104 — Memory Optimization

| Field | Value |
|---|---|
| Episode | 104 |
| Title | Memory Optimization |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 104 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The latency panel looked fine until the pod restarted every forty minutes. Grafana’s heap gauge climbed like a staircase. GC pause metrics spiked near the top of each ramp. That is not a "buy a bigger node" story first — it is a memory story: what retains objects, how large the live set is, and whether native memory or the heap is the real pressure.

Start with the meters you already exposed. `jvm.memory.used` and `jvm.memory.max` by area. GC overhead and pause timers. When using a modern collector, allocation rate matters as much as heap size — high allocation with a stable live set is a different problem than a growing old generation. Micrometer’s JVM binders give you the graphs; heap dumps give you the names.

A Spring-specific leak pattern: unbounded caches. `@Cacheable` without eviction, a home-grown `ConcurrentHashMap` as a "quick cache," or a Caffeine cache with maximum size left unset. Another: listening to application events or WebSocket sessions without deregistration. Another: Hibernate persistence contexts or open sessions held across long HTTP calls, pinning entities.

```java
@Bean
public CacheManager cacheManager() {
    CaffeineCacheManager manager = new CaffeineCacheManager("productBySku");
    manager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(10_000)
            .expireAfterWrite(Duration.ofMinutes(10))
            .recordStats());
    return manager;
}
```

`recordStats()` plus Micrometer cache metrics lets you see hit rate and eviction. A cache that never evicts and always grows is a leak with good intentions.

Watch payload and collection sizes in your own code. Loading `findAll()` into a list for a report, mapping entities to DTOs that embed large blobs, or buffering entire multipart uploads in memory will show up as allocation spikes under load. Stream, page, or spill to disk when the domain allows it.

```java
@Transactional(readOnly = true)
public void exportPrices(Consumer<PriceRow> out) {
    int page = 0;
    Page<PriceRow> slice;
    do {
        slice = prices.findAll(PageRequest.of(page++, 500));
        slice.forEach(out);
    } while (slice.hasNext());
}
```

Container memory limits interact with the JVM. If the cgroup limit is 512Mi and the heap is set as if the machine had 8Gi, you get OOMKills that look mysterious in app logs. Prefer container-aware heap settings (modern JDKs help) and leave headroom for metaspace, direct buffers, and thread stacks. Direct `ByteBuffer` use and Netty arenas can exhaust native memory while the heap graph looks calm — another reason to watch more than one panel.

How to investigate: capture a heap dump on OOM (`-XX:+HeapDumpOnOutOfMemoryError`) or via Actuator/`jcmd` in a safe environment. Dominator trees in Eclipse MAT or VisualVM answer "what retains what?" Class histograms answer "how many of these?" If the dump points at a Spring bean you expected to be a tiny singleton holding a giant map, you found the bug.

Misconception: "GC tuning flags will fix a leak." They can delay the crash. Fix retention. Misconception: "more heap always helps." Oversized heaps make full GCs rarer but longer and hide leaks until traffic peaks.

Today we tied heap gauges to Spring cache and paging habits, respected container limits, and treated dumps as evidence. Metrics, traces, memory hygiene — you have the operational lenses. What remains is bundling them into a definition of "ready to serve production traffic," not merely "feature complete."

That checklist is production readiness.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 104 (*Memory Optimization*).

Narration technique: staircase heap → meters then dumps → Spring leak patterns → Caffeine bounds → paging export → cgroup/native caveats → bridge to readiness.
