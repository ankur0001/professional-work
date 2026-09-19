# Episode 51 — N+1 Problem

| Field | Value |
|---|---|
| Episode | 51 |
| Title | N+1 Problem |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 51 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Ops opens today’s manifest list for vessel `IMO-9312345`. Twenty manifests. The SQL log shows one `SELECT` for manifests — fine — then twenty more as the JSON serializer walks each manifest’s cargo lines. That pattern is the N+1 problem: **1** query for the parents plus **N** queries for children, one per parent.

It shows up wherever lazy associations meet loops.

```java
@Entity
@Table(name = "manifests")
public class Manifest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "manifest_number", nullable = false)
    private String manifestNumber;

    @Column(name = "vessel_imo", nullable = false)
    private String vesselImo;

    @OneToMany(mappedBy = "manifest", fetch = FetchType.LAZY)
    private List<CargoLine> lines = new ArrayList<>();

    public List<CargoLine> getLines() {
        return lines;
    }
}
```

```java
@Transactional(readOnly = true)
public List<ManifestResponse> listForVessel(String vesselImo) {
    List<Manifest> manifests = manifestRepository.findByVesselImo(vesselImo);
    // SQL #1:
    // select * from manifests where vessel_imo = ?

    List<ManifestResponse> responses = new ArrayList<>();
    for (Manifest manifest : manifests) {
        // each getLines() may fire another SELECT:
        // select * from cargo_lines where manifest_id = ?
        // → with 20 manifests, that is SQL #2 through #21 (1 + N)
        responses.add(ManifestResponse.from(manifest, manifest.getLines()));
    }
    return responses;
}
```

Count it out loud. Twenty manifests → twenty child selects → twenty-one statements total. Scale to two hundred manifests on a busy day and the board melts. Lazy is not the villain. Lazy keeps writes and incidental loads cheap. The villain is navigating lazy associations across a collection without a fetch plan. Open-session-in-view can make this "work" without `LazyInitializationException` while still issuing N+1 SQL — silent latency.

Fix it by loading what you need in fewer queries. Join fetch is the clearest teaching fix:

```java
public interface ManifestRepository extends JpaRepository<Manifest, Long> {

    @Query("""
            select distinct m from Manifest m
            left join fetch m.lines
            where m.vesselImo = :vesselImo
            """)
    List<Manifest> findWithLinesByVesselImo(@Param("vesselImo") String vesselImo);
}
```

```java
@Transactional(readOnly = true)
public List<ManifestResponse> listForVessel(String vesselImo) {
    List<Manifest> manifests = manifestRepository.findWithLinesByVesselImo(vesselImo);
    // typically 1 select with a join (watch the log — count should collapse toward 1)
    return manifests.stream()
            .map(m -> ManifestResponse.from(m, m.getLines()))
            .toList();
}
```

`join fetch` tells Hibernate to initialize `lines` while loading `Manifest`. `distinct` softens duplicate parent rows joins can produce in the result list. For pagination, join fetch of collections is awkward — the database page of joined rows is not a page of parent entities. Prefer fetch joins for non-paged detail lists, or page parent ids first, then fetch aggregates by those ids.

`@BatchSize` on the collection reduces N+1 into fewer batched `IN` queries when you cannot join-fetch every path. Entity graphs offer another explicit plan: `@EntityGraph(attributePaths = {"lines"})` on a repository method. A DTO query that selects exactly the columns the screen needs avoids hydrating the graph entirely.

Diagnosis before dogma. Enable SQL logging. Reproduce the manifest list. Count statements. If you see the repeating `cargo_lines` select inside the loop, you found N+1. Fix with fetch join, entity graph, batch size, or a projection — not by marking every association `FetchType.EAGER`, which often moves the pain to writes and to every accidental load.

Notice what these read fixes still assume: an open persistence context spanning the whole operation. Writes raise a sharper problem. Decrement yard stock, write a berth reservation, and append a ledger row — three inserts/updates that must succeed or fail together. If the reservation saves and the ledger write throws, you cannot leave the harbor half-updated. Something has to bound that multi-write unit of work atomically.

That boundary is `@Transactional` — and it is where persistence context lifetime, commit, and rollback become deliberate instead of accidental.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 51 (*N+1 Problem*).
