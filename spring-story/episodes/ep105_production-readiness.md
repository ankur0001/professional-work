# Episode 105 — Production Readiness

| Field | Value |
|---|---|
| Episode | 105 |
| Title | Production Readiness |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 105 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Feature-complete is a product statement. Production-ready is an operations statement. You can demo checkout on a laptop and still be unsafe to expose to real traffic: no probes, secrets in the image, every Actuator endpoint on the public port, zero dashboards, and a single instance with sticky dreams of availability.

Production readiness is the gate where Phase 11’s tools become habits. Health for orchestrators. Metrics and traces for humans. Safe config. Resource limits. Rollback story. You are not collecting trophies — you are removing classes of three-in-the-morning failure.

Start with Actuator honestly. Liveness and readiness are not the same. Liveness failure means restart the process. Readiness failure means stop sending traffic while the process may still be alive — database warmed up, caches primed, dependent check passed.

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
      show-details: when_authorized
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  server:
    port: 8081   # management on a separate port
```

Kubernetes probes hit `/actuator/health/liveness` and `/actuator/health/readiness` on the management port. Custom `HealthIndicator` beans should fail readiness when the app cannot do useful work — empty required config, migration not finished — not when a non-critical cache is cold.

Config and secrets: externalize with env vars or a secret store; never bake production credentials into the jar. Use profiles deliberately. Fail fast on missing required properties with `@ConfigurationProperties` validation. Logging: structured JSON in prod, correlation with trace ids, and levels that do not print payloads containing PII.

From earlier episodes, require a minimum observability bar before "go":

- Micrometer business timers/counters on critical paths
- Prometheus scrape working on the management port
- A Grafana dashboard with traffic, errors, latency, saturation
- Tracing sampled and reachable from that dashboard
- Memory and GC panels watched under a load test
- Alerts on SLO burn, not on every CPU blip

Resilience is part of readiness. Timeouts on every remote call. Bulkheads or concurrency limits where one dependency can exhaust your threads. Circuit breakers where fail-fast beats pile-up. Graceful shutdown so in-flight requests finish when a pod receives SIGTERM:

```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

Capacity: set JVM and container limits that match, horizontal pod autoscaling on a meaningful metric, and a proven rollback — previous image, previous config map. A readiness review that cannot answer "how do we undo this deploy?" is incomplete. Prefer scaling on saturation or request rate tied to SLO burn, not on CPU alone when your bottleneck is a downstream pool.

Run a pre-prod drill once: kill a pod mid-request and confirm graceful shutdown drains connections; break the database and confirm readiness goes false while liveness stays true; scrape metrics from a fresh instance and open the Grafana dashboard cold. Paper checklists lie; drills tell the truth.

Misconception: a green `/actuator/health` means production-ready. Health can be shallow while your payment timer is missing and your scrape endpoint is firewalled wrong. Misconception: readiness is a one-time checklist at first launch. It is a living contract as dependencies and traffic shapes change. Misconception: "we have Kubernetes, so we are ready." Orchestration without probes, budgets, and observability only restarts confusion faster.

Today we closed Phase 11 by binding probes, management ports, observability bars, timeouts, and graceful shutdown into one gate. Once a service survives production, a different pressure appears: the codebase itself gets harder to change — controllers talk to SQL, domain rules scatter, every feature touches everything.

That structural pain is where enterprise architecture begins — starting with the layered baseline most Spring teams already half-use.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 105 (*Production Readiness*).

Narration technique: feature-complete vs ready → probes and management port → observability bar → resilience/shutdown → misconceptions → bridge to layered architecture (Phase 12).
