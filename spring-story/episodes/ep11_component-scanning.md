# Episode 11 — Component Scanning

| Field | Value |
|---|---|
| Episode | 11 |
| Title | Component Scanning |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 11 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Java configuration can declare beans one method at a time. That does not scale when you have eighty services in `com.acme.shop`.

A team adds `PricingService` with `@Service`, starts the app, and gets `NoSuchBeanDefinitionException` at the controller. The class is correct. The package is wrong relative to the scan base. Or the opposite: a scan root set at `com.acme` pulls in test helpers, legacy `package-info` experiments, and a `@Component` sitting in a shared library that was never meant for this process. Startup slows. Mysterious beans appear. Someone disables scanning globally and goes back to hand-registering everything.

Without disciplined discovery, annotation configuration either misses beans or over-includes them. The engineer asks: how does Spring find annotated classes and turn them into bean definitions automatically?

Component scanning is that discovery. You declare base packages — via `@ComponentScan`, `@SpringBootApplication`'s default package, or XML `context:component-scan`. Spring indexes those packages for stereotypes: `@Component` and its specializations `@Service`, `@Repository`, `@Controller`, and others. Each match becomes a bean definition. Filters can include or exclude by annotation, regex, or assignable type when the default is too broad.

```java
@Configuration
@ComponentScan(
        basePackages = "com.acme.shop",
        excludeFilters = @ComponentScan.Filter(
                type = FilterType.ASSIGNABLE_TYPE,
                classes = LegacyCouponHack.class
        )
)
public class ShopConfig { }

@Service
public class PricingService {
    private final TaxCalculator tax;

    public PricingService(TaxCalculator tax) {
        this.tax = tax;
    }

    public Money price(Cart cart) {
        return tax.apply(cart.subtotal());
    }
}
```

At refresh, the scanner walks `com.acme.shop`, finds `PricingService`, registers a definition named by default `pricingService`, and later constructs it with a `TaxCalculator` bean found the same way. `LegacyCouponHack` is skipped by the exclude filter even if it carries `@Component`. Miss the base package by one segment — put `PricingService` in `com.acme.pricing` while scanning only `com.acme.shop` — and the definition never appears. Scanning is not classpath magic; it is bounded discovery.

Boot users often forget that `@SpringBootApplication` already implies a scan starting at the application's package. Placing the main class in `com.acme` and services in `com.acme.shop` works. Placing the main class in `com.acme.app` and services in `com.acme.shop` does not, unless you widen `@ComponentScan`. That single packaging decision explains a shocking number of empty contexts.

A scanning-specific misconception is that every class under the base package becomes a bean. Only stereotype-annotated types (or types matching custom filters) do. Another is scanning the entire company root "just in case," which couples unrelated modules and creates duplicate bean name clashes across libraries.

Once scanning registers dozens of candidates, injection annotations start to matter more — because `@Autowired`, `@Inject`, and `@Resource` do not resolve ambiguity the same way. Choosing among them is the next sharp edge.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 11 (*Component Scanning*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
