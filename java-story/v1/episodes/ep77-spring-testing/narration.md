# Episode 77 — Spring Testing

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Six secured APIs with Spring Security's filter chain. Security and features both need proof — Spring's test story is a first-class tool. The pyramid still applies — many fast unit tests, fewer slice tests, few full contexts.

Misusing at SpringBootTest for everything makes CI slow and flaky. Good tests document contracts — bad tests freeze implementation details. Today — unit, slice, MockMvc, Testcontainers, and what to assert.

Episode Seventy-Seven. Spring Testing. Start with the test pyramid for Spring apps. Unit tests — pure Java, mocks for collaborators, no ApplicationContext. Slice tests — WebMvcTest, DataJpaTest — load only the layer under test.

Integration tests — SpringBootTest with a real or containerized stack. End-to-end tests — few, precious, against a deployed-like environment. Push assertions down the pyramid — speed is a feature of the suite.

Unit and slice testing patterns. Constructor injection makes unit tests trivial — new Service with mocks. WebMvcTest stands up controllers — MockMvc drives HTTP without a server. DataJpaTest boots repositories against an embedded or Testcontainers DB.

MockBean replaces a collaborator inside a slice context. Prefer AssertJ fluent assertions — readable failures save debug time. When SpringBootTest earns its cost. Full context catches wiring mistakes auto-config and security filters create.

Use RANDOM_PORT only when you truly need a listening server. Override properties for tests — never point CI at production databases. DirtiesContext sparingly — it is expensive and often hides design smells.

If every test needs a full boot, your modules are too entangled. Testcontainers bring realistic dependencies to CI. Postgres, Kafka, LocalStack — same engines your service talks to.

Reuse containers across a suite when the framework supports it. Pair with DynamicPropertySource to inject JDBC URLs at runtime. Slower than H2 — faster than debugging prod-only SQL dialects.

Use them for persistence and messaging contracts — not every unit test. Assert behavior, not framework internals. HTTP status, response body shape, and headers clients rely on. Database side effects after a successful command.

Security — anonymous gets four-oh-one, forbidden role gets four-oh-three. Avoid asserting log lines or private field values. Name tests as contracts — createOrder_rejectsNegativeQuantity.

Three common mistakes. One — SpringBootTest on every class — hour-long pipelines. Two — shared mutable database state between tests — order-dependent flakes. Three — testing only the happy path — auth and validation unproven.

Also — over-mocking until the test only proves the mock framework works. Test the risk — not the annotation count. Interview question — how do you test a Spring Boot service? Unit-test domain and services with mocks — no container.

Slice-test web and JPA layers with WebMvcTest and DataJpaTest. Reserve SpringBootTest plus Testcontainers for wiring and persistence truth. Always cover authz negative paths and validation errors.

Optimize for fast feedback — full context is a scalpel, not a hammer. One service is solid — next we split the system. Episode Seventy-Eight — Microservices Basics. When to split, service boundaries, sync versus async, and operational cost.

See you there.
