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

Profiles selected the Stripe bean for production. That bean still needs an API key, a base URL, and a timeout — and those values do not all live in one file.

Here is the outage version of the problem. The key is in `application.properties` for developers. Ops exports `STRIPE_API_KEY` in the container. A deploy script also passes `--stripe.api-key=` on the command line during a rollback test. Different machines silently prefer different sources. Or a `@Value("${stripe.api-key}")` fails at startup in CI because nobody documented which source is required. Teams invent `ConfigLoader` utility classes that read files in custom order, and those utilities disagree between services.

Without a unified property abstraction, configuration precedence becomes tribal knowledge. The engineer asks: where does Spring resolve property keys, and how do I read them without hard-coding source order in every class?

Spring's `Environment` is that abstraction. It sits on the `ApplicationContext` and models active profiles plus a hierarchy of `PropertySource`s — servlet parameters, system properties, environment variables, application property files, and more depending on the stack. Lookup walks the property sources in precedence order and returns the first hit. You inject `Environment` or use `@Value` / `@ConfigurationProperties` which read through it. Profiles and properties work together: profiles shape which beans and which document sets load; `Environment` answers `getProperty("stripe.api-key")`.

```java
@Configuration
public class StripeConfig {

    @Bean
    @Profile("prod")
    PaymentClient stripePaymentClient(Environment env) {
        String key = env.getRequiredProperty("stripe.api-key");
        String baseUrl = env.getProperty("stripe.base-url", "https://api.stripe.com");
        int timeoutMs = env.getProperty("stripe.timeout-ms", Integer.class, 5000);
        return new StripePaymentClient(key, baseUrl, timeoutMs);
    }
}

@Service
public class FeatureGate {
    private final boolean rushShipping;

    public FeatureGate(
            @Value("${features.rush-shipping:false}") boolean rushShipping) {
        this.rushShipping = rushShipping;
    }

    public boolean rushShippingEnabled() {
        return rushShipping;
    }
}
```

When the context refreshes under the `prod` profile, `getRequiredProperty` fails fast if the key is missing — better than a null key at the first charge. `getProperty` with defaults fills optional settings. `@Value` pulls through the same `Environment`, including the `:false` default for a feature flag. Change an OS environment variable that Spring relaxed-binds to `stripe.api-key`, and the bean sees the new value on next startup without code edits. Precedence means a command-line property can override a file for a one-off experiment — powerful when intentional, confusing when accidental.

Learn to inspect which sources are present when values look wrong. In Boot you will later gain `application.yml`, profile-specific documents, and outside-the-jar overrides. The mental model starts here: one `Environment`, many property sources, deterministic precedence.

A misconception unique to `Environment` is reading `System.getenv` directly inside services "because it is simpler," which bypasses precedence, testability, and profile-specific documents. Another is assuming `@Value` is resolved repeatedly on every access for dynamic refresh — standard `@Value` injection is fixed at bean creation unless you add refresh machinery.

Look at the path we traveled through Phase One. You can modularize Spring, invert control, inject dependencies, navigate factories and contexts, define beans, scope them, hook lifecycles, choose configuration styles, scan components, disambiguate injection annotations, and publish profile-aware beans backed by `Environment`. And yet a team can still lose days aligning versions, wiring a datasource, and embedding a server before the first endpoint. That remaining ceremony is exactly why Spring Boot exists — and it is the door into Phase Two.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 16 (*Environment*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
