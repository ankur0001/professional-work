# Episode 110 — Event-Driven Architecture

| Field | Value |
|---|---|
| Episode | 110 |
| Title | Event-Driven Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 110 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`OrderAuthorized` fired inside one JVM. Warehouse, loyalty, and notification still need to react. If checkout synchronously calls all three over HTTP, you couple availability and latency: any slow peer stretches the request, any down peer breaks the purchase path. Event-driven architecture loosens time coupling — producers emit facts; consumers react on their own clocks.

In Spring, you have two ranges. In-process: `ApplicationEventPublisher` and `@EventListener` (optionally `@TransactionalEventListener` to publish after commit). Across processes: messaging with Spring for RabbitMQ, Kafka, or Spring Cloud Stream. Same idea — facts travel; different delivery guarantees.

Prefer domain events that name what happened, not commands dressed as events. `OrderAuthorized` is a fact. `SendEmail` is a command — put it on a command topic or call a service if you own that workflow. Consumers should be idempotent; at-least-once delivery will duplicate.

```java
public record OrderAuthorized(OrderId orderId, Money amount, Instant at) {}

@Component
public class LoyaltyOnOrderAuthorized {
    private final LoyaltyAccounts loyalty;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(OrderAuthorized event) {
        loyalty.accrue(event.orderId(), event.amount());
    }
}
```

`AFTER_COMMIT` matters. If you listen in the same transaction and the commit fails, side effects may already have escaped. If you publish to Kafka before the DB commits, consumers may see an order that rolled back. Outbox patterns exist for a reason: write the event to an outbox table in the same transaction as the aggregate, then a relay publishes to the broker.

```java
@Service
public class AuthorizeOrderService {
    private final OrderRepository orders;
    private final Outbox outbox;

    @Transactional
    public void authorize(OrderId id, Money amount) {
        Order order = orders.findById(id).orElseThrow();
        order.authorize(amount);
        orders.save(order);
        outbox.enqueue(new OrderAuthorized(id, amount, Instant.now()));
    }
}
```

Cross-service consumers use Spring Cloud Stream or a `KafkaListener`. Keep the payload versioned. Include enough data for the consumer to work without synchronous callbacks into the producer — otherwise you reintroduce temporal coupling through the back door. A loyalty consumer that must call checkout "to get the amount" on every event has not become event-driven; it has become chatty.

```java
@KafkaListener(topics = "order.authorized")
public void onAuthorized(OrderAuthorizedEvent payload) {
    if (loyalty.alreadyAccrued(payload.orderId())) {
        return; // idempotent
    }
    loyalty.accrue(payload.orderId(), payload.amount());
}
```

Failure modes are the curriculum. Poison messages need DLQs. Ordering is per key, not global, on most brokers — partition by `orderId` when sequence per order matters. Exactly-once is a property you design for with idempotent handlers and transactional outboxes, not a flag you flip casually. Tracing should propagate through message headers so OpenTelemetry still shows one logical story from HTTP into the consumer span.

Schema evolution deserves an explicit policy. Additive fields are usually safe; renaming or removing fields breaks old consumers. Prefer a version field or a compatible Avro/JSON schema registry workflow when many teams share a topic.

Misconception: events make the system "eventually consistent" so invariants no longer matter. Aggregate invariants still hold inside the write model; eventual consistency applies between projections and peers. Misconception: replace every REST call with a topic. Synchronous APIs remain right for queries and for actions that must complete in the user request. Misconception: "we use Kafka, so we are event-driven." Topics that carry RPC-shaped request/reply pairs are queues with extra ceremony.

Today we moved from in-process domain events to broker integration, stressed after-commit and outbox discipline, and kept consumers idempotent. One pattern shows up constantly once events feed read sides: the model you write is a bad shape for the screens you read.

That deliberate split is CQRS.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 110 (*Event-Driven Architecture*).

Narration technique: sync fan-out pain → in-process vs broker → AFTER_COMMIT listener → outbox sketch → failure modes → misconceptions → bridge to CQRS.
