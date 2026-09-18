# Episode 85 — Service Discovery

| Field | Value |
|---|---|
| Episode | 85 |
| Title | Service Discovery |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 85 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Config Server can tell `order-service` that payment lives at a logical name. It cannot tell you which of three payment pods is healthy at 14:07 after a rolling deploy. Hard-coded hosts die the moment you scale horizontally. Service discovery is the registry pattern: instances register themselves, clients look up instances by service id, and the registry tracks heartbeats so dead nodes disappear.

In the Spring Cloud teaching stack, Netflix Eureka is the classic registry. You run a Eureka Server — another Boot app with `@EnableEurekaServer` — and each microservice becomes a Eureka Client that registers under `spring.application.name`. When order wants payment, it does not need the IP list in YAML. It asks Eureka for instances named `payment-service`, then picks one. Kubernetes DNS can replace Eureka in many production platforms; the Spring programming model still benefits from understanding discovery as a first-class idea, because gateways and load balancers plug into the same abstraction.

```java
@SpringBootApplication
@EnableEurekaServer
public class DiscoveryServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(DiscoveryServerApplication.class, args);
    }
}
```

```yaml
# eureka-server
server:
  port: 8761
eureka:
  client:
    register-with-eureka: false
    fetch-registry: false
```

The server often disables registering itself. Clients do the opposite: they register and fetch.

```yaml
# payment-service client
spring:
  application:
    name: payment-service
eureka:
  client:
    service-url:
      defaultZone: http://discovery:8761/eureka/
  instance:
    prefer-ip-address: true
```

Startup sequence matters. Payment service boots, contacts Eureka, sends instance metadata — host, port, health URL, maybe metadata maps for canaries. Eureka stores the lease. Periodically the client renews. If renewals stop, the instance eventually expires from the registry. Order service, also a client, periodically downloads the registry cache so lookups are local and fast. That cache is why discovery survives brief registry blips, and also why you can briefly see stale instances after a crash — TTLs and self-preservation mode are operational details worth reading before you page people.

How does application code use the registry? Rarely by calling Eureka APIs directly. Higher-level clients resolve a logical service id. RestTemplate with a `@LoadBalanced` bean turns `http://payment-service/charges` into a concrete instance URL. WebClient and OpenFeign do the same through Spring Cloud LoadBalancer. The discovery client is the source of candidates; the load balancer chooses among them.

```java
@Bean
@LoadBalanced
RestTemplate restTemplate() {
    return new RestTemplate();
}

// somewhere in order-service
PaymentResult result = restTemplate.postForObject(
        "http://payment-service/charges",
        chargeRequest,
        PaymentResult.class);
```

That `payment-service` host name is not DNS in the traditional sense when Eureka is in play. The load balancer interceptor recognizes it as a service id, asks discovery for instances, picks one, and rewrites the request. In Kubernetes-native setups, the same logical name might be a ClusterIP Service; Spring Cloud Kubernetes Discovery maps similarly so code can stay stable across platforms.

Misconceptions cluster here. One is treating the registry as a deployment database and manually editing instance lists — discovery only works if registration is automatic and health-driven. Another is pointing every environment at one shared Eureka and then wondering why staging traffic finds prod instances; isolate registries per environment. A third is ignoring health checks: an instance that is “up” for Eureka but failing readiness will still receive traffic until you align Actuator health with registry semantics.

Today we made instance location dynamic: a registry holds live service catalogs, clients register and fetch, and callers address logical names instead of brittle host lists. Config told services what to be; discovery tells them where peers are.

Clients still should not call every internal service URL from browsers and mobile apps. You need a single front door that routes `/orders/**` and `/payments/**` to the right discovered backends, terminates cross-cutting concerns once, and hides the mesh of instances.

That front door is the API Gateway.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 85 (*Service Discovery*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
