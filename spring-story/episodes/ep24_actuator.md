# Episode 24 — Actuator

| Field | Value |
|---|---|
| Episode | 24 |
| Title | Actuator |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 24 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Your app starts. Config binds. Traffic may even flow. Operations still needs a contract: how do we know this process is healthy without SSH and a debugger?

Without Actuator, teams invent ad-hoc `/ping` controllers that always return `"ok"`, even when the database pool is exhausted. Load balancers keep sending traffic. Or someone exposes raw JMX in ways nobody documented. Shipping without standard health and metrics means every service invents its own ops dialect.

The engineer question is blunt: can the platform expose health, info, and metrics endpoints with the same discipline Boot brought to startup?

Spring Boot Actuator is that ops surface. Add `spring-boot-starter-actuator` and Boot auto-configures management endpoints under a base path — by default `/actuator`. The headline endpoint is health. Hit it and you get a status that can aggregate disk space, database connectivity, and custom indicators.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when_authorized
```

Walk a request. Process listens on 8080. Client calls `GET /actuator/health`. The dispatcher routes to Actuator's web layer, not your business controllers. Health contributors run: a DB indicator may open a validation query; disk space checks free bytes. The response body looks like `{"status":"UP"}` when everything passes, or `DOWN` / `OUT_OF_SERVICE` when a contributor fails. Kubernetes readiness and liveness probes often point here — sometimes split into separate readiness and liveness groups in modern Boot.

```bash
curl -s http://localhost:8080/actuator/health
# {"status":"UP"}

curl -s http://localhost:8080/actuator/metrics/http.server.requests
# meter names, counts, and tag dimensions for request traffic
```

`/actuator/info` can publish build info when you configure the build plugin to generate it. `/actuator/metrics` lists meters; a named meter path returns measurements. Other endpoints exist — `env`, `beans`, `threaddump` — and they are powerful enough that exposure must be intentional. Do not open everything on a public port. Prefer limiting exposure, securing management endpoints, or binding management to a separate port.

```yaml
management:
  server:
    port: 8081
```

That split keeps business traffic on 8080 and ops traffic on 8081 behind a tighter network policy. Custom health indicators are ordinary beans implementing `HealthIndicator` when your dependency on a payments cache or message broker matters to "UP."

The misconception is "Actuator is optional decoration for demos." In production it is how platforms ask the process questions. The opposite misconception is enabling every endpoint with full `env` detail on the internet — that is a credentials leak waiting to happen. Treat exposure as a security decision, not a convenience checkbox.

With ops endpoints in place, local developers still want a faster inner loop than stop, rebuild, restart for every controller tweak.

That inner-loop tooling is DevTools.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 24 (*Actuator*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
