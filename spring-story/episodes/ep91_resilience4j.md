# Episode 91 — Resilience4j

| Field | Value |
|---|---|
| Episode | 91 |
| Title | Resilience4j |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 91 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Circuit breakers protect gate from a dead billing dependency. The tide API is a different beast: intermittent 503s, bursty rate limits, and a vendor that hates connection stampedes. Resilience4j gives you composable decorators — retry, rate limiter, bulkhead, time limiter, circuit breaker — you can stack around that call without reinventing thread pools in every service.

Scheduling asks the tide service for predicted height before confirming a berth. Wrap the client:

```java
@Service
public class TideForecastService {
    private final TideApiClient tides;

    public TideForecastService(TideApiClient tides) {
        this.tides = tides;
    }

    @RateLimiter(name = "tideApi")
    @Bulkhead(name = "tideApi")
    @Retry(name = "tideApi")
    @CircuitBreaker(name = "tideApi", fallbackMethod = "cachedTide")
    @TimeLimiter(name = "tideApi")
    public CompletableFuture<TideReading> forecast(String stationId, Instant at) {
        return CompletableFuture.supplyAsync(() -> tides.fetch(stationId, at));
    }

    @SuppressWarnings("unused")
    private CompletableFuture<TideReading> cachedTide(String stationId, Instant at, Throwable ex) {
        return CompletableFuture.completedFuture(TideReading.degraded(stationId, at));
    }
}
```

```yaml
resilience4j:
  ratelimiter:
    instances:
      tideApi:
        limitForPeriod: 10
        limitRefreshPeriod: 1s
        timeoutDuration: 200ms
  bulkhead:
    instances:
      tideApi:
        maxConcurrentCalls: 5
        maxWaitDuration: 100ms
  retry:
    instances:
      tideApi:
        maxAttempts: 3
        waitDuration: 200ms
        enableExponentialBackoff: true
        exponentialBackoffMultiplier: 2
        retryExceptions:
          - org.springframework.web.client.ResourceAccessException
          - com.harbor.tide.TideTransientException
        ignoreExceptions:
          - com.harbor.tide.TideStationUnknownException
  timelimiter:
    instances:
      tideApi:
        timeoutDuration: 1s
  circuitbreaker:
    instances:
      tideApi:
        slidingWindowSize: 30
        failureRateThreshold: 40
```

Read the composition as a story. Rate limiter refuses to stampede the vendor — when the bucket is empty, callers fail in ~200ms instead of opening fifty sockets. Bulkhead caps concurrent tide calls so scheduling’s other threads keep working on berth conflicts that do not need tide. Retry absorbs blips with bounded attempts and backoff; `TideStationUnknownException` is ignored so you do not thrash on permanent 404s. Time limiter kills hung calls at one second. Circuit breaker opens when the vendor is truly down and routes to `cachedTide`. Annotation order and aspect ordering matter — measure once in a test that the stack behaves the way you draw it on the whiteboard. A common surprise: retry outside the breaker retries into an open circuit; the inverse ordering changes incident shape.

Walk symptoms. Without rate limiting, a berth storm during fog season triggers vendor `429`s and then a connection storm when every scheduler retries at once. With bulkhead alone, five tide calls run and the sixth fails fast — scheduling UI stays responsive for non-tide actions. Micrometer binds Resilience4j metrics automatically when the dependency is present: retry success/failure, bulkhead rejected calls, breaker state. Those series belong next to your gate timers in the same scrape job. If `resilience4j_bulkhead_rejected_calls` climbs while CPU is idle, you are protecting the vendor correctly and may need more capacity or a wider bulkhead — a deliberate trade-off, not an automatic “raise the limit.”

Trade-offs: retries help idempotent GETs of tide height; they are dangerous on non-idempotent POSTs that book a berth side effect. Semaphore bulkheads are light; thread-pool bulkheads isolate better and cost threads. Timeouts that are shorter than the vendor’s p99 create self-inflicted failure rates. Cached fallbacks keep the quay moving with stale tide data — label them degraded so operators do not treat them as truth for deep-draft vessels.

Name each Resilience4j instance after the dependency (`tideApi`, `billingQuote`), not after the calling class, so metrics and runbooks stay portable when scheduling refactor moves the call site. Shared names across unrelated vendors accidentally couple their breaker state — a tide outage should not open billing’s breaker because someone reused `remoteCalls`.

A misconception is retrying non-idempotent POSTs until you double-book berths — retries need idempotent semantics or idempotency keys. Another is unbounded retries without jitter that amplify an outage. A third is one global bulkhead for every remote system so tide contention starves billing calls that deserved isolation.

HTTP and resilience cover request/response paths. Some harbor facts should not wait for a synchronous call: a berth assignment changed, and billing and the yard display both need to know without gate orchestrating them.

That push model is messaging with Spring Cloud Stream.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 91 (*Resilience4j*).
