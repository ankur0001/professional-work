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

Before:

```java
public RateCard(
        @Value("${freight.rates.base-per-kg}") BigDecimal basePerKg,
        @Value("${freight.rates.fuel-pct}") double fuelPct,
        @Value("${freight.rates.min-charge}") BigDecimal minCharge,
        @Value("${freight.rates.currency}") String currency) { ... }
```

After:

```java
@ConfigurationProperties(prefix = "freight.rates")
public record FreightRatesProperties(
        BigDecimal basePerKg,
        double fuelPct,
        BigDecimal minCharge,
        String currency) {}
```

The freight-rate service had fourteen `@Value` injections across three classes, three of them misspelled in YAML with silent defaults. Typed `FreightRatesProperties` binding turns a prefix into one object, validates it, and fails startup when required fields are missing — if you enable that validation. Scattered `@Value` strings drift; a single properties type is a contract with ops.

`@ConfigurationProperties` binds Environment properties to a structured Java type. Enable with `@EnableConfigurationProperties(FreightRatesProperties.class)` or `@ConfigurationPropertiesScan`, and register the type as a bean (`@Component` or via `@EnableConfigurationProperties`). Boot's relaxed binding maps `freight.rates.base-per-kg`, `FREIGHT_RATES_BASE_PER_KG`, and `freight.rates.basePerKg` to the same record component. That relaxation is why env vars in Kubernetes and keys in YAML can disagree in punctuation yet agree in meaning.

```yaml
freight:
  rates:
    base-per-kg: 1.25
    fuel-pct: 0.12
    min-charge: 15.00
    currency: USD
```

```java
@Service
public class RateCardService {
    private final FreightRatesProperties rates;

    public RateCardService(FreightRatesProperties rates) {
        this.rates = rates;
    }

    public Money quote(Weight weight) {
        Money raw = Money.of(rates.basePerKg().multiply(weight.kg()), rates.currency());
        Money withFuel = raw.plusPercent(rates.fuelPct());
        return Money.max(withFuel, Money.of(rates.minCharge(), rates.currency()));
    }
}
```

Walk the after side. `prefix = "freight.rates"` scopes binding to that subtree — unrelated `freight.routing.*` keys stay out. Record components declare the shape; Boot binds by constructor for records. `RateCardService` depends on one collaborator instead of four `@Value` parameters. `quote` reads `basePerKg()`, applies fuel, enforces `minCharge` — business math stays readable because configuration access is not interleaved with `@Value` noise.

Runtime during refresh. A binder / `ConfigurationPropertiesBindingPostProcessor` path creates or populates the properties bean from the Environment. Conversion services turn YAML strings into `BigDecimal` and `double`. If you annotate the type with `@Validated` and place `@NotNull` / `@Positive` on components, a `BindException` / constraint violation fails the context before traffic — misspelled `base-per-kilo` leaves `basePerKg` null and startup dies instead of quoting with zero. Without validation, a missing key may leave null and fail later inside `quote` with a `NullPointerException` on the first request — worse. `@Value` still works for true one-offs; properties classes win for groups that evolve together and for IDE metadata via `spring-boot-configuration-processor` (optional dependency that generates hints).

Failure mode from the fourteen-`@Value` era: YAML key `freight.rates.fuel-percent` while code asks `fuel-pct`. `@Value` with a default silently uses the default; quotes undercharge fuel for weeks. Symptom: finance reconciles against a spreadsheet and finds a constant undercharge equal to the missing surcharge. With `@ConfigurationProperties` + validation on `fuelPct`, the bad key leaves the field unset/invalid and refresh fails in CI. Another failure: forgetting to register the properties type as a bean — `RateCardService` cannot autowire `FreightRatesProperties`, startup `NoSuchBeanDefinitionException`. Fix: `@EnableConfigurationProperties` or component-scan the type.

Trade-offs. Properties classes add a type and a registration line; they remove stringly-typed sprawl and enable validation and documentation. Mutable JavaBean-style properties with setters are easy for binding and awkward for immutability; records/`@ConstructorBinding` favor immutability and slightly stricter Boot version awareness. Nested prefixes (`freight.rates.lanes[0].from`) model lists and maps well — overusing deep nests makes YAML harder for humans than flat keys with clear names.

Relaxed binding deserves one concrete freight walkthrough. Environment may expose `FREIGHT_RATES_BASE_PER_KG=1.40` from a Kubernetes Secret while `application.yml` still says `base-per-kg: 1.25`. The binder normalizes both to the `basePerKg` component; the env var wins by precedence. `@Value("${freight.rates.base-per-kg}")` also benefits from relaxed binding for env vars, but fourteen separate `@Value` sites still cannot validate the group as one object or generate a single metadata file for IDE completion. That is why the freight team moved: not because `@Value` is illegal, but because the *set* of rates is one configuration surface.

Misconception unique to configuration properties: "Immutable `@ConfigurationProperties` records cannot work because Boot needs setters." Boot binds constructor parameters of records and constructor-binding types. Setters are one style, not the only style.

Rates are typed and validated in one place. Ops still needs to change those values in Kubernetes without rebuilding the JAR — ConfigMaps, Secrets, and override order — the external configuration story that sits on top of the same binder.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 22 (*Configuration Properties*).
