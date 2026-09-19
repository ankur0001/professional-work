# Episode 48 — Optimistic Locking

| Field | Value |
|---|---|
| Episode | 48 |
| Title | Optimistic Locking |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 48 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Two clerks open berth `B7` at the same moment. Both screens show capacity 4 remaining. Anya assigns a feeder that needs 2 slots. Ben assigns a coastal freighter that needs 3. Without protection, last write wins and you overbook the pier. Optimistic locking assumes conflict is uncommon, lets both read, and detects the collision at write time with a version column.

JPA’s tool is `@Version` on the berth capacity aggregate:

```java
@Entity
@Table(name = "berths")
public class Berth {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "berth_code", nullable = false, unique = true, length = 8)
    private String berthCode;

    @Column(name = "capacity_slots", nullable = false)
    private int capacitySlots;

    @Column(name = "reserved_slots", nullable = false)
    private int reservedSlots;

    @Version
    private long version;

    protected Berth() {}

    public Berth(String berthCode, int capacitySlots) {
        this.berthCode = berthCode;
        this.capacitySlots = capacitySlots;
        this.reservedSlots = 0;
    }

    public void reserve(int slots) {
        if (slots <= 0) {
            throw new IllegalArgumentException("slots must be positive");
        }
        if (reservedSlots + slots > capacitySlots) {
            throw new IllegalStateException("berth " + berthCode + " is full");
        }
        this.reservedSlots += slots;
    }

    public int remaining() {
        return capacitySlots - reservedSlots;
    }
}
```

Hibernate includes the version in `UPDATE` statements:

```sql
UPDATE berths
SET reserved_slots = ?, version = ?
WHERE id = ? AND version = ?
```

If the row’s version changed since you loaded it, zero rows update, and JPA throws `OptimisticLockException` — Spring often wraps it as `ObjectOptimisticLockingFailureException`. The loser must reload, reapply business logic, and retry — or tell the clerk the berth changed under them.

```java
@Service
public class BerthAllocationService {

    private final BerthRepository berths;

    public BerthAllocationService(BerthRepository berths) {
        this.berths = berths;
    }

    @Transactional
    public void reserve(String berthCode, int slots) {
        Berth berth = berths.findByBerthCode(berthCode)
                .orElseThrow(() -> new IllegalArgumentException("unknown berth"));
        berth.reserve(slots);
        // dirty checking + versioned UPDATE on flush
    }
}
```

```java
@RestControllerAdvice
public class BerthLockAdvice {

    @ExceptionHandler(ObjectOptimisticLockingFailureException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public Map<String, String> conflict(ObjectOptimisticLockingFailureException ex) {
        return Map.of(
                "message",
                "Berth capacity changed in another transaction; refresh and retry");
    }
}
```

Walk the collision. Transaction A and B both load `version = 3`, `reservedSlots = 0`, capacity 4. A reserves 2 → flush sets `reservedSlots = 2`, `version = 4`. B reserves 3 with stale `version = 3` → WHERE matches nothing → exception. B does not silently leave the pier overbooked. That is the whole feature.

Version fields can be `long`, `int`, `Short`, or a timestamp type. Prefer numeric versions for berth-style entities; Hibernate increments them. Do not mutate `@Version` yourself in business code. Detached update flows must carry the version from the client or from the previously loaded entity — drop the version and you may overwrite blindly depending on merge behavior.

Optimistic locking fits collaborative berth edits when contention is moderate and retry is acceptable. It does not hold a database lock while a human stares at a form for five minutes — usually a virtue. When a use case cannot tolerate retry and must serialize access to a hot row — last slot on a berth during a storm diversion — you need pessimistic locking instead.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 48 (*Optimistic Locking*).
