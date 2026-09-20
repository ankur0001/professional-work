# Episode 47 — Caching

| Field | Value |
|---|---|
| Episode | 47 |
| Title | Caching |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 47 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The vessel directory is mostly read. Planners open the same IMO profile dozens of times an hour. Without a cache, every open is a SELECT. With a cache that never evicts, a renamed vessel stays wrong until someone restarts the pod. Spring’s cache abstraction sits between those failure modes: cache directory reads; evict on update.

Enable caching with `@EnableCaching` and a `CacheManager` — Boot will autoconfigure simple or Redis-backed managers depending on the classpath. Then declare stereotypes on the service that owns vessel directory access:

```java
@Service
public class VesselDirectory {

    private final VesselRepository vessels;

    public VesselDirectory(VesselRepository vessels) {
        this.vessels = vessels;
    }

    @Cacheable(cacheNames = "vesselsByImo", key = "#imoNumber")
    @Transactional(readOnly = true)
    public VesselView findByImo(String imoNumber) {
        return vessels.findByImoNumber(imoNumber)
                .map(VesselView::from)
                .orElseThrow(() -> new VesselNotFoundException(imoNumber));
    }

    @CacheEvict(cacheNames = "vesselsByImo", key = "#imoNumber")
    @Transactional
    public void rename(String imoNumber, String newName) {
        Vessel vessel = vessels.findByImoNumber(imoNumber).orElseThrow();
        vessel.rename(newName);
    }

    @CacheEvict(cacheNames = "vesselsByImo", allEntries = true)
    @Transactional
    public void importRegistryBatch(List<VesselDraft> drafts) {
        // bulk import — safer to clear the directory cache wholesale
        drafts.forEach(d -> vessels.save(d.toEntity()));
    }
}
```

`@Cacheable` runs the method on a miss and stores the return value under the key. On a hit, the method body — and the SELECT — do not run. `@CacheEvict` removes stale entries when the directory changes. Key design matters: IMO number is a natural key; evicting the wrong key leaves ghosts.

What you cache matters as much as whether you cache. Prefer immutable views or DTOs over managed entities. Caching a managed `Vessel` and then mutating it across threads and transactions is a source of subtle corruption stories. TTL and maximum size belong in the `CacheManager` configuration so a forgotten key cannot grow forever.

```java
@Bean
CacheManager cacheManager() {
    CaffeineCacheManager manager = new CaffeineCacheManager("vesselsByImo");
    manager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(5_000)
            .expireAfterWrite(Duration.ofMinutes(10)));
    return manager;
}
```

Walk a hit. First `findByImo("IMO-9312345")` runs the repository SELECT and stores `VesselView` under that key. The next ten planner clicks return the cached view — SQL log stays quiet. Anya renames the vessel; `@CacheEvict` drops the key; the following read misses and reloads. Without eviction, the directory lies with the old name until TTL or restart.

Caching is not a substitute for an index on `imo_number`. It is not a license to skip eviction. And `@Cacheable` on a private method inside the same class will not fire — Spring AOP proxies intercept external calls, the same self-invocation trap you will see with transactions. Caching `Optional` misses can also pin "not found" answers; decide whether unknown IMOs should be cached at all.

Directory reads can now be cheap without lying after updates. Concurrent clerks still collide when two of them edit the same berth capacity at once. Detecting that collision without locking the row for the whole human think-time is optimistic locking.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 47 (*Caching*).
