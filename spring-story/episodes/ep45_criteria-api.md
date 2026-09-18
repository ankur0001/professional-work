# Episode 45 — Criteria API

| Field | Value |
|---|---|
| Episode | 45 |
| Title | Criteria API |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 45 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

JPQL is excellent when the query shape is fixed. Real admin screens are not fixed. A product search might filter by name, by price range, by category, by "only in stock" — any subset of those, depending on what the user typed. Building that with string-concatenated JPQL is fragile. The Criteria API builds the same query with Java objects: types, predicates, and compilers that fail before the database does.

Criteria code is verbose. That verbosity is the point — every join and predicate is explicit.

```java
@Repository
public class ProductSearchRepository {

    private final EntityManager entityManager;

    public ProductSearchRepository(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    public List<Product> search(ProductFilter filter) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Product> query = cb.createQuery(Product.class);
        Root<Product> product = query.from(Product.class);

        List<Predicate> predicates = new ArrayList<>();

        if (filter.nameContains() != null && !filter.nameContains().isBlank()) {
            predicates.add(cb.like(
                    cb.lower(product.get("name")),
                    "%" + filter.nameContains().toLowerCase() + "%"));
        }
        if (filter.minPrice() != null) {
            predicates.add(cb.greaterThanOrEqualTo(product.get("price"), filter.minPrice()));
        }
        if (filter.maxPrice() != null) {
            predicates.add(cb.lessThanOrEqualTo(product.get("price"), filter.maxPrice()));
        }
        if (Boolean.TRUE.equals(filter.inStockOnly())) {
            predicates.add(cb.greaterThan(product.get("stockQuantity"), 0));
        }

        query.select(product)
                .where(predicates.toArray(Predicate[]::new))
                .orderBy(cb.asc(product.get("name")));

        return entityManager.createQuery(query).getResultList();
    }
}

public record ProductFilter(
        String nameContains,
        BigDecimal minPrice,
        BigDecimal maxPrice,
        Boolean inStockOnly) {}
```

Follow the pieces. `CriteriaBuilder` factories predicates and expressions. `CriteriaQuery` is the query definition. `Root` is the from clause — here `Product`. Each optional filter adds a `Predicate` only when present. Empty predicate list means "all products," which is a conscious product decision, not an accident of a broken WHERE clause.

String attribute names like `product.get("price")` still fail at runtime if you typo. Metamodel classes generate `Product_.price` static fields for compile-time safety:

```java
predicates.add(cb.greaterThanOrEqualTo(product.get(Product_.price), filter.minPrice()));
```

Enable JPA metamodel generation in your build when Criteria becomes a regular tool. The first time a refactor renames `price` and the metamodel breaks the compile, you will not miss string paths.

Joins work the same object way:

```java
CriteriaQuery<Order> query = cb.createQuery(Order.class);
Root<Order> order = query.from(Order.class);
Join<Order, OrderLine> line = order.join("lines", JoinType.INNER);
predicates.add(cb.equal(line.get("sku"), sku));
query.select(order).distinct(true).where(...);
```

You can `fetch` with Criteria too (`order.fetch("lines", JoinType.LEFT)`) when the use case needs initialized collections. Same rule as JPQL: fetch when you will touch children, not by default on every search.

Criteria also powers dynamic updates and bulk deletes, though teams usually keep those as JPQL for readability. Where Criteria dominates is search forms, report filters, and multi-tenant predicates composed from several optional clauses.

The downside is ceremony. For a one-line `findByEmail`, a derived query wins. For a fixed three-way join everyone knows by heart, JPQL in `@Query` wins. Reach for Criteria when the predicate set is data-dependent. If you write Criteria for every repository method "for consistency," you trade clarity for uniformity.

Even Criteria repositories tend to accumulate duplicated predicate blocks — "active customer," "in stock," "placed after." Spring Data Specifications wrap Criteria predicates into composable, reusable pieces that plug into `JpaSpecificationExecutor`.

That composition is Episode Forty-Six.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 45 (*Criteria API*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
