# Episode 13 — @Configuration

| Field | Value |
|---|---|
| Episode | 13 |
| Title | @Configuration |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 13 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Injection annotations assume the beans already exist. Somebody still has to teach Spring how to construct the awkward parts of the graph — especially types your scanner cannot see.

Imagine integrating a payment SDK. You need a single shared `StripeClient` built from an API key, and a `WebhookVerifier` that must use that same client instance. You write a plain class with two `@Bean` methods where `webhookVerifier()` calls `stripeClient()` directly. Without special handling, that is just Java: each call to `stripeClient()` would construct another client. Connection pools double. Rate-limit state splits. Tests lie because they see one instance while production quietly builds two.

What fails is inter-bean referencing inside factory methods if the configuration class is "lite" — processed as ordinary `@Bean` methods on a non-configuration class — instead of full `@Configuration` semantics. The engineer asks: how does Spring make `@Bean` methods participate in the container so that calls between them reuse managed singletons?

`@Configuration` marks a class as a full source of bean definitions. Spring enhances those classes — typically with CGLIB — so that calls to `@Bean` methods from other `@Bean` methods are intercepted and redirected through the container. You write natural Java. The container still guarantees singleton semantics for singleton-scoped beans. `@Configuration` classes are themselves beans, can be profiled, imported, and composed with `@Import`.

```java
@Configuration
public class StripeConfig {

    @Bean
    StripeClient stripeClient(Environment env) {
        return new StripeClient(env.getRequiredProperty("stripe.api-key"));
    }

    @Bean
    WebhookVerifier webhookVerifier() {
        // Full @Configuration: this call returns the container-managed singleton
        // of stripeClient(), not a second new StripeClient().
        return new WebhookVerifier(stripeClient());
    }
}
```

On refresh, Spring registers definitions for `stripeClient` and `webhookVerifier`, creates a enhanced configuration instance, and when `webhookVerifier()` runs, the intercepted `stripeClient()` call returns the already-cached singleton. One API client. One verifier. If you removed `@Configuration` and left only `@Bean` methods on a plain `@Component`, lite mode would not intercept that call — `new StripeClient` could happen twice. That difference is the heart of this episode.

`@Configuration` also signals intent to readers: this type is assembly, not domain. Keep business rules out of it. Use it to bind infrastructure, third-party clients, and explicit wiring that scanning cannot express cleanly. `@Import` other config classes to keep modules bounded instead of one thousand-line config type.

A misconception specific to `@Configuration` is that it is required on every class that uses `@Autowired`. It is not. Another is ignoring lite versus full mode and wondering why singleton guarantees "broke" when you called one `@Bean` method from another on a non-configuration class.

`@Configuration` is the theater. The actors on stage are the `@Bean` methods themselves — how they name beans, accept parameters, and customize init or destroy. That annotation deserves its own close-up next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 13 (*@Configuration*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
