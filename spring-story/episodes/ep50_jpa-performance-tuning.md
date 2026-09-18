# Episode 50 — Performance Tuning

| Field | Value |
|---|---|
| Episode | 50 |
| Title | Performance Tuning |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 50 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

JPA makes the happy path easy — and makes it easy to hide fifty SQL statements behind one repository call. Performance tuning in a Spring Data app is not a single annotation. It is a checklist you apply with evidence: measure SQL, then fix fetch shapes, batching, indexes, and context lifetime.

Start with visibility. If you cannot see statements, you are guessing.

```properties
spring.jpa.show-sql=false
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.orm.jdbc.bind=TRACE
spring.jpa.properties.hibernate.generate_statistics=true
```

In staging, pair that with datasource metrics and a slow-query log on the database. Count statements per API request. A checkout that runs one select and one insert is healthy. A product list that runs one select plus one select per row is not — that pattern has a name waiting in the next episode.

Fetch strategy is the first dial. Default lazy collections are correct for writes and detail screens you do not always need. For a read model that always shows order lines, use a dedicated query with `join fetch` or an `@EntityGraph`:

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @EntityGraph(attributePaths = "lines")
    @Query("select o from Order o where o.id = :id")
    Optional<Order> findDetailedById(@Param("id") Long id);
}
```

Entity graphs keep the fetch plan on the repository method instead of forcing eager mapping on the entity forever. That separation matters: the same `Order` stays lean for admin updates and rich for detail views.

Batching cuts round-trips on writes:

```properties
spring.jpa.properties.hibernate.jdbc.batch_size=50
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
```

When you `persist` fifty new `OrderLine` rows in one transaction, Hibernate can send them in JDBC batches. Identity generators often undermine batch inserts because the database must return keys immediately — sequences or UUIDs batch more cleanly. Match generator choice to write patterns.

Pagination protects list endpoints:

```java
Page<Product> page = productRepository.findByActiveTrue(
        PageRequest.of(pageNumber, 50, Sort.by("name")));
```

Never `findAll()` a production catalog table into memory because the UI "might need it." For scrolling APIs, prefer keyset pagination when offsets get deep — large `OFFSET` values make the database walk and discard rows.

DTO projections and read-only transactions reduce work:

```java
@Transactional(readOnly = true)
public List<ProductPriceView> listPrices() {
    return productRepository.findAllProjectedBy();
}

public interface ProductPriceView {
    String getSku();
    BigDecimal getPrice();
}
```

`readOnly = true` hints the provider and the flush behavior: dirty checking can be lighter, and you signal intent. Interface or class-based projections avoid hydrating full entities when a screen needs three fields.

Indexes belong in the database, not only in hope. If you filter orders by `customer_email` and `status`, add a composite index that matches the query. Hibernate will not invent your indexing strategy. Explain plans tell you whether a Specification is doing a sequential scan on a million-row table.

Clear the persistence context in bulk jobs:

```java
for (int i = 0; i < imports.size(); i++) {
    entityManager.persist(toEntity(imports.get(i)));
    if (i % 50 == 0) {
        entityManager.flush();
        entityManager.clear();
    }
}
```

Without `clear()`, every imported entity stays managed and the first-level cache grows without bound.

Open-session-in-view deserves a conscious decision. Leaving the session open for the whole MVC request makes lazy loads in the view layer work — and hides N+1 until production traffic spikes. Many teams disable it (`spring.jpa.open-in-view=false`) and fetch explicitly inside transactional services.

Tuning gives you knobs. One anti-pattern still deserves its own episode because it is the most common ORM latency incident in the wild: one query for parents, then one query per parent for children.

Episode Fifty-One — the N+1 Problem.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 50 (*Performance Tuning*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
