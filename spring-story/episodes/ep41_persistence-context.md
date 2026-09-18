# Episode 41 — Persistence Context

| Field | Value |
|---|---|
| Episode | 41 |
| Title | Persistence Context |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 41 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Lifecycle states only make sense inside a room where Hibernate keeps its notes. That room is the persistence context — the first-level cache and unit of work for one `EntityManager` / Session.

Say you load a `Customer` twice by the same id inside one transaction:

```java
@Transactional
public void demonstrateIdentity(Long customerId) {
    Customer first = entityManager.find(Customer.class, customerId);
    Customer second = entityManager.find(Customer.class, customerId);

    // true — same managed instance from the persistence context
    assert first == second;
}
```

The second `find` does not hit the database again for that id. The persistence context already holds the managed instance. That is the first-level cache. It is mandatory, per context, and not the same thing as Hibernate's optional second-level cache we will meet later.

Dirty checking lives here too. When an entity becomes managed, Hibernate keeps a snapshot. On flush it compares current values to the snapshot and queues `UPDATE` statements for what changed. You can mutate fields across several service method calls in the same transaction; one flush can write them together.

Flush is the moment the context synchronizes with the database. Triggers include commit, explicit `flush()`, and auto-flush before certain queries so those queries see your pending changes. Flush mode defaults usually do the right thing; forcing `FlushModeType.COMMIT` can make queries miss unflushed writes and confuse people debugging "I set the status but the query still shows the old one."

```java
@Entity
@Table(name = "customers")
public class Customer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String email;

    @Column(nullable = false)
    private String displayName;

    protected Customer() {}

    public Customer(String email, String displayName) {
        this.email = email;
        this.displayName = displayName;
    }

    public void rename(String displayName) {
        this.displayName = displayName;
    }
}
```

```java
@Transactional
public void renameCustomer(Long id, String newName) {
    Customer customer = customerRepository.findById(id).orElseThrow();
    customer.rename(newName);
    // no save() required — managed entity + dirty checking
    // flush on commit writes UPDATE customers SET display_name = ? WHERE id = ?
}
```

That "no save required" rule only holds while the entity is managed inside an open persistence context. Spring's `@Transactional` typically binds one persistence context to the transaction. When the method ends successfully, flush and commit run. When it rolls back, the SQL is not committed — and the in-memory object may still show the new name even though the database does not. Never treat a managed Java instance as proof the row was stored after a failure.

Clear and detach matter under memory pressure or when you batch large imports. `entityManager.clear()` drops the entire first-level cache — every managed entity becomes detached. `detach(entity)` drops one. After clear, further field changes are not tracked until you merge or reload. Batch jobs that persist thousands of rows without clearing can balloon heap because every instance stays managed.

Repeatable read inside one context is a subtlety. If another transaction commits a change to the same row, your managed instance may still show the old values until you refresh. `entityManager.refresh(customer)` reloads from the database and resets the snapshot. That is intentional isolation of the unit of work, not a bug — but it surprises people who expect every getter to be a live SELECT.

Spring Data repositories do not replace the persistence context; they use it. `findById` returns managed instances inside a transaction. `save` on an already managed entity often just returns it after ensuring it is persisted. Out of a transaction, repository calls may open a short-lived context per call — which is why lazy loads and multi-step edits need an explicit transactional boundary. We will deepen that when we reach `@Transactional`; for now, treat "open context for the whole use case" as the rule of thumb.

If you think the persistence context is "just a cache you can turn off," you misunderstand JPA. Without it there is no identity guarantee, no dirty checking, no unit of work. If you keep calling `save` after every setter "to be safe," you are fighting the model instead of using it.

We have a room that tracks entities, caches by id, and flushes SQL. Typing `EntityManager` everywhere still hurts. Teams want a focused API: find by email, save a customer, delete by id — without reinventing DAOs.

That appetite is exactly why Spring Data repositories exist — Episode Forty-Two.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 41 (*Persistence Context*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
