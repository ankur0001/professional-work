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

Testcontainers proved your service talks to a real database. It did not prove that inventory still returns the JSON your Feign client deserializes after their team ships on Friday. End-to-end environments catch that late and flaky. Contract testing catches it earlier: consumer and provider agree on a document — requests and responses — and each side verifies against that document in isolation.

Spring Cloud Contract is the Spring-centric tooling for this. You write contracts — often Groovy or YAML DSL — that describe an HTTP interaction. From those contracts the framework can generate producer-side tests that fail if the controller no longer satisfies the spec, and stub runners that give the consumer a WireMock-like stub in tests so Feign clients keep working without the real provider process.

```groovy
// contracts/inventory/should_return_stock.groovy
Contract.make {
    description "stock by sku"
    request {
        method GET()
        url "/stock/SKU-1"
    }
    response {
        status 200
        headers {
            contentType(applicationJson())
        }
        body([
            sku      : "SKU-1",
            available: 5
        ])
    }
}
```

On the producer (inventory), the build generates a test that performs `GET /stock/SKU-1` against the Spring context and asserts status and body fragments. If someone renames `available` to `qtyAvailable` without updating the contract, the producer build breaks — before consumers discover it in staging.

On the consumer (order), `@AutoConfigureStubRunner` downloads or locates the stub jar built from those contracts and starts stubs on a port. Your Feign client points at that stub during tests.

```java
@SpringBootTest
@AutoConfigureStubRunner(
        ids = "com.example:inventory-service:+:stubs:0",
        stubsMode = StubRunnerProperties.StubsMode.LOCAL)
class OrderServiceContractTest {

    @Autowired
    InventoryClient inventory;

    @Test
    void readsStockFromStub() {
        StockView stock = inventory.getStock("SKU-1");
        assertEquals(5, stock.available());
    }
}
```

The flow across teams becomes a pipeline: contracts live in the producer repo (or a shared contract repo), producer CI publishes stub artifacts, consumer CI runs against stubs at a known version. That is consumer-driven contract testing when consumers propose contracts; it is provider-driven when the provider publishes and consumers must follow. Either way, the artifact is the agreement, not a wiki screenshot of JSON.

Contracts also work for messaging — message inputs and outputs — which pairs cleanly with Spring Cloud Stream from earlier. The same idea holds: generate tests for the producer of the message and stubs for the listener side.

Producer-side generated tests usually sit under `generated-test-sources` and run with the provider’s Spring context — often `@AutoConfigureMockMvc` style under the hood. When a generated test fails, read the contract first, then the controller mapping. The failure means the live API drifted from the agreed document; either fix the API or deliberately revise the contract and republish stubs so consumers can adapt in the same change train.

WireMock stubs from contracts are not an excuse to skip consumer logic tests. They freeze the HTTP conversation so your Feign mapping and domain branching can run quickly. Pair them with a few true integration tests against a real inventory in a shared environment when the risk warrants it.

A misconception is treating contracts as end-to-end tests. They do not prove business workflows across real deployments; they prove shape and status compatibility at the boundary. Another is duplicating every internal field in contracts until churn makes teams disable the suite — contract the fields consumers need. A third is never versioning stubs, so consumers silently float to incompatible producer stubs.

Today we used a contract to lock `GET /stock/SKU-1`, generate producer verification, and run the order Feign client against stubs — breaking builds on incompatible API changes before production does.

You can test units, slices, containers, and contracts and still fly blind in production if you cannot see live latency, error rates, and traffic. After confidence in the build comes telemetry in the running system.

That telemetry starts with Micrometer.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 98 (*Contract Testing*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
