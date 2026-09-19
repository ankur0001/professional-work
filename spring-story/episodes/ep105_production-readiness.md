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

Friday 18:10. Gate’s new Boot jar is “feature complete” in the demo environment. Trucks are already queued for the weekend shift. Kubernetes rolls the Deployment. Within minutes pods restart in a loop, the Service has no ready endpoints, and the booth sees timeouts. Nobody changed the release logic. The jar was not ready for production as an operating problem — probes, startup cost, shutdown, and a missing runbook — even though the feature demo looked fine.

Production readiness is that operating problem. Spring Boot Actuator, Micrometer, and graceful shutdown are tools inside it. They are not a checklist that replaces judgment about how this service fails in front of real traffic.

Start with the Friday failure. Liveness and readiness both pointed at a deep health indicator that pinged billing and the ledger database. A brief billing blip marked the pod not-live; Kubernetes killed it; startup ran Flyway again; the next blip killed it again. Symptom: restart loop during a dependency hiccup while the JVM process itself was fine. Fix the meaning of the probes. Liveness should answer “should the platform kill me?” — cheap process health. Readiness should answer “should I receive traffic?” — including critical dependencies you are unwilling to serve without. Startup probes give Flyway and warm caches time before liveness is allowed to kill a slow boot.

```yaml
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
    port: 8081
```

```yaml
livenessProbe:
  httpGet: { path: /actuator/health/liveness, port: 8081 }
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet: { path: /actuator/health/readiness, port: 8081 }
  periodSeconds: 5
startupProbe:
  httpGet: { path: /actuator/health/liveness, port: 8081 }
  failureThreshold: 30
  periodSeconds: 5
```

Readiness can remove the pod from Service endpoints while the DB is down without restarting it. Liveness stays cheap. If both probes mean “deep dependency check,” you recreate Friday’s loop.

The same go-live has to survive deploy mechanics. Migrations belong in the pipeline with clear ownership — a failed migration fails the rollout instead of leaving half the fleet on schema V41. Observability is not optional decoration: if `releaseGate` has no timer, Prometheus has no scrape, and traces do not cover check-in, the first incident has no baseline. Resilience settings you already learned — timeouts, breakers, bounded caches — are readiness items when the booth depends on them. And shutdown matters: when a pod drains, in-flight releases should finish.

```yaml
server:
  shutdown: graceful
spring:
  lifecycle:
    timeout-per-shutdown-phase: 30s
```

Walk a drain. SIGTERM arrives; Boot stops accepting new work; in-flight `releaseGate` may finish within the timeout; then the process exits. Too short and you cut ledger writes mid-transaction. Too long and deploys stall. Align with kube `terminationGracePeriodSeconds`.

Runbooks are part of the artifact. When `billingQuote` is open, who is paged, what fallback the booth uses, how recovery is verified — including the Grafana link and the breaker metric name — must not live only in Slack history. Rollback for a bad tariff ConfigMap or a bad image belongs next to the forward deploy steps. A practical readiness test: someone unfamiliar with the service follows the runbook for “billing breaker open” and “rollback tariff ConfigMap” using only links in the artifact. If they need tribal knowledge, you are not ready.

Trade-offs stay explicit. Deep readiness checks catch dependency loss early and couple your traffic shape to that dependency’s blips — sometimes degraded mode (accept check-in, queue invoice) beats going NotReady. Document which choice the quay wants before night shift invents one. Another trap: equating “Deployed to prod” with readiness while probes stay UP and the ledger is read-only broken because health never checked what the booth needs. A third: disabling noisy probes instead of fixing the check.

Once a service can survive production operations, a different pressure appears: the codebase itself gets harder to change — controllers talk to SQL, domain rules scatter, every feature touches everything. Architecture boundaries become the next operating concern.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 105 (*Production Readiness*).
