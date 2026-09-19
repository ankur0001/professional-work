# Episode 88 — Feign Client

| Field | Value |
|---|---|
| Episode | 88 |
| Title | Feign Client |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 88 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Every gate class that quotes a tariff should not re-encode the same GET path, query params, and JSON binding. OpenFeign — through Spring Cloud OpenFeign — lets gate declare a `BillingClient` interface that mirrors billing’s HTTP API. A runtime proxy turns method calls into load-balanced requests. The interface becomes the anti-corruption layer between gate’s domain and billing’s wire format.

Enable clients on the Boot application, then write the interface. The `name` attribute is the service id discovery and load balancing already understand.

```java
@SpringBootApplication
@EnableFeignClients
public class GateServiceApplication {
    public static void main(String[] args) {
        SpringApplication.run(GateServiceApplication.class, args);
    }
}

@FeignClient(name = "billing-service")
public interface BillingClient {

    @GetMapping("/tariffs/quote")
    TariffQuote quote(@RequestParam("containerId") String containerId,
                      @RequestParam("hazardClass") String hazardClass);

    @PostMapping("/invoices")
    InvoiceAck createInvoice(@RequestBody InvoiceRequest request);
}
```

```java
@Service
public class GateReleaseService {
    private final BillingClient billing;
    private final GateLedger ledger;

    public GateReleaseService(BillingClient billing, GateLedger ledger) {
        this.billing = billing;
        this.ledger = ledger;
    }

    public CheckInResponse accept(String gateId, TruckCheckIn req) {
        TariffQuote quote = billing.quote(req.containerId(), req.hazardClass());
        InvoiceAck invoice = billing.createInvoice(
                new InvoiceRequest(req.containerId(), quote.amount(), gateId));
        return ledger.record(gateId, req, quote, invoice);
    }
}
```

Read the dependency direction. `GateReleaseService` depends on `BillingClient` the way it would depend on a local port. No URL string lives in the service. At runtime, Feign builds a JDK proxy. `quote("MSCU123", "3")` becomes a GET to a chosen `billing-service` instance at `/tariffs/quote?...`. Encoders and decoders handle JSON. Setting `url` on `@FeignClient` bypasses discovery — fine for a third-party tide vendor, wrong for internal billing you want balanced across three pods.

Production knobs matter. Connect and read timeouts, logger levels for bodies, request interceptors for service-to-service tokens, and error decoders that map HTTP 409 into `TariffConflictException` keep failures typed. Contract drift — billing renames `hazardClass` — still fails at runtime; Feign does not invent schema evolution.

```java
@FeignClient(
        name = "billing-service",
        configuration = BillingFeignConfig.class,
        fallback = BillingClientFallback.class)
public interface BillingClient {
    // ...
}
```

Fallbacks hint at the resilience story ahead. A fallback is deliberate degraded mode — last-known tariff, queue-for-later invoice — not a silent success that hides an outage from the booth supervisor.

A misconception is generating a Feign method for every billing controller endpoint and then chatting in loops from gate; design coarser remote operations. Another is sharing billing’s JPA entities as Feign DTOs across jars until the services cannot deploy independently. A third is forgetting Feign is blocking by default in many setups — if gate is WebFlux end to end, evaluate WebClient instead of forcing Feign onto the event loop.

Declarative clients make the gate↔billing hop easy. Easy remote calls also make cascading failure easy. When billing starts timing out, do gate threads keep piling into a dead dependency until every booth freezes?

That failure mode is why circuit breakers exist.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 88 (*Feign Client*).
