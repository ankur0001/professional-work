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

Support opens a ticket: “checkout failed, but we have no audit row saying it even started.” Engineering replies: “of course — the whole transaction rolled back.” Operations replies: “then how do we prove the attempt?” Same database. Two different truths people need from nested writes.

Propagation is the dial between those truths: when a transactional method calls another, does the inner work join the outer unit, or run in a transaction of its own?

Spring’s default is `Propagation.REQUIRED`. No transaction on the thread? Start one. Already inside one? Join it. Nested `REQUIRED` collaborators share one fate. One rollback undoes everyone who joined.

`Propagation.REQUIRES_NEW` does the opposite split. Suspend the outer transaction if present, open a fresh one, commit or roll it back on its own, then resume the outer. The inner commit can survive outer failure — which is exactly what checkout audit usually wants.

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

        chargePayment(purchase); // may throw → outer rolls back

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

Narrate the nested calls. Client enters `checkout`. Spring opens T1. `auditService.record("CHECKOUT_STARTED", …)` goes through the audit bean’s proxy. `REQUIRES_NEW` suspends T1, opens T2, inserts the audit, commits T2, resumes T1. Purchase saves on T1. Payment throws. T1 rolls back — the purchase is gone. The started audit remains, because T2 already committed. Operations gets the breadcrumb. Finance does not get a phantom purchase.

Flip only the propagation on `record` to plain `@Transactional` — still `REQUIRED`. The audit insert joins T1. Payment fails. Rollback erases “CHECKOUT_STARTED” too. Support sees silence. Same methods. Different nesting rule. Different database truth.

Other modes exist for sharper contracts. `SUPPORTS` joins if present, otherwise runs non-transactional. `NOT_SUPPORTED` suspends and runs without a transaction — long reads that should not hold locks. `MANDATORY` demands an existing transaction and fails otherwise. `NEVER` refuses to run inside one. `NESTED` uses a savepoint inside the same physical transaction when the manager supports it, so a partial rollback can return to that mark without undoing the entire outer unit.

Keep the interview sentence short. Propagation is not “how many databases.” It is “what happens when transactional methods nest on one thread.” The proxy and `TransactionInterceptor` read the attribute before the `PlatformTransactionManager` begins, joins, suspends, or resumes.

Misread it and rollbacks surprise you. Catch an exception from a joined participant, ignore that the outer transaction is rollback-only, and wonder why commit fails later. Call a `REQUIRES_NEW` method on `this` inside the same class — no proxy, no suspension, no independent commit. Design reviews usually debate only two modes in practice: `REQUIRED` for shared atomicity, `REQUIRES_NEW` when a side effect must outlive outer failure.

Joining or splitting still says nothing about what concurrent transactions may observe of each other’s rows while work is in flight.

That visibility question is isolation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 53 (*Propagation*).
