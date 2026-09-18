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

`GateReleaseService` records timers into a `MeterRegistry`. Restart a pod and in-process counters reset. Scale to twelve gate replicas and you have twelve private notebooks. Prometheus scrapes each instance, stores samples over time, and lets you ask what p95 `harbor.gate.release.duration` was across the fleet at 14:02.

Boot exposes a scrape endpoint when `micrometer-registry-prometheus` is on the classpath and Actuator exposes it:

```yaml
# gate-service
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    prometheus:
      enabled: true
  metrics:
    tags:
      application: gate-service
    distribution:
      percentiles-histogram:
        harbor.gate.release.duration: true
```

A scrape returns text like:

```text
# HELP harbor_gate_release_duration_seconds
# TYPE harbor_gate_release_duration_seconds histogram
harbor_gate_release_duration_seconds_bucket{application="gate-service",gate_id="G12",le="0.5"} 790.0
harbor_gate_release_duration_seconds_bucket{application="gate-service",gate_id="G12",le="1.0"} 820.0
harbor_gate_release_duration_seconds_count{application="gate-service",gate_id="G12"} 842.0
harbor_gate_release_duration_seconds_sum{application="gate-service",gate_id="G12"} 126.3
harbor_gate_release_started_total{application="gate-service"} 900.0
harbor_gate_release_succeeded_total{application="gate-service"} 842.0
```

Micrometer turns dots into underscores and appends `_total` for counters, `_seconds` for timers. If you curl the endpoint and do not see `harbor_gate_release_*`, the meter never registered or the scrape hits a different pod than the one you exercised. Walk that check during deploy: port-forward one gate pod, `curl localhost:8081/actuator/prometheus | grep harbor_gate`, confirm series before wiring alerts.

Wire Prometheus to the gate pods:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: harbor-gate
    metrics_path: /actuator/prometheus
    scrape_interval: 15s
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ["harbor"]
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: gate-service
```

PromQL for gate latency and error ratio:

```promql
# p95 release duration across gate pods
histogram_quantile(
  0.95,
  sum by (le) (
    rate(harbor_gate_release_duration_seconds_bucket{application="gate-service"}[5m])
  )
)

# failure ratio from started vs succeeded counters
1 -
(
  sum(rate(harbor_gate_release_succeeded_total[5m]))
  /
  sum(rate(harbor_gate_release_started_total[5m]))
)
```

Read the queries carefully. `rate` needs a range at least several scrape intervals — `[5m]` on a 15s scrape is sane; `[15s]` flaps. Divide by started, not by a raw counter without `rate`, or restarts look like error spikes. `histogram_quantile` needs histogram buckets (`percentiles-histogram: true`); a summary cannot do accurate server-side p95 across instances the same way. Sum by `le` before quantile so you aggregate pods correctly.

Timers in Micrometer become histograms or summaries depending on config; prefer histograms when you need `histogram_quantile`. Protect the scrape endpoint — it should not be world-readable on the public gateway. Cardinality discipline from the Micrometer episode applies here: one unbounded label turns a scrape into a cost incident; Prometheus will still try to ingest until retention and memory hurt.

Failure symptoms: scrape only one replica via a mistaken Service monitor and the dashboard lies about fleet health; alert on absolute counter values and page every process restart; expose `/actuator/prometheus` on the trucker hostname and leak internal series. Another: `up{job="harbor-gate"} == 0` after a path rename to `/actuator/metrics` — wrong path, silent gap in graphs.

Trade-offs: shorter scrape intervals catch spikes faster and cost more; longer intervals miss brief booth storms. Recording rules precompute expensive gate queries for dashboards; they add indirection. Keep raw series for forensics.

Alerting hygiene belongs next to scrape config. Page on `up == 0` for the harbor-gate job when all pods vanish; warn when a single pod’s scrape fails while siblings succeed — that is a pod or network partition, not necessarily a fleet outage. Keep runbook links beside the PromQL so 03:10 does not start with reinventing `histogram_quantile`.

A misconception is scraping only one gate pod and calling it fleet health. Another is alerting on raw counter values instead of rates. A third is exposing `/actuator/prometheus` through the trucker-facing gateway without auth.

Raw PromQL in a black terminal is powerful and miserable during a 3am booth backup. Operators need panels, shared time ranges, and a dashboard that already knows the gate queries. Save the exploratory PromQL for engineering; promote the survivors into Grafana and recording rules once they have earned a page.

That shared picture is Grafana.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 100 (*Prometheus*).
