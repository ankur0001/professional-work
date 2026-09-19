# Episode 39 — Hibernate Internals

| Field | Value |
|---|---|
| Episode | 39 |
| Title | Hibernate Internals |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 39 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A planner moves vessel `IMO-9312345` from berth B2 to berth B7. Your service loads a `BerthAssignment`, calls `reassign("B7")`, and returns. You never called `UPDATE`. Yet the database row changes. That quiet write is Hibernate dirty checking — and it is the internal you need before lifecycle jargon makes sense.

When Hibernate loads an entity inside a persistence context, it keeps a snapshot of the loaded state. On flush — at transaction commit by default, or earlier if you force it — Hibernate compares the current field values to that snapshot. Differences become SQL. Unchanged entities produce no update. That is the unit-of-work idea: you mutate objects; the provider schedules SQL.

```java
@Entity
@Table(name = "berth_assignments")
public class BerthAssignment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "imo_number", nullable = false, length = 10)
    private String imoNumber;

    @Column(name = "berth_code", nullable = false, length = 8)
    private String berthCode;

    @Column(name = "assigned_at", nullable = false)
    private Instant assignedAt;

    protected BerthAssignment() {}

    public void reassign(String newBerthCode) {
        this.berthCode = newBerthCode;
        this.assignedAt = Instant.now();
    }
}
```

```java
@Transactional
public void moveBerth(String imoNumber, String newBerth) {
    BerthAssignment assignment = assignments
            .findByImoNumber(imoNumber)
            .orElseThrow();
    assignment.reassign(newBerth);
    // no repository.save required for a managed entity — flush issues UPDATE
}
```

On flush, Hibernate may emit:

```sql
UPDATE berth_assignments
SET berth_code = ?, assigned_at = ?
WHERE id = ?
```

If `berthCode` never changed, that update does not run. Calling `save` on an already-managed entity is mostly noise — Spring Data’s `save` for a managed instance often just returns the same instance. The persistence context already tracks it.

Flush modes matter when you interleave queries. `AUTO` (default) flushes before certain queries so you do not read stale data you just changed in memory. `COMMIT` delays until commit — faster in some batch paths, surprising if you query mid-transaction expecting to see your own writes. Understanding flush timing prevents "I updated the berth but the next SELECT still shows B2" bugs inside one transaction.

The first-level cache is the same persistence context: load `BerthAssignment` id 17 twice in one transaction and you get the same Java instance, not a second SELECT by default. That identity guarantee is intentional. The second-level cache is optional and cross-transaction — a later lesson. Dirty checking lives in the first level.

People believe every `save` call immediately hits the database. It does not — SQL is deferred until flush. Others mutate a detached assignment after the transaction ended and expect dirty checking to notice; there is no context left to notice. A third trap is opening the SQL log, seeing no update, and assuming Hibernate is broken when the field simply did not change relative to the snapshot.

Dirty checking explains *how* managed entities write themselves. It does not yet name the states an entity can be in — transient, managed, detached, removed — or what `merge` does when a clerk edits a cargo item after the request that loaded it has ended. That lifecycle vocabulary is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 39 (*Hibernate Internals*).
