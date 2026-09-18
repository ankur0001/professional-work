# Episode 83 — Microservices with Spring

| Field | Value |
|---|---|
| Episode | 83 |
| Title | Microservices with Spring |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 83 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You already know how to build one Spring Boot application. Controllers, services, repositories, security filters — one process, one classpath, one deployable jar. Then the organization grows. Checkout wants to ship twice a week. Inventory can only release monthly. Billing has a different SLA and a different on-call rotation. Suddenly the monolith is not a technical preference; it is a release bottleneck. Someone proposes splitting the system into services. That proposal is where Spring Cloud enters the conversation — not as a fashion, as plumbing for problems that appear the moment you have more than one deployable unit.

Picture an order flow that used to be three method calls inside one JVM. After the split, `OrderService` must reach `InventoryService` and `PaymentService` over the network. On day one a junior developer hard-codes `http://inventory:8081` and `http://payment:8082` into RestTemplate. It works in Docker Compose. It fails in the second environment because ports differ. Config for database URLs is copied into twelve `application.yml` files; someone updates prod JDBC credentials in eleven of them. When payment slows down, order threads pile up waiting on HTTP, and the whole checkout path collapses. When a bug spans three services, the logs do not share a request id, so you cannot reconstruct the story. Those are not “microservices ideology” problems. Those are distributed-system chores: configuration, location, routing, resilience, and observability.

Spring Cloud is the family of projects that packages those chores on top of Spring Boot. Keep the naming straight. Spring Framework is the container and modules. Spring Boot is opinionated single-app delivery. Spring Cloud assumes you already have Boot apps and adds patterns for multi-service systems: centralized config, service discovery, API gateways, client-side load balancing, declarative HTTP clients, circuit breakers, messaging binders, and tracing hooks. You do not need every piece on day one. You need the map so you stop reinventing each piece with ad-hoc scripts.

A practical mental model helps. Think of a small commerce platform with four Boot jars: `order-service`, `inventory-service`, `payment-service`, and a future edge gateway. Each jar still looks like a normal Boot app — `@SpringBootApplication`, an embedded server, Actuator. Cloud libraries plug in as dependencies and auto-configuration. A BOM — `spring-cloud-dependencies` — pins compatible versions so Boot 3.x and Cloud 2023.x (or whatever train you are on) do not drift. That version alignment is underrated. Half of “Cloud is hard” is mismatched jars.

```java
@SpringBootApplication
public class OrderServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrderServiceApplication.class, args);
    }
}

@RestController
@RequestMapping("/orders")
class OrderController {
    private final InventoryClient inventory;
    private final PaymentClient payment;

    OrderController(InventoryClient inventory, PaymentClient payment) {
        this.inventory = inventory;
        this.payment = payment;
    }

    @PostMapping
    OrderResponse place(@RequestBody PlaceOrderRequest req) {
        inventory.reserve(req.sku(), req.qty());
        payment.charge(req.customerId(), req.amount());
        return OrderResponse.accepted(req);
    }
}
```

Read that controller as a promise, not as finished architecture. The business method still reads like domain language. The collaborators are remote. How `InventoryClient` finds a host, how it fails when inventory is down, how secrets reach this process — that is Cloud territory. Without a platform, teams fill the gap with environment variables, DNS guesses, and copy-pasted YAML. With Spring Cloud, those concerns become shared, versioned mechanisms.

Notice what Spring Cloud is not. It is not a requirement to use Netflix OSS forever. Eureka, Zuul, and Hystrix shaped early Cloud demos; modern stacks often use Spring Cloud Config, Spring Cloud Gateway, Spring Cloud LoadBalancer, OpenFeign, Resilience4j, and Micrometer Tracing — sometimes with Kubernetes service discovery instead of a Java registry. The patterns survive the library names. Config still needs a source of truth. Instances still need to be found. Traffic still needs an edge. Calls still need bulkheads. Spans still need to hop process boundaries.

A topic-specific misconception is treating “microservices with Spring” as “annotate everything `@FeignClient` and ship.” Splitting without bounded contexts just creates a distributed monolith: chatty calls, shared databases, and coupled releases. Another misconception is that Cloud replaces Boot. Every Cloud service is still a Boot app; Cloud adds remote collaboration patterns. A third is assuming you must stand up every Cloud component before the first service ships. Start with clear service boundaries and honest HTTP or messaging contracts. Add Config when YAML drift hurts. Add discovery when hosts stop being static. Add a gateway when clients should not know every internal URL.

So today we named the moment a single Boot app becomes a fleet, listed the failure modes that appear after the split, and placed Spring Cloud as the pattern kit on top of Boot rather than a replacement for it. We sketched an order service that depends on remote clients and left their wiring unresolved on purpose.

That unresolved wiring starts with a boring question that burns teams weekly: if twenty services need the same feature flags, JDBC URLs, and timeout values, where does that configuration live so it does not rot in twenty repositories?

That question is Configuration Server.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 83 (*Microservices with Spring*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
