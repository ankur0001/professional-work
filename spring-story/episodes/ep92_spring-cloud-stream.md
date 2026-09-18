# Episode 92 — Spring Cloud Stream

| Field | Value |
|---|---|
| Episode | 92 |
| Title | Spring Cloud Stream |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 92 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Resilience4j makes synchronous remote calls safer. It does not change the fact that synchronous calls couple availability: if inventory is slow, order still waits unless you designed an asynchronous boundary. Messaging flips the conversation. Order publishes an event. Inventory consumes it later. The broker absorbs spikes. Spring Cloud Stream exists so your code talks to channels and functions while a binder talks to Kafka, RabbitMQ, or another broker — swap binders without rewriting business listeners.

The modern programming model leans on Spring Cloud Function. You define beans that are `Supplier`, `Function`, or `Consumer`, and Stream binds them to destinations. A supplier can poll or produce messages; a function transforms; a consumer processes. Configuration maps those beans to topics or queues through binder-specific properties.

```java
@Configuration
public class OrderStreamConfig {

    @Bean
    public Supplier<OrderPlaced> orderPlacedSupplier(OrderEventBuffer buffer) {
        return buffer::poll;
    }

    @Bean
    public Consumer<OrderPlaced> reserveInventory(InventoryService inventory) {
        return event -> inventory.reserve(event.sku(), event.qty(), event.orderId());
    }
}
```

```yaml
spring:
  cloud:
    function:
      definition: orderPlacedSupplier;reserveInventory
    stream:
      bindings:
        orderPlacedSupplier-out-0:
          destination: orders.placed
        reserveInventory-in-0:
          destination: orders.placed
          group: inventory
      kafka:
        binder:
          brokers: kafka:9092
```

In one service you might only produce; in another, only consume. The `group` consumer property gives competing consumers — multiple inventory instances share work. Without a group, pub-sub semantics can deliver to every instance depending on binder defaults; know which you want.

Error handling and partitioning are where Stream stops being a demo. Failed messages can go to dead-letter destinations after retries. Partition keys keep all events for one `orderId` on the same partition so consumers can process in order per key. Idempotent consumers matter because at-least-once delivery is common: processing the same `OrderPlaced` twice must not double-reserve stock. That is domain design, not a binder switch.

```java
@Bean
public Function<OrderPlaced, InventoryReserved> allocate() {
    return event -> {
        // pure-ish transform useful in stream pipelines
        return InventoryReserved.of(event.orderId(), event.sku());
    };
}
```

Compared with raw `KafkaTemplate`, Stream reduces boilerplate and standardizes binding names. Compared with Feign, Stream changes the consistency story: you trade immediate response for eventual processing. Checkout might return “accepted” after persisting an outbox row and publishing, while inventory catches up. Distributed transactions across HTTP become sagas or outbox patterns across events — territory you touched conceptually in earlier architecture lessons; Stream is one transport for those designs.

Transactional outbox is the companion pattern when you must not lose “OrderPlaced” after committing the order row. Write the event to an outbox table in the same database transaction as the order, then a poller or CDC publisher feeds Stream. Skipping that and publishing over the network mid-transaction is how you get orders without events — or events without orders — under partial failure.

A misconception is putting Stream and Feign on every path “because Cloud.” Prefer HTTP when the caller needs the answer to continue; prefer events when fire-and-forget or fan-out fits. Another is forgetting consumer groups and then watching every pod process every message. A third is assuming the binder guarantees exactly-once end-to-end business processing — broker exactly-once and your idempotency keys are different layers.

Today we bound functions to Kafka destinations, separated producer and consumer roles, and marked delivery semantics and idempotency as part of the design — completing the main Spring Cloud pattern tour from config through messaging.

Look at what we built across this phase: many moving parts, each able to break in subtle ways. Before those services face production traffic, you need confidence in small units and in assembled slices. That confidence starts with the test runner almost every Spring project already sits on.

That runner is JUnit 5.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 92 (*Spring Cloud Stream*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
