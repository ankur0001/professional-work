# Episode 53 — Propagation

| Field | Value |
|---|---|
| Episode | 53 |
| Title | Propagation |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 53 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You already know `@Transactional` draws a boundary around one method. Real systems rarely stop at one method. A checkout service saves the purchase, then asks an audit service to record “attempted,” then “completed,” then maybe “failed.” Should those audit writes live inside the same database transaction as the purchase — so a checkout rollback erases the audit too? Or should each audit line commit on its own, surviving even when checkout rolls back?

That decision is propagation: how a transactional call behaves when a transaction may already be active on the thread.

Spring’s default is `Propagation.REQUIRED`. If a transaction exists, join it. If none exists, start one. Nested service calls with `REQUIRED` become one shared unit of work. One rollback undoes everyone who joined.

Contrast that with `Propagation.REQUIRES_NEW`. Always suspend the outer transaction if present, start a fresh one, commit or roll it back independently, then resume the outer. The inner work can survive outer failure — or fail without forcing the outer to fail, depending on how you handle exceptions.

```java
@Service
public class CheckoutService {

    private final PurchaseRepository purchases;
    private final AuditService auditService;

    public CheckoutService(PurchaseRepository purchases, AuditService auditService) {
        this.purchases = purchases;
        this.auditService = auditService;
    }

    @Transactional // REQUIRED by default
    public PurchaseId checkout(Cart cart) {
        auditService.record("CHECKOUT_STARTED", cart.id());

        Purchase purchase = Purchase.from(cart);
        purchases.save(purchase);

        chargePayment(purchase); // may throw

        auditService.record("CHECKOUT_COMPLETED", cart.id());
        return purchase.id();
    }
}
```

```java
@Service
public class AuditService {

    private final AuditRepository audits;

    public AuditService(AuditRepository audits) {
        this.audits = audits;
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void record(String event, CartId cartId) {
        audits.save(new AuditEntry(event, cartId, Instant.now()));
    }
}
```

Walk the nested calls. Client hits `checkout`. Spring starts transaction T1. Inside, `auditService.record("CHECKOUT_STARTED", …)` goes through the audit bean’s proxy. Because of `REQUIRES_NEW`, Spring suspends T1, opens T2, inserts the audit row, commits T2, resumes T1. Back in checkout, the purchase is saved on T1. Payment fails. Checkout throws. T1 rolls back — the purchase disappears. The started audit row remains, because it already committed on T2. That is often exactly what operations wants: a durable trail of attempts, not a silent void after rollback.

Flip the thought experiment. Change `record` to plain `@Transactional` — still `REQUIRED`. Now the audit insert joins T1. Payment fails. Everything rolls back, including “CHECKOUT_STARTED.” Your support team has no breadcrumb that a checkout was even attempted. Same business methods. Different propagation. Different truth in the database.

Spring exposes other propagation modes you should recognize even if you use them rarely. `SUPPORTS` runs with a transaction if one exists, otherwise non-transactional. `NOT_SUPPORTED` suspends an outer transaction and runs without one — useful when a long read should not hold locks. `MANDATORY` demands an existing transaction and fails if none is present — a guard for helpers that must never open their own boundary. `NEVER` refuses to run inside a transaction. `NESTED` uses a savepoint inside the same physical transaction when the manager supports it, so a partial rollback can return to that savepoint without undoing the entire outer work.

The mental model that keeps interviews honest is simple. Propagation is not “how many databases.” It is “what happens when transactional methods nest on one thread.” The proxy and `TransactionInterceptor` consult the propagation attribute before they ask the `PlatformTransactionManager` to begin, join, suspend, or resume.

Misread this and you get surprising rollbacks. People annotate an audit method `REQUIRES_NEW`, catch the exception in the outer method, and assume the outer still commits — until they rethrow or leave the transaction marked rollback-only after a joined participant failed. Another trap: calling a `REQUIRES_NEW` method on `this` inside the same class. No proxy, no new transaction, no suspension — just a plain method call.

Hold the two modes you will actually debate in design reviews: `REQUIRED` for shared atomicity across nested collaborators, `REQUIRES_NEW` when a nested side effect must commit on its own timeline. That answers “join or split.” It does not answer what concurrent transactions are allowed to see of each other’s uncommitted or recently committed rows.

Visibility under concurrency is isolation — and that unresolved gap is the next episode.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 53 (*Propagation*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
