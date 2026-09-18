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

Criteria gives you dynamic predicates. Specifications give those predicates names you can reuse: `CargoSpecs.isHazardous().and(CargoSpecs.inPort("SGSIN"))`. Harbor search stops being a private method full of `if` statements and becomes a library of composable rules.

Spring Data JPA’s `JpaSpecificationExecutor` adds `findAll(Specification)` to your repository. A `Specification` is a functional bridge to Criteria — implement `toPredicate`, or build with lambdas.

```java
public final class CargoSpecs {

    private CargoSpecs() {}

    public static Specification<CargoItem> isHazardous() {
        return (root, query, cb) -> cb.isTrue(root.get("hazardous"));
    }

    public static Specification<CargoItem> inPort(String portCode) {
        return (root, query, cb) -> cb.equal(root.get("currentPort"), portCode);
    }

    public static Specification<CargoItem> weightAtLeast(int minKg) {
        return (root, query, cb) -> cb.greaterThanOrEqualTo(root.get("weightKg"), minKg);
    }
}
```

```java
public interface CargoItemRepository
        extends JpaRepository<CargoItem, Long>, JpaSpecificationExecutor<CargoItem> {}
```

```java
Specification<CargoItem> spec = CargoSpecs.isHazardous()
        .and(CargoSpecs.inPort("SGSIN"))
        .and(CargoSpecs.weightAtLeast(500));

List<CargoItem> matches = cargoItems.findAll(spec, Sort.by("trackingCode"));
```

Composition is the win. `and` / `or` / `not` combine specs without knowing how each one builds its predicate. Unit tests can assert combinations against an in-memory database or a repository slice. Product owners request "hazardous cargo in Singapore over 500 kg" and you assemble existing specs instead of inventing a fourth `@Query`.

Read the call site again. Nothing there knows whether `isHazardous` checks a boolean column or a status enum. That opacity is deliberate: when customs rules tighten, you change one spec method and every composed query inherits the fix.

Nullable filters stay readable:

```java
public static Specification<CargoItem> optionalPort(String portCode) {
    return (root, query, cb) -> {
        if (portCode == null || portCode.isBlank()) {
            return cb.conjunction(); // no-op predicate
        }
        return cb.equal(root.get("currentPort"), portCode);
    };
}
```

Join-based specs need care with distinct results when collections multiply rows — same caution as JPQL joins. If a spec joins `lines` to filter on hazardous contents, wrap with `query.distinct(true)` or you will see duplicate parent `CargoItem` rows in the list. Pagination works: `findAll(spec, pageable)`. Count queries follow the spec too — which is why an expensive join in a spec hurts both the page query and the count.

Specifications are not a reason to abandon derived methods for `findByImoNumber`. Use the lightest tool that stays clear. Dumping all business rules into specs that reach across bounded contexts also hurts — keep specs about persistence predicates, not full harbor workflows. And a specification that silently ignores an invalid port code instead of failing fast will hide operator typos behind an empty result set.

You can now query cargo with composable rules. Read-heavy vessel directory screens still hammer the database with identical lookups. Caching those directory reads — and evicting on update — is the next performance lever inside the Spring Data stack.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 46 (*Specifications*).
