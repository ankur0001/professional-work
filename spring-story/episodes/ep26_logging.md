# Episode 26 — Logging

| Field | Value |
|---|---|
| Episode | 26 |
| Title | Logging |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 26 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

DevTools shortens the restart loop. Logging decides whether each restart — and each production incident — teaches you something or buries you.

Every Boot app logs. The failure mode is not "no logs." It is the wrong shape of logs: Hibernate SQL at DEBUG in production melting disks, your package silent at ERROR while a payment bug hides, or three logging facades fighting because someone added Log4j config beside Logback beside `System.out`. Teams also hard-code levels in code and then redeploy to "turn on debug."

So how does Boot want you to configure loggers, levels, and formats — centrally, externally, and without fighting the starter defaults?

Spring Boot's logging starter (pulled in transitively by other starters) sets up a default logging system — typically Logback for servlet stacks — with console output and sensible root levels. You configure through `application.yml` / properties, environment-specific overrides, or a `logback-spring.xml` when you need full control. Prefer Boot's `logging.level.*` keys for everyday work. Use the XML (or Log4j2 config) when you need custom appenders, JSON encoding, or intricate routing.

```yaml
logging:
  level:
    root: INFO
    com.acme.orders: DEBUG
    org.hibernate.SQL: WARN
  pattern:
    console: "%d{HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n"
```

Runtime behavior is immediate on the next log event after Environment bind — and with Actuator or Cloud tooling you can sometimes adjust levels at runtime, but start by getting file-based config right. Your application code should log through SLF4J:

```java
@Service
public class OrderService {
    private static final Logger log = LoggerFactory.getLogger(OrderService.class);

    public Order place(Cart cart) {
        log.debug("placing order for cart {}", cart.id());
        try {
            return repo.save(Order.from(cart));
        } catch (DataAccessException ex) {
            log.error("failed to persist order for cart {}", cart.id(), ex);
            throw ex;
        }
    }
}
```

Notice the facade: `LoggerFactory` from SLF4J, not a direct Logback API in domain code. Boot chooses the backend. You keep the facade so tests and future backend swaps stay calm. Log placeholders use `{}` — not string concatenation — so DEBUG messages skip formatting when the level is disabled.

Profile-specific logging is a common production pattern. Keep `com.acme.orders` at DEBUG in `application-local.yml`, INFO in `application-prod.yml`. Ship correlation-friendly patterns when you later add request IDs. Avoid logging secrets: tokens, passwords, and full card payloads do not belong in INFO lines no matter how helpful they feel during a firefight.

The misconception is configuring logging only inside the IDE console filter and never in the app config — then production looks nothing like your laptop. Another is enabling `org.springframework` at TRACE "temporarily" and leaving it on until the cluster spends its budget on log ingestion. A third is mixing `System.out.println` into services "just for now" until those prints become the only signal anyone trusts.

Levels and packages often need to differ by environment. That is the same profile machinery you met in fundamentals — now applied the Boot way, with `application-{profile}` documents and `spring.profiles.active` as the switch.

Boot profiles are next: activating sets of config and beans for local, test, and prod without forking the codebase.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 26 (*Logging*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
