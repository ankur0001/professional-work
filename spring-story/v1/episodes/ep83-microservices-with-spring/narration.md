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

The harbor ops monolith shipped as one fat jar for years: berth scheduling, gate release, and vessel billing lived in the same process. One deploy window. One shared database schema. One on-call phone. Then scheduling needed a Tuesday hotfix while billing was mid-tariff cutover, and the release train stalled. Splitting is no longer a conference talk — it is a release-calendar problem.

After the cut, three Boot jars stand where one did: `scheduling-service`, `billing-service`, and `gate-service`. A truck check-in that used to be three method calls becomes three network hops. A junior engineer hard-codes `http://billing:8082` into RestTemplate. It works in Compose. Staging uses different ports. Tariff YAML is copied into thirty `application.yml` files; someone updates the hazardous-goods surcharge in twenty-nine of them. When billing slows, gate threads pile up on HTTP and trucks queue at the booth. When a bug spans gateway, gate, and billing, the logs do not share a request id. Those are not ideology problems. They are distributed chores: configuration, location, routing, resilience, and observability.

Spring Cloud packages those chores on top of Spring Boot. Keep the naming straight. Spring Framework is the container and modules. Spring Boot is opinionated single-app delivery. Spring Cloud assumes Boot apps and adds multi-service patterns — centralized config, discovery, API gateways, client-side load balancing, declarative HTTP clients, circuit breakers, messaging binders, tracing hooks. You do not need every piece on day one. You need the map so you stop reinventing each piece with shell scripts.

```java
@SpringBootApplication
public class GateServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(GateServiceApplication.class, args);
    }
}

@RestController
@RequestMapping("/gates")
class GateController {
    private final BillingClient billing;
    private final GateReleaseService releases;

    GateController(BillingClient billing, GateReleaseService releases) {
        this.billing = billing;
        this.releases = releases;
    }

    @PostMapping("/{gateId}/check-ins")
    CheckInResponse checkIn(@PathVariable String gateId, @RequestBody TruckCheckIn req) {
        TariffQuote quote = billing.quote(req.containerId(), req.hazardClass());
        return releases.accept(gateId, req, quote);
    }
}
```

Read that controller as a promise, not finished architecture. The method still speaks harbor language — gate, truck, tariff quote. The collaborators are remote. How `BillingClient` finds a host, how it fails when billing is down, how tariff rules reach thirty processes — that is Cloud territory. Pin versions with the `spring-cloud-dependencies` BOM so Boot 3.x and the Cloud train stay aligned. Half of “Cloud is hard” is mismatched jars.

Spring Cloud is not a requirement to run Netflix OSS forever. Eureka, Zuul, and Hystrix shaped early demos; modern stacks often use Config Server, Gateway, LoadBalancer, OpenFeign, Resilience4j, and Micrometer Tracing — sometimes with Kubernetes discovery instead of a Java registry. The patterns survive the library names. Config still needs a source of truth. Instances still need to be found. Truckers still need one public edge. Calls still need bulkheads. Spans still need to hop process boundaries.

A misconception specific to this split is treating “microservices with Spring” as “annotate everything `@FeignClient` and ship.” Cutting modules without bounded contexts creates a distributed monolith: chatty gate↔billing calls, a shared berth table, and coupled releases. Another is believing Cloud replaces Boot — every Cloud service is still a Boot app. A third is standing up every Cloud component before the first harbor service ships. Start with clear boundaries and honest HTTP or messaging contracts. Add Config when tariff YAML drift hurts. Add discovery when hosts stop being static. Add a gateway when truckers should not know every internal URL.

We named the moment one harbor jar becomes a fleet, listed the failure modes after the split, and placed Spring Cloud as the pattern kit on top of Boot. The unresolved wiring starts with a boring operational burn: if thirty services need the same tariff rules and timeout values, where does that configuration live so it does not rot in thirty repositories?

Centralized configuration is the next pressure.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 83 (*Microservices with Spring*).
