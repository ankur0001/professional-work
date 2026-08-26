# Episode 77 — Spring Testing

| Field | Value |
|---|---|
| Episode | 77 |
| Title | Spring Testing |
| Catalog handbook column | 77 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You have Boot, MVC, Data, and Security in play. A change breaks something subtle. The practical question is how to test without booting the universe for every class. Tests should be fast where possible — slices before full context — and realistic where reality is the point.

Constructor-injected services can be unit-tested with plain JUnit and fakes — no Spring required. When you need MVC wiring, `@WebMvcTest` loads a web slice:

```java
@WebMvcTest(HelloController.class)
class HelloControllerTest {
  @Autowired MockMvc mockMvc;
}
```

`MockMvc` exercises HTTP mappings without a full server. `@DataJpaTest` focuses on persistence slices. `@SpringBootTest` boots a fuller context — use it when you truly need that graph, not as a default for every class. Testcontainers bring real databases or brokers into integration tests when fakes lie. Deterministic data — fixed clocks, explicit fixtures, no order-dependent tests — keeps CI green.

Bootstrapping full context for everything is how suites become slow and flaky. Flaky time and order dependencies teach the team to rerun instead of fix. No failure assertions — only happy paths — miss the validation and security cases that matter.

When `@SpringBootTest`? When you truly need the full context; prefer slices for speed. Say that, then mention Testcontainers for the integration layer where contracts with real infrastructure matter.

Choose the lightest test that can fail for the right reason. Domain pure logic: unit test, no Spring. Controller routing and validation: `@WebMvcTest` with MockMvc and mocked collaborators. Repository queries against a real dialect: `@DataJpaTest` plus Testcontainers when H2 lies. Security filter behavior: dedicated security tests. Full vertical slice through Boot: `@SpringBootTest` sparingly for critical paths.

Flakes teach the wrong lesson. If tests depend on wall-clock time, inject a clock. If tests depend on row order without `ORDER BY`, fix the query or the assertion. If tests share mutable static state, isolate data. Deterministic tests are a production readiness skill, not a nicety.

Testcontainers cost time and buy truth. Use them where contract with infrastructure matters — JSONB queries, lock behavior, Kafka consumer offsets. Do not require a container to assert that a pure tax function rounds correctly.

When `@SpringBootTest` is justified, keep it few and informative. When it is a habit, suites rot. Prefer slices for speed is not anti-integration; it is triage.

This testing discipline is what lets the Spring stack evolve without fear as you move toward distributed systems next.

Choose the lightest test that can fail for the right reason. Domain pure logic: unit test, no Spring. Controller routing and validation: WebMvcTest with MockMvc and mocked collaborators. Repository queries against a real dialect: DataJpaTest plus Testcontainers when H2 lies. Security filter behavior: dedicated security tests. Full vertical slice: SpringBootTest sparingly for critical paths.

Flakes teach the wrong lesson. If tests depend on wall-clock time, inject a clock. If tests depend on row order without ORDER BY, fix the query or the assertion. If tests share mutable static state, isolate data. Deterministic tests are a production readiness skill, not a nicety.

Testcontainers cost time and buy truth. Use them where contract with infrastructure matters. Do not require a container to assert that a pure tax function rounds correctly.

When SpringBootTest is justified, keep it few and informative. When it is a habit, suites rot. Prefer slices for speed is not anti-integration; it is triage. This testing discipline lets the Spring stack evolve without fear as you move toward distributed systems next.

Assert failures, not only successes. A security test that never tries an anonymous caller is incomplete. A validation test that never sends a blank field is incomplete. A persistence test that only saves and reloads the happy entity may miss constraint violations. Spring's test support makes the happy path easy; professionalism lives in the negative paths.

Slice tests also document architecture. If you cannot @WebMvcTest a controller without pulling the entire JPA world, the controller may be doing too much. Painful tests are often design feedback. Listen before you force a full SpringBootTest to silence the pain.

Close with a team policy you can actually run. Every service class with pure logic gets unit tests without Spring. Every controller gets a web slice test for routing, validation, and error mapping. Critical repository queries get a persistence slice against a containerized database. A small set of SpringBootTest scenarios cover security wiring and main happy paths. Failures are asserted. Time is faked. Data is isolated. That policy keeps the suite fast enough to run and realistic enough to trust — which is the only testing strategy that survives contact with microservices and production pressure ahead.

MockMvc assertions should read like a specification. Expect status, expect JSON path, expect a header. When a test only checks that the call did not throw, it is not protecting the contract. Pair that with failure assertions for validation and security, and your web slice becomes living documentation.

DataJpaTest realism improves when you flush and clear the persistence context between act and assert, ensuring you are not reading only the first-level cache. Small technique, fewer false greens. Deterministic data and honest assertions are how Spring test slices earn trust before you ever open a full SpringBootTest.

If a suite cannot fail for the right reason, it cannot protect production. Keep that as the north star when someone proposes booting the full context for every class because it feels easier.

This closes the Spring core arc: container, Boot, web, data, security, tests. Next we zoom out to systems of services — microservices basics — where network failure becomes a design input, not an exception. Episode Seventy-Eight.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Testing (Episode 77).

Narration technique: regression fear → fast vs realistic → unit without Spring → @WebMvcTest example → slices vs @SpringBootTest → Testcontainers/determinism → misconceptions → interview woven → bridge to microservices.

Teaching points preserved: unit without Spring; @WebMvcTest/@DataJpaTest; @SpringBootTest when needed; Testcontainers; deterministic data.
