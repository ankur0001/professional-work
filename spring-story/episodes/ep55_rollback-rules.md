# Episode 55 — Rollback Rules

| Field | Value |
|---|---|
| Episode | 55 |
| Title | Rollback Rules |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 55 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Not every exception means “undo everything.” Imagine a document import that writes a batch header, inserts two hundred line rows, then tries to notify a downstream indexer. If the indexer client throws because the search cluster is briefly unreachable, do you really want to erase two hundred successfully validated lines — or commit the import and retry notification later? Flip the scene: a payment capture throws a domain-checked `PaymentDeclinedException`. If that type is checked and you forgot to declare rollback, Spring may commit the surrounding work anyway — leaving an order marked paid when money never moved.

Rollback rules are how you encode which failures are fatal to the transaction boundary.

Spring’s default is sharp and easy to misremember. Unchecked exceptions — subclasses of `RuntimeException` — and `Error` mark the transaction for rollback. Checked exceptions — subclasses of `Exception` that are not runtime — do not, unless you say so. The interceptor inspects what escapes the advised method, matches it against rollback and no-rollback rules, and tells the transaction manager to commit or roll back.

```java
@Service
public class InvoiceImportService {

    private final InvoiceRepository invoices;
    private final IndexerClient indexer;

    public InvoiceImportService(InvoiceRepository invoices, IndexerClient indexer) {
        this.invoices = invoices;
        this.indexer = indexer;
    }

    @Transactional(
            rollbackFor = PaymentDeclinedException.class,
            noRollbackFor = IndexerUnavailableException.class)
    public ImportResult importBatch(ImportFile file) throws PaymentDeclinedException {
        InvoiceBatch batch = InvoiceBatch.parse(file);
        invoices.save(batch);

        try {
            indexer.submit(batch.id());
        } catch (IndexerUnavailableException ex) {
            // keep the batch; schedule a retry outside this method
            batch.markIndexPending();
            invoices.save(batch);
            return ImportResult.savedWithoutIndex(batch.id());
        }

        return ImportResult.savedAndIndexed(batch.id());
    }
}
```

```java
// checked on purpose — must be listed in rollbackFor to undo the TX
public class PaymentDeclinedException extends Exception {
    public PaymentDeclinedException(String code) {
        super(code);
    }
}

public class IndexerUnavailableException extends RuntimeException {
    public IndexerUnavailableException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

Speak through the annotation. `rollbackFor = PaymentDeclinedException.class` says: even though this is checked, treat it as fatal — roll back. `noRollbackFor = IndexerUnavailableException.class` says: even though this is a runtime exception, do not undo the database work — commit the batch and let the caller handle a pending index state. Without those attributes, the defaults would invert both stories: the declined payment might leave committed debris, and a flaky indexer might wipe a valid import.

You can list multiple types. Rules apply to the exception that actually escapes the method — including subclasses, following Spring’s matching. If you catch an exception inside the method and do not rethrow, the interceptor never sees it; the transaction may commit with whatever partial state you left. Catching and swallowing is not a rollback rule. It is a decision to finish successfully from the interceptor’s point of view.

There is also `rollbackForClassName` / `noRollbackForClassName` for stringly-typed configuration, and XML-era rule sets that still appear in older codebases. Prefer type-safe `rollbackFor` / `noRollbackFor` on the annotation in modern code. In tests, `@Rollback` / `@Commit` on Spring Test methods steer the test transaction — related idea, different switch.

A frequent bug is converting a runtime failure into a checked wrapper, declaring `throws`, and forgetting `rollbackFor`. Another is marking `noRollbackFor` on a broad type like `Exception`, then wondering why serious failures still commit. Be precise. Prefer domain exceptions with clear fatal versus recoverable meaning, and align the annotation with that meaning.

We can now declare the boundary, nest it with propagation, tune what concurrency may see, and decide which exceptions undo work. All of that still assumed one resource manager — typically one database. The day your “one business action” must mutate a database and a message broker, or two databases, in lockstep, local `@Transactional` is no longer enough.

How multiple systems agree — or fail to — is distributed transactions territory. That is where we go next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 55 (*Rollback Rules*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
