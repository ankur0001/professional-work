# Episode 96 — Integration Testing

| Field | Value |
|---|---|
| Episode | 96 |
| Title | Integration Testing |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 96 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Unit tests prove a class. Slice tests prove a layer. Integration tests prove that several real pieces cooperate: HTTP in, security filters, service logic, persistence out — or messaging round trips — with as few doubles as the risk requires. In Spring terms that often means `@SpringBootTest` with a running web environment, test properties, and either an embedded database or an external one the suite can reach.

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("integration")
class OrderCheckoutIntegrationTest {

    @LocalServerPort
    int port;

    @Autowired
    TestRestTemplate rest;

    @Autowired
    OrderRepository orders;

    @Test
    void checkoutPersistsAndReturnsAccepted() {
        PlaceOrderRequest body = new PlaceOrderRequest("SKU-1", 1, "cust-9");

        ResponseEntity<OrderResponse> response = rest.postForEntity(
                "http://localhost:" + port + "/orders",
                body,
                OrderResponse.class);

        assertEquals(HttpStatus.ACCEPTED, response.getStatusCode());
        assertTrue(orders.findById(response.getBody().id()).isPresent());
    }
}
```

`RANDOM_PORT` starts the embedded server on an ephemeral port; `@LocalServerPort` injects it. `TestRestTemplate` or `WebTestClient` exercises the real stack including filters and converters. That catches wiring bugs `@WebMvcTest` will never see: a security rule that blocks POST, a `Filter` that mishandles content types, a missing bean that only appears when the full configuration loads.

Integration scope is a judgment call. Some teams include Testcontainers-backed Postgres in what they call integration tests; others reserve that name for in-process Boot tests with H2 and use “contract” or “component” for containerized suites. Agree on vocabulary in the team. The technical point is the same: more real collaborators, slower feedback, higher confidence about wiring.

```java
@SpringBootTest
@AutoConfigureMockMvc
@Import(TestSecurityConfig.class)
class OrderSecurityIntegrationTest {

    @Autowired
    MockMvc mockMvc;

    @Test
    @WithMockUser(roles = "CUSTOMER")
    void customerCanPlaceOrder() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                            {"sku":"SKU-1","qty":1,"customerId":"cust-9"}
                            """))
                .andExpect(status().isAccepted());
    }

    @Test
    void anonymousIsUnauthorized() throws Exception {
        mockMvc.perform(post("/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("{}"))
                .andExpect(status().isUnauthorized());
    }
}
```

Here the server may stay mock-based (`MockMvc`) while security and validation still run for real. That middle ground is still integration: multiple framework subsystems, one process.

Compare the pyramid out loud. Lots of Mockito unit tests for branching. Fewer Spring slices for MVC and JPA mapping. Still fewer random-port integration tests for security and filter order. Rare full-environment journeys. If your pyramid is upside down — everything is `@SpringBootTest` — builds slow down and failures become harder to localize.

Messaging integrations deserve the same honesty. An `@SpringBootTest` that publishes to an embedded broker — or a Testcontainers Kafka in the next episode — and waits until a listener writes a row proves the binder wiring that unit-mocked `Consumer` beans never see. Use Awaitility with a clear condition on the repository rather than `Thread.sleep(2000)` that flakes on slow CI agents.

```java
await().atMost(Duration.ofSeconds(5))
        .untilAsserted(() ->
                assertTrue(orders.findById(orderId).isPresent()));
```

Flakes appear when integration tests share mutable resources — fixed ports, shared database rows, timing on async listeners. Prefer random ports, transactional rollback or unique keys per test, and deterministic waits on messaging. Clean `@DirtiesContext` is a last resort when a test poisons the cached context; overuse destroys suite speed.

A misconception is replacing unit tests with integration tests because “they catch more.” They catch different things and cost more CPU. Another is asserting only HTTP 200 without checking side effects in the database or outbox table — you have tested a stubbed smile. A third is pointing integration profiles at shared staging services so parallel CI jobs collide.

Today we widened the lens: Boot on a random port, real HTTP calls, security-aware MockMvc flows, and discipline around shared state — confidence in wiring, not only in isolated classes.

H2 will forgive SQL that Postgres rejects. JSONB, locking, and sequences differ across engines. When the integration risk is the database itself, an embedded substitute is not enough.

That gap is why Testcontainers exists.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 96 (*Integration Testing*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
