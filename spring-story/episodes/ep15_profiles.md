# Episode 15 — Profiles

| Field | Value |
|---|---|
| Episode | 15 |
| Title | Profiles |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 15 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`@Bean` methods made it easy to publish a payment client. They also made it easy to publish the wrong payment client in the wrong environment.

A common incident: local development uses `FakePaymentClient` that records charges in memory. Someone forgets to gate it. The production JAR still scans that `@Primary` fake, or both fake and Stripe beans load and ambiguity crashes boot — if you are lucky. If you are unlucky, the fake wins and real orders never charge. Another team copies `application.properties` and uses `if (env.equals("prod"))` inside a `@Bean` method. It works until a staging hostname does not match the string table and silently selects the local branch.

What goes wrong is environment-specific wiring expressed as ad-hoc conditionals instead of a first-class container feature. The engineer asks: how can one codebase activate different beans for local, test, and production without scattering `if` statements?

Spring profiles answer that. A profile is a named group of definitions. Mark a `@Configuration`, `@Component`, or `@Bean` method with `@Profile("prod")` or `@Profile("!prod")`. Activate profiles with `spring.profiles.active`, environment variables, JVM flags, or programmatically on the context. Only definitions matching the active profiles — plus beans with no profile restriction — register. The same binary ships; the active profile set changes the object graph.

```java
@Configuration
public class PaymentClientsConfig {

    @Bean
    @Profile("local")
    PaymentClient fakePaymentClient() {
        return new FakePaymentClient();
    }

    @Bean
    @Profile("prod")
    PaymentClient stripePaymentClient(Environment env) {
        return new StripePaymentClient(env.getRequiredProperty("stripe.api-key"));
    }
}

@Service
public class CheckoutService {
    private final PaymentClient payments;

    public CheckoutService(PaymentClient payments) {
        this.payments = payments;
    }

    public Receipt checkout(Cart cart) {
        return Receipt.of(payments.charge(cart.total()));
    }
}
```

Run with `spring.profiles.active=local` and the context registers `fakePaymentClient` only. `CheckoutService` injects the fake. Run with `prod` and Stripe is the sole `PaymentClient`. Activate neither and injection fails — which is often what you want, rather than a silent default to fake. Profiles also stack: `spring.profiles.active=prod,eu-west` can combine environment and region-specific beans when you design definitions that way.

Use profiles for beans and configuration classes that truly differ by environment: stubs versus real gateways, in-memory stores versus clustered caches. Prefer property values for simple scalars like URLs when the bean type stays the same — profiles for shape changes, properties for value changes. That division keeps profile counts from exploding.

A profile-specific misconception is stuffing every tiny property difference into a new profile name until nobody remembers what `prod-east-canary-2` means. Another is relying on a default profile that includes production-capable beans while developers forget to set `local`, so laptops accidentally talk to shared systems.

Profiles choose which beans exist. They do not, by themselves, explain where `stripe.api-key` is read from, or which property source wins when the same key appears in a file, an env var, and a command-line flag. That layered property resolution lives in Spring's `Environment` abstraction — the next episode.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 15 (*Profiles*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
