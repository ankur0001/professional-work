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

When scheduling assigns berth B7 to vessel IMO 9321483, billing needs a reservation signal and the yard board needs a redraw. Synchronous fan-out from scheduling couples availability: if billing is down, does the berth assignment roll back? Messaging flips the shape. Scheduling publishes `BerthChanged` events; consumers react on their own clocks.

Spring Cloud Stream binds your functions (or suppliers/consumers) to a broker through a binder — Kafka and RabbitMQ are the common ones. You write a `Function`, `Consumer`, or `Supplier` bean; configuration maps it to destinations. The business code stays about events, not about Kafka producer APIs. That separation is the point: swap binders in a test or migrate brokers without rewriting `applyReservation`.

```java
public record BerthChanged(
        String berthId,
        String imoNumber,
        Instant changedAt,
        String reason) {}

@Configuration
public class BerthStreamConfig {

    @Bean
    Supplier<BerthChanged> berthChangedSupplier(BerthChangeQueue outbound) {
        return outbound::poll; // illustrative; often you use StreamBridge
    }

    @Bean
    Consumer<BerthChanged> billingOnBerthChanged(BillingProjection projection) {
        return event -> projection.applyReservation(event);
    }

    @Bean
    Consumer<BerthChanged> yardBoardOnBerthChanged(YardBoardCache board) {
        return event -> board.redraw(event.berthId(), event.imoNumber());
    }
}
```

```java
@Service
public class BerthAssignmentService {
    private final BerthRepository berths;
    private final StreamBridge bridge;

    public BerthAssignmentService(BerthRepository berths, StreamBridge bridge) {
        this.berths = berths;
        this.bridge = bridge;
    }

    @Transactional
    public void assign(String berthId, String imoNumber) {
        berths.save(BerthAssignment.of(berthId, imoNumber));
        bridge.send("berthChanged-out-0",
                new BerthChanged(berthId, imoNumber, Instant.now(), "ASSIGNED"));
    }
}
```

```yaml
spring:
  cloud:
    stream:
      bindings:
        berthChanged-out-0:
          destination: berth.changed
        billingOnBerthChanged-in-0:
          destination: berth.changed
          group: billing
        yardBoardOnBerthChanged-in-0:
          destination: berth.changed
          group: yard-board
      kafka:
        binder:
          brokers: kafka:9092
```

Walk the flow. Scheduling commits the assignment and sends to `berth.changed`. Billing’s consumer group processes the event into an invoice projection. Yard board’s separate group redraws independently. Two groups mean two independent offsets — billing lag does not freeze the yard board. If billing is down, messages wait in the topic; scheduling does not block the crane operator’s UI on billing’s health. Idempotent consumers matter — at-least-once delivery will redeliver; `applyReservation` must tolerate duplicates by natural key (`berthId` + window) or an event id store.

Publishing inside a transaction without an outbox can still lose messages if the process dies after commit and before send — or send before commit and leak phantoms. Symptom of the first: berth shows ASSIGNED in scheduling DB, billing never invoices until a replay tool runs. Symptom of the second: billing opens an invoice for a reservation that rolled back. Treat “after commit + outbox” as the production upgrade path when loss is unacceptable — write the event row with the assignment, relay asynchronously, delete or mark published.

Failure modes to operate: poison messages that throw forever need a DLQ binding, or one bad payload stalls a partition. Schema changes on `BerthChanged` need compatibility discipline — adding optional fields is safer than renaming `imoNumber` on Friday. Consumer concurrency helps throughput; it also reorders relative to single-thread assumptions inside a projection.

Trade-offs: messaging decouples availability and scales fan-out, at the cost of eventual consistency and harder request/response UX. Check-in still wants a synchronous answer. Events shine for facts many systems must learn. Payload size: publish ids and let billing fetch details inside its context when payloads would drag vessel master data across the bus.

A misconception is treating Cloud Stream as “Kafka with annotations” and ignoring consumer groups; without groups, competing consumers do not share work the way you expect. Another is dumping huge payloads on the bus instead of ids and letting consumers fetch details. A third is assuming messaging deletes the need for APIs — check-in still wants request/response; events shine for fan-out facts.

Cloud patterns alone do not prove gate release or tariff math. Phase 10 starts under Spring’s test annotations, at the engine that discovers methods, runs them, and reports pass or fail.

That engine is JUnit 5.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 92 (*Spring Cloud Stream*).
