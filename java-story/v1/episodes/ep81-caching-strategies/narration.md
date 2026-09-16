# Episode 81 — Caching Strategies

**Cut:** v1 (original)

## Transcript (from captions)

Episode Eighty closed the handbook arc with architecture interview framing. Season Two begins where production systems get their speed — caching. A cache stores expensive results closer to the reader — memory, Redis, or CDN.

Done well — latency drops and databases breathe. Done poorly — stale data, stampedes, and mysterious inconsistencies. Today — cache layers, invalidation, stampedes, and interview-ready trade-offs.

Episode Eighty-One. Caching Strategies. Think in layers — each cache has a different job. Client and CDN caches cut round trips for static and semi-static content. Application local caches — Caffeine — are ultra-fast per instance.

Distributed caches — Redis or Memcached — share state across pods. Database buffer pools are caches too — do not ignore them when tuning. Place the cache where the expensive work lives — measure before stacking five layers.

Common access patterns you should name in interviews. Cache-aside — app reads cache, on miss loads DB, then fills cache. Read-through — cache library loads on miss behind a single API.

Write-through — writes update cache and store together. Write-behind — writes hit cache first, flush asynchronously — higher risk. Pick the pattern that matches consistency needs — not the trendiest name.

Invalidation is the hard problem — and the interview favorite. TTL expiry is simple — eventual staleness is explicit. Event-driven invalidation deletes keys when the source of truth changes.

Versioned keys avoid mutating in place — readers fetch the new version. Thundering herds after expiry — use soft TTL plus single-flight refresh. Document your staleness budget — product and engineering must agree.

Cache stampedes and hot keys destroy p99 latency. Many requests miss at once — every instance hits the database together. Mitigations — request coalescing, probabilistic early refresh, locking.

Hot keys — shard the key, local cache in front, or replicate reads. Negative caching — remember short-lived misses for absent records. Load-test cache failure modes — a Redis blip should not melt Postgres.

Consistency trade-offs you must voice out loud. Stronger freshness costs more invalidation complexity. Multi-region caches amplify replication lag — name the lag budget. Never treat the cache as the source of truth for money or inventory.

Idempotent rebuilds matter when you flush an entire namespace. Observability — hit ratio, eviction rate, and origin load after deploys. Three common mistakes. One — caching without a TTL or invalidation story — eternal staleness.

Two — caching user-specific private data in a shared public key. Three — measuring only hit ratio — ignoring stampede behavior on expiry. Also — putting a cache in front of a wrong query — caching the bug.

Cache after the query is correct — never before. Interview question — how would you cache a product catalog API? Cache-aside with Redis for hot product pages — TTL plus update events.

Local Caffeine layer for ultra-hot keys inside each instance. Protect origin with single-flight refresh on expiry. Never cache personalized prices under a shared product key. Watch hit ratio and origin QPS — prove the cache earns its complexity.

Caches accelerate reads — APIs shape how clients evolve. Episode Eighty-Two — API Design Deep Dive. Versioning, idempotency, pagination, and contracts that age well. See you there.
