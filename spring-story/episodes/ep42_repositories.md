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

You understand entities, lifecycle, and the persistence context. You still do not want every berth planner use case to inject `EntityManager` and write the same find/save/delete again. Spring Data JPA repositories are the typed façade — interfaces that become working beans at startup.

Declare what you need for vessels. Spring Data supplies the implementation.

```java
public interface VesselRepository extends JpaRepository<Vessel, Long> {

    Optional<Vessel> findByImoNumber(String imoNumber);

    List<Vessel> findByFlagStateIgnoreCase(String flagState);

    boolean existsByImoNumber(String imoNumber);

    @Query("select v from Vessel v where v.grossTonnage >= :minTonnage")
    List<Vessel> findHeavyEnough(@Param("minTonnage") int minTonnage);
}
```

`JpaRepository` already gives you `save`, `saveAll`, `findById`, `findAll`, `deleteById`, pagination, and flush helpers. Derived query methods parse the method name: `findByImoNumber` becomes a query on the `imoNumber` property — which maps to column `imo_number`. You stay in the entity model — property names, not column names — until you drop to `@Query` or native SQL on purpose.

How does the proxy work? At startup, Spring Data scans for repository interfaces, creates fragments backed primarily by `SimpleJpaRepository`, and registers them as beans. Method calls bind parameters, create a query, and execute through the `EntityManager` tied to the current transaction. Exceptions translate into Spring's `DataAccessException` hierarchy so harbor services are not coupled to vendor SQLState codes.

Pagination belongs in the repository contract when vessel directories grow:

```java
Page<Vessel> page = vesselRepository.findByFlagStateIgnoreCase(
        "SG",
        PageRequest.of(0, 20, Sort.by("name")));
```

`Pageable` controls limit, offset, and sort. Returning `Page` also runs a count query so UIs can render total pages. Returning `Slice` skips the count when you only need "has next."

Custom implementations exist when derived names and `@Query` are not enough. Keep the interface clean and add a fragment class — useful for Criteria or bulk JDBC — without abandoning the repository style.

Sharp edges show up in SQL behavior, not bean wiring. Derived methods that return a single entity but match multiple rows throw `IncorrectResultSizeDataAccessException` — use `List` or tighten the predicate. Modifying queries need `@Modifying` and a transactional boundary, and they bypass dirty checking for entities already in the persistence context:

```java
public interface VesselRepository extends JpaRepository<Vessel, Long> {

    @Modifying(clearAutomatically = true)
    @Query("update Vessel v set v.name = :name where v.imoNumber = :imo")
    int renameByImo(@Param("imo") String imo, @Param("name") String name);
}
```

That bulk update returns the number of rows touched. It is repository work about vessel rows — not a generic service-wiring demo.

Repositories shine for CRUD and query intent. They do not replace domain thinking. A method named `save` will happily persist an invalid `Vessel` if you never enforced invariants. Put rules on the entity or in a domain service; keep the repository as persistence, not harbor policy.

Once your model grows beyond a single table, repositories alone are not enough. A manifest is not one row — it is a header plus cargo lines. Mapping those associations is the next craft.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 42 (*Repositories*).
