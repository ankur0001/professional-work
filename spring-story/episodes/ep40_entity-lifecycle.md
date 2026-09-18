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

Hibernate's Session only cares about entities it recognizes as part of the unit of work. Everything else is just a Java object with fields. That distinction is the entity lifecycle — four states that decide whether a field change becomes SQL, whether an id is assigned, and whether `merge` will help or hurt.

The states are transient, managed, detached, and removed. Learn them with a warehouse `Shipment` entity, because shipping status changes are exactly where teams call the wrong API.

**Transient** means new in memory, never associated with a persistence context. No row yet. No id from the database (unless you assigned one yourself).

**Managed** means the persistence context tracks the instance. Dirty checking applies. `find`, successful `persist`, and loading via query all produce managed entities inside an open context.

**Detached** means the instance once was managed, but the context closed or you explicitly detached it. It still has an id. Changes are invisible to Hibernate until you reattach somehow — usually `merge`.

**Removed** means scheduled for deletion on flush. After flush and commit, the row is gone; the Java object may still exist in memory as a hollow leftover you should stop using.

Walk the transitions with the EntityManager operations that cause them.

```java
@Entity
@Table(name = "shipments")
public class Shipment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String trackingNumber;

    @Enumerated(EnumType.STRING)
    private ShipmentStatus status;

    protected Shipment() {}

    public Shipment(String trackingNumber) {
        this.trackingNumber = trackingNumber;
        this.status = ShipmentStatus.PENDING;
    }

    public void markShipped() {
        this.status = ShipmentStatus.SHIPPED;
    }

    // getters...
}
```

```java
@Transactional
public Shipment createAndShip(String trackingNumber) {
    Shipment shipment = new Shipment(trackingNumber);
    // transient — no persistence context knows this object

    entityManager.persist(shipment);
    // managed — INSERT scheduled; id may appear depending on generator

    shipment.markShipped();
    // still managed — dirty checking will UPDATE status on flush

    return shipment;
}
```

`persist` takes transient → managed. Calling `persist` on an already managed instance is mostly a no-op. Calling `persist` on a detached instance with an id is a mistake path — providers differ, and you can get entity-exists errors. Prefer `merge` when you hold a detached graph from a previous request.

```java
@Transactional
public Shipment updateDetached(Shipment incoming) {
    // incoming arrived from a controller after the previous TX ended → detached
    Shipment managed = entityManager.merge(incoming);
    // merge copies state onto a managed instance (load or create) and returns that managed ref
    managed.markShipped();
    return managed;
}
```

Critical detail: `merge` returns the managed instance. If you keep mutating `incoming` after merge, you may be editing the detached copy while the context tracks someone else. Always continue with the return value.

Removal is explicit:

```java
@Transactional
public void cancel(Long shipmentId) {
    Shipment shipment = entityManager.find(Shipment.class, shipmentId);
    // managed
    entityManager.remove(shipment);
    // removed — DELETE on flush
}
```

Spring Data's `save` hides some of this. For a new entity without id, it persists. For an entity that looks existing, it often merges. That convenience is why beginners never learn lifecycle — until a detached `Shipment` with a stale collection gets merged and unexpectedly inserts orphan rows, or until they call `save` outside a transaction and wonder why nothing commits.

Detachment happens every time a transaction ends if you leave the persistence context. Web apps that serialize entities to JSON after the transaction close are holding detached instances. Lazy associations on those instances will fail unless something kept the session open or you fetched the data while managed.

If someone tells you "just call `save` on everything," they are papering over lifecycle. If someone never uses `merge` because "we only use repositories," they still merge — Spring Data does it for them when ids are present. Own the states: transient until persist, managed while the context lives, detached after, removed when delete is scheduled.

We now know *what* state an entity is in. The next question is *where* that tracking happens — the first-level cache, dirty checking, and flush rules of the persistence context itself.

Episode Forty-One takes us there.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 40 (*Entity Lifecycle*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
