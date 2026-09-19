# Episode 86 — API Gateway

| Field | Value |
|---|---|
| Episode | 86 |
| Title | API Gateway |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 86 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

External truckers should hit one hostname — `https://ops.harbor.example` — not a spreadsheet of gate, billing, and scheduling URLs. TLS terminates once. Authn checks once. Paths fan out to internals that never appear on the public DNS. That front door is an API gateway.

Spring Cloud Gateway is a reactive Boot application built on WebFlux and a route model: predicates decide whether a request matches; filters reshape headers, paths, or responses; the URI — often `lb://gate-service` — sends traffic to a discovered instance. It is not a servlet `RestController` that proxies with RestTemplate. Think route tables, not controller methods. Under load the gateway’s event loop stays non-blocking; a blocking call inside a filter starves other truckers’ requests on the same threads — that is why Gateway sits on WebFlux even when gate and billing remain servlet Boot apps.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: gate-checkins
          uri: lb://gate-service
          predicates:
            - Path=/api/gates/**
          filters:
            - StripPrefix=1
            - name: RequestSize
              args:
                maxSize: 256KB
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 50
                redis-rate-limiter.burstCapacity: 100
        - id: billing-quotes
          uri: lb://billing-service
          predicates:
            - Path=/api/tariffs/**
          filters:
            - StripPrefix=1
        - id: scheduling-berths
          uri: lb://scheduling-service
          predicates:
            - Path=/api/berths/**
            - Method=GET
```

```java
@Bean
RouteLocator truckerRoutes(RouteLocatorBuilder builder) {
    return builder.routes()
            .route("gate-release", r -> r
                    .path("/api/gates/*/releases")
                    .and().method("POST")
                    .filters(f -> f
                            .addRequestHeader("X-Harbor-Edge", "gateway")
                            .circuitBreaker(c -> c.setName("gateReleaseCb")
                                    .setFallbackUri("forward:/fallback/gate")))
                    .uri("lb://gate-service"))
            .build();
}
```

A trucker POSTs `/api/gates/G12/check-ins`. The `Path` predicate matches `gate-checkins`. `StripPrefix=1` drops `/api` (or your configured count) so gate sees the path it actually mapped. `lb://gate-service` resolves through discovery and load balancing to a concrete pod. If StripPrefix is wrong by one segment, gate returns 404 while the gateway log still shows a successful route match — classic symptom: edge `200` path rewritten into an unknown controller mapping. Billing and scheduling stay unreachable except through their declared paths; a curious client probing `/api/internal/ledger` should not find a route.

Global filters can attach correlation headers, enforce JWT at the edge, or rate-limit abusive clients before a gate pod burns CPU. Walk a RateLimiter trip: Redis says the trucker token bucket is empty; Gateway returns `429` without calling gate. Walk a downstream outage: circuit breaker filter opens, fallback URI returns a controlled JSON body, booth scanners show “retry shortly” instead of a raw connection reset. Those behaviors belong at the edge when every public client shares one hostname.

Keep domain logic out of the gateway. Quoting tariffs, releasing cargo, assigning berths — those belong in services. The gateway owns technical cross-cuts: routing, TLS, coarse auth, request size, maybe canary headers (`X-Harbor-Canary` → weighted routes). When the gateway accumulates business rules — “hazard class IMDG_3 must go to billing first” — you have rebuilt the monolith at the wrong layer, and every change to tariff policy requires an edge deploy.

Trade-offs: one gateway simplifies trucker TLS and WAF placement, but it is also a blast radius — a bad route YAML takes down all three backends’ public face. Some teams split edge by audience (trucker vs ops console). Latency adds a hop; measure it. Predicate order matters when two routes could match; put the more specific path first or you will debug “why does GET /api/berths/B7 hit the wrong service?” for an hour.

A misconception is exposing every internal Actuator through the gateway “for convenience” — that convenience is an attack surface. Another is confusing Gateway with Spring MVC reverse-proxy hacks: predicates and filters are the programming model. A third is putting sticky session affinity on by default for a stateless check-in API; prefer token-based identity and any healthy instance.

Truckers now have one edge. Behind it, three billing pods answer the same service id. Who chooses which pod gets the next quote request?

Client-side load balancing makes that choice explicit.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 86 (*API Gateway*).
