# Episode 40 — Entity Lifecycle

| Field | Value |
|---|---|
| Episode | 40 |
| Title | Entity Lifecycle |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 40 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A warehouse handheld loads `CargoItem` `CARGO-441` during a request, shows it on screen, and the HTTP call ends. Two minutes later the clerk taps "mark damaged." If you keep the old Java object and call `save` carelessly, you are holding a *detached* entity — and `merge` mistakes are about to enter the chat.

JPA entities move through named states. **Transient**: a `new CargoItem(...)` that the persistence context has never seen — no row yet. **Managed**: loaded or persisted inside an open persistence context; dirty checking applies. **Detached**: the context closed (typically when the transaction/request ended) but the object still sits in memory with an id. **Removed**: marked for deletion on flush.

```java
@Entity
@Table(name = "cargo_items")
public class CargoItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "tracking_code", nullable = false, unique = true)
    private String trackingCode;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private CargoCondition condition;

    protected CargoItem() {}

    public CargoItem(String trackingCode) {
        this.trackingCode = trackingCode;
        this.condition = CargoCondition.OK;
    }

    public void markDamaged() {
        this.condition = CargoCondition.DAMAGED;
    }
}
```

Walk a request. Controller calls a transactional service. Service does `cargoItems.findByTrackingCode("CARGO-441")` — the instance is **managed**. Request ends; transaction commits; persistence context closes. The object the UI still references is now **detached**. Calling `markDamaged()` on that detached instance changes only the JVM heap. Nothing schedules SQL.

The common mistake is "merge everything":

```java
@Transactional
public void markDamagedWrong(CargoItem detachedFromUi) {
    detachedFromUi.markDamaged();
    cargoItems.save(detachedFromUi); // Spring Data may merge — easy to overwrite stale fields
}
```

`EntityManager.merge` copies state onto a managed instance (or loads one). If the UI sent a half-populated object, merge can overwrite database columns with nulls or stale values. Prefer an explicit reload inside the new transaction:

```java
@Transactional
public void markDamaged(String trackingCode) {
    CargoItem item = cargoItems.findByTrackingCode(trackingCode)
            .orElseThrow();
    item.markDamaged(); // managed — dirty checking writes CONDITION on flush
}
```

Transient → managed via `persist` / `save` on a new entity. Managed → removed via `remove` / `delete`. Managed → detached when the context closes. Detached → managed via find/reload (safe) or merge (powerful, sharp).

Lifecycle callbacks (`@PrePersist`, `@PreUpdate`) can stamp `updatedAt` on cargo rows, but they are not a substitute for clear state handling. Believing "once an entity always managed" across requests is the root misconception. Another is using merge as a generic upsert without knowing which fields the detached graph carries. A third is mutating a detached collection of cargo lines and expecting orphan removal to run — orphan removal requires a managed parent.

Lifecycle names the states. The room those managed instances live in for the duration of a unit of work — and the rule that the same database row is the same Java instance inside that room — is the persistence context.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 40 (*Entity Lifecycle*).
