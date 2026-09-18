# Episode 22 — Configuration Properties

| Field | Value |
|---|---|
| Episode | 22 |
| Title | Configuration Properties |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 22 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Boot already binds dozens of `spring.*` keys into framework objects. Your product has its own settings — payment base URLs, feature flags, retry budgets — and scattering `@Value` across services ages badly.

Watch a codebase rot. One service injects `@Value("${payments.base-url}")`. Another copies the same key with a typo in the default. A third reads a timeout as a String and parses it by hand. Nothing fails at startup. Failures arrive in production when a property is missing or the wrong type. Configuration becomes tribal knowledge instead of a typed contract.

The question becomes: can we bind a prefix of the Environment into one object, validate it early, and inject that object like any other bean?

Spring Boot's `@ConfigurationProperties` is that contract. You declare a class — often a record or a simple POJO — with fields that match property names under a prefix. Boot binds relaxed names: `payments.base-url`, `payments.baseUrl`, and `PAYMENTS_BASE_URL` can map to the same field depending on source. Enable the class with `@EnableConfigurationProperties` or annotate it with `@ConfigurationProperties` plus `@Component` / `@ConfigurationPropertiesScan`. Prefer constructor binding for immutability when you can.

```java
@ConfigurationProperties(prefix = "payments")
public record PaymentsProperties(
    String baseUrl,
    Duration timeout,
    boolean resilient
) {}
```

```java
@SpringBootApplication
@EnableConfigurationProperties(PaymentsProperties.class)
public class OrdersApplication { }
```

```yaml
payments:
  base-url: https://payments.internal/api
  timeout: 2s
  resilient: true
```

Wire `PaymentsProperties` into a client. The client no longer knows about property key strings. Tests construct a `PaymentsProperties` directly. At startup, Boot converts `2s` into a `Duration`. Add `spring-boot-starter-validation` and Bean Validation annotations on the properties type, and illegal config can fail fast instead of shipping a null base URL.

```java
@Service
public class PaymentsClient {
    private final PaymentsProperties props;
    private final RestClient http;

    public PaymentsClient(PaymentsProperties props, RestClient.Builder builder) {
        this.props = props;
        this.http = builder.baseUrl(props.baseUrl()).build();
    }
}
```

Compare that to a pile of `@Value` fields. `@Value` is fine for a single one-off. `@ConfigurationProperties` wins when a feature has a cluster of related settings, needs conversion, or should be documented as a group. Boot's own `DataSourceProperties` and server properties use the same idea — your code can follow the same pattern.

The trap is treating properties classes as dumping grounds for every key in the app. Keep prefixes feature-sized: `payments`, `inventory.cache`, `orders.shipping`. Another trap is mutable setters without validation and then mutating the object at runtime until nobody knows the effective config. A third is forgetting relaxed binding rules and declaring "YAML is broken" when the field name simply did not match.

Typed properties still have to come from somewhere outside the JAR when environments differ — files, environment variables, command-line overrides, profile-specific documents.

That outside story is external configuration: precedence, profile files, and how the Environment actually layers sources.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 22 (*Configuration Properties*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
