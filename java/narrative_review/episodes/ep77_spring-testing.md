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

`MockMvc` exercises HTTP mappings without a full server. Assertions should read like a specification: expect status, expect JSON path, expect a header. A test that only checks that the call did not throw is not protecting the contract. `@DataJpaTest` focuses on persistence slices — flush and clear the persistence context between act and assert so you are not reading only the first-level cache. `@SpringBootTest` boots a fuller context — use it when you truly need that graph, not as a default for every class.

Choose the lightest test that can fail for the right reason. Domain pure logic: unit test, no Spring. Controller routing and validation: `@WebMvcTest` with MockMvc and mocked collaborators. Repository queries against a real dialect: `@DataJpaTest` plus Testcontainers when H2 lies. Security filter behavior: dedicated security tests — anonymous access and forbidden-role cases beside happy paths. Full vertical slice: `@SpringBootTest` sparingly for critical paths. When `@SpringBootTest` is a habit, suites rot. Prefer slices for speed is not anti-integration; it is triage.

Testcontainers cost time and buy truth. Use them where contract with infrastructure matters — JSONB queries, lock behavior, Kafka consumer offsets. Do not require a container to assert that a pure tax function rounds correctly.

Flakes teach the wrong lesson. If tests depend on wall-clock time, inject a clock. If tests depend on row order without `ORDER BY`, fix the query or the assertion. If tests share mutable static state, isolate data. Deterministic data — fixed clocks, explicit fixtures, no order-dependent tests — keeps CI green. Assert failures, not only successes. A validation test that never sends a blank field is incomplete. Spring's test support makes the happy path easy; professionalism lives in the negative paths.

Slice tests also document architecture. If you cannot `@WebMvcTest` a controller without pulling the entire JPA world, the controller may be doing too much. Painful tests are often design feedback. Listen before you force a full `@SpringBootTest` to silence the pain.

Close with a team policy you can actually run. Every service class with pure logic gets unit tests without Spring. Every controller gets a web slice test for routing, validation, and error mapping. Critical repository queries get a persistence slice against a containerized database. A small set of `@SpringBootTest` scenarios cover security wiring and main happy paths. Failures are asserted. Time is faked. Data is isolated. That policy keeps the suite fast enough to run and realistic enough to trust.

When `@SpringBootTest`? When you truly need the full context; prefer slices for speed. Then mention Testcontainers for the integration layer where contracts with real infrastructure matter. If a suite cannot fail for the right reason, it cannot protect production.

This closes the Spring core arc: container, Boot, web, data, security, tests. Next we zoom out to systems of services — microservices basics — where network failure becomes a design input, not an exception. Episode Seventy-Eight.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Testing (Episode 77).

Narration technique: regression fear → fast vs realistic → unit without Spring → @WebMvcTest → slices vs @SpringBootTest → Testcontainers/determinism → team policy → bridge to microservices.

Teaching points preserved: unit without Spring; @WebMvcTest/@DataJpaTest; @SpringBootTest when needed; Testcontainers; deterministic data.
