# Episode 90 — Distributed Tracing

| Field | Value |
|---|---|
| Episode | 90 |
| Title | Distributed Tracing |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 90 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A trucker reports check-in took forty seconds. Gateway logs look fine. Gate logs show a slow billing call. Billing logs show a slow DB. Without shared identifiers, those three files are three novels. Distributed tracing stitches them: one trace id for the whole check-in, one span per hop, parent-child links across gateway → gate → billing.

In modern Spring, Micrometer Tracing with an OpenTelemetry or Brave bridge propagates context over HTTP. Boot instruments servlet/WebFlux requests and outbound clients — RestTemplate, WebClient, Feign — so W3C `traceparent` (or B3) headers ride along. You rarely hand-roll headers; you verify they appear and that your sampler is intentional. When a hop is missing from the waterfall, the usual culprit is an outbound client built without the instrumented builder — a plain `WebClient.create()` that never inherited the observation filter.

```yaml
# gate-service & billing-service
management:
  tracing:
    sampling:
      probability: 1.0   # demos; lower in hot prod
  endpoints:
    web:
      exposure:
        include: health,prometheus
logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]"
```

```java
@Service
public class GateReleaseService {
    private final BillingClient billing;
    private final GateLedger ledger;
    private final Tracer tracer;

    public GateReleaseService(BillingClient billing, GateLedger ledger, Tracer tracer) {
        this.billing = billing;
        this.ledger = ledger;
        this.tracer = tracer;
    }

    public CheckInResponse accept(String gateId, TruckCheckIn req) {
        Span span = tracer.nextSpan().name("gate.accept").start();
        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            span.tag("gate.id", gateId);
            span.tag("container.id", req.containerId());
            TariffQuote quote = billing.quote(req.containerId(), req.hazardClass());
            return ledger.record(gateId, req, quote);
        } finally {
            span.end();
        }
    }
}
```

Follow one check-in. Gateway creates root span `http POST /api/gates/G12/check-ins`. Gate continues the trace on inbound because `traceparent` arrived, adds `gate.accept`, Feign starts a child span for `GET billing-service/tariffs/quote`. Billing’s inbound span nests under that child. In a trace UI you see where the forty seconds went — connection wait, SQL, or a circuit-open fail-fast that returns in milliseconds. Breaker opens that finish in 2ms look different from 8s timeouts; traces make that visible without guessing. Log lines carrying `%X{traceId}` let you jump from a booth complaint ticket to the exact waterfall when the trucker gives you a time window.

Sampling is policy. `probability: 1.0` is fine for a staging quay; production usually samples a fraction and always keeps error traces if your stack supports it. High-cardinality tags — raw truck plate on every span — explode storage the same way metric tags do. Prefer low-cardinality dimensions (`gate.id`, `hazard.class`) and put unique identifiers in logs correlated by trace id.

Failure symptoms without tracing discipline: three teams each swear their service was fine; MTTR stretches while someone greps by approximate timestamp; a missing child span makes billing look instantaneous when Feign was never instrumented. With tracing but bad clocks, skew across pods confuses duration math — keep NTP healthy. With 100% sampling on a hot gateway, the collector lags and operators lose the tool during the incident they need it for.

Trade-offs: full tracing everywhere is expensive; metrics alone cannot show critical path across processes. Start with ingress + inter-service HTTP, add custom spans where business methods hide time (`gate.accept`, `ledger.record`), and leave getter noise out of the waterfall. Baggage can carry a check-in correlation across hops, but treat it as carefully as headers — do not put secrets in baggage.

A misconception is equating “we added a correlation id filter years ago” with full distributed tracing; a log field without parent/child spans does not give you a critical path. Another is enabling 100% sampling on a hot gateway and surprising the collector budget. A third is forgetting outbound Feign instrumentation and wondering why gate spans never show billing children.

Traces explain one request. Resilience still needs more than open/closed: retries with backoff, rate limits against a flaky tide vendor, bulkheads so tide threads cannot starve gate’s billing pool.

That toolbox is Resilience4j beyond the single breaker annotation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 90 (*Distributed Tracing*).
