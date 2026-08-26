# Episode 81 — Caching Strategies

| Field | Value |
|---|---|
| Episode | 81 |
| Title | Caching Strategies |
| Catalog handbook column | 81 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A product page is hot. The database is not. Someone says "add a cache." Caches buy latency with correctness risk — and invalidation is the boss fight. Without an invalidation story, you have a faster way to be wrong.

Local caches live in-process — fast, simple, per instance. Distributed caches shared across instances avoid each node reloading the same miss, at the cost of network and operational complexity. Choose deliberately. A local Caffeine cache may be enough for read-mostly data with short TTL on each pod. A Redis-style cache may be needed when hit rate must be shared or eviction coordinated.

```java
LoadingCache<String, User> cache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(5))
    .build(this::loadUser);
```

Size bounds, TTL or TTI eviction — time to live or idle — keep the cache from becoming Episode Fifty-Seven's unbounded map. Cache-aside means the app checks the cache, loads on miss, then populates. Read-through means the cache library loads for you via a loader — as above. Write policies vary: write-through, write-behind, invalidate on write. Pick one and document it.

Stampede control matters when a popular key expires and a hundred requests miss together, all hitting the database. Single-flight loading, slightly staggered TTLs, or soft values reduce the thundering herd. Measure hit rate and staleness. A high hit rate serving wrong data is not a win. Caching non-idempotent results blindly — like "create payment" responses — is how duplicates appear.

Hardest cache problem? Invalidation and stampede under concurrent misses. Say that, then mention bounds, TTL, and explicit delete-on-write as the ordinary tools that prevent heroic outages.

Invalidation is the boss fight because freshness and hit rate pull opposite directions. Short TTL increases misses and load. Long TTL increases staleness. Delete-on-write keeps freshness for that key but needs every write path to cooperate — including admin tools and batch jobs that bypass the app. Document who is allowed to mutate the source of truth and how the cache learns.

Local versus distributed also changes failure modes. Local caches go stale independently per instance after a write to another instance unless you broadcast invalidations. Distributed caches add a dependency that can be down — your resilience story must include cache miss fallback without melting the database.

Stampede control can be as simple as `LoadingCache`'s single-flight loader, or as deliberate as locking on a miss key. Measure not only hit rate but miss latency and origin load. A cache that "works" while the database CPU spikes on expiry waves is unfinished.

Caching non-idempotent results blindly deserves an example: caching a POST response that creates a seat reservation. A retry hits the cache and returns success without a seat. Separate read models you cache from write side effects you do not.

Measure hit rate and staleness together. A dashboard that shows only hits hides whether users see yesterday's price. Product rules define acceptable staleness; engineering enforces them with TTL and invalidation. When rules are unspoken, caches become political.

Cache-aside versus read-through is mostly about where load logic lives. Keep it consistent across the codebase. Mixed patterns without documentation cause double-fetches and inconsistent invalidation.

Unbounded caches return from Episode Fifty-Seven wearing performance clothing. maximumSize and expireAfterWrite are not optional decorations on the Caffeine builder — they are the difference between acceleration and a leak. Soft references alone are not a substitute, as Episode Sixty-One warned.

Hardest cache problem remains invalidation and stampede under concurrent misses — because both are timing problems under load, invisible in quiet staging.

Write-path discipline completes the design. On update, do you update the cache, delete the key, or wait for TTL? Delete-on-write is often safest for correctness; update-on-write is faster when you can guarantee every writer cooperates. Batch jobs that bypass services are famous for forgetting the cache. Put invalidation beside every write in code review checklists.

Local caches in a fleet of twenty pods mean twenty independent views after a write unless you publish invalidation messages. That may be acceptable for short TTL display data and unacceptable for permissions. Match strategy to risk.

Stampede control under concurrent misses is the other half of the hardest problem. Even perfect invalidation can create a miss storm at expiry. Combine bounded size, TTL, single-flight load, and origin protection — shed or queue — when the origin is fragile.

Caches buy latency with correctness risk. Keep saying both halves. Interviewers hear the second half and trust you more.

Connect caching to API design next door. Cache keys should follow resource identifiers clients already understand. Do not invent a parallel key taxonomy nobody can invalidate. When an API response is personalized, cache carefully or not at all — privacy and correctness both suffer when one user receives another's cached page.

TTL, size, invalidation, stampede control, hit rate, staleness — if your design doc names those, you are ready to implement. If it only says "use Redis," you are not.

Before shipping a cache, write the invalidation sentence in the PR: "On product update, we delete key product:{id}; TTL is five minutes as a backstop; loader is single-flight." If you cannot write that sentence, the cache is not designed yet. Implementation without that sentence recreates unbounded maps with prettier APIs.

If hit rate is high and origin load is still high, you are caching the wrong grain or suffering stampedes at expiry — dig into miss traces before growing the cache cluster again. Growing Redis to hide a stampede wastes money and delays the real fix.

APIs that sit in front of caches and databases need long-term contracts. Episode Eighty-Two is API design — idempotency, errors, and compatibility.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Caching Strategies (Episode 81).

Narration technique: hot page situation → latency vs correctness → local vs distributed → Caffeine example → TTL/size/cache-aside → stampede → interview woven → bridge to API design.

Teaching points preserved: local vs distributed; TTL/TTI/size; cache-aside vs read-through; stampede control; measure hit rate/staleness.
