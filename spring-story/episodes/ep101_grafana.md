# Episode 101 — Grafana

| Field | Value |
|---|---|
| Episode | 101 |
| Title | Grafana |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 101 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

At 03:10 the quay lead does not want to invent PromQL. They want a dashboard titled Gate Release that already shows p95 duration, error ratio, and request rate for the last hour. Grafana turns scraped series into that shared picture — panels, variables for `gate_id`, and alerts that fire on the same queries you trust.

Provision a datasource and a starter dashboard as code so every environment matches:

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
```

```json
{
  "title": "Harbor Gate Release",
  "panels": [
    {
      "title": "Gate release p95",
      "type": "timeseries",
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum by (le) (rate(harbor_gate_release_duration_seconds_bucket{application=\"gate-service\"}[5m])))"
        }
      ]
    },
    {
      "title": "Release error ratio",
      "type": "timeseries",
      "targets": [
        {
          "expr": "1 - (sum(rate(harbor_gate_release_succeeded_total[5m])) / sum(rate(harbor_gate_release_started_total[5m])))"
        }
      ]
    },
    {
      "title": "HTTP 5xx rate (gate)",
      "targets": [
        {
          "expr": "sum(rate(http_server_requests_seconds_count{application=\"gate-service\",status=~\"5..\"}[5m]))"
        }
      ]
    },
    {
      "title": "Billing breaker open",
      "targets": [
        {
          "expr": "resilience4j_circuitbreaker_state{name=\"billingQuote\",state=\"open\"}"
        }
      ]
    }
  ]
}
```

Walk an on-call use. Page fires on error ratio. Open Gate Release, set time range to “last 1 hour,” glance p95 and 5xx, then the breaker panel. If breaker is open and p95 collapsed, fail-fast is working and billing is the dependency. If breaker is closed and p95 climbed with Feign client timers high, billing is slow but still accepting — capacity or DB. That story only works if panels share the same PromQL you alert on. Divergent ad-hoc queries in a laptop JSON file produce “green dashboard, red alert” arguments.

Alerting belongs on the same expressions. A rule on error ratio > 2% for five minutes pages the gate on-call; a rule on p95 > 2s warns before trucks queue visibly. Variables like `$gate` rewrite queries to `gate_id="$gate"` when you have a manageable set of booths — not when every temporary lane becomes a label explosion. Folder permissions matter: quay leads need view; only platform edits provisioning.

Grafana cannot invent meters Spring never recorded. If `harbor.gate.release.duration` is missing, the panel stays empty and the honesty falls back to Micrometer placement. Dashboards are views over instrumentation, not a substitute for it. Empty panels at go-live are a readiness defect, not a Grafana bug.

Failure symptoms: twenty pretty panels, zero alerts; screenshot-driven ops when the only dashboard lives on someone’s desktop; mixed billing and gate on one overloaded row until nobody knows which SLO burned; auto-refresh so aggressive it hammers Prometheus during an incident. Another: templating on high-cardinality labels until the variable dropdown times out.

Trade-offs: few golden signals (RED — rate, errors, duration — plus dependency state) beat a wall of vanity charts. Provisioning-as-code keeps staging and prod aligned; UI-only edits drift. Link panels to runbooks and trace UIs so the next click after “p95 high” is not a blank search box.

During a booth backup, the quay lead should change only the time range and maybe `$gate`. If they must edit PromQL mid-incident, the dashboard failed its job. Keep a “debug” row collapsed by default — Hikari pending, Feign client timers, breaker state — for engineers without cluttering the first viewport operators see.

A misconception is building twenty pretty panels with no alerts and calling the service observable. Another is screenshot-driven ops — dashboards that only exist in a laptop JSON file. A third is mixing billing and gate on one overloaded row until nobody knows which SLO burned.

Metrics answer how much and how often. They still struggle with what happened on *this* truck’s check-in as it crossed gateway, gate, and billing. That is traces correlated with the same meters — OpenTelemetry’s territory.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 101 (*Grafana*).
