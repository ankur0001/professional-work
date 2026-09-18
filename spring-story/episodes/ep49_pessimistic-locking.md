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

Optimistic locking detects lost updates after the fact. Sometimes you cannot afford the retry. The last concert seat, a payment capture against a wallet balance, a job queue row that must be claimed by exactly one worker — those paths need the database to refuse concurrent writers while the transaction runs. That is pessimistic locking: `SELECT ... FOR UPDATE` (and cousins) through JPA lock modes.

Spring Data exposes lock modes on repository queries:

```java
public interface SeatRepository extends JpaRepository<Seat, Long> {

    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @Query("select s from Seat s where s.id = :id")
    Optional<Seat> findForUpdate(@Param("id") Long id);
}

@Entity
@Table(name = "seats")
public class Seat {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String eventCode;

    @Column(nullable = false)
    private String seatLabel;

    @Enumerated(EnumType.STRING)
    private SeatStatus status;

    protected Seat() {}

    public void reserve(String customerId) {
        if (status != SeatStatus.AVAILABLE) {
            throw new IllegalStateException("seat not available: " + seatLabel);
        }
        this.status = SeatStatus.RESERVED;
        // customerId stored on a sibling assignment entity in a fuller model
    }
}
```

```java
@Service
public class SeatReservationService {

    private final SeatRepository seats;

    public SeatReservationService(SeatRepository seats) {
        this.seats = seats;
    }

    @Transactional
    public void reserve(Long seatId, String customerId) {
        Seat seat = seats.findForUpdate(seatId)
                .orElseThrow(() -> new IllegalArgumentException("unknown seat"));
        seat.reserve(customerId);
        // row lock held until commit/rollback; peer transactions wait or time out
    }
}
```

`LockModeType.PESSIMISTIC_WRITE` typically translates to `FOR UPDATE`. `PESSIMISTIC_READ` maps toward shared locks where the dialect supports them. `PESSIMISTIC_FORCE_INCREMENT` combines a write lock with a version increment — useful when you need both serialization and version movement for readers using optimistic checks.

Timeouts matter. A lock held while you call an external payment API is how you freeze the whole seat map. Keep the critical section tiny: lock, mutate, commit. Do I/O outside the lock. Configure wait behavior with hints when the provider supports it:

```java
@QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))
@Lock(LockModeType.PESSIMISTIC_WRITE)
@Query("select s from Seat s where s.id = :id")
Optional<Seat> findForUpdate(@Param("id") Long id);
```

If the lock cannot be acquired in time, you get a lock timeout exception instead of hanging a request thread forever. Handle it as contention — retry once, or fail fast to the user.

Pessimistic locking interacts with isolation and indexes. Locking by a non-unique search without care can lock more rows than you expect. Prefer locking the precise primary key row. In a worker claim pattern, `SELECT ... FOR UPDATE SKIP LOCKED` (via native query or vendor hint) lets other workers grab the next available job instead of waiting — powerful for queues, easy to misuse for business entities.

Compare the two strategies as product decisions. Optimistic: higher throughput under light contention, conflicts become HTTP 409 and retries. Pessimistic: lower concurrency on hot rows, stronger serialization, risk of waits and deadlocks. Using both on the same aggregate is allowed — version for general edits, explicit `findForUpdate` for checkout. Using pessimistic locks on every repository method "to be safe" will serialize your application into a single file line.

Locks and versions protect correctness. They do not automatically make queries fast. Once correctness tools are in place, latency questions take over: what to fetch, how to batch, which indexes matter, and which Hibernate settings shape SQL.

Episode Fifty — Performance Tuning.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 49 (*Pessimistic Locking*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
