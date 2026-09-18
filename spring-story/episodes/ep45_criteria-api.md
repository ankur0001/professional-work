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

A port-search screen starts with three optional filters: flag state, minimum gross tonnage, and a name fragment. On Monday the planner uses only the name box. On Tuesday all three. If you concatenate JPQL strings for each combination, you either miss a combination or invite injection-shaped bugs. The Criteria API builds the same query tree in Java, predicate by predicate, at runtime.

Criteria is verbose on purpose. You get a typesafe-ish query graph from the `EntityManager` (or from a custom repository fragment). Bootstrapped metamodels can make paths fully typesafe; even without them, structured predicates beat string soup.

```java
public List<Vessel> search(PortVesselFilter filter) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Vessel> query = cb.createQuery(Vessel.class);
    Root<Vessel> vessel = query.from(Vessel.class);

    List<Predicate> predicates = new ArrayList<>();

    if (filter.flagState() != null && !filter.flagState().isBlank()) {
        predicates.add(cb.equal(
                cb.lower(vessel.get("flagState")),
                filter.flagState().toLowerCase(Locale.ROOT)));
    }
    if (filter.minGrossTonnage() != null) {
        predicates.add(cb.greaterThanOrEqualTo(
                vessel.get("grossTonnage"),
                filter.minGrossTonnage()));
    }
    if (filter.nameContains() != null && !filter.nameContains().isBlank()) {
        predicates.add(cb.like(
                cb.lower(vessel.get("name")),
                "%" + filter.nameContains().toLowerCase(Locale.ROOT) + "%"));
    }

    query.where(predicates.toArray(Predicate[]::new));
    query.orderBy(cb.asc(vessel.get("name")));

    return entityManager.createQuery(query).getResultList();
}
```

Each optional filter adds a `Predicate` only when present. An empty predicate list means "all vessels" — decide whether that is allowed for your screen. `CriteriaBuilder` supplies `equal`, `like`, `greaterThanOrEqualTo`, conjunctions, and disjunctions. Joins exist when you need cargo or berth associations in the filter.

Wire this behind a custom repository fragment so controllers never see `EntityManager`:

```java
public interface VesselRepository
        extends JpaRepository<Vessel, Long>, VesselRepositoryCustom {}

public interface VesselRepositoryCustom {
    List<Vessel> search(PortVesselFilter filter);
}
```

Walk one Monday query. Only `nameContains = "pacific"` is set. The predicate list holds a single `like` on lowercased `name`. Hibernate emits one SELECT with one WHERE clause. On Tuesday, flag state and tonnage join in — same Java method, wider WHERE, still no string concatenation of JPQL fragments.

Criteria shines for dynamic port search. It is heavy for a static `findByImoNumber` — use a derived method or JPQL there. Generating the JPA static metamodel (`Vessel_.flagState`) removes magic strings in `get("flagState")` and catches renames at compile time; invest in that when Criteria becomes common in the codebase.

People rebuild Criteria for every fixed query and drown in boilerplate. Others paste user input into `cb.literal(...)` paths incorrectly — still bind and compare through the API rather than inventing SQL fragments. A third trap is creating a new `EntityManager` manually in a Spring app instead of injecting one and participating in the transactional persistence context.

Dynamic filters work. When the same building blocks recur — "is hazardous," "in port SGSIN" — you want composable, named pieces you can `and` together in tests and in services. Spring Data Specifications are that vocabulary on top of Criteria.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 45 (*Criteria API*).
