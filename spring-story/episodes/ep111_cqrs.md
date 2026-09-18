# Episode 111 — CQRS

| Field | Value |
|---|---|
| Episode | 111 |
| Title | CQRS |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 111 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

An `Order` aggregate protects write invariants — authorize before capture, lines frozen after authorize. The customer support screen wants a denormalized page: order header, payment status, shipment tracking, loyalty points, last five notes. Forcing that screen through the write aggregate produces either N+1 queries, bloated aggregates, or transactions that lock too much. CQRS — Command Query Responsibility Segregation — separates the write model from the read model on purpose.

Command side: validate and mutate aggregates, emit events. Query side: answer reads from models shaped for screens — SQL views, separate tables, Redis documents, Elasticsearch. The two sides can share a database in a mild form or use different stores in a strong form. Mild CQRS is often enough in a modular Spring monolith.

```java
// write model — commands only
@RestController
@RequestMapping("/orders")
public class OrderCommandController {
    private final AuthorizeOrderService authorize;

    @PostMapping("/{id}/authorize")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void authorize(@PathVariable OrderId id, @RequestBody AuthorizeRequest body) {
        authorize.authorize(id, body.amount());
    }
}

// read model — queries only
@RestController
@RequestMapping("/order-views")
public class OrderQueryController {
    private final OrderViewRepository views;

    @GetMapping("/{id}")
    public OrderSupportView get(@PathVariable String id) {
        return views.findSupportView(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND));
    }
}
```

```java
public interface OrderViewRepository {
    Optional<OrderSupportView> findSupportView(String orderId);
}

// projection updated from events
@Component
public class OrderViewProjector {
    private final OrderViewJdbc views;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(OrderAuthorized event) {
        views.markAuthorized(event.orderId().value(), event.amount());
    }

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(OrderShipped event) {
        views.attachTracking(event.orderId().value(), event.trackingNumber());
    }
}
```

```sql
-- read table shaped for the support screen
CREATE TABLE order_support_view (
  order_id        TEXT PRIMARY KEY,
  status          TEXT NOT NULL,
  authorized_amt  NUMERIC,
  tracking_number TEXT,
  loyalty_points  INT,
  updated_at      TIMESTAMPTZ NOT NULL
);
```

Reads become simple SELECTs. Writes stay strict. Consistency between them is eventual unless you update the read model in the same transaction — possible when both share a DB, harder when the read side is another technology.

Spring Data fits naturally: one repository style for aggregates, another for query objects or JOINs via JDBC templates. Do not expose write entities on query controllers "just this once" — that once becomes the permanent API.

CQRS is not required everywhere. A settings page with three fields can use one model. Adopt CQRS where read shapes and write invariants diverge painfully — support consoles, search, personalized feeds. Event sourcing is optional and heavier; CQRS does not demand event sourcing, though they pair often. When you do both, the event store is the write log and projections become the query models — powerful, and a bigger operational commitment than a single SQL view.

Watch lag. A Micrometer gauge or a `updated_at` age on the projection tells on-call whether support is looking at stale data. Without that signal, every "wrong status in the UI" ticket becomes a ghost hunt across write and read paths.

Misconception: CQRS means microservices. You can CQRS inside one deployable. Misconception: every query must be eventually consistent. Same-database projections updated in-transaction keep read-your-writes for many flows. Misconception: the write model may never be queried. Admin tools sometimes need a careful get-by-id on the aggregate; the split is about default paths and screen shapes, not a religious ban.

Today we split command and query controllers, projected an `order_support_view` from domain events, and kept the write aggregate focused. Patterns only earn trust when they survive messy production constraints — traffic, people, legacy, and tradeoffs.

The last episode is where those patterns meet case studies and the series closes.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 111 (*CQRS*).

Narration technique: write vs support-screen conflict → CQRS definition → separate controllers → projector + SQL view → when to use → misconceptions → bridge to case studies / series close.
