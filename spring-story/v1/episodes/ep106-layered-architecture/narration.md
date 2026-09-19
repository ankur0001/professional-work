# Episode 106 — Layered Architecture

| Field | Value |
|---|---|
| Episode | 106 |
| Title | Layered Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 106 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Gate is ops-ready and still structurally muddy: controllers call repositories, tariff rules sit in a `@RestController`, JPA entities serialize straight to truckers. Layered architecture is the classic Spring map — web → service → persistence — with dependency arrows pointing inward toward the domain, not outward toward frameworks.

In a harbor app the packages usually look like:

```text
com.harbor.gate
  web          // controllers, HTTP DTOs
  service      // GateReleaseService, tariff orchestration
  domain       // GateRelease, TruckCheckIn value types
  persistence  // Spring Data repositories, JPA entities
```

```java
@RestController
@RequestMapping("/gates")
public class GateController {
    private final GateReleaseService releases;

    public GateController(GateReleaseService releases) {
        this.releases = releases;
    }

    @PostMapping("/{gateId}/check-ins")
    ResponseEntity<CheckInResponse> checkIn(@PathVariable String gateId,
                                            @Valid @RequestBody CheckInRequest body) {
        CheckInResponse response = releases.releaseGate(gateId, body.toCommand());
        return ResponseEntity.accepted().body(response);
    }
}

@Service
public class GateReleaseService {
    private final GateLedgerRepository ledger;
    private final BillingClient billing;

    public GateReleaseService(GateLedgerRepository ledger, BillingClient billing) {
        this.ledger = ledger;
        this.billing = billing;
    }

    @Transactional
    public CheckInResponse releaseGate(String gateId, TruckCheckIn cmd) {
        TariffQuote quote = billing.quote(cmd.containerId(), cmd.hazardClass());
        GateRelease saved = ledger.save(GateRelease.open(gateId, cmd, quote));
        return CheckInResponse.from(saved);
    }
}
```

Discipline at the boundary: HTTP DTOs in `web`, domain commands in `service`/`domain`, JPA entities stay in `persistence` unless you consciously accept the coupling. Walk a leak. `GateRelease` entity gains a `Lazy` collection; Jackson serializes it on the way out; a trucker GET triggers `LazyInitializationException` or an accidental N+1. The layered fix is a dedicated `CheckInResponse` assembled in the service — not “open session in view” as architecture. Another leak: controller injects `GateLedgerRepository` and duplicates release rules for a “quick” admin path until two definitions of release diverge at 2am.

ArchUnit can enforce “web does not import persistence” when code review fatigue sets in.

```java
@ArchTest
static final ArchRule webMustNotTouchPersistence =
        noClasses().that().resideInAPackage("..web..")
                .should().dependOnClassesThat().resideInAPackage("..persistence..");

@ArchTest
static final ArchRule servicesDoNotReturnResponseEntity =
        noClasses().that().resideInAPackage("..service..")
                .should().dependOnClassesThat().resideInAPackage("org.springframework.http..");
```

Runtime and team symptoms of layer collapse: every feature touches four packages for one field rename; mobile breaks when a JPA column rename ships because the entity was the API; transactional boundaries unclear because repositories are called from controllers without a service. Layers still help onboarding — most Spring developers can navigate web/service/persistence in minutes — but package names without dependency direction are cosplay.

Trade-offs: strict layering adds mapping boilerplate (DTO ↔ domain ↔ entity). That cost buys independent change rates: HTTP can version while persistence evolves. For tiny admin CRUD, a thinner path may be fine — document the exception so gate release does not copy it. A single `service` package that absorbs everything becomes a dumping ground; split by capability (`release`, `tariff`, `ais`) before you invent microservices to escape the ball of mud.

Onboarding test: a new engineer should find “where does check-in authorization live?” in one service method, not half in the controller and half in a repository `@Query`. When that answer takes a tour of four packages with duplicated ifs, layers have already collapsed regardless of folder names. Fix by moving policy inward and leaving web as translation — status codes, JSON, validation annotations — not berth or tariff rules.

A misconception is renaming packages without changing dependencies and calling it architecture. Another is a single `service` package that becomes a dumping ground for everything not named controller. A third is forbidding DTOs “to move faster” and then breaking mobile clients when a JPA field rename ships.

When the pain is “domain must not know Spring Web or JPA at all,” layers need ports, adapters, and an inside that stays pure. That tightening is hexagonal architecture around gate release — same harbor check-in story, stricter arrows, fewer excuses for a controller that speaks SQL.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 106 (*Layered Architecture*).
