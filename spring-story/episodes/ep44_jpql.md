# Episode 44 — JPQL

| Field | Value |
|---|---|
| Episode | 44 |
| Title | JPQL |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 44 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Derived repository method names are great until the question outgrows English. "Find orders for this email with status NEW that contain SKU-42 and were placed after Monday" becomes a method name nobody wants to read. JPQL — Jakarta Persistence Query Language — queries the entity model instead of the physical schema.

JPQL looks like SQL with a different subject. You select entities and properties. You join associations by field name. Hibernate translates to SQL for your dialect.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("""
            select distinct o from Order o
            join o.lines line
            where o.customerEmail = :email
              and o.status = :status
              and line.sku = :sku
            """)
    List<Order> findOpenOrdersWithSku(
            @Param("email") String email,
            @Param("status") OrderStatus status,
            @Param("sku") String sku);

    @Query("""
            select o from Order o
            left join fetch o.lines
            where o.id = :id
            """)
    Optional<Order> findWithLinesById(@Param("id") Long id);
}
```

Walk the first query. `from Order o` uses the entity name (defaults to the simple class name). `join o.lines line` navigates the `@OneToMany` field — not the table name `order_lines`. The `where` clause filters on entity properties. Parameters are bound by name. `distinct` helps when joins multiply parent rows in the result list.

The second query introduces `join fetch`. That is not decoration. It tells Hibernate to load `lines` in the same select so later `order.getLines()` does not fire a second query. Without fetch, a lazy `lines` collection stays uninitialized until touched — and if you touch it in a loop across many orders, you invent the N+1 problem. Remember this pattern; Episode Fifty-One will put it under a microscope.

Projection queries keep payloads small:

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("""
            select new com.example.orders.OrderSummary(o.id, o.customerEmail, o.status, count(line))
            from Order o
            left join o.lines line
            where o.customerEmail = :email
            group by o.id, o.customerEmail, o.status
            """)
    List<OrderSummary> summarizeForCustomer(@Param("email") String email);
}

public record OrderSummary(Long id, String email, OrderStatus status, long lineCount) {}
```

Here you are not managing full `Order` aggregates — you are selecting a DTO constructor expression. Useful for read models and list screens. You cannot dirty-check a DTO; it is not an entity.

Updates and deletes in JPQL are bulk operations:

```java
@Modifying(clearAutomatically = true)
@Query("update Order o set o.status = :status where o.id in :ids")
int markStatus(@Param("ids") Collection<Long> ids, @Param("status") OrderStatus status);
```

Bulk JPQL skips the persistence context's usual per-entity lifecycle. Managed instances already loaded can go stale — hence `clearAutomatically`. Use bulk when you mean bulk; use entity mutation when you need lifecycle callbacks and dirty checking.

Native queries (`nativeQuery = true`) speak SQL and column names. Reach for them when the dialect feature has no JPQL equivalent — window functions, vendor hints — not as a first reflex. Mixing native SQL with entity mapping requires care about what is returned and whether Hibernate can still manage the result.

JPQL errors often show up as `PropertyReferenceException` or unexpected SQL. Turn on SQL logging and compare your mental join to the generated join. If you filter on a column that exists only in the database and not as a mapped field, JPQL cannot see it — map it or use native SQL deliberately.

Static JPQL strings still struggle when the filter set is dynamic: maybe email, maybe status, maybe a date range, maybe none. String concatenation of JPQL is how injection and broken syntax sneak back in. The Criteria API builds queries as objects for those cases.

Episode Forty-Five — Criteria API.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 44 (*JPQL*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
