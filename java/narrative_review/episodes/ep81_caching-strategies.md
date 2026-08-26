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

Local caches live in-process — fast, simple, per instance. Distributed caches shared across instances avoid each node reloading the same miss, at the cost of network and operational complexity. A local Caffeine cache may be enough for read-mostly data with short TTL on each pod. A Redis-style cache may be needed when hit rate must be shared. Local caches go stale independently after a write to another instance unless you broadcast invalidations — acceptable for short-TTL display data, unacceptable for permissions. Distributed caches add a dependency that can be down; your resilience story must include cache-miss fallback without melting the database.

```java
LoadingCache<String, User> cache = Caffeine.newBuilder()
    .maximumSize(10_000)
    .expireAfterWrite(Duration.ofMinutes(5))
    .build(this::loadUser);
```

Size bounds and TTL or TTI eviction keep the cache from becoming Episode Fifty-Seven's unbounded map. Soft references alone are not a substitute — Episode Sixty-One warned. Cache-aside means the app checks the cache, loads on miss, then populates. Read-through means the cache library loads via a loader — as above. Keep the pattern consistent across the codebase.

Invalidation is the boss fight because freshness and hit rate pull opposite directions. Short TTL increases misses; long TTL increases staleness. Delete-on-write keeps freshness for that key but needs every write path to cooperate — including admin tools and batch jobs that bypass the app. Before shipping, write the invalidation sentence in the PR: "On product update, we delete key product:{id}; TTL is five minutes as a backstop; loader is single-flight." If you cannot write that sentence, the cache is not designed yet.

Stampede control matters when a popular key expires and a hundred requests miss together. Single-flight loading — like `LoadingCache`'s loader — slightly staggered TTLs, or soft values reduce the thundering herd. Measure hit rate and staleness together. A high hit rate serving wrong data is not a win. If hit rate is high and origin load is still high, dig into miss traces before growing the cache cluster — you may be caching the wrong grain or suffering stampedes at expiry.

Caching non-idempotent results blindly is how duplicates appear. Caching a POST response that creates a seat reservation means a retry can return success without a seat. Separate read models you cache from write side effects you do not. Cache keys should follow resource identifiers clients already understand — and those identifiers live inside longer-lived API contracts. Personalized responses demand extra care for privacy and correctness.

Hardest cache problem? Invalidation and stampede under concurrent misses. Say that, then mention bounds, TTL, and explicit delete-on-write as the ordinary tools that prevent heroic outages. Caches buy latency with correctness risk — keep saying both halves.

APIs that sit in front of caches and databases need long-term contracts — idempotency, errors, and compatibility — or every cache win becomes a client migration tax.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Caching Strategies (Episode 81).

Narration technique: hot page → latency vs correctness → local vs distributed → Caffeine example → invalidation sentence → stampede → bridge to API design.

Teaching points preserved: local vs distributed; TTL/TTI/size; cache-aside vs read-through; stampede control; measure hit rate/staleness.
