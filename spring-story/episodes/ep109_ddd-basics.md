# Episode 109 — DDD Basics

| Field | Value |
|---|---|
| Episode | 109 |
| Title | DDD Basics |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 109 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

CRUD honesty fails on the quay. A row named `berths` with columns `status` and `vessel_id` does not explain why two schedulers cannot both reserve B7 for overlapping windows, or why billing says “reserved” while the yard says “empty.” Domain-driven design starts with ubiquitous language and bounded contexts — then protects invariants inside aggregates like `Berth`.

In the scheduling context, people say *assign*, *reserve*, *release*, *conflict*, *tidal window*. In billing, the same physical quay might be *billable reservation* and *demurrage start*. Do not force one God model. Bounded contexts allow different models that integrate deliberately — often through events or anti-corruption adapters. When a ticket says “fix berth status,” ask which language the speaker is using before you touch a column.

```java
public class Berth {
    private final BerthId id;
    private BerthStatus status;
    private ImoNumber occupiedBy;
    private final List<ReservationWindow> reservations = new ArrayList<>();

    public BerthReserveResult reserve(ImoNumber imo, ReservationWindow window) {
        if (status == BerthStatus.OUT_OF_SERVICE) {
            return BerthReserveResult.rejected("berth out of service");
        }
        boolean overlaps = reservations.stream().anyMatch(r -> r.overlaps(window));
        if (overlaps) {
            return BerthReserveResult.rejected("overlapping reservation");
        }
        reservations.add(ReservationWindow.forImo(imo, window));
        status = BerthStatus.RESERVED;
        occupiedBy = imo;
        return BerthReserveResult.accepted(new BerthReserved(id, imo, window));
    }
}
```

```java
@Service
public class ReserveBerthService {
    private final BerthRepository berths;
    private final ApplicationEventPublisher events;

    @Transactional
    public void reserve(BerthId id, ImoNumber imo, ReservationWindow window) {
        Berth berth = berths.findById(id).orElseThrow();
        BerthReserveResult result = berth.reserve(imo, window);
        if (!result.accepted()) {
            throw new BerthConflictException(result.reason());
        }
        berths.save(berth);
        events.publishEvent(result.event());
    }
}
```

The aggregate root is `Berth`. Outside code does not sprinkle `reservations.add` on a list from a controller — it calls `reserve` so overlaps stay impossible to forget. Repositories load and save aggregates, not arbitrary rows for every join the UI wants. Domain events like `BerthReserved` speak the language of the context and become integration points later.

Walk a concurrency failure. Two schedulers load B7, both see no overlap, both call `reserve`, both save. Without optimistic locking (`@Version` on the aggregate) or a DB exclusion constraint on windows, you get a double booking that the domain method alone cannot see across transactions. DDD does not replace transactional discipline; it concentrates the rules where they belong and still needs persistence concurrency control. Symptom in ops: two vessels told they own B7; yard crane chaos; billing double-charges.

DDD is not mandatory ceremony for every screen. A simple reference-data editor for hazard codes may stay CRUD. Use aggregates where invariants hurt when violated — berth conflicts, gate release against unpaid invoices, tally counts that must match the manifest. Value objects (`BerthId`, `ImoNumber`, `Money`) kill primitive obsession — a method that accepts three `String`s will swap gate id and IMO eventually.

Failure symptoms of anemic models: `BerthManager` services with all the ifs, entities that are bags of getters, and every new rule added in a controller “just this once.” Opposite ceremony: aggregates spanning half the quay graph so every reservation loads the world — keep aggregate boundaries tight around consistency needs, not around the ER diagram.

Trade-offs: richer models cost design time and careful mapping to ORM. They pay off when rules change weekly and bugs are expensive. Ubiquitous language meetings sound soft; they prevent scheduling and billing from shipping incompatible meanings of “reserved.”

A misconception is equating DDD with microservices — you can have rich aggregates in a modular monolith. Another is anemic “entities” that are only getters/setters with all rules in services named `*Manager`. A third is one enterprise-wide entity model shared by scheduling and billing until every change requires a committee.

Once `BerthReserved` is a fact inside the process, the next pressure is letting billing react without a synchronous call from scheduling on every assignment. That shift is event-driven architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 109 (*DDD Basics*).
