# Episode 52 — @Transactional

| Field | Value |
|---|---|
| Episode | 52 |
| Title | @Transactional |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 52 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The warehouse page shows twelve units of SKU-4401. A picker confirms a reservation for eight. Somewhere between the click and the toast, the stock row decrements, the reservation insert dies on a unique constraint, and the ledger never writes. Morning inventory is short by eight with no reservation to explain it. Three tables participated. Only one kept the change.

That is the unit-of-work problem in warehouse language: stock, reservation, and ledger must share one fate.

Before Spring drew the boundary for you, teams scripted it by hand. Borrow a connection. Disable auto-commit. Decrement stock. Insert the reservation. Append the ledger. Commit — or roll back and close, on every failure path, including the ones nobody remembered. Miss a branch and you leak connections or strand half-applied inventory. The ceremony outgrew the business rule.

Declarative transactions flip the ownership. You mark the boundary. Infrastructure begins, commits, and rolls back.

```java
@Service
public class WarehouseReservationService {

    private final StockRepository stockRepository;
    private final ReservationRepository reservationRepository;
    private final LedgerRepository ledgerRepository;

    public WarehouseReservationService(
            StockRepository stockRepository,
            ReservationRepository reservationRepository,
            LedgerRepository ledgerRepository) {
        this.stockRepository = stockRepository;
        this.reservationRepository = reservationRepository;
        this.ledgerRepository = ledgerRepository;
    }

    @Transactional
    public ReservationId reserve(Sku sku, int qty, WarehouseId warehouse) {
        Stock stock = stockRepository.findForUpdate(warehouse, sku)
                .orElseThrow(() -> new SkuNotFoundException(sku));

        if (stock.available() < qty) {
            throw new InsufficientStockException(sku, qty, stock.available());
        }

        stock.decrement(qty);
        stockRepository.save(stock);

        Reservation reservation = Reservation.open(warehouse, sku, qty);
        reservationRepository.save(reservation);

        // mid-failure here (constraint, transient error) must undo stock + reservation
        ledgerRepository.append(LedgerEntry.reserved(reservation.id(), sku, qty));
        return reservation.id();
    }
}
```

Walk the method as a spoken clock. Enter `reserve`. The proxy starts a transaction and binds the JDBC connection or JPA `EntityManager` to the thread. Stock decrements. Reservation persists. Ledger appends. Return normally and Spring commits — all three tables agree. Throw `InsufficientStockException`, or fail on the ledger insert after stock already changed in memory, and Spring rolls back. The decrement, the reservation row, and any ledger attempt vanish together. Atomicity is the point; the annotation is how you name the boundary.

Strip `@Transactional` and each `save` can auto-commit on its own connection. Stock sticks. Reservation fails. Ledger is silent. The warehouse lies. With the annotation, mid-method failure is not “best effort cleanup.” It is rollback.

Under the hood this is proxy plus interceptor, not a rewrite of your class file on the common path. A call through the bean proxy hits `TransactionInterceptor`. Attributes from `@Transactional` feed a `PlatformTransactionManager`. The manager begins or joins work; your method runs; commit or rollback follows. `TransactionSynchronizationManager` keeps the resource tied to the thread for that boundary.

Defaults matter when you debug. Runtime exceptions and errors roll back; checked exceptions do not unless you say so. Self-invocation skips the proxy — `this.reserve(...)` from inside the same class never sees the interceptor. `readOnly = true` is a hint for reads, not a magic shield. The same annotation spans JDBC, JPA, and MyBatis when the right manager is configured.

One misconception: treating `@Transactional` as “this method may touch the database.” It scopes a unit of work; repositories still do the talking. Another: sprinkling it on private helpers and expecting advice to fire. External calls through the proxy count. Internal ones do not.

We drew the warehouse boundary so stock, reservation, and ledger commit or disappear together. Nested collaborators change the story: does an inner call join that boundary, or open a second one that can survive when the outer work fails?

Propagation is how Spring answers that nesting question.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 52 (*@Transactional*).
