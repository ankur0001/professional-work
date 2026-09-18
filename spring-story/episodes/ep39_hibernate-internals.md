# Episode 39 — Hibernate Internals

| Field | Value |
|---|---|
| Episode | 39 |
| Title | Hibernate Internals |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 39 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Last episode we mapped a `Product` and called `productRepository.save`. The method returned. A row appeared. That can feel like magic — and magic is a terrible mental model for production databases.

So peel the stack. Spring Data's repository proxy receives `save`. If the entity has no id, the call typically reaches `EntityManager.persist`. If it already has an id and is treated as detached or existing, the path may go through `merge` or an update flush. Either way, the JPA facade hands work to Hibernate — the provider that owns Session, dirty checking, SQL generation, and the dialect for your database.

Think of Hibernate as three cooperating ideas. First, a metamodel: every `@Entity` becomes a persister that knows the table, columns, id generator, and associations. Second, a Session (Hibernate's richer cousin of `EntityManager`): a unit of work that holds managed instances and queues SQL until flush. Third, a JDBC batching and dialect layer that turns those queued actions into concrete statements for Postgres, MySQL, or whatever you configured.

Watch a create path with an order line item — still entity and database, not bean wiring theater.

```java
@Entity
@Table(name = "order_lines")
public class OrderLine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String sku;

    @Column(nullable = false)
    private int quantity;

    @Column(nullable = false)
    private BigDecimal unitPrice;

    protected OrderLine() {}

    public OrderLine(String sku, int quantity, BigDecimal unitPrice) {
        this.sku = sku;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }
}

// inside a @Transactional boundary
OrderLine line = new OrderLine("SKU-42", 2, new BigDecimal("19.99"));
entityManager.persist(line);
// no INSERT yet — only scheduled
entityManager.flush();
// Hibernate: INSERT INTO order_lines (sku, quantity, unit_price) VALUES (?, ?, ?)
```

`persist` does not mean "SQL right now." It means "make this instance managed and schedule an insert for flush." Flush happens before query execution when needed, on explicit `flush()`, and typically before commit. That delay is intentional: Hibernate can reorder statements, batch inserts, and use the persistence context as a write-behind cache.

Updates ride a different trick. Load a managed `OrderLine`, change `quantity`, and do nothing else. On flush, Hibernate compares the current field values to a snapshot taken at load time. If they differ, it emits `UPDATE`. That is dirty checking. You did not call `update`. The Session noticed.

```java
OrderLine line = entityManager.find(OrderLine.class, 15L);
line.setQuantity(5);
// no repository.save required while managed
entityManager.flush();
// UPDATE order_lines SET quantity = 5 WHERE id = 15
```

Under Boot, you rarely inject `Session` directly. You inject repositories or occasionally `EntityManager`. The Session is still there — bound to the transaction by Spring's `JpaTransactionManager` and Hibernate's session context. Open-session-in-view may keep the Session alive for the whole HTTP request in web apps; that choice affects lazy loading later. For internals, remember: one persistence context per unit of work, SQL at flush boundaries.

Id generation shapes SQL timing. `IDENTITY` often forces an early insert to obtain the key. `SEQUENCE` (and Hibernate's pooled optimizers) can defer inserts and batch better. `UUID` assigned in Java needs no database round-trip for the id. Teams that ignore generator choice discover mysterious flush order and batching limits under load.

Enable SQL logging in development when you are learning:

```properties
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true
logging.level.org.hibernate.orm.jdbc.bind=TRACE
```

Those logs are not decoration. They are how you verify that "I updated a field" became one `UPDATE`, not a delete-plus-insert, and that "I loaded an order" did not secretly fire twelve child selects — a problem we will name later as N+1.

People sometimes treat Hibernate as "a SQL generator I should fight with native queries everywhere." Native SQL is a tool, not a lifestyle. The provider earns its keep when dirty checking, cascading, and the unit of work match your domain operations. People also assume `save` always issues SQL immediately. It schedules work; the transaction and flush policy decide when the database sees it.

We opened the engine: metamodel, Session as unit of work, persist versus flush, dirty checking, dialects, and generators. The next gap is sharper. If an entity can be "managed," what are the other states — and what happens when you call `persist`, `merge`, or `remove` on the wrong one?

That is the entity lifecycle — Episode Forty.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 39 (*Hibernate Internals*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
