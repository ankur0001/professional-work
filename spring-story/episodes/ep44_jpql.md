# Episode 44 — JPQL

| Field | Value |
|---|---|
| Episode | 44 |
| Title | JPQL |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 44 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Derived repository method names run out of breath. "Find manifests for vessel IMO-9312345 with arrival date on 2026-09-18" is still readable as a method. Add three more predicates and the name becomes a novel. JPQL lets you query the entity model — property names, associations — without writing table-column SQL by hand.

JPQL looks like SQL but speaks entities. You write `select m from Manifest m`, not `select * from manifests`. Fields are Java properties. Associations are navigated with dots or joins. Hibernate translates to SQL for your dialect.

```java
public interface ManifestRepository extends JpaRepository<Manifest, Long> {

    @Query("""
            select m from Manifest m
            where m.vesselImo = :imo
              and m.arrivalDate = :day
            order by m.manifestNumber
            """)
    List<Manifest> findByVesselAndDay(
            @Param("imo") String imo,
            @Param("day") LocalDate day);

    @Query("""
            select m from Manifest m
            join m.lines line
            where m.vesselImo = :imo
              and line.weightKg >= :minWeight
            """)
    List<Manifest> findWithHeavyLines(
            @Param("imo") String imo,
            @Param("minWeight") int minWeight);
}
```

Parameter binding uses `:name` with `@Param`, or ordinal `?1` style. Prefer named parameters for harbor queries you will revisit at 3am. `join m.lines` navigates the association you mapped — you did not type `cargo_lines.manifest_id`.

Projection queries return what a screen needs without hydrating full graphs:

```java
public interface ManifestSummary {
    String getManifestNumber();
    String getVesselImo();
    LocalDate getArrivalDate();
}

@Query("""
        select m.manifestNumber as manifestNumber,
               m.vesselImo as vesselImo,
               m.arrivalDate as arrivalDate
        from Manifest m
        where m.vesselImo = :imo
        """)
List<ManifestSummary> summarizeForVessel(@Param("imo") String imo);
```

`@Modifying` on an update/delete JPQL query marks it as a write. Bulk JPQL updates bypass the persistence context’s dirty checking for already-managed instances — clear the context if you mixed styles.

Native SQL with `nativeQuery = true` is an escape hatch when you need a database-specific hint. Prefer JPQL while the query stays in entity terms; drop to native when the dialect feature is the point.

Read the vessel-and-day query against a real ops question: "show me everything for IMO-9312345 arriving today, ordered by manifest number." The JPQL states that in entity language. Hibernate emits the SQL with the real column names for your dialect. When you rename `arrivalDate` in Java, the query updates with the model — not with a buried `arrival_date` string in twelve native queries.

Writing table columns inside JPQL (`manifest_number`) is a common failure — JPQL wants `manifestNumber`. Selecting entities and then filtering in Java loops is how N+1 and memory problems start. And treating JPQL as "string SQL with different keywords" misses the point: refactor a property name and your JPQL should follow the model, not the physical schema.

JPQL is great when the query shape is known at compile time. When port-search filters appear and disappear at runtime — optional flag state, optional tonnage range, optional name fragment — string-concatenated JPQL gets unsafe and ugly. The Criteria API builds those predicates programmatically.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 44 (*JPQL*).
