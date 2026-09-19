# Episode 89 — Circuit Breaker

| Field | Value |
|---|---|
| Episode | 89 |
| Title | Circuit Breaker |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 89 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Billing’s p99 jumps from 80ms to 8 seconds. Without protection, every gate check-in thread blocks on Feign until the pool saturates. Trucks wait at the booth while healthy gate CPU sits in socket reads. A circuit breaker flips that failure mode: after enough errors or slow calls, the breaker opens, subsequent calls fail fast (or hit a fallback), and a half-open probe later checks whether billing recovered.

Spring Cloud CircuitBreaker provides an abstraction; Resilience4j is the usual implementation on Boot 3. Annotate the gate method that calls billing, or wrap the call programmatically. The important part is the state machine — closed, open, half-open — around the gate↔billing boundary. Closed means traffic flows and outcomes fill a sliding window. Open means the library short-circuits before the network. Half-open means a few trial calls decide whether to trust billing again.

```java
@Service
public class GateReleaseService {
    private final BillingClient billing;
    private final GateLedger ledger;
    private final TariffCache lastKnown;

    public GateReleaseService(BillingClient billing, GateLedger ledger, TariffCache lastKnown) {
        this.billing = billing;
        this.ledger = ledger;
        this.lastKnown = lastKnown;
    }

    @CircuitBreaker(name = "billingQuote", fallbackMethod = "quoteFallback")
    public TariffQuote quoteOrDegrade(TruckCheckIn req) {
        return billing.quote(req.containerId(), req.hazardClass());
    }

    @SuppressWarnings("unused")
    private TariffQuote quoteFallback(TruckCheckIn req, Throwable ex) {
        return lastKnown.find(req.containerId(), req.hazardClass())
                .orElseThrow(() -> new BillingDegradedException("billing open; no cached tariff", ex));
    }
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      billingQuote:
        slidingWindowSize: 20
        failureRateThreshold: 50
        waitDurationInOpenState: 10s
        permittedNumberOfCallsInHalfOpenState: 3
        slowCallDurationThreshold: 2s
        slowCallRateThreshold: 50
        recordExceptions:
          - java.io.IOException
          - feign.FeignException$InternalServerError
```

Walk a burst. Twenty quote calls, half time out past `slowCallDurationThreshold` or throw recorded exceptions. Failure or slow-call rate crosses 50%. The breaker opens. The next check-ins skip the network and enter `quoteFallback` — maybe a cached tariff with a `degraded=true` flag so the booth knows to reconcile later. After `waitDurationInOpenState`, a few calls probe half-open. If they succeed, the circuit closes; if not, it opens again. Gate capacity stays available for local ledger work even while billing burns.

Symptoms you can hear from ops: before the breaker, gate thread dumps show stacks stuck in Feign read; Tomcat’s pool fills; unrelated endpoints on the same JVM slow down. After a correct open, those stacks disappear and `resilience4j.circuitbreaker.state` (via Micrometer) shows OPEN while check-in latency drops to fallback time. If latency stays high with the breaker “enabled,” Feign’s connect/read timeouts are longer than the booth’s patience — the breaker never sees failures in time because threads are still waiting. Align client timeouts below user patience and below cascading budgets.

Compose with Feign carefully. Fallbacks must be honest: returning a zero-amount invoice and writing nothing durable is hidden data loss, not resilience. Prefer explicit degraded responses, metrics on fallback invocations, and a runbook that says whether the booth may release on cached tariff. Ignore exceptions you should not trip on — a `400` for a bad hazard class is a client bug, not a reason to open the circuit for everyone.

Trade-offs: a tight `failureRateThreshold` protects gate fast but flaps on blips; a loose threshold lets billing poison the booth longer. Per-dependency breakers (`billingQuote` vs `tideApi`) isolate blast radius; one global breaker couples unrelated outages. Fail-fast without a fallback returns errors quickly — sometimes that is better than a stale tariff — but the booth UX must match.

A misconception is setting thresholds so tight that normal blips permanently open the circuit, or so loose that a real billing outage never trips it. Another is a fallback that looks like success in metrics while operators see no signal. A third is wrapping purely in-process calls “for consistency”; breakers earn their keep on unreliable boundaries — network, process, shared resource contention.

Fail-fast at the billing hop stops the cascade. It does not tell you *which* hop in gateway→gate→billing ate the latency for one truck. For that you need a single trace id that survives process boundaries.

Distributed tracing is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 89 (*Circuit Breaker*).
