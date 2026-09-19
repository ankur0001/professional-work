# Episode 50 — JPA Performance Tuning

| Field | Value |
|---|---|
| Episode | 50 |
| Title | JPA Performance Tuning |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 50 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The harbor schedule board takes four seconds to paint. The network is fine. The JVM is fine. SQL logging shows dozens of similar selects and wide entity graphs for a screen that only needs vessel name, berth code, and ETA. JPA performance tuning starts by measuring that gap — then applying batch size, entity graphs, and projections on purpose.

Enable SQL logging (or a statement counter) in a lower environment and reproduce the board load. Count statements. Note payload width. Only then pick a tool.

**Batch size** reduces chatty lazy loads when you must keep associations lazy:

```java
@Entity
@Table(name = "schedule_slots")
public class ScheduleSlot {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    private Vessel vessel;

    @ManyToOne(fetch = FetchType.LAZY)
    private Berth berth;

    private Instant eta;
}
```

```java
@Entity
@BatchSize(size = 25)
public class Vessel { /* ... */ }
```

When the board touches twenty vessels’ lazy state, Hibernate can load them with fewer `WHERE id IN (...)` queries instead of twenty singles. Batch size is a blunt instrument — better than N singles, not always better than one intentional join.

**Entity graphs** declare what a use case needs up front:

```java
public interface ScheduleSlotRepository extends JpaRepository<ScheduleSlot, Long> {

    @EntityGraph(attributePaths = {"vessel", "berth"})
    @Query("select s from ScheduleSlot s where s.eta between :from and :to")
    List<ScheduleSlot> findBoard(Instant from, Instant to);
}
```

The graph tells Hibernate to fetch `vessel` and `berth` with the slots for that board query — without marking the associations `EAGER` globally for every other use case.

**Projections** shrink what comes back when the board does not need full entities:

```java
public interface ScheduleBoardRow {
    String getVesselName();
    String getBerthCode();
    Instant getEta();
}

@Query("""
        select v.name as vesselName,
               b.berthCode as berthCode,
               s.eta as eta
        from ScheduleSlot s
        join s.vessel v
        join s.berth b
        where s.eta between :from and :to
        order by s.eta
        """)
List<ScheduleBoardRow> projectBoard(Instant from, Instant to);
```

No managed graph. No accidental lazy navigation in the JSON serializer. Columns the screen needs — nothing more.

Other levers: pagination so the board cannot ask for a year of slots; read-only transactions for pure paints; avoiding Open Session in View when it turns rendering into a query engine; second-level cache only after you understand eviction. Indexes still matter — JPA will not invent an index on `eta` for you.

Marking every association `EAGER` "for performance" often makes writes and incidental loads worse. Caching entities without a plan recreates stale berth boards. Micro-optimizing flush modes before counting SQL is folklore.

Even a tuned board can hide a sharper anti-pattern: one query for manifests, then one query per manifest for cargo lines as a loop touches the collection. That classic explosion has a name — N+1 — and it deserves its own walkthrough with a real loop and a join-fetch fix.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 50 (*JPA Performance Tuning*).
