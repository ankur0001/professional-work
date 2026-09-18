# Episode 109 — DDD Basics

| Field | Value |
|---|---|
| Episode | 109 |
| Title | DDD Basics |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 109 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Clean rings keep Spring out of the center. They do not tell you what belongs in that center when the business is genuinely complicated. CRUD entity graphs run out of honesty: an `Order` with forty nullable columns and a 2,000-line service class is not a model — it is a database mirror with aspirations. Domain-Driven Design gives language for the hard part: bounded contexts, ubiquitous language, aggregates, and domain events.

Start with bounded context, not with repositories. In a retail platform, "Customer" in marketing is not "Customer" in billing. Forcing one shared `CustomerEntity` across teams creates coupling disguised as reuse. Prefer separate models per context, integrated through explicit interfaces or events. Spring apps map cleanly to one deployable per context — or at least one package tree with a firewall between contexts.

Ubiquitous language means the code uses the same words as the domain experts. If they say "authorize payment" and "capture payment," do not name methods `updateStatus`. Names in the core should sound like the business conversation.

Aggregates cluster entities that must change together under one consistency boundary. An `Order` aggregate might own `OrderLine` value objects and enforce "cannot capture more than authorized." External references go by id — `CustomerId`, `SkuId` — not by holding another aggregate’s graph.

```java
public class Order {
    private final OrderId id;
    private OrderStatus status;
    private final List<OrderLine> lines = new ArrayList<>();
    private Money authorized;

    public void authorize(Money amount) {
        if (status != OrderStatus.DRAFT) {
            throw new DomainException("Only draft orders authorize");
        }
        this.authorized = amount;
        this.status = OrderStatus.AUTHORIZED;
    }

    public void addLine(SkuId sku, int qty, Money unitPrice) {
        if (status != OrderStatus.DRAFT) {
            throw new DomainException("Cannot change lines after authorize");
        }
        lines.add(new OrderLine(sku, qty, unitPrice));
    }

    public Money total() {
        return lines.stream().map(OrderLine::lineTotal).reduce(Money.ZERO, Money::plus);
    }
}
```

Repositories load and save whole aggregates, not arbitrary rows for UI convenience. In Spring Data terms that often means a repository per aggregate root, with mapping to JPA entities inside an adapter — the hexagonal split from two episodes ago.

Domain events capture facts the rest of the system may care about: `OrderAuthorized`, `OrderShipped`. Publish them from the aggregate or the application service after a successful state change. Inside one process, Spring’s `ApplicationEventPublisher` is enough. Across services, you graduate to a broker — which is the next episode’s territory.

```java
@Service
public class AuthorizeOrderService {
    private final OrderRepository orders;
    private final ApplicationEventPublisher events;

    @Transactional
    public void authorize(OrderId id, Money amount) {
        Order order = orders.findById(id).orElseThrow();
        order.authorize(amount);
        orders.save(order);
        events.publishEvent(new OrderAuthorized(id, amount));
    }
}
```

DDD is not mandatory for every screen. A simple settings CRUD does not need aggregates and event storms. Use DDD where rules, invariants, and language complexity justify it — usually the revenue and fulfillment cores.

Misconception: DDD means a folder named `domain` with the same anemic entities as before. Behavior-rich aggregates are the tell. Misconception: one giant enterprise-wide domain model. Bounded contexts exist because that dream fails.

Today we named contexts, practiced an aggregate that protects invariants, and published a domain event after commit-worthy work. Once facts need to leave the process — other services reacting without a synchronous chain — architecture shifts from request/response only to events as first-class integration.

That shift is event-driven architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 109 (*DDD Basics*).

Narration technique: CRUD honesty failure → bounded context + language → aggregate code → repository/events → Spring publisher example → when not to use DDD → bridge to EDA.
