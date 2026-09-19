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

A manifest import throws `ManifestException` — checked, on purpose, so callers must handle bad customs data. The service method is `@Transactional`. The exception escapes. The transaction commits anyway. Half a manifest sits in the database with a status that says “accepted.” Nightly reconciliation fails. Someone asks why Spring “ignored” the error.

It did not ignore the error. It followed the default rollback rules.

Unchecked exceptions — `RuntimeException` and subclasses — and `Error` mark the transaction for rollback. Checked exceptions do not, unless you list them. The interceptor inspects what escapes the advised method, matches rollback and no-rollback rules, and tells the manager to commit or roll back.

For harbor manifests, the business meaning is usually clear: a checked `ManifestException` is fatal to the unit of work. Say so on the annotation.

```java
@Service
public class ManifestIntakeService {

    private final ManifestRepository manifests;
    private final CustomsNotifier notifier;

    public ManifestIntakeService(ManifestRepository manifests, CustomsNotifier notifier) {
        this.manifests = manifests;
        this.notifier = notifier;
    }

    @Transactional(
            rollbackFor = ManifestException.class,
            noRollbackFor = CustomsLinkDownException.class)
    public ManifestId intake(ManifestDraft draft) throws ManifestException {
        Manifest manifest = Manifest.from(draft);
        manifests.save(manifest);

        if (!manifest.passesCustomsRules()) {
            throw new ManifestException("CUSTOMS_REJECT", manifest.id());
        }

        try {
            notifier.announce(manifest.id());
        } catch (CustomsLinkDownException ex) {
            manifest.markNotifyPending();
            manifests.save(manifest);
            return manifest.id(); // commit intake; retry notify later
        }

        return manifest.id();
    }
}
```

```java
public class ManifestException extends Exception {
    public ManifestException(String code, ManifestId id) {
        super(code + ":" + id);
    }
}

public class CustomsLinkDownException extends RuntimeException {
    public CustomsLinkDownException(String message, Throwable cause) {
        super(message, cause);
    }
}
```

Read the attributes aloud. `rollbackFor = ManifestException.class` means: even though this is checked, undo the transaction. Without it, the default would commit the saved manifest after a customs reject — the bug that started this episode. `noRollbackFor = CustomsLinkDownException.class` means: even though this is a runtime exception, keep the intake; mark notify-pending and let a retry path finish the side effect. Defaults would have wiped a valid manifest because a downstream link blinked.

Rules match the exception that actually escapes, including subclasses. Catch inside the method and swallow without rethrowing, and the interceptor sees success — partial state may commit. Catching is not a rollback rule; it is a decision that the boundary completed.

You can list multiple types, or use the stringly `rollbackForClassName` forms in older configs. Prefer explicit class literals. In tests, `@Rollback` / `@Commit` steer the test transaction — related idea, different switch.

A frequent bug is wrapping a runtime failure in a checked type, adding `throws`, and forgetting `rollbackFor`. Another is `noRollbackFor = Exception.class`, then wondering why serious failures still commit. Prefer domain exceptions with clear fatal versus recoverable meaning, and align the annotation with that meaning — especially for checked `ManifestException` on intake paths.

Local rules still assume one resource manager. The day intake must write Postgres and publish a JMS booking message in one breath, a single local boundary is no longer enough.

Distributed transactions are where that stretch gets honest — and expensive.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 55 (*Rollback Rules*).
