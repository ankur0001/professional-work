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

A transaction that commits or rolls back correctly can still be wrong under concurrency. Two cashiers update the same seat inventory. A report reads a balance while a transfer is mid-flight. One session inserts a row that another session’s query “should not” have seen yet. Atomicity answered all-or-nothing. Isolation answers what concurrent readers and writers are allowed to observe of each other.

Databases define classic anomalies. A dirty read sees another transaction’s uncommitted change — change that might still roll back. A non-repeatable read means you select a row twice inside one transaction and get different committed values because a writer sneaked a commit between your reads. A phantom read means a range query returns a new row the second time because another transaction inserted into that range and committed.

Isolation levels are the dials that trade correctness for throughput by allowing or forbidding those anomalies.

```java
@Service
public class SeatHoldService {

    private final SeatRepository seats;

    public SeatHoldService(SeatRepository seats) {
        this.seats = seats;
    }

    @Transactional(isolation = Isolation.REPEATABLE_READ)
    public HoldId holdSeat(EventId eventId, String seatLabel, CustomerId customerId) {
        Seat seat = seats.findByEventAndLabel(eventId, seatLabel)
                .orElseThrow(() -> new SeatMissingException(seatLabel));

        if (!seat.isOpen()) {
            throw new SeatTakenException(seatLabel);
        }

        // another concurrent hold might still race depending on DB + locking
        seat.holdFor(customerId);
        seats.save(seat);
        return HoldId.newId();
    }
}
```

```java
@Service
public class BalanceReportService {

    private final AccountRepository accounts;

    public BalanceReportService(AccountRepository accounts) {
        this.accounts = accounts;
    }

    @Transactional(readOnly = true, isolation = Isolation.READ_COMMITTED)
    public Money availableBalance(AccountId id) {
        return accounts.findById(id)
                .orElseThrow(() -> new AccountNotFoundException(id))
                .available();
    }
}
```

Name the four levels Spring exposes on `@Transactional`, matching JDBC’s vocabulary. `READ_UNCOMMITTED` permits dirty reads — almost never what you want for money or inventory. `READ_COMMITTED` blocks dirty reads; each statement sees only committed data, but two reads of the same row inside one transaction can disagree. Many production databases default here. `REPEATABLE_READ` keeps rows you already read stable for the rest of your transaction; phantoms may still appear depending on the engine. `SERIALIZABLE` is the strictest common setting: the system behaves as if transactions ran one after another, at the cost of locks, retries, or aborted transactions under contention.

Spring does not invent these levels. It passes your choice to the `PlatformTransactionManager`, which sets isolation on the underlying connection when the transaction begins — if the database and driver honor it. Some engines silently upgrade or ignore unsupported levels. PostgreSQL, MySQL, and Oracle do not implement every textbook guarantee the same way. Always verify against your engine’s docs when you raise isolation for a hot path.

Why put isolation on the annotation at all? Because one service method may need a stricter contract than the connection pool default. Seat holds and double-booking fights often want stronger guarantees or explicit locking. A dashboard balance read may be fine at `READ_COMMITTED`. Declaring isolation next to the boundary documents intent for the next engineer who touches the method.

Misconceptions pile up quickly. People assume `REPEATABLE_READ` makes lost updates impossible without also thinking about how updates lock rows. Isolation is about read phenomena and scheduling; lost updates still need careful update patterns, version columns, or `SELECT … FOR UPDATE`. Others raise everything to `SERIALIZABLE` “to be safe,” then discover throughput cliffs and serialization failures that force application-level retries. Another trap: believing Spring’s isolation attribute alone fixes races visible in the UI. If two requests each read “seat open” before either writes, you still need a locking or constraint strategy — isolation is one tool in that kit, not the whole kit.

So we separated commit/rollback from concurrent visibility, named the anomalies, and saw how `@Transactional(isolation = …)` asks the database for a specific contract. We have not yet asked which exceptions should undo the work when something fails. Runtime failures roll back by default. Checked exceptions often do not. Business rules sometimes need the opposite of those defaults.

Encoding “which failures are fatal” is rollback rules — next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 54 (*Isolation Levels*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
