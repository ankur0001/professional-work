# Episode 97 — Testcontainers

| Field | Value |
|---|---|
| Episode | 97 |
| Title | Testcontainers |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 97 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Integration tests with H2 prove that your Spring wiring can talk to a database. They do not prove that your Flyway migration, native Postgres query, or `JSONB` column works on Postgres. Testcontainers starts real Docker containers from JUnit tests — databases, brokers, browsers — and exposes mapped ports so Spring can connect. The container lifecycle can follow a single test, a class, or a shared singleton across the suite.

Here is a focused example: a real PostgreSQL database behind a Spring Data repository test.

```java
@Testcontainers
@SpringBootTest
@ActiveProfiles("tc")
class OrderRepositoryContainerIT {

    @Container
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16-alpine")
                    .withDatabaseName("orders")
                    .withUsername("test")
                    .withPassword("test");

    @DynamicPropertySource
    static void datasourceProps(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    OrderRepository orders;

    @Test
    void savesAndFindsBySku() {
        OrderEntity saved = orders.save(OrderEntity.newForSku("SKU-1"));
        assertTrue(orders.findById(saved.getId()).isPresent());
        assertEquals("SKU-1", orders.findBySku("SKU-1").orElseThrow().getSku());
    }
}
```

Narrate the run. Jupiter starts. The Testcontainers JUnit extension sees `@Container` and starts Postgres 16 in Docker. `@DynamicPropertySource` registers the ephemeral JDBC URL into Spring’s Environment before the context refreshes. Boot migrates schema (Flyway/Liquibase) against the real engine. The test saves and reads through JPA. After the class, the container stops. You exercised a real database without maintaining a shared snowflake CI database.

Spring Boot 3.1+ also offers service connection support — `@ServiceConnection` on a container bean — to reduce manual property wiring for supported technologies. The idea is the same: container first, Spring connects to whatever host port Docker published.

```java
@Bean
@ServiceConnection
PostgreSQLContainer<?> postgresContainer() {
    return new PostgreSQLContainer<>("postgres:16-alpine");
}
```

That bean form shines in `@TestConfiguration` shared across several IT classes. Whether you use `@DynamicPropertySource` or `@ServiceConnection`, assert against behavior that H2 would lie about: a native query, a partial index migration, or `SKIP LOCKED` semantics.

Containers are not only for SQL. Kafka, LocalStack, Redis, and Selenium images cover messaging, cloud APIs, caches, and UI. Reuse patterns matter for speed: a static container per class is cheaper than per-method; Ryuk cleans up orphaned containers when the JVM exits. CI runners need Docker (or a compatible engine) available; without it, these tests fail at infrastructure, not assertion.

When migrations fail against Postgres but passed on H2, this is exactly the feedback you wanted — better in CI than after a Friday deploy. Read the container logs (`postgres.getLogs()`) when connection or SQLSTATE errors confuse you; the engine’s message is usually clearer than Spring’s wrapper.

Parallel CI needs enough Docker capacity. Sharing one container via a singleton pattern across test classes reduces churn:

```java
public abstract class PostgresSupport {
    static final PostgreSQLContainer<?> POSTGRES =
            new PostgreSQLContainer<>("postgres:16-alpine")
                    .withReuse(true);
    static {
        POSTGRES.start();
    }
}
```

Reuse requires Testcontainers config enabling it and discipline about leftover schema — truncate or migrate cleanly between classes if tests are not transactional.

A misconception is starting a new heavy container for every tiny test method until the suite takes longer than a lunch break — share containers where isolation allows. Another is using latest tags for database images so Monday’s CI differs from Friday’s; pin versions. A third is treating Testcontainers as a replacement for unit tests; keep Mockito-level tests for pure logic and reserve containers for boundary risk.

Today we ran a Spring Boot test against a real Postgres started by Testcontainers, injected JDBC properties dynamically, and proved repository behavior on the engine you ship.

Your database contract is one boundary. Another sits between services: the HTTP JSON shape order expects from inventory. Containers will not catch inventory renaming a field if your suite never involves both sides’ agreement.

That agreement is Contract Testing.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 97 (*Testcontainers*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
