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

Gate needs billing. At 06:00 there are three billing pods. At 06:12 one dies during a deploy. At 06:15 a fourth starts on a different node. If gate still dials `http://10.0.4.22:8080`, check-ins fail while healthy instances sit idle. Discovery answers a simple question: given the logical name `billing-service`, which live instances exist right now?

A registry holds the catalog. Each instance registers on startup with host, port, health URL, and metadata. Clients — or a platform DNS layer — query the catalog and choose a target. In classic Spring Cloud demos that registry is Eureka. On Kubernetes, CoreDNS and Endpoints often play the same role; Spring Cloud Kubernetes can adapt the programming model. The pattern matters more than the brand: register, heartbeat, fetch, call by name.

```yaml
# billing-service
spring:
  application:
    name: billing-service
eureka:
  client:
    service-url:
      defaultZone: http://eureka:8761/eureka/
  instance:
    prefer-ip-address: true
    metadata-map:
      zone: quay-a
    lease-renewal-interval-in-seconds: 10
    lease-expiration-duration-in-seconds: 30
```

```yaml
# gate-service
spring:
  application:
    name: gate-service
eureka:
  client:
    service-url:
      defaultZone: http://eureka:8761/eureka/
    registry-fetch-interval-seconds: 5
```

```java
@RestController
class GateBillingProbe {
    private final DiscoveryClient discovery;

    GateBillingProbe(DiscoveryClient discovery) {
        this.discovery = discovery;
    }

    @GetMapping("/debug/billing-instances")
    List<String> billingInstances() {
        return discovery.getInstances("billing-service").stream()
                .map(si -> si.getHost() + ":" + si.getPort()
                        + " zone=" + si.getMetadata().getOrDefault("zone", "?"))
                .toList();
    }
}
```

At runtime, billing heartbeats. Eureka (or your platform) marks it UP. Gate’s `DiscoveryClient.getInstances("billing-service")` returns the three healthy URIs. Higher-level clients — load-balanced WebClient, Feign, Gateway `lb://` URIs — consume that list so application code never embeds pod IPs. Self-preservation and lease timeouts matter: a flapping network should not empty the registry and black-hole the quay, but a dead pod that stops renewing must leave the catalog within tens of seconds or gate keeps selecting a corpse.

Walk a deploy failure. Billing pod B2 stops heartbeats at 06:12. Until the lease expires, gate may still receive B2 in the instance list and open sockets that time out. Symptom at the booth: intermittent 504s on check-in while two other pods are fine. Your debug probe still shows three rows until expiry; after expiry it shows two, then three again when B4 registers. That timeline is why `registry-fetch-interval-seconds` and lease settings are operational knobs, not decoration. Too aggressive and you thrash; too slow and you serve dead IPs through a whole truck queue.

Health integration is not optional decoration. If billing’s `/actuator/health` goes DOWN because Postgres is unreachable, the registry should stop handing that instance to gate. Otherwise discovery lies and load balancers keep selecting a dying pod. Prefer-IP versus hostname, zone metadata, and secure-port flags show up the first time TLS or multi-AZ routing is real. Zone `quay-a` on the instance is how later load balancers prefer local billing when cross-quay latency hurts.

Trade-offs: a Java registry (Eureka) gives Spring-native metadata and demos that teach the model; Kubernetes DNS gives fewer moving parts if every service already lives in the cluster and you accept platform-shaped discovery. Mixing both without a clear owner — some Feign clients on DNS, some on Eureka — produces “works in staging, wrong host in prod” nights. Pick one source of truth for `billing-service` and make gate’s clients use it.

A misconception is hard-coding hostnames “temporarily” beside discovery and then shipping both paths — callers diverge and on-call cannot tell which URL is authoritative. Another is assuming discovery replaces load balancing; discovery gives you candidates, balancing chooses among them. A third is registering every batch job and one-off tool into the same registry namespace until `billing-service` returns noise.

Gate can now ask for `billing-service` by name. Truckers on the public internet still should not open a VPN to every internal pod. Something at the edge must accept one hostname and route inward.

That edge is the API gateway.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 85 (*Service Discovery*).
