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

Feature-complete is not go-live. Gate can release cargo in a demo and still fail Kubernetes probes, run migrations by hand on Friday, or lack a runbook when billing’s circuit opens. Production readiness is the gate checklist before the quay trusts the new Boot jar with real trucks.

Probes first. Liveness answers “should the platform kill and restart me?” Readiness answers “should I receive traffic?” Do not point both at a deep dependency check or a DB blip flaps the pod forever — symptom: restart loops during a brief Postgres blip while the process was fine.

```yaml
# gate-service
management:
  endpoint:
    health:
      probes:
        enabled: true
      group:
        readiness:
          include: readinessState,db
        liveness:
          include: livenessState
  server:
    port: 8081   # management on a separate port when the mesh requires it
```

```yaml
# kubernetes deployment fragment
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8081
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8081
  periodSeconds: 5
startupProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8081
  failureThreshold: 30
  periodSeconds: 5
```

Startup probes give Flyway and warm caches time before liveness kills a slow boot. Readiness removes the pod from Service endpoints while DB is down without restarting it. Liveness stays cheap — process alive, not “can I quote tariffs.”

Migrations belong in the deploy pipeline — Flyway/Liquibase with clear ownership — not SSH and hope. A failed migration must fail the rollout, not leave half the fleet on schema V41. Observability bar: Micrometer timers on `releaseGate`, Prometheus scrape, Grafana panels with alerts, traces on the check-in path. Resilience bar: timeouts on Feign, breaker around billing, bounded AIS caches. Shutdown bar: graceful shutdown so in-flight check-ins finish when a pod drains.

```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

Walk a drain. SIGTERM arrives; Boot stops accepting new connections; in-flight `releaseGate` may finish within the timeout; then the process exits. Too short a timeout and you cut ledger writes mid-transaction. Too long and deploys stall. Align with kube `terminationGracePeriodSeconds`.

Runbooks are part of the artifact. When `billingQuote` is open, who gets paged, what fallback is expected at the booth, how to verify recovery? Include the Grafana dashboard link, the breaker metric name, and the “cached tariff allowed?” answer. If that paragraph exists only in someone’s head, you are not ready. Rollback path for bad tariff config — previous ConfigMap, previous image — belongs beside the forward deploy steps.

Failure symptoms of false readiness: probes always UP while the ledger is read-only broken because health never checked what the booth needs; noisy probes disabled instead of fixed; go-live without a scrapable `/actuator/prometheus` so the first incident has no baseline; secrets still in the image.

Trade-offs: deep readiness checks catch dependency loss early and couple your traffic shape to that dependency’s blips — sometimes a degraded mode (accept check-in, queue invoice) is better than going NotReady. Document which choice the quay wants before night shift discovers it.

A go-live review that works: someone unfamiliar with the service follows the runbook to answer “billing breaker open — what do I do?” using only links in the artifact. If they need Slack archaeology, readiness failed. Same test for “rollback tariff ConfigMap” and “confirm Prometheus still scrapes after the new management port.”

A misconception is equating “Deployed to prod” with readiness when readiness probes still return UP while the ledger is read-only broken. Another is disabling probes because they were noisy instead of fixing the check. A third is shipping without a rollback path for a bad tariff config refresh.

Once a service survives production, a different pressure appears: the codebase itself gets harder to change — controllers talk to SQL, domain rules scatter, every feature touches everything. Phase 12 starts with the classic layered map of a harbor app, then tightens boundaries.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 105 (*Production Readiness*).
