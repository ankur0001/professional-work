# Episode 14 — @Bean

| Field | Value |
|---|---|
| Episode | 14 |
| Title | @Bean |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 14 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Debugger stuck in `SmsClient.<init>`. The cinema (and every other product in the building) uses a third-party SMS SDK. You cannot put `@Component` on `com.vendor.sms.SmsClient` — you do not own the source, and the vendor constructor needs an API key plus a timeout the container will not invent. Stereotype scanning is the wrong door. `@Bean` is the door that fits: a factory method you write, returning an object Spring then manages.

A `@Bean` method is a factory method whose return value Spring registers as a container-managed object. Method name defaults to the bean name. Parameters are injected from the container. You can declare `initMethod` / `destroyMethod` for objects that expose lifecycle without Spring annotations. This is how you adapt the world you do not control into the graph you do — SDKs, legacy singletons, `ObjectMapper` customizations, connection clients.

```java
@Configuration
public class SmsConfig {

    @Bean(initMethod = "start", destroyMethod = "shutdown")
    SmsClient smsClient(Environment env) {
        SmsClient client = new SmsClient();
        client.setApiKey(env.getRequiredProperty("sms.api-key"));
        client.setConnectTimeout(Duration.ofSeconds(
            env.getProperty("sms.connect-timeout-seconds", Integer.class, 5)));
        return client;
    }

    @Bean
    BookingNotifier bookingNotifier(SmsClient smsClient) {
        return new SmsBookingNotifier(smsClient);
    }
}
```

Walk the factory. `smsClient(Environment env)` receives the Environment bean as a parameter — no field injection required. `getRequiredProperty("sms.api-key")` fails fast if the key is missing; `getProperty(..., 5)` supplies a default timeout when unset. `new SmsClient()` is ordinary construction inside *your* method; returning `client` hands the instance to Spring. `initMethod = "start"` means after the method returns and the object is registered, Spring reflects and calls `start()` on it. `destroyMethod = "shutdown"` registers a destruction callback for context close. `bookingNotifier(SmsClient smsClient)` asks the container for the `smsClient` singleton by type — one client, shared — and wraps it in an app-owned `SmsBookingNotifier` that your domain can depend on without importing vendor packages everywhere.

Runtime during refresh. Spring defines beans `smsClient` and `bookingNotifier` from method metadata. When creating `smsClient`, it invokes your method, then `start`. If `start` opens a vendor connection pool and throws, context refresh fails — you see the exception during startup, not on the first booking confirmation. Dependents like `bookingNotifier` are created afterward (or as needed) with the same instance injected. On `ConfigurableApplicationContext.close()`, Spring calls `shutdown` even though the vendor never heard of `@PreDestroy`. Your notifier can stay a plain class; only the configuration module imports `com.vendor.sms.SmsClient`.

`@Bean` also covers conditional registration (`@ConditionalOnProperty`), `@Profile` on methods, and `@Primary` / `@Qualifier` on the return. Example: local profile returns a `ConsoleBookingNotifier` from another `@Bean` method while prod returns `SmsBookingNotifier` — same `BookingNotifier` type, different instances gated by profile. It is not a lesser cousin of `@Component`. It is the escape hatch and the integration seam.

Failure mode with clear symptoms: omit `destroyMethod` (and the vendor has no Spring lifecycle hooks). On every Boot DevTools restart or test context close, SMS connections leak until the vendor's remote side rate-limits you — symptom is "too many open sessions" from the SMS API after a day of local restarts, while production looks fine because pods recycle less often. Another failure: call `new SmsClient()` inside `SmsBookingNotifier`'s constructor instead of injecting the `@Bean` — two clients, two API sessions, initMethod only ran on the unused bean. Symptom: metrics show double outbound SMS traffic or duplicate confirmations.

Trade-offs. `@Bean` localizes foreign construction and lifecycle in one config class — easy to audit, easy to fake in `@TestConfiguration`. You must remember destroy callbacks for resources the vendor expects closed. `@Component` on *your* types is shorter when you own the source and need only constructor injection; it cannot wrap sealed third-party classes. Returning interface types (`BookingNotifier`) from `@Bean` methods hides vendor types from the rest of the app — worth the extra wrapper when the SDK is noisy.

Misconception unique to `@Bean`: "Returning `new` from `@Bean` means Spring does not manage the object — it is unmanaged because I constructed it." False. You constructed it inside the factory method; Spring still applies scope, lifecycle callbacks you declared, and injects that instance into dependents. Management starts when the method returns into the container, not when the bytecode used `new`.

SMS works in one environment. Staging and production need different API keys, and local dev wants a console notifier instead of real texts. Same artifact, different bean sets — that is the profile problem waiting behind the configuration class.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 14 (*@Bean*).
