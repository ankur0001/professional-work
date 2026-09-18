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

A green `@WebMvcTest` can still hide a broken `@Transactional` boundary or a security matcher that rejects the booth scanner. Integration tests load more of the real Boot application — often with `@SpringBootTest` and `MockMvc` or a random-port `TestRestTemplate` — and exercise the gate release flow as collaborators wire together.

```java
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class GateReleaseFlowIT {

    @Autowired
    MockMvc mockMvc;

    @Autowired
    GateLedgerRepository ledger;

    @MockBean
    BillingClient billing;

    @BeforeEach
    void stubBilling() {
        when(billing.quote(anyString(), anyString()))
                .thenReturn(new TariffQuote(Money.of("108.00"), "USD"));
        when(billing.createInvoice(any()))
                .thenReturn(new InvoiceAck("INV-9", InvoiceStatus.OPEN));
        ledger.deleteAll();
    }

    @Test
    @WithMockUser(roles = "GATE_OPERATOR")
    void operatorCanReleaseThroughHttp() throws Exception {
        mockMvc.perform(post("/gates/G12/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"containerId":"MSCU123","hazardClass":"IMDG_3","plate":"SGP-4421"}
                                """))
                .andExpect(status().isAccepted());

        assertTrue(ledger.findByContainerId("MSCU123").isPresent());
        verify(billing).createInvoice(any(InvoiceRequest.class));
    }

    @Test
    void anonymousIsRejected() throws Exception {
        mockMvc.perform(post("/gates/G12/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"containerId":"MSCU123","hazardClass":"NONE","plate":"SGP-4421"}
                                """))
                .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "GATE_OPERATOR")
    void billingFailureSurfacesAsProblemJson() throws Exception {
        when(billing.quote(anyString(), anyString()))
                .thenThrow(new BillingUnavailableException("billing down"));

        mockMvc.perform(post("/gates/G12/check-ins")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"containerId":"MSCU999","hazardClass":"IMDG_3","plate":"SGP-9"}
                                """))
                .andExpect(status().isServiceUnavailable())
                .andExpect(jsonPath("$.title").exists());

        assertTrue(ledger.findByContainerId("MSCU999").isEmpty());
    }
}
```

Read what is real and what is faked. Spring Security, MVC, the ledger repository, and transactional proxies are real. Billing stays a `@MockBean` so the test does not need a live billing pod — you are proving gate’s flow, not billing’s SQL. Assert side effects in the ledger, not only HTTP 202. The billing-failure case proves the transactional boundary: no ledger row when quoting dies mid-flow. Anonymous access must fail if the booth scanner is supposed to authenticate.

Random-port style catches serialization and client configuration that MockMvc can miss:

```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class GateReleaseHttpIT {

    @Autowired
    TestRestTemplate http;

    @Test
    void healthIsUp() {
        ResponseEntity<String> response = http.getForEntity("/actuator/health", String.class);
        assertEquals(HttpStatus.OK, response.getStatusCode());
    }
}
```

Keep integration profiles pointed at isolated databases — embedded, ephemeral containers, or per-job schemas. Shared staging schemas make parallel CI jobs collide and produce ghosts: one job deletes rows another just asserted. `@DirtiesContext` is a blunt hammer when bean state leaks; prefer cleanup in `@BeforeEach` and immutable test data ids. Transactional tests that roll back automatically are convenient until you assert on data visible only after commit — know whether your test transaction wraps the HTTP call.

Runtime cost is the trade-off you feel. Full context startup dominates wall time; context caching across classes helps when configurations match. Too many unique `@MockBean` sets break that cache and CI slows for invisible reasons. Symptom: “integration suite used to be four minutes, now twenty” after every test class invented its own mock set. Another runtime tell: a test passes with MockMvc but fails on `RANDOM_PORT` because a filter only runs on the real servlet path, or because JSON dates serialize differently through `TestRestTemplate`’s message converters.

Security and transactions are why this layer exists. `@WithMockUser` proves matchers; it does not prove JWT parsing. If gate’s booth scanners send bearer tokens, add at least one test that builds a signed test token — or accept that token wiring lives in a narrower security test. For `@Transactional` on `releaseGate`, assert both the happy ledger write and the empty ledger after a mid-flow billing failure; that is the integration bug `@WebMvcTest` will never see.

A misconception is replacing unit tests with integration tests because “they catch more.” They catch different things and cost more CPU. Another is asserting only status codes without ledger side effects. A third is `@MockBean` on so many types that the test no longer integrates anything meaningful.

Mocked billing and in-memory stores still skip the SQL dialect you ship. When `VesselRepository` must prove derived queries against real Postgres, reach for Testcontainers. Keep a short matrix in the team’s head: Mockito for tariff branches, `@WebMvcTest` for JSON and validation, `@SpringBootTest` for security-plus-ledger wiring, containers for SQL truth — each layer answers a different lie the previous one can tell.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 96 (*Integration Testing*).
