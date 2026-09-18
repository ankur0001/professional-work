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

Two warehouse clerks open the same inventory row. Both see quantity 10. One reserves 4. The other reserves 5. Without protection, last write wins and you sell stock you do not have. Pessimistic locking would lock the row for the whole edit. Optimistic locking assumes conflict is uncommon, lets both read, and detects the collision at write time with a version column.

JPA's tool is `@Version`.

```java
@Entity
@Table(name = "inventory_items")
public class InventoryItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String sku;

    @Column(nullable = false)
    private int quantity;

    @Version
    private long version;

    protected InventoryItem() {}

    public InventoryItem(String sku, int quantity) {
        this.sku = sku;
        this.quantity = quantity;
    }

    public void reserve(int amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("amount must be positive");
        }
        if (quantity < amount) {
            throw new IllegalStateException("insufficient stock for " + sku);
        }
        this.quantity -= amount;
    }
}
```

Hibernate includes the version in `UPDATE` statements:

```sql
UPDATE inventory_items
SET quantity = ?, version = ?
WHERE id = ? AND version = ?
```

If the row's version changed since you loaded it, zero rows update, and JPA throws `OptimisticLockException` (often wrapped by Spring as `ObjectOptimisticLockingFailureException`). The loser must reload, reapply business logic, and retry — or tell the user the data changed.

```java
@Service
public class InventoryService {

    private final InventoryItemRepository items;

    public InventoryService(InventoryItemRepository items) {
        this.items = items;
    }

    @Transactional
    public void reserve(String sku, int amount) {
        InventoryItem item = items.findBySku(sku)
                .orElseThrow(() -> new IllegalArgumentException("unknown sku"));
        item.reserve(amount);
        // dirty checking + versioned UPDATE on flush
    }
}
```

```java
@RestControllerAdvice
public class LockingExceptionHandler {

    @ExceptionHandler(ObjectOptimisticLockingFailureException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public Map<String, String> conflict(ObjectOptimisticLockingFailureException ex) {
        return Map.of(
                "message",
                "Inventory changed in another transaction; refresh and retry");
    }
}
```

Walk a collision. Transaction A and B both load `version = 3`, `quantity = 10`. A reserves 4 → flush sets `quantity = 6`, `version = 4`. B reserves 5 with stale `version = 3` → WHERE matches nothing → exception. B does not silently leave quantity at 5. That is the whole feature.

Version fields can be `long`, `int`, `Short`, or a timestamp type. Prefer numeric versions for inventory-style entities; Hibernate increments them. Do not mutate `@Version` yourself in business code. Detached update flows must carry the version from the client or from the previously loaded entity — if the UI sends an older version on purpose, you are implementing conditional updates; if it drops the version, you may overwrite blindly depending on merge behavior.

Optimistic locking fits collaborative edits, configuration rows, and inventory when contention is moderate and retry is acceptable. It does not hold a database lock while a human stares at a form for five minutes — which is usually a virtue. When a use case cannot tolerate retry and must serialize access to a hot row (seat reservation at the last ticket, bank ledger line), you need pessimistic locking instead.

Episode Forty-Nine — Pessimistic Locking.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 48 (*Optimistic Locking*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
