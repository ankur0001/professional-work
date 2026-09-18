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

```java
@Configuration
public class CinemaTicketingConfig {

    @Bean
    SeatMap seatMap() {
        return SeatMap.load("classpath:auditoriums/imax-12.json");
    }

    @Bean
    PricingPolicy pricingPolicy() {
        return new MatineePricingPolicy();
    }

    @Bean
    TicketService ticketService() {
        return new TicketService(seatMap(), pricingPolicy());
    }

    @Bean
    PaymentGateway paymentGateway(Environment env) {
        return new CardPresentGateway(env.getRequiredProperty("cinema.payment.merchant-id"));
    }
}
```

No `@ComponentScan`. No stereotype on `TicketService`. The full-screen cinema box office wires every collaborator in one `@Configuration` class so the seating map never appears twice by accident and ops can read the graph top to bottom before Friday night rush.

`@Configuration` marks a class as a source of bean definitions via `@Bean` methods. In full (default) mode, Spring enhances the configuration class — historically with CGLIB — so calls between `@Bean` methods on the same class do not create a second instance. When `ticketService()` calls `seatMap()`, that call is intercepted and returns the singleton already managed by the container, not a fresh `SeatMap.load(...)`. That interception is the whole point of default `@Configuration` semantics.

Walk each method. `seatMap()` loads auditorium JSON once when the bean is first created; method name `seatMap` becomes the default bean name. `pricingPolicy()` returns a matinee policy singleton. `ticketService()` looks like ordinary Java calling two neighbors — under enhancement it is not: each nested call asks the container for the singleton of that bean name. `paymentGateway(Environment env)` uses a different injection style: method *parameters* are satisfied from the container (`Environment` is a built-in bean), then the method body constructs the card-present gateway with a required property. No sibling call needed.

Runtime refresh for the cinema app, in order. Context registers `CinemaTicketingConfig` as a configuration class and enhances it when `proxyBeanMethods` remains true (the default). It derives bean definitions named `seatMap`, `pricingPolicy`, `ticketService`, `paymentGateway`. At end of refresh (or on first demand), instantiating `ticketService` invokes the enhanced method; inside, `seatMap()` and `pricingPolicy()` resolve through the interceptor to container-managed singletons — one JSON load, one policy. Cashiers in the same JVM share that seat map. You still need session-scoped or request-scoped hold state elsewhere if reserved seats are per guest; configuration mode only guarantees singleton *definition* semantics for these beans, not business-level locking across kiosks.

Lite mode flips the footgun back on. `@Configuration(proxyBeanMethods = false)` — or plain `@Bean` methods on a class *without* `@Configuration` — skips enhancement. Then `ticketService()` calling `seatMap()` truly executes `SeatMap.load` again. Symptom: two `SeatMap` instances in memory; cashier A reserves seat H12 on map instance 1; cashier B still sees H12 free on map instance 2; double-booking until something hits the database constraint. Another symptom in tests: asserting `ticketService` and a separately injected `SeatMap` are `==` fails under lite mode and passes under full mode. Fix when you want lite mode for faster startup: do not call sibling `@Bean` methods — inject collaborators as method parameters:

```java
@Bean
TicketService ticketService(SeatMap seatMap, PricingPolicy pricingPolicy) {
    return new TicketService(seatMap, pricingPolicy);
}
```

Failure mode without lite mode involved: forgetting `@Configuration` entirely and only using `@Bean` on a `@Component` class — methods may still register beans, but inter-bean calls are plain Java, same split-brain risk. Symptom often appears only under concurrent kiosk use, not in a single-threaded unit test that never compares identities.

Trade-offs. Full `@Configuration` makes method-call wiring safe and readable for small graphs; enhancement adds a proxy/subclass and a bit of startup cost. Lite mode and parameter injection scale better for large configs and avoid proxy surprises, at the cost of losing "just call the method" style. Explicit `@Configuration` without component scanning maximizes auditability for regulated box-office systems; it costs a registration line whenever a new service appears.

Misconception unique to `@Configuration`: "A `@Configuration` class is just a factory with annotations; method calls behave like ordinary Java." In default proxy-bean-methods mode they do not. That is the feature. If you need ordinary Java call semantics, set `proxyBeanMethods = false` and inject collaborators as method parameters instead of calling sibling `@Bean` methods.

Cinema wiring is explicit and readable. The SMS confirmation vendor SDK still cannot be annotated `@Component` because the cinema does not own that JAR. Registering foreign objects needs the `@Bean` method pattern as a first-class tool — not only inside cozy configuration demos.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 13 (*@Configuration*).
