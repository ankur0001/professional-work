# Episode 49 — Pessimistic Locking

| Field | Value |
|---|---|
| Episode | 49 |
| Title | Pessimistic Locking |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 49 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Storm diversion. One free slot left on berth `B7`. Two reservation requests hit the API within milliseconds. Optimistic locking would let both read "one slot left," then fail one at commit — acceptable for clerks who can retry, painful when an automated gate must answer now and only one ship may win. Pessimistic locking serializes access: the first transaction locks the row; the second waits or fails fast.

JPA expresses this with lock modes on `find` / query APIs. `LockModeType.PESSIMISTIC_WRITE` typically becomes `SELECT ... FOR UPDATE` on databases that support it.

```java
public interface BerthRepository extends JpaRepository<Berth, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("select b from Berth b where b.berthCode = :code")
    Optional<Berth> findForUpdate(@Param("code") String code);
}
```

```java
@Service
public class HotBerthReservation {

    private final BerthRepository berths;

    public HotBerthReservation(BerthRepository berths) {
        this.berths = berths;
    }

    @Transactional
    public void reserveLastSlot(String berthCode) {
        Berth berth = berths.findForUpdate(berthCode)
                .orElseThrow(() -> new IllegalArgumentException("unknown berth"));
        berth.reserve(1);
    }
}
```

Walk the timeline. Transaction A calls `findForUpdate("B7")` and holds the row lock. Transaction B’s `findForUpdate("B7")` blocks until A commits or rolls back — or times out, depending on database and Spring lock timeout settings. After A commits with zero remaining slots, B loads the fresh state and `reserve(1)` throws a business exception instead of overbooking. No version collision theater; the database queue did the serialization.

`PESSIMISTIC_READ` is a shared lock where the dialect supports it — useful for read-stable sections, less common for reservation. `PESSIMISTIC_WRITE` is the reservation tool. Lock timeout and deadlock detection are operational concerns: set timeouts so a stuck transaction does not freeze the whole pier board, and keep the critical section short — lock, decide, write, commit. Do not lock, then call a remote tide API, then write.

Pessimistic locking is not free. It reduces concurrency on hot rows. Holding locks across user think-time is how you recreate the worst of pessimistic UIs. Prefer optimistic locking for ordinary collaborative edits; reach for `PESSIMISTIC_WRITE` when the business rule is "exactly one winner, no retry loop."

Using `@Version` and `PESSIMISTIC_WRITE` on every entity "for safety" fights itself — you pay lock costs and still write version columns without a clear policy. Locking in a non-transactional method also fails: without a transaction boundary, the lock has nowhere to live. And forgetting that `FOR UPDATE` behavior varies by dialect leads to surprises when tests on H2 differ from Postgres in production.

You can now choose optimistic vs pessimistic for berth fights. Separately, the schedule board can still feel slow even when no one is colliding — not because of locks, but because of how you load graphs, batch lazy collections, and project columns. That is JPA performance tuning.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 49 (*Pessimistic Locking*).
