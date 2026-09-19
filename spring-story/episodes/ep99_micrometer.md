# Episode 99 — Micrometer

| Field | Value |
|---|---|
| Episode | 99 |
| Title | Micrometer |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 99 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Contracts are green. Then the pager fires: gate release feels slow on quay B. Someone asks “how slow, for which gate, since when?” and the best answer is a screenshot of a log line. That gap — between “booths are backed up” and “we can prove it” — is why Phase 11 starts with metrics.

Micrometer is Spring’s vendor-neutral metrics facade. You write against `MeterRegistry`. Boot wires a registry. Exporters — Prometheus, Datadog, CloudWatch — plug in from classpath and config. Gate code stays about counters and timers, not about a vendor SDK. Swap the registry binder and the same `harbor.gate.release.duration` name still means the same thing in the next backend.

Four meter types you will actually use: `Counter` (only up — releases started, billing fallbacks), `Timer` (duration and count — perfect around `releaseGate`), `Gauge` (current value — open booth sessions, queue depth), `DistributionSummary` (sizes that are not time — bytes on bill-of-lading uploads). Business instrumentation usually starts with Counter and Timer. Gauges need a lasting reference to the thing they observe — a cache, a queue — or they report stale nonsense after GC.

```java
@Service
public class GateReleaseService {
    private final BillingClient billing;
    private final GateLedger ledger;
    private final Counter releaseStarted;
    private final Counter releaseSucceeded;
    private final Counter releaseFailed;
    private final Timer releaseTimer;

    public GateReleaseService(BillingClient billing, GateLedger ledger, MeterRegistry registry) {
        this.billing = billing;
        this.ledger = ledger;
        this.releaseStarted = registry.counter("harbor.gate.release.started");
        this.releaseSucceeded = registry.counter("harbor.gate.release.succeeded");
        this.releaseFailed = registry.counter("harbor.gate.release.failed");
        this.releaseTimer = registry.timer("harbor.gate.release.duration");
    }

    public CheckInResponse releaseGate(String gateId, TruckCheckIn req) {
        releaseStarted.increment();
        try {
            CheckInResponse response = releaseTimer.record(() -> {
                TariffQuote quote = billing.quote(req.containerId(), req.hazardClass());
                return ledger.record(gateId, req, quote);
            });
            releaseSucceeded.increment();
            return response;
        } catch (RuntimeException ex) {
            releaseFailed.increment();
            throw ex;
        }
    }
}
```

Read the names. `harbor.gate.release.started` versus `succeeded` versus `failed` yields success and error ratios without scraping HTTP alone. `harbor.gate.release.duration` isolates the booth-critical method — including billing wait if that call sits inside the timer. Tags belong on low-cardinality dimensions you will filter — `gate.id` only if you have dozens of gates, not thousands of truck plates. High-cardinality tags explode time series and bill you in storage; the failure symptom is a TSDB that crawls and a sudden cost alert, not a clear stack trace in gate.

Boot already exposes JVM meters, HTTP server timers, and often datasource pool gauges when Actuator and Micrometer sit on the classpath. Custom business meters sit beside those. `@Timed` can wrap a method via AOP; prefer explicit registry use when the timer must surround only the billing hop inside `releaseGate` while excluding JSON serialization, or the opposite — include everything the booth feels. Common meters for Resilience4j and Hikari appear automatically once those libraries integrate; wire them before inventing parallel names.

Walk an incident with meters present. Quay B reports backup. `harbor.gate.release.duration` p95 jumped at 14:02; `release.failed` rate flat; Hikari pending climbs on billing, not gate. You already know to look at billing capacity before rewriting gate controllers. Without business timers you only see generic HTTP latency and argue about the gateway.

Trade-offs: too few meters and you fly blind; too many tagged series and you blind the store. Name consistently (`harbor.<context>.<operation>.<metric>`). Prefer ratios from counters over “current error boolean” gauges that miss spikes between scrapes.

A misconception is treating Micrometer as “Prometheus annotations.” Micrometer is the API; Prometheus is one backend. Another is measuring only HTTP status codes and calling that observability — percentiles on `releaseGate` and fallback counters tell you where to look. A third is tagging every meter with `containerId` until cardinality melts the TSDB.

Numbers in a process are still trapped in that process. The open question is how an outside system pulls them on a schedule across gate pods.

That pull model is Prometheus.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 99 (*Micrometer*).
