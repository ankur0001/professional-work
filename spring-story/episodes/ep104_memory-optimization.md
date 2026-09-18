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

Gate’s heap chart looks like a staircase: climb, small drop, higher climb, OOMKill. Latency was fine until the pod died. The suspect in this harbor is an unbounded AIS position cache — every vessel ping retained “for the map,” nothing ever evicted. Memory optimization starts with meters, then dumps, then a bounded structure.

```java
// the leak pattern
@Service
public class AisPositionCache {
    private final Map<String, Position> byMmsi = new ConcurrentHashMap<>();

    public void onMessage(AisUpdate update) {
        byMmsi.put(update.mmsi(), update.position()); // grows without bound
    }
}
```

```java
// bounded replacement
@Service
public class AisPositionCache {
    private final Cache<String, Position> byMmsi = Caffeine.newBuilder()
            .maximumSize(50_000)
            .expireAfterWrite(Duration.ofMinutes(30))
            .recordStats()
            .build();

    public AisPositionCache(MeterRegistry registry) {
        registry.gauge("harbor.ais.cache.size", byMmsi, Cache::estimatedSize);
        registry.gauge("harbor.ais.cache.hitRate", byMmsi,
                c -> c.stats().hitRate());
    }

    public void onMessage(AisUpdate update) {
        byMmsi.put(update.mmsi(), update.position());
    }
}
```

Read JVM gauges first: `jvm.memory.used` for heap pools, GC pause timers, and your custom `harbor.ais.cache.size`. If the cache size metric tracks the staircase, you found the villain without a dump. When you need proof, capture a heap dump on OOM (`-XX:+HeapDumpOnOutOfMemoryError`) or via `jcmd` and look for `ConcurrentHashMap` retaining millions of `Position` instances — often reachable from a static or a long-lived `@Service`. Soft/weak references are not a strategy by themselves — bounds and TTLs are. After bounding, watch hit rate: a bound so tight the yard map thrashes is a different incident (CPU + Feign refetch), not success.

Container cgroups matter. A JVM that believes it has the node’s RAM will not GC as a 512Mi limit requires. Prefer container-aware heap settings on modern JDKs (`UseContainerSupport` is default on recent releases) and set requests/limits intentionally. Symptom of mismatch: pod killed by the node while heap graphs look “only 40% used” because the JVM’s max heap exceeded the cgroup. Native memory (direct buffers, metaspace, compressed class space) can kill a pod while heap looks calm — different tools (`Native Memory Tracking`, allocator profiles), same discipline of evidence.

Paging exports and large bill-of-lading byte arrays in memory deserve the same skepticism: stream to disk or object storage; do not buffer an entire PDF fleet in a `byte[]` list. Hibernate session caches and “open EntityManager in view” surprises retain graphs longer than a request needs — close the persistence context at the boundary you designed.

Walk the fix timeline. Deploy Caffeine bounds; `harbor.ais.cache.size` plateaus near 50k; heap sawtooth returns to a healthy GC pattern; OOMKills stop. If size plateaus but heap still climbs, you have a second retainer — continue with a dump instead of raising the cache again. Raising `-Xmx` alone without a bound postpones the kill and takes neighboring pods with you when the node pressures.

Trade-offs: larger heaps absorb spikes and lengthen GC pauses; smaller heaps fail fast. Off-heap caches move pressure without removing the need for bounds. Eviction by size versus time depends on whether stale AIS is useless after thirty minutes regardless of map cardinality.

After an OOMKill, pull the dump from the crashed container’s volume or an object-store hook before the node reaps disk. Annotate the incident with `harbor.ais.cache.size` at kill time and the dominant retained type from the dump analyzer. That pair — metric plus dump class — is what stops the next “raise the heap” argument in the postmortem.

A misconception is “raising the heap” as the first fix for an unbounded cache — you postponed the OOM and raised the blast radius. Another is enabling every Spring cache region with eternal TTLs. A third is ignoring cache hit/miss metrics after bounding, so you never see whether the bound is too tight for the yard map.

Metrics, traces, memory hygiene — you have operational lenses. What remains is bundling them into a definition of ready to serve production traffic, not merely feature complete.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 104 (*Memory Optimization*).
