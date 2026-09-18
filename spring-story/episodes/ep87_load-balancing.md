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

Gateway said `lb://order-service`. Discovery returned three instance records. Something still has to choose among them for this particular request. That something is load balancing. In cloud demos you often hear “Ribbon.” In current Spring Cloud, the default client-side balancer is Spring Cloud LoadBalancer. Same job, maintained library: given a service id, pick an instance, and give callers a concrete host and port.

There are two classic places load balancing can live. Server-side: a reverse proxy or cloud load balancer spreads traffic across a pool the client never sees. Client-side: each caller downloads the instance list and picks locally. Spring Cloud’s `lb://` and `@LoadBalanced` RestTemplate/WebClient paths are client-side. They shine when services talk to each other inside the mesh without forcing every hop back through a central proxy. You can still put a server-side balancer in front of the gateway for public traffic; the patterns stack.

```java
@Configuration
public class ClientsConfig {

    @Bean
    @LoadBalanced
    WebClient.Builder loadBalancedWebClientBuilder() {
        return WebClient.builder();
    }
}

@Service
public class InventoryGateway {
    private final WebClient client;

    public InventoryGateway(WebClient.Builder builder) {
        this.client = builder.baseUrl("http://inventory-service").build();
    }

    public StockView stock(String sku) {
        return client.get()
                .uri("/stock/{sku}", sku)
                .retrieve()
                .bodyToMono(StockView.class)
                .block();
    }
}
```

The `@LoadBalanced` builder registers an exchange filter that intercepts the logical host `inventory-service`, asks `ReactiveLoadBalancer` (or the blocking equivalent) for a choice, and substitutes the real URI. Round-robin is the usual default mental model: request one goes to instance A, request two to B, request three to C, then back to A. You can plug in different `ReactorLoadBalancer` implementations — random, weighted, zone-aware — when topology demands it.

Failure behavior is part of balancing, not an afterthought. If instance B starts returning connection resets, a naive balancer keeps hitting B until discovery removes it. Spring Cloud LoadBalancer can integrate health checks and caching so bad instances drop out faster. Still, brief windows of bad routing happen; callers need timeouts and retries sized for that reality. Balancing spreads load; it does not invent resilience by itself.

Compare with gateway routing. The gateway uses the same load-balancer abstraction when it sees `lb://`. A service-to-service WebClient uses it too. That consistency is the point of the Cloud abstractions: one service catalog, one selection mechanism, many entry points. Configuration lives under `spring.cloud.loadbalancer` — cache TTLs, health check intervals, configurations per service id when one dependency needs different rules.

```yaml
spring:
  cloud:
    loadbalancer:
      inventory-service:
        health-check:
          initial-delay: 5s
          interval: 10s
```

Zone preference is the other dial teams reach for in multi-AZ setups. Prefer same-zone instances to cut latency, fall back cross-zone when the local pool is empty. That only works if instance metadata carries zone information from the platform or Eureka metadata maps. Without metadata, every instance looks equal and round-robin is honest about its ignorance.

A misconception is assuming client-side balancing replaces Kubernetes Services. Inside Kubernetes, a ClusterIP already load-balances at the platform layer; adding another client balancer can be redundant or complementary depending on whether you use Spring Cloud Kubernetes discovery or plain DNS. Know your platform. Another misconception is sticky sessions by default — most REST APIs should be stateless so any instance can serve any request. If you need affinity, configure it deliberately and accept the operational cost. A third is forgetting that `@LoadBalanced` only affects clients created from that annotated builder; a plain `WebClient.create("http://inventory-service")` will try to resolve the name as real DNS and fail in Eureka-only setups.

Today we made instance selection explicit: Spring Cloud LoadBalancer turns a service id into a chosen instance for RestTemplate, WebClient, and Gateway, with algorithms and health-aware caching as the knobs.

Calling remote APIs with WebClient builders still means writing HTTP details in Java. Teams often want something thinner: an interface that looks like a local dependency, annotated with paths and verbs, while the framework builds the HTTP call — preferably still load-balanced by service id.

That declarative style is Feign Client.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 87 (*Load Balancing*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
