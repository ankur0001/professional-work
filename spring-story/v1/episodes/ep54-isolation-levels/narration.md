# Episode 54 — Isolation Levels

| Field | Value |
|---|---|
| Episode | 54 |
| Title | Isolation Levels |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 54 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Two clerks book berths for the same evening tide window. Clerk A counts free slots in quay 7 and sees three. Clerk B, a moment later, counts the same range and also sees three. Both assign. The schedule board briefly shows four vessels on three berths. Nobody rolled back. Atomicity held inside each transaction. Concurrent visibility did not.

Isolation is the contract for what concurrent readers and writers are allowed to observe of each other.

Name the classic anomalies in berth language. A dirty read would see another clerk’s uncommitted assignment — one that might still vanish. A non-repeatable read means you re-read the same berth row inside one transaction and get a different committed value because someone else finished an update between your reads. A phantom read is the quay-7 story: a range query returns a new row the second time because another transaction inserted into that range and committed. Phantoms are how “three free berths” becomes a lie without any single row looking corrupted.

Isolation levels are the dials that permit or forbid those anomalies, trading correctness for throughput.

```java
@Service
public class BerthBookingService {

    private final BerthRepository berths;

    public BerthBookingService(BerthRepository berths) {
        this.berths = berths;
    }

    @Transactional(isolation = Isolation.REPEATABLE_READ)
    public AssignmentId assign(QuayId quay, Instant window, VesselId vessel) {
        List<Berth> free = berths.findFreeInWindow(quay, window);
        if (free.isEmpty()) {
            throw new NoBerthAvailableException(quay, window);
        }
        Berth chosen = free.getFirst();
        chosen.assign(vessel, window);
        berths.save(chosen);
        return AssignmentId.newId();
    }
}
```

```java
@Service
public class QuayBoardService {

    private final BerthRepository berths;

    public QuayBoardService(BerthRepository berths) {
        this.berths = berths;
    }

    @Transactional(readOnly = true, isolation = Isolation.READ_COMMITTED)
    public List<BerthSnapshot> board(QuayId quay, Instant window) {
        return berths.findFreeInWindow(quay, window).stream()
                .map(BerthSnapshot::from)
                .toList();
    }
}
```

Spring exposes the JDBC vocabulary on `@Transactional`. `READ_UNCOMMITTED` allows dirty reads — almost never what harbor scheduling wants. `READ_COMMITTED` blocks dirty reads; each statement sees committed data, but two reads of the same row inside one transaction can disagree. Many engines default here. `REPEATABLE_READ` keeps rows you already read stable for the rest of the transaction; phantoms may still appear depending on the database. `SERIALIZABLE` aims at one-after-another behavior, paid for with locks, retries, or aborted transactions under contention.

Spring does not invent these guarantees. It asks the `PlatformTransactionManager` to set isolation on the connection when the transaction begins — if the driver and engine honor it. PostgreSQL, MySQL, and Oracle do not implement every textbook promise the same way. Raising isolation on a hot berth path without reading your engine’s docs is optimism, not safety.

Why declare isolation on the method at all? Because the connection pool default may be fine for a quay board read and too weak for an assignment that must not invent phantom capacity. Putting the level next to the boundary documents intent for the next engineer who touches concurrent booking.

Misconceptions cluster here. People assume `REPEATABLE_READ` alone prevents lost updates without locking or version checks — isolation addresses read phenomena; lost updates still need careful update patterns, `@Version`, or `SELECT … FOR UPDATE`. Others set everything to `SERIALIZABLE` “to be safe,” then drown in serialization failures. Another trap: believing the annotation alone fixes two requests that each read “three free” before either writes. You still need constraints or explicit locks. Isolation is one tool, not the whole kit.

We can commit cleanly and still be wrong under concurrency unless we name the visibility contract. The next knob is different: which exceptions should undo the work when a business rule fails as a checked type.

Rollback rules encode that policy.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 54 (*Isolation Levels*).
