# Episode 06 — ApplicationContext

| Field | Value |
|---|---|
| Episode | 06 |
| Title | ApplicationContext |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 6 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`BeanFactory` can answer `getBean`. A shipping backend usually needs the container to do more before the first request arrives.

Consider a payments API that must publish a `PaymentCompletedEvent` when a charge succeeds, resolve a localized decline message for the UI, load a classpath schema for validation, and fail fast at startup if the fraud-check bean cannot be constructed. With only a bare factory, you wire those concerns yourself — a static event bus here, ad-hoc property files there, lazy surprises in production when the first customer hits a broken singleton. The graph "works" in a smoke test that never requested the broken bean.

Without an application-level context, teams reinvent the same surround sound: events, resources, environment, and startup validation. The question becomes unavoidable: is there a Spring container that extends the factory with those application services and a defined refresh lifecycle?

That container is `ApplicationContext`. It extends `BeanFactory` and adds the features production code expects. It is also a `MessageSource` for i18n, an `ApplicationEventPublisher` for events, a `ResourcePatternResolver` for classpath and file resources, and the home of `Environment` for profiles and properties. On refresh, a typical context pre-instantiates singleton beans, so configuration errors surface at boot instead of at 2 a.m. under load.

```java
@Configuration
@ComponentScan("com.acme.payments")
public class PaymentsConfig { }

@Service
public class PaymentService {
    private final ApplicationEventPublisher events;

    public PaymentService(ApplicationEventPublisher events) {
        this.events = events;
    }

    public void charge(ChargeRequest request) {
        // charge against the gateway, then notify the rest of the app
        events.publishEvent(new PaymentCompletedEvent(request.token()));
    }
}

// bootstrap
AnnotationConfigApplicationContext context =
        new AnnotationConfigApplicationContext(PaymentsConfig.class);
PaymentService payments = context.getBean(PaymentService.class);
payments.charge(new ChargeRequest("tok_42", Money.usd(20)));
context.close();
```

When `AnnotationConfigApplicationContext` starts with `PaymentsConfig`, it registers bean definitions from the configuration and component scan, then refreshes. Singleton services are created up front. `PaymentService` receives the context's event publisher through DI — not by holding the whole context. Publishing `PaymentCompletedEvent` notifies `@EventListener` methods elsewhere. Closing the context runs destroy hooks. That is the application runtime story, not merely `getBean`.

Contexts come in flavors worth naming. `AnnotationConfigApplicationContext` for Java config. `ClassPathXmlApplicationContext` for XML-era apps. Web and Boot supply their own context types. Same conceptual role: factory plus application services plus refresh.

A misconception unique to this layer is "I should inject `ApplicationContext` into every service so I can look up beans." That turns the context into a service locator and hides real dependencies. Prefer injecting the collaborators — or `ApplicationEventPublisher`, `Environment`, `ResourceLoader` — the narrow interfaces the context already implements. Another misconception is that `ApplicationContext` replaces `BeanFactory`. It does not replace it; it builds on it. When documentation says bean factory, you are still inside the context's lower half.

You now have a living container. But refresh only works if the context knows what to build. Where do those recipes live — class name, scope, lazy flag, constructor arguments? That metadata is the bean definition, and without understanding it the context remains a black box.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 6 (*ApplicationContext*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
