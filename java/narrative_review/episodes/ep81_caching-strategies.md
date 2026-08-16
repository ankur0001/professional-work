# Episode 81 — Caching Strategies

| Field | Value |
|---|---|
| Episode | 81 |
| Title | Caching Strategies |
| Catalog handbook column | S2 |
| Narration source script | `make_episode_81.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Eighty closed the handbook arc with architecture interview framing.
2. Season Two begins where production systems get their speed — caching.
3. A cache stores expensive results closer to the reader — memory, Redis, or CDN.
4. Done well — latency drops and databases breathe.
5. Done poorly — stale data, stampedes, and mysterious inconsistencies.
6. Today — cache layers, invalidation, stampedes, and interview-ready trade-offs.

### Scene `title` (renderer: `title`)

1. Episode Eighty-One.
2. Caching Strategies.

### Scene `layers` (renderer: `layers`)

1. Think in layers — each cache has a different job.
2. Client and CDN caches cut round trips for static and semi-static content.
3. Application local caches — Caffeine — are ultra-fast per instance.
4. Distributed caches — Redis or Memcached — share state across pods.
5. Database buffer pools are caches too — do not ignore them when tuning.
6. Place the cache where the expensive work lives — measure before stacking five layers.

### Scene `patterns` (renderer: `patterns`)

1. Common access patterns you should name in interviews.
2. Cache-aside — app reads cache, on miss loads DB, then fills cache.
3. Read-through — cache library loads on miss behind a single API.
4. Write-through — writes update cache and store together.
5. Write-behind — writes hit cache first, flush asynchronously — higher risk.
6. Pick the pattern that matches consistency needs — not the trendiest name.

### Scene `invalidation` (renderer: `invalidation`)

1. Invalidation is the hard problem — and the interview favorite.
2. TTL expiry is simple — eventual staleness is explicit.
3. Event-driven invalidation deletes keys when the source of truth changes.
4. Versioned keys avoid mutating in place — readers fetch the new version.
5. Thundering herds after expiry — use soft TTL plus single-flight refresh.
6. Document your staleness budget — product and engineering must agree.

### Scene `stampedes` (renderer: `stampedes`)

1. Cache stampedes and hot keys destroy p99 latency.
2. Many requests miss at once — every instance hits the database together.
3. Mitigations — request coalescing, probabilistic early refresh, locking.
4. Hot keys — shard the key, local cache in front, or replicate reads.
5. Negative caching — remember short-lived misses for absent records.
6. Load-test cache failure modes — a Redis blip should not melt Postgres.

### Scene `consistency` (renderer: `consistency`)

1. Consistency trade-offs you must voice out loud.
2. Stronger freshness costs more invalidation complexity.
3. Multi-region caches amplify replication lag — name the lag budget.
4. Never treat the cache as the source of truth for money or inventory.
5. Idempotent rebuilds matter when you flush an entire namespace.
6. Observability — hit ratio, eviction rate, and origin load after deploys.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — caching without a TTL or invalidation story — eternal staleness.
3. Two — caching user-specific private data in a shared public key.
4. Three — measuring only hit ratio — ignoring stampede behavior on expiry.
5. Also — putting a cache in front of a wrong query — caching the bug.
6. Cache after the query is correct — never before.

### Scene `interview` (renderer: `interview`)

1. Interview question — how would you cache a product catalog API?
2. Cache-aside with Redis for hot product pages — TTL plus update events.
3. Local Caffeine layer for ultra-hot keys inside each instance.
4. Protect origin with single-flight refresh on expiry.
5. Never cache personalized prices under a shared product key.
6. Watch hit ratio and origin QPS — prove the cache earns its complexity.

### Scene `teaser` (renderer: `teaser`)

1. Caches accelerate reads — APIs shape how clients evolve.
2. Episode Eighty-Two — API Design Deep Dive.
3. Versioning, idempotency, pagination, and contracts that age well.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Episode 81** is a **Season 2 production-systems bonus** track. It is **not** one of the handbook’s 80 lessons.
- Topic framing for the video: **Caching Strategies** (continuity after Episode 80’s architecture interview wrap).
- Narration was **original written for the video** (scene-synced beats), not copied verbatim from the handbook.
