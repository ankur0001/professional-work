# Episode 106 — Layered Architecture

| Field | Value |
|---|---|
| Episode | 106 |
| Title | Layered Architecture |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 106 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You can be production-ready operationally and still drown in structural mud. Controllers open JDBC connections. Entities serialize straight to JSON with lazy-loading landmines. One "util" package imports everything. Phase 12 starts here because most Spring codebases already gesture at layers — and then violate them under deadline pressure.

Layered architecture organizes the app into horizontal bands with a one-way dependency rule: outer/upper layers may call inward/downward; domain and persistence must not reach up into web concerns. In a typical Spring Boot service the bands are web (controllers, DTOs), application/service (use cases, transactions), domain (model, rules), and persistence (repositories, JPA entities). Names vary; the direction does not.

Why bother? Without layers, every change fans out. Swap JSON field names and you break SQL. Write a unit test and you boot Tomcat. Circular package dependencies appear because nothing forbade them. Layers give a default map for where code goes when the team is moving fast.

Spring encourages this map with stereotypes and package layout:

```text
com.example.checkout
  web          → @RestController, request/response DTOs
  service      → @Service, @Transactional use cases
  domain       → Order, Money, domain services (often pure Java)
  persistence  → Spring Data repositories, @Entity types
```

```java
@RestController
@RequestMapping("/orders")
public class OrderController {
    private final OrderService orders;

    public OrderController(OrderService orders) {
        this.orders = orders;
    }

    @PostMapping
    public OrderResponse place(@Valid @RequestBody PlaceOrderRequest req) {
        Order placed = orders.place(req.toCommand());
        return OrderResponse.from(placed);
    }
}

@Service
public class OrderService {
    private final OrderRepository repo;
    private final PaymentGateway payments;

    @Transactional
    public Order place(PlaceOrderCommand cmd) {
        PaymentResult paid = payments.charge(cmd.total());
        return repo.save(Order.create(cmd, paid));
    }
}
```

Notice the translation at the boundary. The controller speaks HTTP DTOs. The service speaks domain types and commands. The repository speaks persistence. Mapping costs a few lines and saves you from exposing `@Entity` graphs as API contracts — a classic layered failure mode when a lazy collection serializes after the session closes.

Enforce the rule mechanically when you can. ArchUnit tests that `..web..` may depend on `..service..` but `..domain..` must not depend on `..web..` or `..persistence..` catch drift in CI. Package-by-layer is not the only option — package-by-feature also works — but each feature still needs an internal dependency direction.

```java
@ArchTest
static final ArchRule domain_does_not_depend_on_web =
        noClasses().that().resideInAPackage("..domain..")
                .should().dependOnClassesThat().resideInAPackage("..web..");
```

Transactions usually live on the service layer — `@Transactional` on use-case methods — so controllers stay free of persistence session concerns. Repositories return domain objects or entities that the service maps; controllers never inject `EntityManager` "just this once."

Limits appear as the domain grows. Layers do not by themselves stop framework types from leaking downward: a domain module that imports `Pageable` or `HttpServletRequest` is still coupled. Layers also tempt anemic models — entities as bags of getters and all rules in services. Those pressures push teams toward hexagonal and clean variations next.

Misconception: "we have `@RestController` and `@Service`, so we have architecture." Stereotypes without dependency direction are naming, not structure. Misconception: more layers always help. Four clear bands beat seven bands of pass-through methods that only forward calls.

Today we set the baseline map, showed DTO-at-boundary discipline, and admitted where layers leak. When the pain is "domain should not know Spring Web or JPA at all," you need ports, adapters, and an inside that stays pure.

That reshaping is hexagonal architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 106 (*Layered Architecture*).

Narration technique: ops-ready but structurally muddy → dependency direction → package map + controller/service code → ArchUnit → limits of layers → bridge to hexagonal.
