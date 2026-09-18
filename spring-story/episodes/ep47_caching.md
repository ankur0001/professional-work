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

Inside one transaction, the persistence context already caches by id. That first-level cache does not help the next HTTP request, the next pod, or the next transaction that loads the same product catalog entry ten thousand times a day. Caching in the JPA conversation means knowing which layer you are talking about — and what invalidation you just signed up for.

Three layers show up in Spring Data apps. The **persistence context** (first-level) is mandatory and per unit of work. Hibernate's **second-level cache** is optional, shared across sessions in the same JVM (or clustered with a provider), keyed by entity id and region. Spring's **`@Cacheable`** abstraction sits above repositories or services and can use Caffeine, Redis, or another `CacheManager` — it caches method results, not necessarily managed entities.

Start with second-level caching for a mostly-read reference entity:

```java
@Entity
@Table(name = "product_categories")
@jakarta.persistence.Cacheable
@org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class ProductCategory {

    @Id
    private String code;

    @Column(nullable = false)
    private String displayName;

    protected ProductCategory() {}

    public ProductCategory(String code, String displayName) {
        this.code = code;
        this.displayName = displayName;
    }
}
```

```properties
spring.jpa.properties.hibernate.cache.use_second_level_cache=true
spring.jpa.properties.hibernate.cache.region.factory_class=jcache
```

After enabling a cache provider, `entityManager.find(ProductCategory.class, "HOME")` can skip the database when the region holds that id. Collections and associations need their own cache configuration if you expect collection caching — caching the parent alone does not magically cache lazy children.

Query cache is a separate switch. It stores query result id lists, then resolves entities through the second-level cache. Stale query cache entries are a classic footgun when underlying tables change and regions are not invalidated carefully. Prefer second-level entity caching for reference data before enabling query cache globally.

Spring Cache often fits repository read methods better when you want explicit keys and TTLs:

```java
public interface ProductRepository extends JpaRepository<Product, Long> {

    @Cacheable(cacheNames = "productsBySku", key = "#sku")
    Optional<Product> findBySku(String sku);

    @CacheEvict(cacheNames = "productsBySku", key = "#result.sku")
    <S extends Product> S save(S entity);
}
```

Here the cache stores the method return value. Evict on save so the next read misses and reloads. If you cache entities and then mutate them outside a clear eviction story, you serve ghosts. Prefer caching immutable snapshots or DTOs when the object graph is rich.

What should you cache? Stable reference data: categories, country codes, tax rates. Hot product reads with disciplined eviction. What should you not cache first? Highly transactional balances, rows that change every second, or entire aggregates "because findAll is slow" — fix the query and indexes first.

Concurrency strategies on Hibernate's `@Cache` matter. `READ_ONLY` suits immutable reference data. `READ_WRITE` allows updates with soft locking semantics. `NONSTRICT_READ_WRITE` trades stricter consistency for speed. Choose based on how wrong a slightly stale category name is versus a slightly stale inventory count — those are different businesses.

Caching does not remove concurrency collisions on writes. Two transactions can still load the same `Product` price, change it, and overwrite each other. When lost updates hurt, you need a version column and optimistic locking — not a bigger cache.

Episode Forty-Eight — Optimistic Locking.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 47 (*Caching*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
