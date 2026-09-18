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

Episode One left us with a promise: Spring assembles an object graph so your domain can stay plain Java. That promise only makes sense if you know what "Spring" actually is on the classpath — because Spring is not one giant JAR that does everything.

Picture a team shipping a nightly inventory reconciliation job. The job needs a container for wiring repositories and a mail client. Someone adds a dependency named vaguely "spring" and suddenly the build pulls web MVC, servlet APIs, and half a messaging stack the batch process will never call. Classpath size climbs. Version alignment gets fragile. Onboarding engineers cannot tell which modules are load-bearing and which arrived by accident. The failure mode is not a missing annotation. It is modular blindness.

So an engineer asks a precise question: which Spring modules do we actually depend on, and what job does each layer own?

Spring Framework answers with a layered module architecture. At the center sits the core container — `spring-core`, `spring-beans`, and `spring-context`. That trio is where bean definitions, factories, and the application context live. Around it, optional modules attach when you need them: `spring-aop` for cross-cutting proxies, `spring-web` and `spring-webmvc` for HTTP, `spring-jdbc` / `spring-orm` / `spring-tx` for data access and transactions, `spring-test` for test support. You compose a stack the way you compose a meal — take the base, add only the courses you will eat.

That modularity is the architecture lesson. A REST API can depend on `spring-webmvc` plus the container. A pure domain service library can depend on `spring-context` alone. A messaging worker can skip MVC entirely. Dependency direction matters: higher-level modules may rely on the container, but your business code should not sprawl into every Spring package just because it is available.

```java
// Batch job: container + JDBC only — no web stack required
@Configuration
@ComponentScan("com.acme.inventory")
public class InventoryBatchConfig {

    @Bean
    DataSource dataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:postgresql://db/inventory");
        return ds;
    }

    @Bean
    JdbcTemplate jdbcTemplate(DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }
}
```

When this configuration boots inside an `AnnotationConfigApplicationContext`, Spring loads container modules and JDBC support. It does not invent a `DispatcherServlet`. The architecture is doing work by absence: unused modules stay off the classpath, so the runtime stays honest about what the process is.

People often treat "Spring architecture" as a slide of colored boxes to memorize for interviews. Boxes without dependency stories are decoration. Another trap is assuming Boot starters erase the need to understand modules. Starters choose modules for you; they do not change what each module is for. When a transitive dependency surprises you, module literacy is how you diagnose it.

Hold the mental map: core container first, then AOP, data, web, and test as optional rings. Once that map is clear, a deeper question appears. Inside the container modules themselves — who actually owns creating objects and deciding when they live? That ownership flip is Inversion of Control, and it is the next idea we need.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 2 (*Spring Architecture*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
