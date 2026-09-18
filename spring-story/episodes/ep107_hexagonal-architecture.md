# Episode 107 — Hexagonal Architecture

| Field | Value |
|---|---|
| Episode | 107 |
| Title | Hexagonal Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 107 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Layered Spring apps often still let the framework sit in the middle of the onion. A "domain" class annotated with JPA and Jackson, a service that returns `ResponseEntity`, a repository interface that extends Spring Data in the same package as business rules — the layers have names, but the center is not isolated. Hexagonal architecture — ports and adapters — flips the gravity: the domain sits in the center; everything else plugs in around it.

Alistair Cockburn’s idea is simple to say. The application core defines ports — interfaces for things it needs and things that drive it. Adapters implement those ports for HTTP, databases, message brokers, mail. The core never imports Spring Web. Spring remains the composition root that wires adapters to ports.

Draw one hexagon for checkout:

- Driving (primary) port: `PlaceOrderUseCase` — what the outside world can ask the app to do.
- Driven (secondary) ports: `OrderRepository`, `PaymentGateway` — what the app needs from the outside.
- Adapters: `OrderController` (Spring MVC) drives the use case; `JpaOrderAdapter` and `StripePaymentAdapter` implement driven ports.

```java
// domain + application core — no Spring Web imports
public interface PlaceOrderUseCase {
    Order place(PlaceOrderCommand command);
}

public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(OrderId id);
}

public class PlaceOrderService implements PlaceOrderUseCase {
    private final OrderRepository orders;
    private final PaymentGateway payments;

    public PlaceOrderService(OrderRepository orders, PaymentGateway payments) {
        this.orders = orders;
        this.payments = payments;
    }

    @Override
    public Order place(PlaceOrderCommand command) {
        PaymentResult paid = payments.charge(command.total());
        return orders.save(Order.create(command, paid));
    }
}
```

```java
// adapter — Spring Web talks to the port only
@RestController
@RequestMapping("/orders")
public class OrderController {
    private final PlaceOrderUseCase placeOrder;

    public OrderController(PlaceOrderUseCase placeOrder) {
        this.placeOrder = placeOrder;
    }

    @PostMapping
    public OrderResponse post(@Valid @RequestBody PlaceOrderRequest body) {
        Order order = placeOrder.place(body.toCommand());
        return OrderResponse.from(order);
    }
}
```

```java
// adapter — persistence implements the driven port
@Repository
public class JpaOrderAdapter implements OrderRepository {
    private final SpringDataOrderRepo springData;

    public JpaOrderAdapter(SpringDataOrderRepo springData) {
        this.springData = springData;
    }

    @Override
    public Order save(Order order) {
        return springData.save(OrderEntity.fromDomain(order)).toDomain();
    }
    // ...
}
```

Boot’s job is wiring. A `@Configuration` class constructs `PlaceOrderService` with adapter beans, or you mark the core service with a thin stereotype if you accept a minimal Spring annotation in the application layer. The test payoff is immediate: unit-test `PlaceOrderService` with fakes for `OrderRepository` and `PaymentGateway` — no `@SpringBootTest` required for the core rule.

Hexagonal is not "rewrite everything into six packages named port and adapter." It is dependency inversion at the boundaries that hurt. Start with the payment gateway and the web API; leave trivial read-only admin screens layered if they are stable.

Misconception: hexagons forbid Spring. They forbid Spring in the core. Misconception: every interface needs an adapter hierarchy six types deep. One port, one implementation is enough until a second adapter exists.

Today we put the domain in the center, showed a use-case port driven by MVC and implemented repositories as adapters, and kept Spring at the edges. Clean architecture pushes the same dependency rule further with explicit rings and use-case interactors — a sharpening of what you just saw.

That sharpening is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 107 (*Hexagonal Architecture*).

Narration technique: framework-in-the-middle pain → ports/adapters → core use case without Spring Web → MVC + JPA adapters → wiring/tests → misconceptions → bridge to clean architecture.
