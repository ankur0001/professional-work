# Episode 02 — Spring Architecture

| Field | Value |
|---|---|
| Episode | 02 |
| Title | Spring Architecture |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 2 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The baggage-tracking system at Gate West started as one WAR. Tag scanners, carousel boards, lost-bag claims, overnight reconciliation — all in one deployable. Three years later, a carousel outage still forced a full redeploy of claims and reconciliation. The monolith was not just "big." It was one classpath, one restart boundary, and one blame surface.

When the team finally split modules, Spring became the awkward part of the conversation. Someone had pulled a vague "spring" dependency into the reconciliation JAR and dragged servlet APIs, MVC, and messaging into a nightly batch that never served HTTP. Build times grew. On-call could not tell which Spring modules were load-bearing. The failure was modular blindness, not a missing annotation.

Spring Framework is layered on purpose. At the center sit `spring-core`, `spring-beans`, and `spring-context` — the core container that understands bean definitions, factories, and the application context. Optional rings attach when you need them: `spring-aop` for proxies, `spring-web` / `spring-webmvc` for HTTP, `spring-jdbc` / `spring-orm` / `spring-tx` for data access, `spring-test` for tests. You compose a stack the way you compose a meal: take the base, add only what you will eat.

For Gate West that meant three deployables with different Spring shapes. The scanner ingest service needed the container plus messaging. The carousel board needed webmvc. The overnight reconciliation job needed the container plus JDBC — and nothing from the web stack.

```java
// Reconciliation module: container + JDBC only — no webmvc on the classpath
@Configuration
@ComponentScan("com.gatewest.baggage.reconcile")
public class BaggageReconcileConfig {

    @Bean
    DataSource dataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:postgresql://bags-db/reconcile");
        return ds;
    }

    @Bean
    JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean
    LostBagMatcher lostBagMatcher(JdbcTemplate jdbc) {
        return new LostBagMatcher(jdbc);
    }
}
```

At runtime the container does not care that this job never opens port 8080. It reads bean-definition metadata, registers types in a `BeanFactory`, and materializes the graph. `ApplicationContext` sits on top of that factory with events, messages, and resource loading — which the carousel UI will need later, and which the batch job may barely touch. Higher modules may depend on the container; your baggage domain should not sprawl into every Spring package just because a transitive dependency made it available.

Misconception unique to architecture: "If the app uses Spring, it uses Spring Web." False. Spring is a modular toolbox. A classpath that includes MVC in a headless reconciler is an architecture smell, not proof you needed a controller.

After the split, Gate West could restart carousel boards without bouncing claims. But a quieter problem remained inside each module: services still constructed doctors of collaborators with `new`, and tests still fought construction order. Who actually owns object creation once the modules are drawn?

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 2 (*Spring Architecture*).
