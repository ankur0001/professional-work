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

After you accept multiple Boot services, configuration becomes a product of its own. `order-service` needs a payment base URL. `payment-service` needs a merchant key. Both need logging levels that change during an incident. If each team edits its own `application-prod.yml` in git and hopes the values stay aligned, you will eventually debug a outage caused by one service still pointing at last quarter’s host. Centralized configuration exists to stop that drift.

Spring Cloud Config Server is a Boot application whose job is to serve property sources to other Boot applications. Clients do not bake every environment value into their jar. They ask the Config Server at startup — and optionally refresh later — for a property set keyed by application name, profile, and label. The server itself usually reads from a Git repository, though you can back it with the filesystem, Vault, or other backends. Git is the common teaching path because reviews, history, and rollbacks already exist there.

Stand up the server side first in your head. You add `spring-cloud-config-server`, annotate the application with `@EnableConfigServer`, and point it at a Git URI. The repo might contain files named `order-service.yml`, `order-service-prod.yml`, `payment-service.yml`, and a shared `application.yml` for defaults. When a client named `order-service` with profile `prod` asks for config, the server composites those files in a defined order and returns a JSON (or other) property payload.

```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
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
          uri: https://git.example.com/platform/config-repo.git
          default-label: main
server:
  port: 8888
```

On the client, modern Boot (2.4+) prefers `spring.config.import` over the older bootstrap context. You declare something like `spring.config.import=optional:configserver:http://localhost:8888` and set `spring.application.name=order-service`. The Config Data API imports remote properties into the Environment early enough for the rest of auto-configuration to see them. `optional:` keeps local developer laptops from failing hard when the server is down; production often omits optional so missing config is loud.

```yaml
# order-service application.yml
spring:
  application:
    name: order-service
  config:
    import: "optional:configserver:http://config-server:8888"
  profiles:
    active: prod
```

Walk a property lookup. Order service asks for `payment.base-url`. The Environment may contain local defaults, then profile-specific local files, then Config Server property sources. Precedence rules matter: remote overrides are deliberate when you want ops to change behavior without rebuilding jars; local overrides are deliberate when a developer needs to force a value. Know which side wins in your setup, or you will chase ghosts.

Refresh is the second half of the story. Changing a Git file does not automatically rewrite every running JVM. Historically, `/actuator/refresh` or Spring Cloud Bus propagated updates to beans annotated with `@RefreshScope`. Those beans are re-created with new property values. Not every bean is refresh-safe — connection pools and thread pools need care. Many teams treat Config Server as startup-time truth and redeploy for sensitive changes. Both strategies are valid; pick one consciously.

A misconception is using Config Server as a secret dump without access control. Merchant keys in a wide-open Git repo behind an unauthenticated config endpoint are a breach waiting to happen. Encrypt secrets, restrict the server, or integrate a secret manager. Another misconception is stuffing huge binary or environment-specific infrastructure into config files until the repo becomes unreadable. Keep config boring: URLs, timeouts, feature flags, credentials references. A third is forgetting `spring.application.name`, then wondering why the server returns empty or wrong documents — the name is the primary lookup key.

So today we replaced copy-pasted YAML with a Config Server backed by Git, showed how a client imports remote property sources by application name and profile, and marked refresh as an operational choice rather than magic.

Services can now agree on configuration. They still have a different problem the moment instances scale: which host and port is the living `payment-service` right now, and how does a caller learn that without a spreadsheet of IPs?

That is Service Discovery.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 84 (*Configuration Server*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
