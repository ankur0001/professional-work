# Episode 98 — Contract Testing

| Field | Value |
|---|---|
| Episode | 98 |
| Title | Contract Testing |
| Phase | Phase 10 — Testing |
| Catalog handbook lesson | 98 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Gate’s `BillingClient` expects `GET /tariffs/quote` to return `{ "amount": "108.00", "currency": "USD" }`. Billing renames `amount` to `total` on a Friday. Gate’s Feign decoder fails on Monday’s shift change. Neither side’s unit tests lied — they never shared a wire contract. Contract testing makes that share explicit: a pact or Spring Cloud Contract stub that billing must satisfy and gate can consume in CI.

With Spring Cloud Contract, billing authors a contract DSL; the build generates verification tests for the producer and stub jars for consumers. Gate’s tests run Feign against the stub, not against a hope.

```groovy
// billing-service contract: shouldReturnTariffQuote.groovy
Contract.make {
    description("quote for container + hazard")
    request {
        method GET()
        urlPath("/tariffs/quote") {
            queryParameters {
                parameter("containerId", "MSCU123")
                parameter("hazardClass", "IMDG_3")
            }
        }
    }
    response {
        status 200
        headers {
            contentType(applicationJson())
        }
        body([
                amount  : "108.00",
                currency: "USD"
        ])
        bodyMatchers {
            jsonPath('$.amount', byRegex('[0-9]+\\.[0-9]{2}'))
            jsonPath('$.currency', byEquality())
        }
    }
}
```

```java
@SpringBootTest
@AutoConfigureStubRunner(
        ids = "com.harbor:billing-service:+:stubs:0",
        stubsMode = StubRunnerProperties.StubsMode.LOCAL)
class GateBillingContractTest {

    @Autowired
    BillingClient billing;

    @Test
    void feignMatchesBillingStub() {
        TariffQuote quote = billing.quote("MSCU123", "IMDG_3");
        assertEquals("USD", quote.currency());
        assertEquals(new BigDecimal("108.00"), quote.amount());
    }
}
```

Producer side: billing’s CI runs the generated smoke tests against its controllers — if the stub says 200 with `amount`, the controller must still do that. Rename the JSON field without updating the contract and producer verification fails before merge. Consumer side: gate’s CI downloads stubs and exercises `BillingClient`. Breaking the contract breaks the build before the quay feels it. Walk the Friday rename with contracts in place: billing’s build turns red on verification; gate never ships a decoder that expects a missing field.

Contracts are not end-to-end substitutes. They lock shapes and status codes at the boundary. Business sequencing — check-in then invoice — still needs integration or journey tests. Prefer dedicated client DTOs on both sides so contract fields do not drag JPA entities across jars. Version stub artifacts so gate can pin a known-good billing stub while billing develops the next incompatible change on a new contract file.

Failure symptoms without contracts: Feign `DecodeException` at 06:00 after a billing deploy; each team’s green pipeline; blame traveling across Slack. With contracts too loose (`byRegex(".*")` on every field), the same outage returns because nothing forced `amount` to stay a money string. With stubs published once and never re-verified, drift accumulates silently until a consumer bumps the stub version.

Trade-offs: consumer-driven contracts (Pact-style) put gate in charge of expectations; producer-first Contract DSL puts billing in charge of publishing stubs. Either works if both pipelines run. Contracts add build complexity; they pay off when multiple consumers (gate, scheduling, ops tooling) depend on billing’s HTTP shape. Do not contract every admin CRUD endpoint on day one — start with the tariff quote path that stops trucks when it breaks.

Walk a coordinated change. Billing must add `degraded` to the quote JSON. Update the contract body and matchers first; regenerate stubs; fix gate’s DTO and Feign decoder; merge producer verification green; then consumers bump the stub version. Reversing that order — ship billing first — recreates Monday’s decoder failure with extra ceremony. Contracts are a change protocol, not only a test type.

A misconception is writing contracts so loose (`byRegex(".*")` everywhere) that they never fail. Another is generating stubs once and never re-running producer verification. A third is treating contracts as documentation only without wiring them into both pipelines.

Green contracts and green tariff tests still leave a production question unanswered: how slow is `releaseGate`, for whom, since when? Phase 11 starts with meters, not dashboards.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 98 (*Contract Testing*).
