# Episode 16 — Environment

| Field | Value |
|---|---|
| Episode | 16 |
| Title | Environment |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 16 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Ops starts the tolling roadside service with:

```bash
java -jar tolling.jar --tolling.express-lane.enabled=false \
  --spring.datasource.url=jdbc:postgresql://toll-db/prod
```

The process still opens express-lane pricing. A ConfigMap file says `true`. An environment variable says `true`. The CLI says `false`. Nobody can explain precedence without opening Spring's property source order charts. Feature flags and DB URLs for tolling are supposed to resolve from env, files, and CLI through one abstraction: `Environment`. When that abstraction is ignored — or when code reads `System.getenv` in one place and `@Value` in another — operators lose the kill switch.

`Environment` models two ideas together: active profiles, and a hierarchy of `PropertySource` instances. When you call `env.getProperty("tolling.express-lane.enabled")`, Spring walks property sources in precedence order and returns the first hit. Boot adds several sources for you — command-line args typically beat environment variables, which beat application YAML inside the jar, and so on — but the interface you code against stays `Environment`, or `@Value` / `@ConfigurationProperties` that read through it. Profiles decide which documents join the stack; Environment is what answers after the stack is built.

```java
@Service
public class LanePricingService {
    private final boolean expressEnabled;
    private final String datasourceUrl;

    public LanePricingService(Environment env) {
        this.expressEnabled = env.getProperty(
            "tolling.express-lane.enabled", Boolean.class, false);
        this.datasourceUrl = env.getRequiredProperty("spring.datasource.url");
    }

    public Money price(Vehicle vehicle, Plaza plaza) {
        Money base = plaza.tariff().forClass(vehicle.axleClass());
        if (expressEnabled && vehicle.hasTransponder()) {
            return base.discounted(plaza.expressDiscount());
        }
        return base;
    }
}
```

```yaml
# application.yml (lowest among these examples)
tolling:
  express-lane:
    enabled: true
```

Walk the service. The constructor captures resolved values once at bean creation — a snapshot suitable for flags that should not flip mid-request without a refresh story. `getProperty(key, Boolean.class, false)` converts the string through Spring's conversion service and defaults to `false` if the key is absent everywhere. `getRequiredProperty` throws `IllegalStateException` if the datasource URL is missing — fail startup rather than connect to a phantom default. `price` uses the captured boolean; it never re-queries Environment per vehicle, so a later change to a mounted file would not be visible until the bean is rebuilt.

Runtime for that CLI launch. Boot (or a manually prepared context) builds the Environment *before* refreshing most application beans. Command-line property source is consulted first for `tolling.express-lane.enabled` → `false`. The YAML `true` and any ConfigMap-derived env var never win for that key. `LanePricingService` constructs with false; express discounts stay off. Change only the ConfigMap, omit the CLI flag, restart, and the same code path yields true without recompilation. If someone adds `@Value("${tolling.express-lane.enabled}")` on another bean while a third class calls `Boolean.parseBoolean(System.getenv("TOLLING_EXPRESS_LANE_ENABLED"))`, you can get split decisions inside one process — the failure mode that made ops distrust the kill switch.

Failure mode symptoms: CLI says `false`, plaza receipts still show express discounts. Checklist: confirm the property key spelling matches exactly (relaxed binding helps for env vars like `TOLLING_EXPRESS_LANE_ENABLED`, but only when read *through* Environment); confirm the bean actually injected Environment/`@Value` rather than a static getenv; dump high-precedence sources via a secured actuator `env` endpoint and look for an unexpected winner; confirm the flag was not read only into a `@Bean` that was cached before you thought you changed config. Another symptom: `getRequiredProperty` fails at startup naming `spring.datasource.url` even though `DATABASE_URL` is set — wrong key, or a custom property source never added.

Trade-offs. Reading Environment in constructors is simple and testable with a `MockEnvironment`; it freezes values at creation. Re-querying Environment per call picks up refreshed property sources if you adopt a refresh mechanism, at the cost of scattered lookups and harder reasoning. `@ConfigurationProperties` groups keys with validation — usually better than many raw `getProperty` calls — but still sits on the same precedence stack. Bypassing Environment with `System.getenv` or `System.getProperty` is occasionally needed for code outside Spring; inside beans it is how precedence bugs are born.

Misconception unique to Environment: "`System.getenv` and `Environment.getProperty` always see the same map." Environment includes env vars as one source, but also JVM system properties, config files, random value sources, and command-line args, with precedence. Reading `System.getenv` bypasses that merge and can disagree with what Spring injected elsewhere.

Tolling pricing finally respects the CLI kill switch. The remaining mystery is sharper: which exact property sources sit in the chain, who adds them, and how Boot's opinionated startup sequence wires that chain before your first bean constructor runs — the reason teams reach for Spring Boot instead of assembling contexts by hand.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 16 (*Environment*).
