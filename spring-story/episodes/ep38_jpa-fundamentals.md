# Episode 38 — JPA Fundamentals

| Field | Value |
|---|---|
| Episode | 38 |
| Title | JPA Fundamentals |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 38 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Harbor ops can expose a REST board forever and still not have a product. Sooner or later someone asks you to store a vessel, reload it tomorrow by IMO number, and update its berth flag without corrupting the row. That is when Java objects meet relational tables — and the mismatch becomes the real work.

Picture a vessel registry written with raw JDBC. You open a connection, write `INSERT INTO vessels (imo_number, name, flag_state) VALUES (?, ?, ?)`, then walk a `ResultSet` column by column into a `Vessel` object. Tomorrow you add `gross_tonnage`. Every mapper breaks. You concatenate SQL for filters and hope nobody injects a quote. You copy the same `findById` / `save` / `delete` boilerplate for berths, manifests, and cargo lines. Transactions live in try/finally blocks scattered through services. There is no shared identity for "the same vessel row I already loaded." There is no unit of work — only statements you remember to run.

That tax is not a Java syntax problem. It is an object-relational problem. Objects have graphs, identity, and lifecycle. Tables have rows, keys, and joins. Something has to translate.

JPA — the Jakarta Persistence API — is that standard translation layer. You map a class to a table with annotations. An `EntityManager` (or a Spring Data repository sitting on top of one) loads and saves those entities. Hibernate is the most common JPA provider in Spring apps: it implements the specification and generates the SQL. Spring Data JPA then removes the DAO boilerplate so you declare an interface and get a working repository at runtime.

Keep the names stacked. JPA is the API and mapping rules. Hibernate is the engine that talks to the database. Spring Data JPA is the Spring abstraction that generates repository implementations and plugs into Spring transactions. Boot wires the datasource, `EntityManagerFactory`, and transaction manager when `spring-boot-starter-data-jpa` is on the classpath.

Make the before-and-after concrete with a `Vessel` entity — not a service that only wires beans:

```java
@Entity
@Table(name = "vessels")
public class Vessel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "imo_number", nullable = false, unique = true, length = 10)
    private String imoNumber;

    @Column(nullable = false, length = 120)
    private String name;

    @Column(name = "flag_state", nullable = false, length = 2)
    private String flagState;

    @Column(name = "gross_tonnage")
    private Integer grossTonnage;

    protected Vessel() {
        // JPA requires a no-arg constructor
    }

    public Vessel(String imoNumber, String name, String flagState) {
        this.imoNumber = imoNumber;
        this.name = name;
        this.flagState = flagState;
    }

    // getters...
}
```

`@Entity` marks a persistence type. `@Table` names the table when it differs from the class. `@Id` declares the primary key; `@GeneratedValue` lets the database assign it. Columns become fields. The protected no-arg constructor is for the provider — your domain still constructs with a real constructor. When Hibernate loads a row, it materializes a `Vessel` instance. When you change `name` inside a transaction and flush, Hibernate issues `UPDATE`. You did not write the SQL string.

Spring Data JPA then shrinks the repository side:

```java
public interface VesselRepository extends JpaRepository<Vessel, Long> {
    Optional<Vessel> findByImoNumber(String imoNumber);
}
```

`save`, `findById`, and derived finders appear without a hand-written DAO. Underneath, SQL still runs. JPA does not erase the database; it mediates it.

JPA is not "annotations instead of SQL forever." You still need to understand joins, indexes, and transactional boundaries. Annotating a random DTO with `@Entity` because you want Jackson to serialize it is another wrong turn — entities are persistence types with identity and lifecycle, not wire formats. And skipping the no-arg constructor until runtime blows up is a rite of passage you can skip by reading the mapping rules once.

You can map a vessel and save it. What Hibernate does between "field changed" and "UPDATE left the process" — dirty checking, snapshots, flush — is the next layer of honesty.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 38 (*JPA Fundamentals*).
