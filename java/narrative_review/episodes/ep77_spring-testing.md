# Episode 77 — Spring Testing

| Field | Value |
|---|---|
| Episode | 77 |
| Title | Spring Testing |
| Catalog handbook column | 77 |
| Narration source script | `make_episode_77.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Six secured APIs with Spring Security's filter chain.
2. Security and features both need proof — Spring's test story is a first-class tool.
3. The pyramid still applies — many fast unit tests, fewer slice tests, few full contexts.
4. Misusing at SpringBootTest for everything makes CI slow and flaky.
5. Good tests document contracts — bad tests freeze implementation details.
6. Today — unit, slice, MockMvc, Testcontainers, and what to assert.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Seven.
2. Spring Testing.

### Scene `pyramid` (renderer: `pyramid`)

1. Start with the test pyramid for Spring apps.
2. Unit tests — pure Java, mocks for collaborators, no ApplicationContext.
3. Slice tests — WebMvcTest, DataJpaTest — load only the layer under test.
4. Integration tests — SpringBootTest with a real or containerized stack.
5. End-to-end tests — few, precious, against a deployed-like environment.
6. Push assertions down the pyramid — speed is a feature of the suite.

### Scene `unit_slice` (renderer: `unit_slice`)

1. Unit and slice testing patterns.
2. Constructor injection makes unit tests trivial — new Service with mocks.
3. WebMvcTest stands up controllers — MockMvc drives HTTP without a server.
4. DataJpaTest boots repositories against an embedded or Testcontainers DB.
5. MockBean replaces a collaborator inside a slice context.
6. Prefer AssertJ fluent assertions — readable failures save debug time.

### Scene `spring_boot_test` (renderer: `spring_boot_test`)

1. When SpringBootTest earns its cost.
2. Full context catches wiring mistakes auto-config and security filters create.
3. Use RANDOM_PORT only when you truly need a listening server.
4. Override properties for tests — never point CI at production databases.
5. DirtiesContext sparingly — it is expensive and often hides design smells.
6. If every test needs a full boot, your modules are too entangled.

### Scene `testcontainers` (renderer: `testcontainers`)

1. Testcontainers bring realistic dependencies to CI.
2. Postgres, Kafka, LocalStack — same engines your service talks to.
3. Reuse containers across a suite when the framework supports it.
4. Pair with DynamicPropertySource to inject JDBC URLs at runtime.
5. Slower than H2 — faster than debugging prod-only SQL dialects.
6. Use them for persistence and messaging contracts — not every unit test.

### Scene `what_to_assert` (renderer: `what_to_assert`)

1. Assert behavior, not framework internals.
2. HTTP status, response body shape, and headers clients rely on.
3. Database side effects after a successful command.
4. Security — anonymous gets four-oh-one, forbidden role gets four-oh-three.
5. Avoid asserting log lines or private field values.
6. Name tests as contracts — createOrder_rejectsNegativeQuantity.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — SpringBootTest on every class — hour-long pipelines.
3. Two — shared mutable database state between tests — order-dependent flakes.
4. Three — testing only the happy path — auth and validation unproven.
5. Also — over-mocking until the test only proves the mock framework works.
6. Test the risk — not the annotation count.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you test a Spring Boot service?
2. Unit-test domain and services with mocks — no container.
3. Slice-test web and JPA layers with WebMvcTest and DataJpaTest.
4. Reserve SpringBootTest plus Testcontainers for wiring and persistence truth.
5. Always cover authz negative paths and validation errors.
6. Optimize for fast feedback — full context is a scalpel, not a hammer.

### Scene `teaser` (renderer: `teaser`)

1. One service is solid — next we split the system.
2. Episode Seventy-Eight — Microservices Basics.
3. When to split, service boundaries, sync versus async, and operational cost.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **77** — *Spring Testing*.
- **Series catalog:** Episode 77 ↔ handbook lesson 77 — *Spring Testing*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Six secured APIs with Spring Security's filter chain._
- **`title`** — starts from: _Episode Seventy-Seven._
- **`pyramid`** — starts from: _Start with the test pyramid for Spring apps._
- **`unit_slice`** — starts from: _Unit and slice testing patterns._
- **`spring_boot_test`** — starts from: _When SpringBootTest earns its cost._
- **`testcontainers`** — starts from: _Testcontainers bring realistic dependencies to CI._
- **`what_to_assert`** — starts from: _Assert behavior, not framework internals._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you test a Spring Boot service?_
- **`teaser`** — starts from: _One service is solid — next we split the system._
