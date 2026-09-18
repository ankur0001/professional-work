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

Resist the folklore fix. Gate p95 is high; someone proposes “rewrite in WebFlux” before reading a single span. Performance tuning in a Spring harbor stack starts from signals: RED metrics on `releaseGate`, saturation gauges on pools, traces for critical path, and — when CPU is the villain — a flame graph that names the hot method.

Triage in order. Is it error rate or latency? If latency, is it time in gate code, time in Feign to billing, or time in billing SQL? Micrometer HTTP timers and your `harbor.gate.release.duration` split edge versus business method. Traces confirm. Only then profile. Skipping steps is how teams spend a week on reactive rewrites while billing’s connection pool was the whole story.

```text
# illustrative async-profiler / continuous profiling readout (gate pod)
harbor.gate.release
  ├─ BillingClient#quote          62%
  │    └─ waiting on socket       58%
  ├─ GateLedger#record            18%
  └─ Jackson serialize             9%
```

Here the flame is not a Java hot loop — it is waiting on billing. The fix might be caching non-hazard quotes, batching, or raising billing capacity — not rewriting gate’s controllers. A different flame that shows `TariffCalculator.quote` burning CPU on every request might mean an accidental O(n²) surcharge table scan. Socket wait versus CPU burn demand opposite remedies; the profile distinguishes them when metrics only say “slow.”

```java
// before: N sequential Feign calls for a multi-container truck
for (String containerId : req.containerIds()) {
    billing.quote(containerId, req.hazardClass());
}

// after: one remote operation when the contract allows
billing.quoteMany(new BulkQuoteRequest(req.containerIds(), req.hazardClass()));
```

Walk the before/after with numbers. Six containers at 80ms each is ~480ms of Feign alone on the critical path; one bulk quote at 120ms changes the booth math without touching WebFlux. If the contract cannot bulk yet, parallel calls with a bounded executor help — and need a bulkhead so you do not stampede billing. Measure again on the same Grafana panels; anecdotes are not acceptance criteria.

Pool tuning follows gauges, not vibes:

```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 20
      leak-detection-threshold: 20s
  cloud:
    openfeign:
      client:
        config:
          billing-service:
            connectTimeout: 200
            readTimeout: 800
```

If `hikaricp_connections_pending` climbs while CPU is idle, enlarge carefully or shorten queries — do not guess. Feign timeouts that exceed user patience keep threads stuck; timeouts that are far below billing p99 manufacture errors. Load-test after each change with a realistic check-in mix — multi-container trucks, hazard classes, cold caches — and watch the same Grafana panels that page you. A laptop profile with an empty billing stub will not show socket wait.

Failure modes of folklore tuning: more replicas that each still fan out N Feign calls; JVM flag churn before fixing N+1 or unbounded retries; caching without eviction that trades latency for the memory incident in the next episode; “optimize Jackson” when 58% of the flame is socket wait.

Trade-offs: caching tariff quotes helps non-hazard traffic and risks stale rates for IMDG changes — key by hazard and version the tariff table. Vertical scaling buys time; chatty APIs return when traffic multiplies. Prefer eliminating round trips over micro-optimizing serializers.

Document each change with before/after p95 on the same panel and the same load-test script. If you cannot show the number, you did not finish the tuning — you only shipped a hypothesis. Rollback is part of tuning: a bulk endpoint that regresses billing CPU should revert while you redesign the query.

A misconception is equating “more replicas” with a fix when each replica still makes the same chatty Feign fan-out. Another is tuning JVM flags before fixing an N+1 or unbounded retry storm. A third is trusting a local laptop profile when production waits on a different billing region.

When the bad signal is heap growth, GC thrash, or native memory, the lens narrows further — memory optimization with dumps and cache bounds.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 103 (*Performance Tuning*).
