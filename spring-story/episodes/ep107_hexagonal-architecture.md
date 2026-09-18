# Episode 107 — Hexagonal Architecture

| Field | Value |
|---|---|
| Episode | 107 |
| Title | Hexagonal Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 107 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Layered Spring apps often still let the framework sit in the middle of the onion. A “domain” class annotated with JPA and Jackson, a service that returns `ResponseEntity`, a repository interface that extends Spring Data in the same package as release rules — the layers have names, but the center is not isolated. Hexagonal architecture — ports and adapters — flips the gravity for gate release: the domain sits in the center; HTTP, billing Feign, and JPA plug in around it.

Alistair Cockburn’s idea is concrete here. The application core defines ports — interfaces for what drives gate release and what release needs. Adapters implement those ports. The core never imports Spring Web. Boot remains the composition root that wires adapters to ports.

Draw one hexagon for gate release:

- Driving (primary) port: `ReleaseGateUseCase` — what the booth can ask the app to do.
- Driven (secondary) ports: `GateLedger`, `BillingPort` — what release needs from the outside.
- Adapters: `GateController` (MVC) drives the use case; `JpaGateLedgerAdapter` and `BillingFeignAdapter` implement driven ports.

```java
// domain + application core — no Spring Web imports
public interface ReleaseGateUseCase {
    GateRelease release(ReleaseGateCommand command);
}

public interface GateLedger {
    GateRelease save(GateRelease release);
}

public interface BillingPort {
    TariffQuote quote(String containerId, HazardClass hazard);
}

public class ReleaseGateService implements ReleaseGateUseCase {
    private final GateLedger ledger;
    private final BillingPort billing;

    public ReleaseGateService(GateLedger ledger, BillingPort billing) {
        this.ledger = ledger;
        this.billing = billing;
    }

    @Override
    public GateRelease release(ReleaseGateCommand command) {
        TariffQuote quote = billing.quote(command.containerId(), command.hazard());
        return ledger.save(GateRelease.open(command, quote));
    }
}
```

```java
// adapter — Spring Web talks to the port only
@RestController
@RequestMapping("/gates")
public class GateController {
    private final ReleaseGateUseCase releaseGate;

    public GateController(ReleaseGateUseCase releaseGate) {
        this.releaseGate = releaseGate;
    }

    @PostMapping("/{gateId}/check-ins")
    public CheckInResponse post(@PathVariable String gateId,
                                @Valid @RequestBody CheckInRequest body) {
        GateRelease released = releaseGate.release(body.toCommand(gateId));
        return CheckInResponse.from(released);
    }
}
```

```java
// adapter — Feign behind the driven port
@Component
public class BillingFeignAdapter implements BillingPort {
    private final BillingClient client;

    public BillingFeignAdapter(BillingClient client) {
        this.client = client;
    }

    @Override
    public TariffQuote quote(String containerId, HazardClass hazard) {
        return client.quote(containerId, hazard.name());
    }
}
```

Unit tests construct `ReleaseGateService` with fake `BillingPort` and `GateLedger` — no MockMvc required for tariff branching. Slice tests cover the MVC adapter. Production wiring is a `@Configuration` that binds interfaces to adapters. The hexagon is not a folder religion; it is dependency direction you can point at in review.

A misconception is drawing hexagons in Confluence while controllers still call Feign clients directly. Another is ports for every trivial getter until the core is an interface museum. A third is putting Spring Data interfaces in the domain package and declaring victory because the folder says `domain`.

Hexagonal’s cousin names the same gravity with rings and an explicit dependency rule: source code dependencies point only inward. That formulation is Clean Architecture — and it sharpens what the gate domain may import.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 107 (*Hexagonal Architecture*).
