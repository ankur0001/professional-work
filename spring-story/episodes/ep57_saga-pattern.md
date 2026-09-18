# Episode 57 — Saga Pattern

| Field | Value |
|---|---|
| Episode | 57 |
| Title | Saga Pattern |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 57 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Two-phase commit tried to make many resources behave like one database. For long business flows — book a flight, reserve a hotel, charge a card, email a confirmation — that medicine is often worse than the disease. Steps take seconds or minutes. Participants are other teams’ APIs. Locks cannot stay open across prepare forever. You need a different promise: each step commits locally, and if a later step fails, earlier steps run compensating actions that undo their business effect.

That is the saga pattern. Not one global transaction. A narrative of local transactions with explicit recovery.

Say travel booking. Step one: reserve a seat — local commit in the inventory service. Step two: hold a hotel room — local commit in hotels. Step three: charge the card. If the charge fails, you do not “roll back” the seat the way JDBC rolls back a row. You call `releaseSeat` and `cancelHotelHold` — compensations that are themselves ordinary local transactions. The system may pass through visible intermediate states. Guests might briefly see a held seat that later frees. Saga trades immediate global consistency for availability and clearer failure handling across services.

```java
@Service
public class TripBookingSaga {

    private final InventoryClient inventory;
    private final HotelClient hotels;
    private final PaymentsClient payments;

    public TripBookingSaga(
            InventoryClient inventory,
            HotelClient hotels,
            PaymentsClient payments) {
        this.inventory = inventory;
        this.hotels = hotels;
        this.payments = payments;
    }

    public BookingResult book(TripRequest request) {
        SeatHold seat = inventory.reserveSeat(request.flightId(), request.seat());
        HotelHold hotel = null;
        try {
            hotel = hotels.holdRoom(request.hotelId(), request.nights());
            payments.charge(request.customerId(), request.total());
            return BookingResult.confirmed(seat, hotel);
        } catch (RuntimeException ex) {
            if (hotel != null) {
                hotels.cancelHold(hotel.id());
            }
            inventory.releaseSeat(seat.id());
            throw ex;
        }
    }
}
```

That sketch is orchestration: one component directs the steps and compensations. Choreography is the other style — each service listens for events and reacts. `SeatReserved` triggers hotel holding. `HotelHeld` triggers payment. `PaymentFailed` triggers `ReleaseSeat` and `CancelHotel`. Orchestration is easier to follow in one place. Choreography avoids a central boss but scatters the flow across consumers. Both are sagas if they share the compensation mindset.

Spring does not ship a single `@Saga` annotation that solves distributed workflows for you. What Spring gives you are the building blocks: local `@Transactional` boundaries per service, messaging with Spring Kafka or AMQP, transactional outbox patterns so an event publish reliably follows a local commit, and application code or state machines that track saga progress. Libraries and platforms exist on top — but the idea you must own is independent of any one library: forward actions plus compensations, idempotent handlers, and timeouts.

Idempotency matters because compensations and retries duplicate. Releasing an already-released seat must be safe. Payments need clear capture versus void semantics. Store saga state — which steps succeeded — so a crash mid-flow can resume or compensate without guessing.

Misconceptions to kill early. Saga is not XA with friendlier branding; it deliberately allows temporary inconsistency. Compensation is not always the mechanical inverse of insert — canceling a shipped order may mean refund plus restock, not deleting history. And saga does not remove the need for local transactions; every step still wants a solid `@Transactional` boundary inside its service.

We have closed the transaction arc from one-method boundaries through nesting, isolation, rollback rules, XA limits, and sagas. Step back and notice a pattern that kept appearing: something intercepts method calls to start transactions, maybe later to log, authorize, or time them. That cross-cutting interception is not unique to transactions.

What modularizes those concerns so every service method does not copy-paste them? Aspect-oriented programming — and that is the door into the next phase.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 57 (*Saga Pattern*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
