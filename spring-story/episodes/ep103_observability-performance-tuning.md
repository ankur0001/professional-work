# Episode 103 — Performance Tuning

| Field | Value |
|---|---|
| Episode | 103 |
| Title | Performance Tuning |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 103 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

OpenTelemetry showed a span that spent eight hundred milliseconds inside `InventoryClient.reserve`. Someone’s first instinct is to "add a cache" or "bump the heap." Stop. Performance tuning in an observable Spring system starts from evidence: which signal moved, which resource is saturated, what experiment will falsify the guess.

Use a simple triage order. Latency up with error rate flat often means slow dependency or lock contention. Latency up with error rate up means failures and retries. CPU pegged with healthy latency elsewhere means hot code or excessive serialization. Threads or DB connections exhausted means you are queueing — more replicas may hide the bug for a week and then amplify it.

Read Boot’s free meters before inventing new ones. `http.server.requests` timers by URI and status. HikariCP gauges: active, idle, pending. Tomcat or Netty thread pool metrics. JVM CPU and GC pause metrics. Pair them with the custom business timers from Episode 99. If `checkout.payment.duration` is fine but HTTP p99 is not, the waste is in your own service — serialization, chatty repositories, or synchronous fan-out.

A concrete Spring-shaped example. Trace shows ten sequential `RestClient` calls to inventory for a cart with ten lines. Fix the algorithm, not the JVM flags:

```java
// Before: N remote calls
for (CartLine line : cart.lines()) {
    inventory.reserve(line.sku(), line.qty());
}

// After: one batch reserve — one span, one round-trip
inventory.reserveAll(cart.lines());
```

Another evidence-backed fix: connection pool too small under load. Pending threads climb on the Hikari gauge while DB CPU is idle. Raising `maximum-pool-size` carefully — and fixing leaks that hold connections across remote calls — is tuning. Blindly setting the pool to five hundred is not.

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      connection-timeout: 3000
```

Jackson and payload shape show up in traces as time spent in the MVC adapter after the service returns. Huge entity graphs serialized as JSON, or `OpenEntityManagerInView` holding a session open while the view lazily loads associations, look like "Spring is slow" when the design is chatty. Close the session before rendering, map to slim DTOs, and confirm with SQL counts per request.

Cache only what the metrics justify. A Micrometer cache hit ratio that sits at five percent means you cached the wrong key or the wrong TTL. `@Cacheable` without hit/miss meters is optimism. GC thrashing after a "performance" change often means you cached huge object graphs — memory is the next episode for a reason.

Load tests belong after you have a hypothesis. Reproduce with a realistic mix, watch the same Grafana dashboard you use in prod, change one variable, compare. If you cannot show a before/after on p99 and error rate, you did not finish the tuning loop. Keep a short runbook: hypothesis, meter or span that should move, change, result. That document prevents the next engineer from re-tuning the same pool by folklore.

A hard misconception: "we need virtual threads" or "we need WebFlux" as the first move. Sometimes yes; often the span points at an N+1 query or a missing index — cheaper fixes. Another misconception: optimizing average latency while SLO is about p99. Customers live in the tail. A third: scaling pods horizontally when each pod’s connection pool is already saturating the database — you scaled the queue, not the bottleneck.

Today we practiced reading RED and saturation signals, fixing a sequential remote fan-out, and adjusting a pool from gauges rather than folklore. When the bad signal is heap growth, GC thrashing, or native memory, the tuning lens narrows further.

Memory deserves its own pass.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 103 (*Performance Tuning*).

Narration technique: resist folklore → triage from signals → Boot meters → batch remote calls example → pool tuning → load-test loop → misconceptions → bridge to memory.
