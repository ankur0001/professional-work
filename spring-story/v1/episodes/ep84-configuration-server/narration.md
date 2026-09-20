# Episode 84 — Configuration Server

| Field | Value |
|---|---|
| Episode | 84 |
| Title | Configuration Server |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 84 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Thirty harbor services — gate pods, billing replicas, scheduling workers, tide adapters — each ship with an `application.yml`. The hazardous-goods surcharge changes on Monday. By Wednesday, nineteen replicas still quote the old rate. That drift is not a YAML taste problem. It is a source-of-truth problem.

Spring Cloud Config Server is a Boot app that serves property sources from a backend — usually Git — keyed by application name, profile, and optional label (branch or tag). Clients bootstrap, ask the server for their properties, and merge them over local defaults. One Git commit updates the fleet’s view of tariff rules when clients refresh or restart.

```yaml
# config-repo/billing-service-prod.yml
harbor:
  tariff:
    base-per-teu: 42.50
    hazardous-surcharge: 18.00
    currency: USD
management:
  endpoints:
    web:
      exposure:
        include: health,info,refresh
```

```java
@SpringBootApplication
@EnableConfigServer
public class HarborConfigServer {
    public static void main(String[] args) {
        SpringApplication.run(HarborConfigServer.class, args);
    }
}
```

```yaml
# config-server application.yml
spring:
  cloud:
    config:
      server:
        git:
          uri: https://git.harbor.example/config-repo.git
          default-label: main
server:
  port: 8888
```

On the client, import the config and name the application so the server can find `billing-service-prod.yml`:

```yaml
# billing-service
spring:
  application:
    name: billing-service
  config:
    import: "optional:configserver:http://config-server:8888"
  profiles:
    active: prod
```

```java
@ConfigurationProperties(prefix = "harbor.tariff")
public record TariffProperties(BigDecimal basePerTeu,
                               BigDecimal hazardousSurcharge,
                               String currency) {}
```

Walk the path. Billing starts, resolves `spring.application.name` and the active profile, GETs the Config Server, receives property sources, and binds `TariffProperties`. Gate and scheduling do the same for their own files in the same repo. Operators change `hazardous-surcharge` in Git; a controlled refresh or rolling restart picks it up. Secrets still belong in a secret store or sealed files — Config Server can integrate, but dumping passwords into a public Git history is not “centralized,” it is a leak.

Refresh is optional and operational. `@RefreshScope` beans rebuild when `/actuator/refresh` fires (or via a bus). Prefer restart-on-config for rare tariff cuts if your platform already rolls pods safely. Live refresh without discipline produces “half the fleet on old rules” during the window.

A misconception is treating Config Server as a replacement for environment-specific secrets management — it is a property distribution mechanism, not a vault. Another is stuffing every service’s entire YAML into one mega-file so nobody can review a billing-only change. A third is marking `config.import` as required in laptops that cannot reach the server, then wondering why local boot fails — `optional:configserver:` exists for a reason.

Tariff rules now have a home. The next failure mode appears the moment gate must call billing and the host list is no longer a Compose alias you typed by hand.

Services need a way to find each other by name.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 84 (*Configuration Server*).
