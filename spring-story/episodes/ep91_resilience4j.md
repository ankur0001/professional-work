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

The circuit breaker episode showed one Resilience4j module in action. Resilience4j is broader than that tripwire. It is a lightweight fault-tolerance library built for Java functional style — decorators you compose around a `Supplier` or a method — and Spring Boot starters wire those decorators into annotations and metrics. Where Netflix Hystrix was the old Cloud demo default, Resilience4j is the usual modern choice: circuit breaker, retry, rate limiter, bulkhead, and time limiter as separate, composable operators.

Think in layers around one remote call. A time limiter bounds how long you are willing to wait. A retry absorbs transient blips with backoff — only on idempotent operations. A circuit breaker stops calling after sustained failure. A bulkhead limits concurrent calls so one dependency cannot consume every thread in your pool. A rate limiter protects a fragile peer (or yourself) from stampedes. You do not enable all five everywhere. You pick the combination that matches the failure mode.

```java
@Service
public class InventoryResilientClient {
    private final InventoryClient feign;

    public InventoryResilientClient(InventoryClient feign) {
        this.feign = feign;
    }

    @CircuitBreaker(name = "inventory")
    @Retry(name = "inventory")
    @Bulkhead(name = "inventory")
    @TimeLimiter(name = "inventory")
    public CompletableFuture<StockView> stock(String sku) {
        return CompletableFuture.supplyAsync(() -> feign.getStock(sku));
    }
}
```

```yaml
resilience4j:
  timelimiter:
    instances:
      inventory:
        timeoutDuration: 2s
  retry:
    instances:
      inventory:
        maxAttempts: 3
        waitDuration: 200ms
        retryExceptions:
          - java.io.IOException
          - feign.RetryableException
  bulkhead:
    instances:
      inventory:
        maxConcurrentCalls: 20
  circuitbreaker:
    instances:
      inventory:
        slidingWindowSize: 20
        failureRateThreshold: 50
```

Annotation order and async return types deserve respect. TimeLimiter often expects a `CompletionStage` so it can cancel or complete exceptionally when the budget expires. Retry should not blindly wrap non-idempotent POSTs that charge cards twice. Bulkhead rejection is a success for system stability even when it feels like a failure to the caller — surface a clear exception or fallback. Micrometer binds Resilience4j metrics so dashboards show retry counts, breaker states, and bulkhead rejections next to your traces from the previous episode.

Programmatic decoration is useful when annotations fight you:

```java
CircuitBreaker cb = circuitBreakerRegistry.circuitBreaker("inventory");
Retry retry = retryRegistry.retry("inventory");

Supplier<StockView> supplier = CircuitBreaker
        .decorateSupplier(cb, () -> feign.getStock(sku));
supplier = Retry.decorateSupplier(retry, supplier);
StockView view = supplier.get();
```

That style makes composition order obvious — decorate carefully, outermost versus innermost changes which operator sees which failures.

Rate limiters deserve a concrete picture. If a partner API allows one hundred requests per second, a `RateLimiter` on your side sheds excess locally instead of earning HTTP 429 storms. Combined with a bulkhead, you protect both the partner and your own thread pool. Combined with tracing, you can see a spike of rate-limiter rejections as a span attribute or metric and tell “we throttled ourselves” from “they were down.”

A misconception is copying a single YAML block across every client with identical thresholds. Payment and product-catalog have different SLAs; tune per dependency. Another is retrying on every exception type including business 400s — retries should target transient infrastructure failures. A third is assuming Resilience4j replaces timeouts in the HTTP client; configure both so you are not waiting on a socket longer than the time limiter intends.

Today we treated Resilience4j as a toolbox — time limit, retry, bulkhead, rate limit, circuit breaker — composed around remote calls, with metrics feeding the same operational picture tracing opened.

Not every collaboration should be a synchronous HTTP round trip. Sometimes order should publish “OrderPlaced” and let inventory react when it can, without holding a Tomcat thread across the network. That shift from request/response to messages is the next Spring Cloud chapter.

That chapter is Spring Cloud Stream.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 91 (*Resilience4j*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
