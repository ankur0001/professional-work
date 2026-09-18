# Episode 51 — N+1 Problem

| Field | Value |
|---|---|
| Episode | 51 |
| Title | N+1 Problem |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 51 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You load twenty orders for a customer dashboard. SQL log shows one `SELECT` for orders — good. Then, as the JSON serializer or a loop touches each order's lines, nineteen more selects appear. Or twenty. Or two hundred on a busier day. That is the N+1 problem: **1** query for the parents plus **N** queries for children, one per parent.

It shows up wherever lazy associations meet loops.

```java
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String customerEmail;

    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderLine> lines = new ArrayList<>();

    public List<OrderLine> getLines() {
        return lines;
    }
}
```

```java
@Transactional(readOnly = true)
public List<OrderResponse> listForCustomer(String email) {
    List<Order> orders = orderRepository.findByCustomerEmail(email);
    // 1 query: select * from orders where customer_email = ?

    List<OrderResponse> responses = new ArrayList<>();
    for (Order order : orders) {
        // each getLines() may fire: select * from order_lines where order_id = ?
        responses.add(OrderResponse.from(order, order.getLines()));
    }
    return responses;
}
```

Lazy is not the villain. Lazy is the default that keeps writes and incidental loads cheap. The villain is navigating lazy associations across a collection without a fetch plan. Open-session-in-view can make this "work" without `LazyInitializationException` while still issuing N+1 SQL — silent latency.

Fix it by loading what you need in fewer queries. Join fetch is the clearest teaching fix:

```java
public interface OrderRepository extends JpaRepository<Order, Long> {

    @Query("""
            select distinct o from Order o
            left join fetch o.lines
            where o.customerEmail = :email
            """)
    List<Order> findWithLinesByCustomerEmail(@Param("email") String email);
}
```

```java
@Transactional(readOnly = true)
public List<OrderResponse> listForCustomer(String email) {
    List<Order> orders = orderRepository.findWithLinesByCustomerEmail(email);
    // typically 1 select with a join (or a follow-up select, depending on plan)
    return orders.stream()
            .map(order -> OrderResponse.from(order, order.getLines()))
            .toList();
}
```

`join fetch` tells Hibernate to initialize `lines` as part of loading `Order`. `distinct` softens duplicate parent rows that joins can produce in the result list. For pagination, join fetch of collections is awkward — the database page of joined rows is not the same as a page of parent entities. Prefer fetching collections for non-paged detail use cases, or use a two-step approach: page parent ids, then fetch aggregates by those ids with `join fetch` or `@BatchSize`.

`@BatchSize` on the collection or entity reduces N+1 into fewer batched IN queries:

```java
@OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
@BatchSize(size = 25)
private List<OrderLine> lines = new ArrayList<>();
```

Instead of twenty single-id selects, Hibernate may load lines for twenty orders in one or a few `WHERE order_id IN (...)` queries. Still not always one query — but dramatically better — and useful when you cannot join fetch every path.

Entity graphs offer another explicit plan:

```java
@EntityGraph(attributePaths = {"lines"})
List<Order> findByCustomerEmail(String email);
```

Diagnosis before dogma. Enable SQL logging. Reproduce the endpoint. Count statements. If you see the repeating child select, you found N+1. Fix with fetch join, entity graph, batch size, or a DTO query that selects exactly the columns the screen needs — not by marking every association `FetchType.EAGER`, which often moves the pain to writes and to every accidental load.

Notice what all of these fixes assume: an open persistence context and a transaction that spans the whole read. If each repository call opens and closes its own short transaction, even a good fetch query can be followed by lazy failures when you touch something else. The boundary that keeps the unit of work honest has a name in Spring.

`@Transactional` — Episode Fifty-Two — is where persistence context lifetime, commit, and rollback become deliberate instead of accidental.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 51 (*N+1 Problem*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
