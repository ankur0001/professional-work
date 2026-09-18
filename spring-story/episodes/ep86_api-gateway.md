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

Discovery solved “where is payment-service?” It did not solve “should every phone app know twelve internal hostnames and CORS policies?” An API gateway is the edge hop: one public entry point that routes to internal services, applies cross-cutting rules, and keeps clients ignorant of how many pods sit behind `/api/orders`.

Spring Cloud Gateway is the reactive, Boot-based successor to the older Zuul teaching demos. It is not a servlet MVC app pretending to proxy. It builds on WebFlux and a filter chain of its own. You declare routes: predicates match a request, filters mutate it, and a URI — often `lb://order-service` — sends the call through the load balancer into discovery. The gateway becomes the place for path rewriting, request rate limiting, header injection, and sometimes authentication at the edge.

```java
@SpringBootApplication
public class GatewayApplication {
    public static void main(String[] args) {
        SpringApplication.run(GatewayApplication.class, args);
    }

    @Bean
    RouteLocator commerceRoutes(RouteLocatorBuilder builder) {
        return builder.routes()
            .route("orders", r -> r
                .path("/api/orders/**")
                .filters(f -> f
                    .rewritePath("/api/orders/(?<segment>.*)", "/orders/${segment}")
                    .addRequestHeader("X-Edge", "spring-cloud-gateway"))
                .uri("lb://order-service"))
            .route("payments", r -> r
                .path("/api/payments/**")
                .filters(f -> f.stripPrefix(2))
                .uri("lb://payment-service"))
            .build();
    }
}
```

You can express the same routes in YAML. Many teams prefer config for route tables so ops can adjust without recompiling.

```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: orders
          uri: lb://order-service
          predicates:
            - Path=/api/orders/**
          filters:
            - RewritePath=/api/orders/(?<segment>.*), /orders/${segment}
```

Say the word `lb://` out loud. That scheme tells Gateway to use Spring Cloud LoadBalancer with the service id `order-service`. Without discovery, you could still point `uri` at `http://fixed-host:8080`, but then you are back to static topology. With Eureka or Kubernetes discovery on the classpath, the gateway resolves instances per request or per cache window.

Walk one request. A mobile client calls `https://api.example.com/api/orders/42`. TLS may terminate at a load balancer in front. The request hits Gateway. Predicates select the orders route. Filters rewrite the path to `/orders/42` and maybe attach a correlation header. The gateway asks the load balancer for an `order-service` instance, opens a proxied HTTP call, streams the response back, and the client never learned the pod IP. If order-service is down, the failure surfaces at the edge where you can map it to a clean status and message.

Cross-cutting filters are why gateways earn their keep. Authentication can validate a JWT once at the edge before internal services see traffic — with the caveat that defense in depth still matters inside. Rate limiting can protect fragile backends. Retry filters can absorb blips — carefully, because retries on non-idempotent POSTs hurt. Global filters run for every route; gateway filters run per route. Knowing which layer you configured saves hours.

Operational details separate demos from production. Path predicates are only one matcher — you can match on headers, methods, host, query params, or custom predicates. When two routes could match, specificity and order matter; mis-ordered routes are a classic “why is my rewrite wrong?” bug. Websocket and streaming responses need care because Gateway is reactive end to end: blocking work inside a filter starves the event loop. For auth at the edge, prefer validating tokens and forwarding identity headers over inventing a second session store in the gateway process.

A misconception is stuffing business logic into the gateway until it becomes a second monolith. Keep routes and technical filters at the edge; keep domain rules in services. Another is exposing every internal Actuator through the gateway “for convenience” — that convenience is an attack surface. A third is confusing Gateway with Spring MVC `RestController` reverse-proxy hacks: Gateway’s programming model is route + predicate + filter, not controller methods returning remote calls.

Today we placed Spring Cloud Gateway as the public front door: predicates match, filters reshape, `lb://` URIs lean on discovery, and clients talk to one host while the mesh of services stays private.

Routing to a service name still leaves a choice when three healthy instances exist. Who picks which pod gets this request — and what algorithm keeps one hot instance from taking all the load?

That choice is Load Balancing.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 86 (*API Gateway*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
