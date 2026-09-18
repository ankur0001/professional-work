# Episode 27 — Profiles (Boot)

| Field | Value |
|---|---|
| Episode | 27 |
| Title | Profiles |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 27 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Logging levels, datasource URLs, and even entire beans need to change between laptop and production. Boot profiles are how one artifact wears those different outfits.

You met profiles in Phase One as a Framework idea: `@Profile` on beans, active profiles in the Environment. Boot makes the day-to-day workflow concrete. Document defaults in `application.yml`. Put overrides in `application-dev.yml`, `application-staging.yml`, `application-prod.yml`. Activate with `spring.profiles.active`, an environment variable, or a command-line flag. Without that discipline, teams either hard-code environment checks in Java or maintain separate branches per deploy target — both rot.

The question to hold: how do we activate a named set of property documents and beans so "prod" is a switch, not a rewrite?

Boot's profile documents are loaded when their profile is active. Multiple profiles can be active; later sources still follow the Environment precedence rules you already saw. Group profiles can compose — for example a `cloud` group that includes `prod` and `kubernetes` — so activation stays declarative.

```yaml
# application.yml
spring:
  application:
    name: orders
server:
  port: 8080
```

```yaml
# application-dev.yml
spring:
  datasource:
    url: jdbc:h2:mem:orders
logging:
  level:
    com.acme.orders: DEBUG
```

```yaml
# application-prod.yml
spring:
  datasource:
    url: jdbc:postgresql://db.prod.internal:5432/orders
logging:
  level:
    com.acme.orders: INFO
```

```bash
java -jar orders.jar --spring.profiles.active=prod
# or
export SPRING_PROFILES_ACTIVE=prod
```

Beans participate too. A `@Profile("dev")` `@Bean` might expose an H2 console helper or a stub payments client. A `@Profile("prod")` bean supplies the real gateway. On startup Boot logs the active profiles — read that line every time you debug "wrong datasource." If the line says `dev` in a prod pod, stop looking at SQL and fix activation.

```java
@Configuration
public class PaymentsConfig {

    @Bean
    @Profile("dev")
    PaymentsClient stubPayments() {
        return new StubPaymentsClient();
    }

    @Bean
    @Profile("prod")
    PaymentsClient livePayments(PaymentsProperties props) {
        return new HttpPaymentsClient(props);
    }
}
```

Default profiles cover the case when nothing is set — useful so local runs work out of the box. Prefer explicit activation in shared environments. Keep secrets out of profile files in git; combine profiles with external env vars for credentials. Profile-specific `application-prod.yml` can still say `password: ${DB_PASSWORD}` and let the platform inject the value.

The trap is proliferating micro-profiles until nobody knows what `spring.profiles.active=a,b,c,d` means. Another is using profiles for feature toggles that should be ordinary boolean properties — profiles shine for environment-shaped differences, not for every experiment. A third is forgetting that `@Profile` beans are skipped entirely when inactive, which can leave you with a missing bean definition error if no alternate bean exists for the active profile.

When config, logging, and profile-specific beans are under control, you still have to ship the process. How does Boot turn this application into something you can `java -jar` — with dependencies nested and an embedded server inside?

That packaging model is the last Boot lesson before we open the web layer for real.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 27 (*Profiles*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
