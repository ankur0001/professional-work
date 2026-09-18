# Episode 43 — Relationships

| Field | Value |
|---|---|
| Episode | 43 |
| Title | Relationships |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 43 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A single `@Entity` maps one table. Real domains are graphs. An order has lines. A line belongs to an order. A product may appear on many lines. Relationship mappings tell Hibernate how foreign keys and join tables mirror those links — and whether loading a parent also loads children.

Start with the classic pair: `Order` and `OrderLine`.

```java
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String customerEmail;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLine> lines = new ArrayList<>();

    protected Order() {}

    public Order(String customerEmail) {
        this.customerEmail = customerEmail;
        this.status = OrderStatus.NEW;
    }

    public void addLine(String sku, int quantity, BigDecimal unitPrice) {
        OrderLine line = new OrderLine(this, sku, quantity, unitPrice);
        lines.add(line);
    }

    public List<OrderLine> getLines() {
        return Collections.unmodifiableList(lines);
    }
}

@Entity
@Table(name = "order_lines")
public class OrderLine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @Column(nullable = false)
    private String sku;

    private int quantity;

    private BigDecimal unitPrice;

    protected OrderLine() {}

    OrderLine(Order order, String sku, int quantity, BigDecimal unitPrice) {
        this.order = order;
        this.sku = sku;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }
}
```

Read the mapping as a conversation. `@OneToMany(mappedBy = "order")` says the foreign key lives on the `OrderLine` side — the `order` field owns the relationship. `cascade = CascadeType.ALL` means persisting or removing the `Order` cascades to its lines. `orphanRemoval = true` means removing a line from the collection schedules a delete for that line row. `@ManyToOne(fetch = LAZY)` keeps the parent from loading until touched — and keeps line queries from eagerly pulling the whole order graph unless you ask.

Always maintain both sides in one place. The `addLine` method sets `line.order` and adds to `lines`. If you only add to the list and leave `order` null, the foreign key may not write. If you only set `order` and forget the collection, in-memory navigation lies to you even when the database is fine.

Cardinality choices matter. `@ManyToOne` / `@OneToMany` cover parent-child. `@OneToOne` fits a dedicated shipping address row. `@ManyToMany` needs a join table — use it sparingly; often a first-class association entity (like `Enrollment`) is clearer than a naked many-to-many.

Fetch type is where production pain hides. JPA's default for `@ManyToOne` and `@OneToOne` is eager in the specification, though teams often override to lazy. Collections default to lazy. Eager collections on `Order.lines` look convenient until you load fifty orders and Hibernate joins or selects every line every time. Prefer lazy defaults and fetch what a use case needs with a query — join fetch, entity graphs, or batch size — which we will sharpen in JPQL and N+1 episodes.

```java
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerEmail(String email);
}

@Transactional
public Long placeOrder(String email, List<LineRequest> requests) {
    Order order = new Order(email);
    for (LineRequest request : requests) {
        order.addLine(request.sku(), request.quantity(), request.unitPrice());
    }
    return orderRepository.save(order).getId();
    // cascade persists lines; FK order_id set from the many-to-one side
}
```

Cascade is not free affection. Cascading `REMOVE` from a shared reference (say cascading from `Product` to every `OrderLine` that ever used it) is how you delete history by accident. Cascade along true ownership boundaries — order owns lines — not along every association you can annotate.

Bidirectional mappings need `equals`/`hashCode` care. Using a generated id in `hashCode` before persist breaks `Set` membership. Many teams equal by business key or use identity only after the id exists. Do not put entities into sets casually without a strategy.

Relationship mappings give you a graph. Querying that graph with SQL strings tied to column names fights the model. JPQL lets you query entities and associations in object terms — select orders, join lines, filter by customer — without dropping to JDBC.

That is Episode Forty-Four — JPQL.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 43 (*Relationships*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
