# Episode 41 — Persistence Context

| Field | Value |
|---|---|
| Episode | 41 |
| Title | Persistence Context |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 41 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Inside one harbor booking request, you load `Booking` id 500 twice — once to authorize the trucker, once to attach a gate pass. Do you get two Java objects or one? In JPA, inside one persistence context, you get **one**. That identity guarantee is the persistence context’s quiet contract.

The persistence context is the first-level cache and the unit-of-work boundary. It tracks managed entities, their snapshots for dirty checking, and pending inserts, updates, and deletes until flush. In a typical Spring Boot app it is transaction-scoped: open when the transactional method starts, close when it ends. Open-session-in-view can stretch it across the whole web request — convenient for lazy reads, dangerous when it hides N+1 until production.

```java
@Entity
@Table(name = "bookings")
public class Booking {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "reference_code", nullable = false, unique = true)
    private String referenceCode;

    @Column(name = "gate_pass_issued", nullable = false)
    private boolean gatePassIssued;

    protected Booking() {}

    public void issueGatePass() {
        this.gatePassIssued = true;
    }
}
```

```java
@Transactional
public void authorizeAndIssuePass(String referenceCode) {
    Booking first = bookings.findByReferenceCode(referenceCode).orElseThrow();
    Booking second = bookings.findById(first.getId()).orElseThrow();

    // same persistence context → same instance
    if (first != second) {
        throw new IllegalStateException("identity broken inside one context");
    }

    second.issueGatePass();
}
```

`first == second` is reference equality, not merely equal ids. Hibernate did not need a second SELECT for the `findById` after the entity was already managed — the context returned the tracked instance. Change fields through either variable; there is only one snapshot to dirty-check.

Across transactions the guarantee disappears. A booking loaded in request A and a booking loaded in request B are different instances even for the same row. That is why detached-edit bugs from the previous lesson appear: people pass instances across contexts as if identity were global.

`EntityManager.clear()` detaches all managed entities — useful in batch jobs, catastrophic mid-request if you still hold references you plan to dirty-check. `flush()` pushes SQL early without closing the context. `detach(entity)` removes one instance from tracking.

The persistence context is not the second-level cache, not the database session in the JDBC sense alone, and not "wherever Hibernate feels like remembering things." It is a well-defined map of managed entities tied to a unit of work. Believing two finds always mean two SELECTs misses the cache. Believing two finds across transactions share an instance misses the boundary.

You understand the room managed entities live in. You still do not want every use case to inject `EntityManager` and write find/save by hand. Spring Data JPA repositories are the typed façade — and for vessels, that starts with `findByImoNumber`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 41 (*Persistence Context*).
