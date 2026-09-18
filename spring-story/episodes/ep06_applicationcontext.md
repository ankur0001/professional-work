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

The pharmacy kiosk on Floor 2 is showing English labels to a Spanish-speaking patient again. Ops restarts the process. The drug catalog still points at the staging URL because someone exported the wrong shell variables on the thin client. Meanwhile the waiting-room board never lights up when a prescription is ready — the notifier writes a log line and hopes a polling job notices.

Those three failures are not BeanFactory failures. The services are wired. What is missing is the application layer Spring stacks on top of the factory: messages, environment, events, and resource loading.

`ApplicationContext` extends `BeanFactory`. You still `getBean`. You also get `MessageSource` for i18n, `Environment` / `PropertyResolver` for profiles and properties, an event bus via `ApplicationEventPublisher`, and `ResourceLoader` / `ResourcePatternResolver` for classpath and file resources. Most real applications program to an ApplicationContext — `AnnotationConfigApplicationContext`, `ClassPathXmlApplicationContext`, or Boot's context — not to the raw factory API.

```java
@Configuration
public class PharmacyKioskConfig {

    @Bean
    MessageSource messageSource() {
        ResourceBundleMessageSource ms = new ResourceBundleMessageSource();
        ms.setBasename("i18n/kiosk");
        ms.setDefaultEncoding("UTF-8");
        return ms;
    }

    @Bean
    PrescriptionReadyListener prescriptionReadyListener(WaitingRoomBoard board) {
        return new PrescriptionReadyListener(board);
    }
}

@Component
public class FulfillmentService {
    private final ApplicationEventPublisher events;
    private final MessageSource messages;
    private final Environment env;

    public FulfillmentService(ApplicationEventPublisher events,
                              MessageSource messages,
                              Environment env) {
        this.events = events;
        this.messages = messages;
        this.env = env;
    }

    public void markReady(PrescriptionId id, Locale locale) {
        String catalog = env.getRequiredProperty("pharmacy.catalog-url");
        String text = messages.getMessage("rx.ready", new Object[]{id}, locale);
        events.publishEvent(new PrescriptionReadyEvent(id, text, catalog));
    }
}
```

Walk the "ready" press on the kiosk after a successful context refresh. Refresh has already built singletons: the `ResourceBundleMessageSource` is registered under the well-known `MessageSource` role, `PrescriptionReadyListener` is a bean (and, if annotated with `@EventListener` or implementing `ApplicationListener`, subscribed through the multicaster), and `FulfillmentService` holds three collaborators that are themselves context services. `markReady` calls `env.getRequiredProperty("pharmacy.catalog-url")`. Environment resolution walks registered `PropertySource` instances — system properties, OS environment variables, `application.yml`, profile-specific files — in documented precedence order. Staging URL on the thin client means a wrong source won, not a missing bean. Next, `messages.getMessage("rx.ready", …, locale)` loads `i18n/kiosk_es.properties` (or falls back through the basename chain). Missing key → `NoSuchMessageException` unless you configured a default message. Then `events.publishEvent(...)` hands the event to `ApplicationEventMulticaster`. By default that delivery is synchronous on the caller's thread: the listener updates `WaitingRoomBoard` before `markReady` returns. Same bean graph a BeanFactory would build — plus these services participating as first-class collaborators.

Failure mode symptoms map cleanly onto the three Floor 2 incidents. English-only UI with a Spanish Locale: missing `i18n/kiosk_es.properties` on the classpath, wrong basename (`i18n/kiosk` vs `messages/kiosk`), or Locale never set on the request — MessageSource falls back to the default bundle and operators blame "i18n is broken" when the file was never packaged. Staging catalog URL after restart: `pharmacy.catalog-url` resolved from an exported shell variable that outranked the intended ConfigMap/file source; `env.getProperty` returns the wrong string without throwing, while `getRequiredProperty` only helps when the key is absent. Waiting-room board silent: listener not registered (component scan missed the package), event type mismatch (`PrescriptionReadyEvent` vs a similarly named DTO), or someone assumed `publishEvent` was async and looked for a queue that does not exist. Process kill mid-handler loses the in-memory event — it is not Kafka.

Trade-offs. ApplicationContext buys a standard refresh lifecycle, i18n, Environment post-processors, resource patterns, and an event multicaster at the cost of heavier startup than a bare factory. For the pharmacy kiosk that cost is the product: you need those services. For the warehouse CLI next door, a `DefaultListableBeanFactory` may still be enough. Boot's `SpringApplication` always builds an ApplicationContext; you rarely construct one by hand in production apps, but understanding what it adds explains why `MessageSource`, `Environment`, and `ApplicationEventPublisher` inject without you writing factory lookups.

Misconception unique to ApplicationContext: "Publishing an event means asynchronous, reliable messaging." Inside a single context, `publishEvent` is typically synchronous on the caller's thread unless you configure an `ApplicationEventMulticaster` with an async executor. Exceptions in a listener propagate to the publisher by default. Losing the process mid-handler loses the event. Another misconception: "ApplicationContext replaces BeanFactory." It extends it. `getBean` still bottoms out in the factory; the context wraps richer services around the same core.

The kiosk finally speaks the right language when Locale and bundles line up, and the board lights when the listener is actually subscribed. That success raises a sharper question about the metadata itself: when the plugin team wants to load payment adapters from YAML at startup, what exactly is Spring storing for each bean before any instance exists?

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 6 (*ApplicationContext*).
