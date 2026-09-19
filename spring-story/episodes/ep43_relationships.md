# Episode 43 — Relationships

| Field | Value |
|---|---|
| Episode | 43 |
| Title | Relationships |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 43 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A ship’s manifest is a document with lines. In the database that is two tables. In Java you want a `Manifest` that owns a list of `CargoLine` — and when a clerk deletes a line from the list, you want the row gone without a separate delete call. That is relationship mapping with orphan removal.

JPA association annotations describe cardinality and ownership. `@OneToMany` / `@ManyToOne` cover the manifest↔line case. `@ManyToMany` and `@OneToOne` exist too; misuse them and join tables multiply. For harbor cargo, start with the classic parent-child:

```java
@Entity
@Table(name = "manifests")
public class Manifest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "manifest_number", nullable = false, unique = true)
    private String manifestNumber;

    @Column(name = "vessel_imo", nullable = false)
    private String vesselImo;

    @OneToMany(mappedBy = "manifest", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<CargoLine> lines = new ArrayList<>();

    protected Manifest() {}

    public void addLine(CargoLine line) {
        lines.add(line);
        line.setManifest(this);
    }

    public void removeLine(CargoLine line) {
        lines.remove(line);
        line.setManifest(null);
    }
}
```

```java
@Entity
@Table(name = "cargo_lines")
public class CargoLine {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String description;

    @Column(name = "weight_kg", nullable = false)
    private int weightKg;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "manifest_id")
    private Manifest manifest;

    protected CargoLine() {}

    void setManifest(Manifest manifest) {
        this.manifest = manifest;
    }
}
```

`mappedBy = "manifest"` says the child owns the foreign key column `manifest_id`. Cascade `ALL` means persisting a new manifest persists new lines. `orphanRemoval = true` means removing a line from the collection schedules a `DELETE` for that cargo row on flush — the relational mirror of "this line no longer belongs to the document."

Always maintain both sides in `addLine` / `removeLine`. If you only `lines.add(line)` and forget `line.setManifest(this)`, the foreign key may stay null depending on flush order and owning side rules. Prefer `FetchType.LAZY` on collections so loading one manifest for a header screen does not pull every line until you ask.

Bidirectional relationships are not free. Equals/hashCode on entities with generated ids is a footgun inside sets. Cascading `REMOVE` from manifest to lines is powerful — deleting a manifest deletes its lines; do that only when the business rule matches. `@ManyToMany` between vessels and ports often wants an explicit association entity (`PortCall`) instead of a bare join table, because the call has its own arrival time.

People mark every association `EAGER` "so I never see LazyInitializationException" and then wonder why a simple manifest list issues a forest of joins. Others forget orphan removal and leave cargo rows pointing at deleted manifests — or delete lines manually in three places. A third mistake is putting `@JoinColumn` on both sides of a bidirectional pair and confusing Hibernate about ownership.

Associations give you a graph. Querying that graph without dropping to table columns — "manifests for this vessel on this date" — is JPQL’s job.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 43 (*Relationships*).
