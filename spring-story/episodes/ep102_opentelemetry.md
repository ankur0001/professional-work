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

Your Grafana panel says payment p99 jumped. Useful — and incomplete. Which hop inside the request burned the time: API gateway, checkout service, inventory, or the card network adapter? Metrics aggregate. Logs fragment. Distributed tracing follows one request across process boundaries and shows you the timeline.

OpenTelemetry — OTel — is the open standard for that instrumentation story. Traces, metrics, and logs share context ideas: a trace id, span ids, baggage. In Spring Boot 3 the Micrometer Observation API and the OTel bridge are the usual path. You depend on Micrometer Tracing with an OTel tracer, export via OTLP to a collector, and the collector fans out to Jaeger, Tempo, Zipkin, or a vendor backend.

Picture a single checkout crossing three services. Gateway receives `POST /checkout`. Checkout service charges payment. Inventory service reserves stock. Without propagation, each service has a private span world. With W3C Trace Context headers — `traceparent` — the same trace id rides the HTTP calls. In a trace UI you see one tree: gateway span, checkout span, child payment span, sibling inventory span. The slow child lights up in red.

Boot wiring at a high level looks like this:

```xml
<!-- Maven sketch — versions via Boot BOM -->
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
  <groupId>io.opentelemetry</groupId>
  <artifactId>opentelemetry-exporter-otlp</artifactId>
</dependency>
```

```yaml
management:
  tracing:
    sampling:
      probability: 1.0   # lab only; use lower in prod
  otlp:
    tracing:
      endpoint: http://otel-collector:4318/v1/traces
```

HTTP server and WebClient/RestClient instrumentation often create spans for you once tracing is on the classpath. Custom work still needs an Observation or an explicit span around the business boundary you care about:

```java
@Service
public class InventoryClient {
    private final RestClient http;
    private final ObservationRegistry observations;

    public Reservation reserve(Sku sku, int qty) {
        return Observation.createNotStarted("inventory.reserve", observations)
                .lowCardinalityKeyValue("sku.category", sku.category())
                .observe(() -> http.post()
                        .uri("/reservations")
                        .body(new ReserveRequest(sku.code(), qty))
                        .retrieve()
                        .body(Reservation.class));
    }
}
```

The Observation name becomes a span name. Low-cardinality keys become attributes you can filter on. The HTTP client span nests underneath when propagation works. If you see three disconnected traces instead of one tree, check headers on the wire and sampling decisions — a service sampling at zero percent produces silence that looks like a break.

Correlate with logs by including trace ids in the pattern (`traceId`, `spanId` via Micrometer Tracing’s MDC integration). Then a Grafana tempo panel and a log backend can jump between "this span" and "these log lines." Metrics still matter: use a trace to find the slow span type, then a Micrometer timer on that operation for fleet-wide percentiles.

Propagation fails in boring ways. A `RestTemplate` built with `new` instead of a Boot-configured builder may omit interceptors. A message consumer that ignores trace headers starts a new root span for every event. Async work on a bare thread pool drops context unless you wrap the executor with context propagation. When the UI shows broken trees, check the client construction and the thread boundary before blaming the collector.

Misconceptions thrash teams here. OTel is not a replacement for Micrometer counters; it complements them. One hundred percent sampling in production can drown collectors — tune probability and tail-based sampling at the collector. Putting high-cardinality ids on every span attribute recreates the Prometheus cardinality problem inside your trace backend.

Today we followed one checkout across services, wired OTLP export, and nested a custom Observation under HTTP spans. You can see where time goes. The next discipline is deciding what to change when the evidence says a pool is saturated or a query is hot — tuning from signals, not from folklore.

That is observability-driven performance work.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 102 (*OpenTelemetry*).

Narration technique: p99 without a culprit → OTel + Micrometer Tracing → cross-service trace walk → OTLP config → Observation code → sampling/cardinality pitfalls → bridge to performance tuning.
