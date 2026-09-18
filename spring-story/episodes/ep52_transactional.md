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

Picture a warehouse reservation that must touch three tables in one business action. You decrement available stock. You insert a reservation row. You write an audit ledger entry so finance can prove what happened. If stock decrements and then the reservation insert fails — maybe a unique constraint, maybe a transient outage — you cannot leave the inventory permanently short. Those three writes need one outcome: all committed, or all undone.

That is a transaction boundary. Not a framework slogan. A contract with the database: begin, do work, commit on success, roll back on failure.

Teams used to write that contract by hand. Open a connection. `setAutoCommit(false)`. Try the three statements. `commit()`. On any failure, `rollback()`, and hope every path remembered to close the connection. Copy that try/catch into every service method that touches more than one table. Miss one catch branch and you leak connections or leave half-applied state. The ceremony dwarfed the business rules.

Spring’s answer is declarative: mark the boundary, let the infrastructure own begin, commit, and rollback.

```java
@Service
public class ReservationService {

    private final StockRepository stockRepository;
    private final ReservationRepository reservationRepository;
    private final LedgerRepository ledgerRepository;

    public ReservationService(
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

        ledgerRepository.append(LedgerEntry.reserved(reservation.id(), sku, qty));
        return reservation.id();
    }
}
```

Read the method as a spoken story. Enter `reserve`. Spring starts a transaction and binds the JDBC connection or JPA `EntityManager` to the current thread. Decrement stock. Persist the reservation. Append the ledger. If every step succeeds, Spring commits when the method returns. If `InsufficientStockException` or any other runtime failure escapes, Spring rolls back — stock decrement, reservation insert, and ledger append all disappear together.

Without `@Transactional`, each repository `save` can auto-commit on its own connection. You might persist the stock change, then fail on the reservation, and wake up to inventory that no longer matches reality. The annotation is the boundary that restores atomicity across those steps.

Under the hood, Spring does not rewrite your bytecode for this feature in the common path. It wraps the bean in a proxy. A call through the proxy hits a `TransactionInterceptor`. The interceptor reads attributes from `@Transactional`, asks a `PlatformTransactionManager` to get or create a transaction, invokes your method, then commits or rolls back. `TransactionSynchronizationManager` keeps the resource — connection or persistence context — tied to the thread for the duration of that boundary.

A few details matter in production conversations. The default rollback policy is runtime exceptions and errors — checked exceptions do not roll back unless you say so. Self-invocation bypasses the proxy: if `reserve` calls another `@Transactional` method on `this`, that inner annotation is invisible. Read-only flags hint the manager and sometimes the persistence provider that you intend queries only. And the same annotation works across JDBC, JPA, and MyBatis as long as a transaction manager is configured for the resource you use.

One misconception is treating `@Transactional` as “make this method talk to the database.” It does not open a repository for you. It scopes a unit of work. Another is sprinkling it on every private helper. Advice applies to external calls through the proxy, not to every method on the class file.

So we named the boundary, walked a multi-step reservation that must succeed or vanish together, and saw the proxy plus interceptor own begin, commit, and rollback. But the story is incomplete the moment one transactional method calls another. Does the inner call join the outer transaction, or does it demand a brand-new one that can commit even if the outer work later fails?

That nested-call question is propagation — and it is where the next episode starts.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 52 (*@Transactional*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
