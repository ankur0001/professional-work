# Episode 46 — Specifications

| Field | Value |
|---|---|
| Episode | 46 |
| Title | Specifications |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 46 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Criteria gave us type-safe dynamic queries. The next annoyance is copying the same predicate into three repositories. "Email domain is corporate," "order is open," "product is in stock" — these are domain filters that deserve names. Spring Data Specifications package a Criteria predicate as a reusable object and let you compose them with `and` / `or`.

Extend the repository with `JpaSpecificationExecutor`:

```java
public interface OrderRepository
        extends JpaRepository<Order, Long>, JpaSpecificationExecutor<Order> {
}
```

That single addition unlocks `findAll(Specification)`, `findAll(Specification, Pageable)`, `count(Specification)`, and friends. Now define named specs for the order model:

```java
public final class OrderSpecs {

    private OrderSpecs() {}

    public static Specification<Order> hasCustomerEmail(String email) {
        return (root, query, cb) ->
                cb.equal(root.get("customerEmail"), email);
    }

    public static Specification<Order> hasStatus(OrderStatus status) {
        return (root, query, cb) ->
                cb.equal(root.get("status"), status);
    }

    public static Specification<Order> placedAfter(Instant instant) {
        return (root, query, cb) ->
                cb.greaterThanOrEqualTo(root.get("placedAt"), instant);
    }

    public static Specification<Order> containsSku(String sku) {
        return (root, query, cb) -> {
            Join<Order, OrderLine> lines = root.join("lines", JoinType.INNER);
            query.distinct(true);
            return cb.equal(lines.get("sku"), sku);
        };
    }
}
```

Each method returns a `Specification` — a functional interface whose `toPredicate` receives the same root, query, and criteria builder you met in raw Criteria. The difference is packaging: callers compose without seeing the builder.

```java
@Transactional(readOnly = true)
public Page<Order> search(OrderSearchCriteria criteria, Pageable pageable) {
    Specification<Order> spec = Specification.unrestricted();

    if (criteria.email() != null) {
        spec = spec.and(OrderSpecs.hasCustomerEmail(criteria.email()));
    }
    if (criteria.status() != null) {
        spec = spec.and(OrderSpecs.hasStatus(criteria.status()));
    }
    if (criteria.placedAfter() != null) {
        spec = spec.and(OrderSpecs.placedAfter(criteria.placedAfter()));
    }
    if (criteria.sku() != null) {
        spec = spec.and(OrderSpecs.containsSku(criteria.sku()));
    }

    return orderRepository.findAll(spec, pageable);
}
```

Composition is the win. Unit tests can assert that `hasStatus(NEW).and(containsSku("SKU-1"))` restricts correctly by running against an in-memory database or by testing the repository slice. Product owners can request "open orders for this customer with this SKU" and you assemble existing specs instead of inventing a fourth `@Query`.

Join-aware specs need care. If two specs each `join("lines")`, you can get double joins and duplicated predicates. Centralize join-heavy specs, or use aliases consistently. Distinct belongs with collection joins. Pagination plus collection fetch remains tricky — Specifications that `fetch` collections with `Pageable` can break count queries; prefer fetch in a dedicated find-by-id style query, not in paged list specs.

Specifications are still Criteria underneath. They inherit metamodel benefits and the same SQL generation. They do not replace JPQL for fixed, readable queries. Use `@Query` when the shape is stable and specs when filters combine at runtime.

When the same `findById` or expensive report query runs constantly, even a perfect Specification still hits the database every time. Read-heavy paths start asking about caching — first-level we already have, and second-level or query caches beyond it.

Episode Forty-Seven — Caching.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 46 (*Specifications*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
