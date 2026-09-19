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

When the team finally split modules, Spring became the awkward part of the conversation. Someone had pulled a vague "spring" dependency into the reconciliation JAR and dragged servlet APIs, MVC, and messaging into a nightly batch that never served HTTP. Build times grew. On-call could not tell which Spring pieces were load-bearing. The failure was modular blindness, not a missing annotation.

Spring Framework is layered so you can compose different shapes for different jobs. At the center sit `spring-core`, `spring-beans`, and `spring-context` — the container that understands bean definitions, factories, and the application context. Everything else is optional: you add a ring only when that deployable needs it.

Watch how that maps onto Gate West after the split. Scanner ingest is a headless process that receives bag-tag events. Its classpath needs the container plus messaging — not MVC. The carousel board is an HTTP service; it adds `spring-webmvc` (and whatever view or JSON stack you choose) on top of the same container core. Overnight reconciliation is a batch job with JDBC access to the bags database: container plus `spring-jdbc` / transaction support — and deliberately nothing from the web stack. Same Spring family. Three different module graphs. Three restart boundaries.

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

At runtime that job never opens port 8080, and the container does not care. It reads bean-definition metadata, registers types in a `BeanFactory`, and materializes the graph. `ApplicationContext` sits on top of that factory with events, messages, and resource loading — which the carousel UI will lean on later, and which the batch job may barely touch. Higher-level Spring modules may depend on the container; your baggage domain should not sprawl into every Spring package just because a transitive dependency made it available.

The architecture misconception that bit Gate West is simple: "If the app uses Spring, it uses Spring Web." False. Spring is a modular toolbox. A classpath that includes MVC in a headless reconciler is an architecture smell, not proof you needed a controller. Another smell: one shared "utils" module that imports every Spring starter so every deployable inherits everyone else's stack.

After the split, Gate West could restart carousel boards without bouncing claims. But a quieter problem remained inside each module: services still constructed collaborators with `new`, and tests still fought construction order. Who actually owns object creation once the module boundaries are drawn?

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 2 (*Spring Architecture*).
