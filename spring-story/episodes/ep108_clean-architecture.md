# Episode 108 — Clean Architecture

| Field | Value |
|---|---|
| Episode | 108 |
| Title | Clean Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 108 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Hexagonal said ports and adapters for gate release. Clean Architecture — Robert C. Martin’s rings — states the dependency rule bluntly: source code dependencies point only inward. The domain must not import Spring Web. Controllers, Feign, and JPA may depend on the domain; the domain depends on nothing from those frameworks.

Map the rings onto the harbor gate service:

1. **Entities** — `GateRelease`, `HazardClass`, money invariants.
2. **Use cases** — `ReleaseGateInteractor`, input/output models. Pure Java; depends only on entities and outbound ports.
3. **Interface adapters** — MVC controllers, presenters, JPA gateways, Feign billing adapters.
4. **Frameworks & drivers** — Spring Boot, the servlet container, Postgres drivers.

```java
public record ReleaseGateInput(String gateId, String containerId, HazardClass hazard) {}
public record ReleaseGateOutput(String releaseId, String status, Money charged) {}

public class ReleaseGateInteractor {
    private final GateLedger ledger;
    private final BillingPort billing;

    public ReleaseGateInteractor(GateLedger ledger, BillingPort billing) {
        this.ledger = ledger;
        this.billing = billing;
    }

    public ReleaseGateOutput execute(ReleaseGateInput input) {
        TariffQuote quote = billing.quote(input.containerId(), input.hazard());
        GateRelease saved = ledger.save(GateRelease.open(input, quote));
        return new ReleaseGateOutput(saved.id(), saved.status().name(), quote.amount());
    }
}
```

```java
@RestController
@RequestMapping("/gates")
public class ReleaseGateController {
    private final ReleaseGateInteractor interactor;

    public ReleaseGateController(ReleaseGateInteractor interactor) {
        this.interactor = interactor;
    }

    @PostMapping("/{gateId}/check-ins")
    ReleaseGateResponse post(@PathVariable String gateId,
                             @Valid @RequestBody CheckInRequest body) {
        ReleaseGateOutput out = interactor.execute(body.toInput(gateId));
        return ReleaseGateResponse.from(out);
    }
}
```

Where does `@Transactional` live? Often on the adapter or a thin application service around the interactor — not on domain entities. The dependency rule cares about imports: if `GateRelease.java` contains `import org.springframework.web.bind.annotation...`, you broke the ring regardless of folder names. ArchUnit can assert that `..domain..` does not depend on `org.springframework.web..` or `org.springframework.data..`.

Walk a violation that bites at runtime. An entity annotated with both JPA and Jackson live on the wire; a lazy field serializes after the session closes; truckers see 500s. Clean’s pressure is to keep `GateRelease` free of those annotations so adapters map explicitly. Another violation: use case imports `FeignException` and branches on HTTP status — billing transport details leaked inward; prefer a domain `BillingUnavailable` mapped at the adapter.

Clean and hexagonal overlap heavily in Spring shops. Use whichever vocabulary your team shares; enforce the same arrow: frameworks outward, policy inward. Pragmatism still applies — not every admin CRUD screen needs a full interactor ceremony on day one. Carve rings where change and risk concentrate: gate release, tariff quoting, berth assignment. Composition root remains Spring: `@Configuration` beans wire `ReleaseGateInteractor` with JPA and Feign adapters at the outer ring.

Failure symptoms of cargo-cult Clean: package names copied from a blog while entities still import Spring Web; every class named `*Impl` twice; use cases that are pass-throughs with no policy — ceremony without benefit. Opposite failure: a “pragmatic” domain that absorbs controllers until tests need MockMvc to prove money rounding.

Trade-offs: more types and mappers versus a domain you can unit-test with plain `new` and fakes. Teams new to the harbor often start layered and extract rings when Spring imports appear in core. Do not rewrite the whole monolith overnight for purity points.

A practical gate: can `ReleaseGateInteractorTest` run without `@SpringBootTest`? If yes, the ring is earning its keep. If every policy test needs MockMvc and a DataSource, Spring has crept inward and the dependency rule is theater. Fix imports first; rename packages second.

A misconception is “Clean Architecture means no Spring.” Spring is an excellent outer-ring composition root. Another is copying package templates from a blog without moving imports. A third is putting JPA annotations on entities “temporarily” until temporary becomes the permanent domain model.

Rings protect dependency direction. They do not by themselves give you a shared language for berth capacity, reservations, and what “assigned” means to scheduling versus billing. That language work is domain-driven design around the `Berth` aggregate.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 108 (*Clean Architecture*).
