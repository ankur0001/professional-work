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

Pager, 02:10, seaport gate API. Containers are "Running." Clients time out. On-call curls from the jump host:

```bash
curl -s https://gate.internal:8081/actuator/health | jq
```

JSON returns `"status":"DOWN"` with `db` detail `Connection refused`. Not a mystery novel — Actuator turned a black box into a health document. The outage was a drained connection pool after a Postgres failover the app never learned about. Without that endpoint, the next step would have been speculative pod deletes and a debugger on a live gate.

Spring Boot Actuator exposes operational endpoints: health, info, metrics, env (careful), loggers, heapdump (very careful), and more. Add `spring-boot-starter-actuator`. Secure them. In production, expose only what ops needs, often on a separate management port so public traffic and ops traffic do not share the same accidental exposure.

```yaml
management:
  server:
    port: 8081
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when_authorized
  health:
    db:
      enabled: true
```

```java
@Component
public class TideApiHealthIndicator implements HealthIndicator {
    private final TideClient tides;

    public TideApiHealthIndicator(TideClient tides) {
        this.tides = tides;
    }

    @Override
    public Health health() {
        try {
            tides.ping();
            return Health.up().withDetail("tideApi", "reachable").build();
        } catch (Exception ex) {
            return Health.down(ex).withDetail("tideApi", "unreachable").build();
        }
    }
}
```

Walk the config and indicator. `management.server.port: 8081` binds actuators away from the main 8080 API port. `exposure.include` is an allowlist — nothing else is web-exposed. `show-details: when_authorized` avoids leaking DB URLs to anonymous callers. `TideApiHealthIndicator` is a custom check: `health()` pings the tide service the gate depends on for clearance windows; UP/DOWN with details aggregates into the overall document. Built-in DB indicators check the DataSource similarly.

Runtime of `/actuator/health`. A web endpoint (management context if configured) invokes `HealthEndpoint`, which aggregates `HealthIndicator` / `ReactiveHealthIndicator` beans — DB, disk space, custom tide API. Each returns UP, DOWN, OUT_OF_SERVICE, or UNKNOWN with optional details. Aggregate status follows severity rules (DOWN wins over UP). Kubernetes can probe `/actuator/health/liveness` and `/actuator/health/readiness` separately so a failing dependency marks the app *unready* (stop sending traffic) without killing the JVM if you split indicators carefully — a dependency blip should not always restart the pod. The metrics endpoint exposes Micrometer meters; with `prometheus` on the include list, scrapers pull time series from the same process that just answered health.

Failure mode from 02:10: health DOWN on db, pods still "Running" in Kubernetes because liveness was a TCP port check, not readiness on actuator. Symptom: Service still routes traffic to broken pods; clients time out; actuator on 8081 tells the truth. Fix probes to use readiness. Another failure: exposing `/actuator/env` and `/actuator/heapdump` on the public app port without auth — attackers read secrets or trigger expensive dumps. Symptom may be security findings or sudden CPU spikes from heapdump. Lock down `include`, use management port, require auth.

Trade-offs. Actuator shortens incidents by making process state HTTP-queryable; every endpoint is also an attack and load surface. Fine-grained health indicators improve signal and can flap readiness if they check unstable dependencies — sometimes a dependency belongs in metrics/alerts, not in readiness. Prefer few, meaningful indicators over a dozen remote pings on every probe.

Walk the 02:10 curl one layer deeper. `HealthEndpoint` does not open JDBC itself; it asks the `db` indicator, which borrows a connection from the DataSource and runs a validation query (or relies on pool validation). `Connection refused` means the TCP path to Postgres failed — host, port, or network policy — not "Spring is down." Custom `TideApiHealthIndicator` runs in the same aggregation pass; if tide is DOWN but you configured it only for details and kept readiness on liveness-separate groups, you can still serve gate traffic while alerting on tide. That knobs-and-groups design is why Actuator health is a model, not a single boolean.

Misconception unique to Actuator: "Exposing `/actuator/env` and `/actuator/heapdump` on the public app port is fine because Actuator is 'ops only'." Actuator endpoints are HTTP APIs. Unsecured, they leak configuration and enable denial-of-service. Management port, auth, and tight `include` lists are part of the feature — not optional manners.

Health shows UP again after Postgres recovers. Developers fixing the museum ticket UI still restart the whole Boot app for every Thymeleaf tweak. The feedback loop hurts — DevTools exists for that loop, with its own sharp edges.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 24 (*Actuator*).
