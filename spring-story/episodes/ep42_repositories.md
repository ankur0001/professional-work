# Episode 42 — Repositories

| Field | Value |
|---|---|
| Episode | 42 |
| Title | Repositories |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 42 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You understand entities, lifecycle, and the persistence context. You still do not want every use case to inject `EntityManager` and write the same find/save/delete again. Spring Data JPA repositories are the typed façade over that context — interfaces that become working beans at startup.

Declare what you need. Spring Data supplies the implementation.

```java
public interface CustomerRepository extends JpaRepository<Customer, Long> {

    Optional<Customer> findByEmail(String email);

    List<Customer> findByDisplayNameContainingIgnoreCase(String fragment);

    boolean existsByEmail(String email);

    @Query("select c from Customer c where c.email like concat(:domain, '%')")
    List<Customer> findByEmailDomain(@Param("domain") String domain);
}
```

`JpaRepository` already gives you `save`, `saveAll`, `findById`, `findAll`, `deleteById`, pagination, and flush helpers. Derived query methods parse the method name: `findByEmail` becomes a query on the `email` property. `ContainingIgnoreCase` adds wildcards and case-insensitive comparison. You stay in the entity model — property names, not column names — until you drop to `@Query` or native SQL on purpose.

How does the proxy work? At startup, Spring Data scans for repository interfaces, creates fragments backed primarily by `SimpleJpaRepository`, and registers them as beans. Method calls bind parameters, create a query, and execute through the `EntityManager` tied to the current transaction. Exceptions translate into Spring's `DataAccessException` hierarchy so services are not coupled to vendor SQLState codes.

Pagination belongs in the repository contract when lists can grow:

```java
public interface ProductRepository extends JpaRepository<Product, Long> {
    Page<Product> findByNameContaining(String name, Pageable pageable);
}

// caller
Page<Product> page = productRepository.findByNameContaining(
        "mug",
        PageRequest.of(0, 20, Sort.by("name")));
```

`Pageable` controls limit, offset, and sort. Returning `Page` also runs a count query so UIs can render total pages. Returning `Slice` skips the count when you only need "has next." Choosing wrong here is a performance footgun on large catalogs.

Custom implementations exist when derived names and `@Query` are not enough. You keep the interface clean and add a fragment class — useful for Criteria or bulk JDBC — without abandoning the repository style. Prefer that over a parallel DAO hierarchy that bypasses Spring Data entirely.

A few sharp edges. Derived methods that return an entity but match multiple rows throw `IncorrectResultSizeDataAccessException` — use `List` or tighten the predicate. `deleteByEmail` derived deletes may load entities one by one unless you annotate a bulk `@Modifying` query. Modifying queries need `@Modifying` and usually `@Transactional`, and they bypass dirty checking for entities already in the persistence context — clear the context if you mixed both styles.

```java
public interface InventoryRepository extends JpaRepository<InventoryItem, Long> {

    @Modifying(clearAutomatically = true)
    @Query("update InventoryItem i set i.quantity = i.quantity - :qty where i.sku = :sku and i.quantity >= :qty")
    int reserveStock(@Param("sku") String sku, @Param("qty") int qty);
}
```

That bulk update returns the number of rows touched. It is repository work about tables and quantities — not a generic service wiring demo.

Repositories shine for CRUD and query intent. They do not replace domain thinking. A method named `save` will happily persist an invalid `Customer` if you never enforced invariants. Put rules on the entity or in a domain service; keep the repository as persistence, not business policy.

Once your model grows beyond a single table, repositories alone are not enough. An order is not one row — it is a header plus lines, maybe a customer reference, maybe a shipping address. Mapping those associations is the next craft.

Episode Forty-Three — Relationships.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 42 (*Repositories*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
