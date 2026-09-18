# Episode 108 — Clean Architecture

| Field | Value |
|---|---|
| Episode | 108 |
| Title | Clean Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 108 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Hexagonal gave you a center and adapters. Clean Architecture — Robert C. Martin’s rings — says the same dependency rule with a stricter vocabulary: source code dependencies point inward. Enterprise business rules sit at the center. Frameworks, UI, and databases are outer details. An inner circle never knows the name of a type declared in an outer circle.

Map the rings onto a Spring codebase without drowning in ceremony.

1. **Entities** — enterprise rules: `Order`, `Money`, invariants. Pure Java.
2. **Use cases** — application rules: `PlaceOrderInteractor`, input/output models. Pure Java, depends only on entities and outbound ports.
3. **Interface adapters** — controllers, presenters, gateways that convert between use-case models and outer formats.
4. **Frameworks & drivers** — Spring MVC, JPA, the actual Postgres driver, the servlet container.

The practical difference from a loose hexagon is often the request/response models. Use cases do not accept HTTP DTOs or return JPA entities. They accept input data objects and return output data objects. Adapters map both ways.

```java
public record PlaceOrderInput(String customerId, List<LineInput> lines) {}
public record PlaceOrderOutput(String orderId, String status) {}

public class PlaceOrderInteractor {
    private final OrderRepository orders;
    private final PaymentGateway payments;

    public PlaceOrderOutput execute(PlaceOrderInput input) {
        Order order = Order.create(input);
        payments.charge(order.total());
        Order saved = orders.save(order);
        return new PlaceOrderOutput(saved.id().value(), saved.status().name());
    }
}
```

```java
@RestController
public class PlaceOrderController {
    private final PlaceOrderInteractor interactor;

    @PostMapping("/orders")
    public ResponseEntity<OrderHttpResponse> place(@RequestBody OrderHttpRequest http) {
        PlaceOrderOutput out = interactor.execute(http.toInput());
        return ResponseEntity.accepted().body(OrderHttpResponse.from(out));
    }
}
```

Transaction boundaries usually sit in an adapter or a thin application wrapper annotated with `@Transactional`, not inside the entity. The interactor stays free of Spring stereotypes if you construct it in configuration. That purity is the point: you can move the use case to another runtime without dragging MVC annotations with it.

Clean Architecture overlaps heavily with hexagonal. Teams argue about diagrams more than about dependency direction. Use clean rings when you need a shared language for "who may import whom" across a large codebase; use hexagonal language when ports/adapters communicate better to your team. Do not implement both as duplicate folder trees for the same service.

Where Spring fights you: Spring Data repository interfaces and `@Entity` classes want to be the model. Resist by keeping domain entities separate from JPA entities when the model is non-trivial, or accept a pragmatic compromise on simple CRUD screens and reserve strict rings for the core revenue path. Dogma that doubles every type for a three-field admin form is not clean — it is ceremony.

Testing is where the rings pay rent. An interactor test constructs the class with fakes and asserts output records — no `@SpringBootTest`. Adapter tests use `@WebMvcTest` or Data JPA slices against the outer ring only. If every test boots the full context to prove a total calculation, the dependency rule is only a slide.

Misconception: clean architecture means no Spring Boot. Boot is an excellent outer ring. Misconception: more interfaces equal more cleanliness. Interfaces at real boundaries beat interfaces between every package. Misconception: entities must be immutable records always. Immutability helps; invariants enforced by methods matter more than the record keyword.

Today we enforced the inward dependency rule, separated use-case IO from HTTP, and placed Spring in the outer ring. Boundaries protect structure — but they do not invent a language for complex business rules. When "Order" means different things to billing and warehouse teams, you need domain modeling vocabulary.

That vocabulary is DDD basics.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 108 (*Clean Architecture*).

Narration technique: rings + dependency rule → Spring mapping → interactor + HTTP adapter → transactional placement → hex overlap → pragmatism → bridge to DDD.
