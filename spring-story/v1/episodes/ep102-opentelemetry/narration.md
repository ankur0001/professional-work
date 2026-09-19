# Episode 102 — OpenTelemetry

| Field | Value |
|---|---|
| Episode | 102 |
| Title | OpenTelemetry |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 102 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Grafana shows gate p95 climbing. Which span is guilty — gateway auth, gate’s `releaseGate`, Feign to billing, or billing’s SQL? OpenTelemetry (OTel) standardizes traces, metrics, and baggage so one check-in becomes a tree of spans you can open beside the Prometheus series that alerted you.

In Spring Boot 3, Micrometer Tracing bridges to OTel (or Brave). Auto-instrumentation covers inbound HTTP and outbound clients. You export via OTLP to a collector, which fans out to your trace backend. Correlate by keeping stable metric names and span names around the same operation — `harbor.gate.release` as both timer and span name is deliberate. When names diverge (`releaseGate` in metrics, `GateReleaseService.accept` in traces), humans waste minutes joining worlds by timestamp alone.

```yaml
# gate-service
management:
  tracing:
    sampling:
      probability: 0.25
  otlp:
    tracing:
      endpoint: http://otel-collector:4318/v1/traces
  metrics:
    tags:
      application: gate-service
```

```java
@Service
public class GateReleaseService {
    private final BillingClient billing;
    private final GateLedger ledger;
    private final ObservationRegistry observations;

    public GateReleaseService(BillingClient billing, GateLedger ledger,
                              ObservationRegistry observations) {
        this.billing = billing;
        this.ledger = ledger;
        this.observations = observations;
    }

    public CheckInResponse releaseGate(String gateId, TruckCheckIn req) {
        return Observation.createNotStarted("harbor.gate.release", observations)
                .lowCardinalityKeyValue("gate.id", gateId)
                .observe(() -> {
                    TariffQuote quote = billing.quote(req.containerId(), req.hazardClass());
                    return ledger.record(gateId, req, quote);
                });
    }
}
```

`Observation` is Boot’s preferred API: one abstraction can emit a timer and a span together when configured. `lowCardinalityKeyValue` mirrors the Micrometer tag rule. Follow a check-in. Gateway span (sampled) carries `traceparent` to gate. Gate’s Observation creates `harbor.gate.release` and nests the Feign client span. Billing continues the trace. In the UI you jump from a Grafana spike at 14:02 to traces in that window and sort by duration. When the breaker opens, child spans fail fast — the trace shows milliseconds, not a mystery hang. Exemplars (when enabled) can link a Prometheus histogram bucket back to a trace id; even without them, matching timestamps and operation names gets you close.

Sampling and cardinality rules return. 100% traces on the public gateway can drown the collector — symptom: rising export queue, dropped spans exactly when incidents happen. High-cardinality span attributes — raw plate numbers — create the same cost problem as metric tags. Put plates in application logs keyed by trace id instead.

Walk a missing-child failure. Gate spans exist; billing never appears. Causes: Feign client not using the instrumented factory; billing sampling at zero while gate samples; W3C vs B3 mismatch across a legacy hop; or a sidecar that strips `traceparent`. Fix by curling headers on a test check-in and confirming the outbound request carries the parent. Another failure: custom spans never `end()` in a finally path — leaks and skewed durations.

Trade-offs: the Java agent auto-instruments wide; Micrometer Observation gives explicit business spans with less surprise. Use both carefully — double instrumentation duplicates spans. Traces without RED metrics leave you blind between sampled requests; metrics without traces leave you blind on critical path. Keep both.

When correlating from Grafana, filter traces by service `gate-service`, operation `harbor.gate.release`, and the spike’s time window; sort by duration descending. The top trace usually names the guilty child — billing SQL, DNS, or a retry storm — faster than reading three log files. If no traces appear in the window, check sampling and collector health before blaming the application.

A misconception is installing an OTel Java agent and never verifying Feign/WebClient propagation on the gate↔billing hop. Another is treating traces as a replacement for RED metrics — you need both. A third is custom spans around every getter until the waterfall is unreadable.

You can see where time goes. The next discipline is deciding what to change when evidence says a method is hot or a pool is saturated — tuning from signals, not folklore.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 102 (*OpenTelemetry*).
