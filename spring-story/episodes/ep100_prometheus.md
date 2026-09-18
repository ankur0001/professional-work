# Episode 100 — Prometheus

| Field | Value |
|---|---|
| Episode | 100 |
| Title | Prometheus |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 100 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Last episode your `CheckoutService` recorded timers and counters into a `MeterRegistry`. Those meters live in memory inside each JVM. Restart the pod and the in-process counters reset. Scale to twenty replicas and you have twenty private notebooks. You need a system that scrapes each instance, stores samples over time, and lets you ask "what was p99 payment duration across the fleet at 14:02?"

Prometheus is that system for many Spring shops. It is a time-series database and scraper. It pulls — it does not wait for your app to push every sample — on an interval you configure. Your Boot app’s job is to expose a text exposition endpoint Prometheus understands. Micrometer’s Prometheus registry formats your meters into that exposition.

Wire it with the usual Boot pieces. Add the Actuator starter and the Micrometer Prometheus registry dependency. Expose the prometheus endpoint. Keep management endpoints on a dedicated port or tightly authorize them in production.

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus,metrics
  endpoint:
    prometheus:
      enabled: true
  metrics:
    tags:
      application: checkout-service
      env: prod
```

With `micrometer-registry-prometheus` on the classpath, Actuator serves something like `GET /actuator/prometheus`. Hit it locally and you should see lines such as `checkout_payment_duration_seconds_bucket` and `jvm_memory_used_bytes` — name mangling and unit suffixes are part of the Prometheus convention. Micrometer timers become `_seconds` histograms or summaries depending on configuration. Prefer histograms when you need accurate percentiles via `histogram_quantile`; summaries compute quantiles in-process and are harder to aggregate across replicas.

Secure the scrape path. In production, put management endpoints on port `8081`, restrict network access to the Prometheus scrape identity, or require authentication. Exposing every Actuator route on the public `8080` alongside your API is a common foot-gun.

Prometheus itself needs a scrape job pointed at your instances. In Kubernetes that often means a PodMonitor or ServiceMonitor; in a simple lab it is a static target:

```yaml
# prometheus.yml (scrape config sketch)
scrape_configs:
  - job_name: checkout-service
    metrics_path: /actuator/prometheus
    scrape_interval: 15s
    static_configs:
      - targets: ["checkout:8080"]
```

Walk the loop once. App records a payment timer. Micrometer updates the in-memory Prometheus meter. Fifteen seconds later Prometheus GETs `/actuator/prometheus`. Samples land in TSDB. You query with PromQL: `histogram_quantile(0.99, sum(rate(checkout_payment_duration_seconds_bucket[5m])) by (le))`. That query is how "feels slow" becomes a number with a time window.

Common tags from Boot — `application`, `env`, and often instance identity — let you group without rewriting every meter. MeterFilters can deny high-cardinality tag keys before they escape. If a developer tags by `userId`, you will feel it in Prometheus cardinality long before the dashboard looks pretty. A practical filter denies known-dangerous keys and enforces a naming prefix so one team’s `orders` counter does not collide with another’s.

```java
@Bean
MeterFilter denyUserIdTags() {
    return MeterFilter.deny(id -> id.getTags().stream()
            .anyMatch(t -> t.getKey().equals("userId")));
}
```

Relabeling and recording rules on the Prometheus side can precompute expensive queries — for example a recording rule for checkout success ratio — so dashboards stay snappy. That is still downstream of honest exposition from the app.

Do not confuse Actuator’s `/actuator/metrics` JSON browse UI with the Prometheus scrape endpoint. The JSON endpoint is for humans and quick checks. Scrapers want the Prometheus text format. Also do not push application metrics into logs and call it done; logs and metrics answer different questions, and scrape-based metrics aggregate across replicas cleanly when the exposition is correct.

Today we connected Micrometer’s in-process meters to a scrape target, exposed `/actuator/prometheus`, and sketched the PromQL path from timer buckets to a percentile. Raw PromQL in a black terminal is powerful and still hard to live in during an incident. Operators need panels, time ranges, and shared dashboards.

That visualization layer is Grafana.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 100 (*Prometheus*).

Narration technique: trapped in-process meters → Prometheus pull model → Boot exposure → scrape config → PromQL example → cardinality/endpoint pitfalls → bridge to dashboards.
