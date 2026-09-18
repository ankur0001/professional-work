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

H2 forgives SQL that Postgres rejects. A `VesselRepository.findByImoNumber` that “works” on H2 can fail in the quay’s Postgres on a type, JSON function, or lock. Testcontainers starts a real `PostgreSQLContainer` for the test JVM, gives Spring JDBC URLs dynamically, and tears the container down after the class or suite.

```java
@SpringBootTest
@Testcontainers
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
class VesselRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
            .withDatabaseName("harbor")
            .withUsername("harbor")
            .withPassword("harbor");

    @DynamicPropertySource
    static void datasourceProps(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    VesselRepository vessels;

    @Test
    void findsByImoNumber() {
        vessels.save(Vessel.flag("9321483", "Pacific Trader"));

        Optional<Vessel> found = vessels.findByImoNumber("9321483");

        assertTrue(found.isPresent());
        assertEquals("Pacific Trader", found.get().getName());
    }

    @Test
    void unknownImoIsEmpty() {
        assertTrue(vessels.findByImoNumber("0000000").isEmpty());
    }

    @Test
    void uniqueImoConstraintSurfaces() {
        vessels.save(Vessel.flag("9321483", "Pacific Trader"));
        assertThrows(DataIntegrityViolationException.class,
                () -> vessels.save(Vessel.flag("9321483", "Duplicate")));
    }
}
```

Walk the lifecycle. JUnit starts the class. Testcontainers pulls (or reuses) `postgres:16-alpine`, waits for readiness, exposes a JDBC URL on a random host port. `@DynamicPropertySource` feeds Boot before the context refreshes — without it, Boot may still point at H2 from `application-test.yml` and you think you tested Postgres when you did not. Spring Data runs against real Postgres. Unique constraints, `timestamptz`, and JSONB operators behave as production. The container stops when the class ends — or lives longer with reuse enabled for local speed.

```yaml
# optional: reuse across runs in local ~/.testcontainers.properties
# testcontainers.reuse.enable=true
```

Use the same major version you run in production when practical. Flyway/Liquibase migrations should run in this test profile so schema matches what gate and scheduling deploy — a repository green against an entity-only schema that never applied migration `V42__berth_window.sql` is false comfort. Pair `@DataJpaTest` with Testcontainers when you want a repository slice without the full web stack — still real Postgres, narrower context, faster feedback on derived queries. If `@DataJpaTest` replaces your DataSource by default, keep `Replace.NONE` and the dynamic properties; otherwise you silently fall back to H2 and the whole point evaporates.

Failure symptoms: CI agents without Docker cannot start containers — the suite fails loudly at environment setup, which is better than silent H2 substitution if you forbade replace. Parallel classes sharing one reused container without truncating tables produce cross-talk. Pinning `postgres:latest` means an upstream major bump breaks CI overnight; pin `16-alpine` or your prod minor. Slow first pull on cold agents dominates runtime — warm the image in the pipeline image cache. Another tell: tests pass locally on an Apple-silicon image tag and fail on CI’s amd64 agent because someone floated a platform-specific tag without a multi-arch digest.

Trade-offs: fidelity versus speed. Not every tariff-math unit test deserves a container. Reserve Testcontainers for persistence, Flyway, locking, and SQL that has bitten you on H2. Kafka and Redis modules exist too when Cloud Stream or caches are the risk — same pattern, different `GenericContainer`. For `VesselRepository`, the unique-IMO test above is the kind of constraint H2 may soft-pedal depending on mode; Postgres is blunt, which is what you want before a quay deploy.

A misconception is treating Testcontainers as a replacement for unit tests of pure tariff math — containers are for infrastructure fidelity, not for every assertion. Another is sharing one container with mutable data across parallel classes without isolation. A third is pinning `postgres:latest` and wondering why CI broke on an upstream major bump.

Repositories now meet real SQL. Service boundaries still break when gate’s Feign shape drifts from billing’s controller. Contract tests lock that wire format between teams. When both container SQL tests and contracts are green, you have proven persistence and the HTTP edge — still not the full booth journey, but far fewer Monday surprises than H2-plus-hope.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 97 (*Testcontainers*).
