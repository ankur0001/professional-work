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

Skip the coordinator fantasy for a moment and book a trip the way product actually sells it: flight seat, hotel night, rental car. Three services. Three local databases. A card charge at the end. You cannot hold XA locks across a hotel API that takes eight seconds and a car broker that times out on Tuesdays. You need a different promise — each step commits locally, and if a later step fails, earlier steps run compensating actions that undo their business effect.

That is the saga pattern. Not one global transaction. A narrative of local transactions with explicit recovery.

Step one: reserve the flight seat — local commit in inventory. Step two: hold the hotel room — local commit in hotels. Step three: reserve the car. Step four: charge the card. If the charge fails, you do not “roll back” the seat the way JDBC rolls back a row. You call `releaseSeat`, `cancelHotelHold`, and `releaseCar` — compensations that are themselves ordinary local transactions. Guests may briefly see a held seat that later frees. Saga trades immediate global consistency for availability and clearer failure handling across services.

```java
@Service
public class TripBookingSaga {

    private final FlightClient flights;
    private final HotelClient hotels;
    private final CarClient cars;
    private final PaymentsClient payments;

    public TripBookingSaga(
            FlightClient flights,
            HotelClient hotels,
            CarClient cars,
            PaymentsClient payments) {
        this.flights = flights;
        this.hotels = hotels;
        this.cars = cars;
        this.payments = payments;
    }

    public BookingResult book(TripRequest request) {
        SeatHold seat = flights.reserveSeat(request.flightId(), request.seat());
        HotelHold hotel = null;
        CarHold car = null;
        try {
            hotel = hotels.holdRoom(request.hotelId(), request.nights());
            car = cars.reserve(request.carClass(), request.pickup());
            payments.charge(request.customerId(), request.total());
            return BookingResult.confirmed(seat, hotel, car);
        } catch (RuntimeException ex) {
            if (car != null) {
                cars.release(car.id());
            }
            if (hotel != null) {
                hotels.cancelHold(hotel.id());
            }
            flights.releaseSeat(seat.id());
            throw ex;
        }
    }
}
```

That sketch is orchestration: one component directs steps and compensations. Choreography is the other style — each service listens for events and reacts. `SeatReserved` triggers hotel holding. `HotelHeld` triggers car reservation. `PaymentFailed` triggers releases and cancels. Orchestration is easier to follow in one place. Choreography avoids a central boss but scatters the flow. Both are sagas if they share the compensation mindset.

Spring does not ship a single `@Saga` annotation that finishes distributed workflows for you. Building blocks yes: local `@Transactional` per service, messaging, transactional outbox so an event publish reliably follows a local commit, and application code or state machines that track progress. Libraries exist on top. The idea you must own is independent of any one of them: forward actions plus compensations, idempotent handlers, and timeouts.

Idempotency matters because retries duplicate. Releasing an already-released seat must be safe. Payments need clear capture versus void semantics. Persist saga state — which steps succeeded — so a crash mid-flow can resume or compensate without guessing.

Kill early misconceptions. Saga is not XA with friendlier branding; it deliberately allows temporary inconsistency. Compensation is not always the mechanical inverse of insert — canceling a started trip may mean refund plus restock, not deleting history. And saga does not remove local transactions; every step still wants a solid boundary inside its service.

We have closed the transaction arc from one-method boundaries through nesting, isolation, rollback rules, XA limits, and sagas. Step back and notice what kept intercepting method calls: begin transaction, maybe later log, authorize, or time. That cross-cutting interception is not unique to transactions.

What modularizes those concerns so every harbor service method does not copy-paste them? Aspect-oriented programming.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 57 (*Saga Pattern*).
