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

Synchronous fan-out hurts. After `Berth.reserve` succeeds, scheduling used to call billing over Feign, then the yard board, then notifications. If billing was down, did the reservation roll back? Event-driven architecture decouples that timeline: scheduling publishes `BerthReserved`; billing and others consume when they can.

Distinguish in-process events from broker events. Spring’s `ApplicationEventPublisher` notifies listeners inside the same JVM — useful for clearing caches or updating a local projection. Cross-service decoupling needs a broker (Kafka via Cloud Stream, for example) and delivery rules you can operate. Mixing them without care — a transactional listener that assumes local and remote are the same — is how phantom invoices appear.

```java
public record BerthReserved(BerthId berthId, ImoNumber imo, ReservationWindow window) {}

@Service
public class ReserveBerthService {
    private final BerthRepository berths;
    private final ApplicationEventPublisher publisher;

    @Transactional
    public void reserve(BerthId id, ImoNumber imo, ReservationWindow window) {
        Berth berth = berths.findById(id).orElseThrow();
        BerthReserveResult result = berth.reserve(imo, window);
        if (!result.accepted()) {
            throw new BerthConflictException(result.reason());
        }
        berths.save(berth);
        publisher.publishEvent(result.event());
    }
}

@Component
public class BerthReservedAfterCommitListener {
    private final StreamBridge bridge;

    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void on(BerthReserved event) {
        bridge.send("berthReserved-out-0", event);
    }
}
```

```java
@Component
public class BillingBerthReservedHandler {
    private final BillingProjection projection;

    @Bean
    Consumer<BerthReserved> billingOnBerthReserved() {
        return event -> projection.openReservationInvoice(event);
    }
}
```

`AFTER_COMMIT` matters: listeners that run before commit can publish a reservation that rolls back. Outbox patterns upgrade this further — write the event to an outbox table in the same transaction, then relay to Kafka — when loss is unacceptable. Walk dual-write loss: process dies after commit, before `bridge.send`; scheduling shows B7 reserved; billing never invoices until replay. Walk dual-write phantom: send before commit, transaction rolls back on a later constraint; billing invoices a ghost. Outbox makes the event row commit atomically with the berth row; a relay polls or tails that table.

Consumers must be idempotent; at-least-once delivery will replay `BerthReserved` for B7. Key invoices by `berthId` + window or by event id. Failure modes stay honest. Billing lag means invoices trail assignments — observe projection lag with a gauge (`harbor.billing.projection.lag.seconds`). Poison messages need a dead-letter path, not infinite retries that stall the partition. Events are facts about the past (`Reserved`), not commands (`ReserveBerth`) dressed as events — commands ask for work; events announce what already happened.

Runtime symptoms: operators see the board update instantly (same JVM projection) while billing invoices appear minutes later (broker consumer) — that is eventual consistency working, not a bug, unless lag SLO burns. Another: duplicate invoices after a rebalance when the consumer was not idempotent. Another: a “event” named `CreateInvoice` that still expects a synchronous response — that is an RPC on a topic.

Trade-offs: decoupling availability and fan-out versus harder end-to-end reasoning and eventual consistency UX. Keep synchronous APIs for trucker check-in; use events for facts many contexts must learn. Payload size: ids plus enough fields for the consumer to act beats dragging full vessel graphs across Kafka. Ordering: partition by `berthId` when per-berth order matters.

Schema evolution needs the same honesty as Feign contracts. Add optional fields; avoid renaming `imo` under a live consumer group. When a breaking change is unavoidable, a new topic version (`berth.reserved.v2`) beats silent poison on `v1`. Measure consumer lag per group; a single stuck billing consumer should not be invisible because yard-board lag is fine.

A misconception is replacing every API with events until a trucker check-in requires five topics to return a response. Another is publishing from a transaction that has not committed. A third is huge payloads on the bus instead of ids plus follow-up queries inside the billing context.

Once events feed read sides, a familiar split appears: the model you write for berth invariants is a bad shape for the schedule board screen. That intentional split is CQRS.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 110 (*Event-Driven Architecture*).
