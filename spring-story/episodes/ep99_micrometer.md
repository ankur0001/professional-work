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

You shipped the feature. Tests are green. Contracts hold. Then a pager goes off at two in the morning: checkout feels slow. Someone asks, "how slow, for whom, since when?" and the best answer in the room is a screenshot of a log line. That gap — between "something feels wrong" and "we can prove it" — is why Phase 11 starts with metrics, not with dashboards.

Micrometer is Spring’s vendor-neutral metrics facade. You write against `MeterRegistry`. Boot wires a registry for you. Exporters — Prometheus, Datadog, CloudWatch, and others — plug in based on classpath and configuration. Your service code stays about counters and timers, not about a particular monitoring vendor’s SDK.

Think in four meter types you will actually use. A `Counter` only goes up: payments charged, retries attempted, cache misses. A `Timer` records both how long something took and how often it ran — perfect for a service method. A `Gauge` samples a current value: queue depth, active sessions, heap used. A `DistributionSummary` captures sizes or amounts that are not durations — payload bytes, items per batch. Most business instrumentation starts with Counter and Timer.

Here is the shape you want on a checkout path. Inject the registry, name the meters with stable names and low-cardinality tags, and record where the work happens — not in a filter that only sees HTTP status.

```java
@Service
public class CheckoutService {
    private final PaymentGateway gateway;
    private final Counter checkoutStarted;
    private final Counter checkoutSucceeded;
    private final Timer paymentTimer;

    public CheckoutService(PaymentGateway gateway, MeterRegistry registry) {
        this.gateway = gateway;
        this.checkoutStarted = registry.counter("checkout.started");
        this.checkoutSucceeded = registry.counter("checkout.succeeded");
        this.paymentTimer = registry.timer("checkout.payment.duration");
    }

    public Receipt checkout(Cart cart) {
        checkoutStarted.increment();
        PaymentResult paid = paymentTimer.record(() -> gateway.charge(cart.total()));
        checkoutSucceeded.increment();
        return Receipt.from(paid);
    }
}
```

Read the names carefully. `checkout.started` and `checkout.succeeded` let you compute a success ratio. `checkout.payment.duration` isolates the gateway call from the rest of the request. Tags belong on dimensions you will filter by later — `region`, `payment_method` — not on unbounded values like user id or cart id. High-cardinality tags explode time series and bill you in storage and query cost.

Boot already gives you a lot for free. With Actuator and Micrometer on the classpath you typically get JVM metrics, HTTP server request timers, and often datasource pool gauges without writing a line. Custom meters sit beside those. The `MetricsEndpoint` under Actuator can show a snapshot for debugging. Production scraping usually goes through a dedicated registry format — and that is the next episode’s job.

Annotations exist too. `@Timed` on a bean method can wrap timing when AOP is enabled. Prefer explicit registry use when the metric must sit around one collaborator call, not the whole method, or when you need counters that are not durations. Own the placement; do not sprinkle `@Timed` hoping the right story appears.

A frequent mistake is treating Micrometer as "Prometheus annotations." Micrometer is the API. Prometheus is one backend. Another mistake is measuring only HTTP status codes and calling that observability. Latency percentiles on the payment hop, error counters by failure type, and saturation gauges on the thread pool tell you where to look. Status codes alone tell you that customers are unhappy.

So today we named the facade, practiced Counter and Timer on a real service method, and drew the line between free JVM/HTTP meters and intentional business meters. Numbers in a process are still trapped in that process. The open question is how an outside system pulls them on a schedule and stores them as time series you can query across pods.

That pull model is Prometheus.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 99 (*Micrometer*).

Narration technique: outage question → Micrometer facade → meter types → Timer/Counter on CheckoutService → cardinality warning → free Boot meters → misconceptions → bridge to scrape/export.
