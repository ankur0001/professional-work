# Episode 87 — Load Balancing

| Field | Value |
|---|---|
| Episode | 87 |
| Title | Load Balancing |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 87 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Discovery returns three billing pods. Gate still has to pick one for this quote. Round-robin across healthy instances is the boring, correct default. Sticky routing to a dying pod is the expensive mistake. Spring Cloud LoadBalancer sits between the logical name `billing-service` and the concrete URI.

Wire a load-balanced WebClient (or RestTemplate) so the hostname in the URL is a service id, not a DNS A record you own:

```java
@Configuration
class GateClientsConfig {

    @Bean
    @LoadBalanced
    WebClient.Builder loadBalancedWebClientBuilder() {
        return WebClient.builder();
    }

    @Bean
    WebClient billingWebClient(WebClient.Builder loadBalancedWebClientBuilder) {
        return loadBalancedWebClientBuilder.baseUrl("http://billing-service").build();
    }
}

@Service
class GateTariffClient {
    private final WebClient billing;

    GateTariffClient(WebClient billingWebClient) {
        this.billing = billingWebClient;
    }

    public TariffQuote quote(String containerId, String hazardClass) {
        return billing.get()
                .uri("/tariffs/quote?containerId={c}&hazardClass={h}", containerId, hazardClass)
                .retrieve()
                .bodyToMono(TariffQuote.class)
                .block(); // illustrative; prefer non-blocking if the stack is reactive
    }
}
```

```yaml
spring:
  cloud:
    loadbalancer:
      billing-service:
        configuration:
          spring.cloud.loadbalancer.configurations: health-check
      health-check:
        path:
          billing-service: /actuator/health
        interval: 10s
```

The `@LoadBalanced` builder registers a filter that intercepts host `billing-service`, asks the load balancer for an instance, and rewrites the request to `http://10.0.8.11:8080/...`. Next call may land on `10.0.8.12`. Health-aware configurations skip instances that fail actuator checks. Feign clients with a service `name` ride the same mechanism — declarative clients and load balancing compose.

Walk a bad morning. Pod B1’s health flips DOWN because its Hikari pool is exhausted. Without health-check configuration, round-robin still sends one third of quotes to B1; gate sees intermittent timeouts while B2 and B3 are fine. With health-check enabled, B1 drops from the usable set until it recovers. Symptom shift: error rate collapses to the pods still marked UP. If your debug logs show the same IP for every call after a sticky-session experiment, you have reintroduced affinity — fine for rare sticky needs, wrong for a stateless tariff quote.

Inside Kubernetes, a ClusterIP already balances at the platform layer. Adding Spring Cloud LoadBalancer can be redundant or complementary depending on whether you use Spring Cloud Kubernetes discovery or plain DNS. Know your platform before stacking balancers. Two layers both retrying can amplify a partial outage into a retry storm. Zone preference and weighted instances matter when quay-A and quay-B have different latency to billing’s database — prefer same-zone instances when metadata carries `zone`, and accept cross-zone only when local capacity is gone.

Trade-offs: client-side balancing gives the caller control and rich instance metadata; platform balancing is simpler ops when every consumer is inside the mesh. Weighted response-time policies help when one billing pod shares a noisy neighbor, but they need good metrics or they thrash. Caching the instance list reduces registry chatter; stale cache after a scale-down is the failure mode you watch with short TTLs and health probes.

Debug with intent. Log the chosen instance id on quote failures (low cardinality — pod name, not URL with query strings). If every error shares one pod id, drain it. If errors spray evenly, the problem is billing-wide, not balancing. Retry policies on the client must not silently pin forever to a bad instance; combine short retries with removal of failing instances from the usable set when your load-balancer implementation supports it.

A misconception is assuming client-side balancing replaces platform Services everywhere — sometimes DNS is enough. Another is enabling session affinity by default on a stateless gate API. A third is creating a plain `WebClient.create("http://billing-service")` without `@LoadBalanced` and watching it fail DNS lookup in Eureka-only setups — the hostname is a service id only when the load-balancer filter is present.

Selecting an instance still leaves you writing HTTP verbs, paths, and DTO decoding by hand. Teams that call billing from many gate classes want a thinner surface: a Java interface that looks like a local collaborator.

Declarative HTTP clients — OpenFeign — are that surface.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 87 (*Load Balancing*).
