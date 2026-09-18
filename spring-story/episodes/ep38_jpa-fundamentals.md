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

You can ship a REST controller that returns JSON forever and still not have a product. Sooner or later someone asks you to store an order, reload it tomorrow, and update its status without corrupting the row. That is when Java objects meet relational tables — and the mismatch becomes the real work.

Picture a checkout service written with raw JDBC. You open a connection, write `INSERT INTO orders (...)`, then walk a `ResultSet` column by column into an `Order` object. Tomorrow you add a column. Every mapper breaks. You concatenate SQL for filters and hope nobody injects a quote. You copy the same `findById` / `save` / `delete` boilerplate for customers, products, and invoices. Transactions live in try/finally blocks scattered through the service. There is no shared identity for "the same order row I already loaded." There is no lazy association. There is no unit of work — only statements you remember to run.

That tax is not a Java syntax problem. It is an object-relational problem. Objects have graphs, identity, and lifecycle. Tables have rows, keys, and joins. Something has to translate.

JPA — the Jakarta Persistence API, still widely called Java Persistence API — is that standard translation layer. You map a class to a table with annotations. An `EntityManager` (or Spring Data repository sitting on top of one) loads and saves those entities. Hibernate is the most common JPA provider in Spring apps: it implements the specification and generates the SQL. Spring Data JPA then removes the DAO boilerplate so you declare an interface and get a working repository at runtime.

Hold the layers clear, because interviews mash the names together. JPA is the API and mapping rules. Hibernate is the engine that talks to the database. Spring Data JPA is the Spring abstraction that generates repository implementations and plugs into Spring transactions. Boot wires the datasource, `EntityManagerFactory`, and transaction manager when `spring-boot-starter-data-jpa` is on the classpath. You can use Hibernate without Spring. In this series we stay in the Spring Boot path, because that is how most teams ship.

Make the before-and-after concrete with a catalog entity — not a service that only wires beans.

```java
@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 120)
    private String sku;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private BigDecimal price;

    protected Product() {
        // JPA requires a no-arg constructor
    }

    public Product(String sku, String name, BigDecimal price) {
        this.sku = sku;
        this.name = name;
        this.price = price;
    }

    // getters...
}
```

Read that mapping slowly. `@Entity` marks a persistence type. `@Table` names the table when it differs from the class. `@Id` declares the primary key; `@GeneratedValue` lets the database assign it. Columns become fields. The protected no-arg constructor is for the provider — your domain still constructs with a real factory or public constructor. When Hibernate loads a row, it materializes a `Product` instance. When you change `price` inside a transaction and flush, Hibernate issues `UPDATE`. You did not write the SQL string.

Spring Data JPA then shrinks the repository side:

```java
public interface ProductRepository extends JpaRepository<Product, Long> {
    Optional<Product> findBySku(String sku);
}
```

No `ProductDaoImpl`. At startup, Spring Data creates a proxy backed by `SimpleJpaRepository`. `save`, `findById`, `findAll`, and `delete` are already there. Method names like `findBySku` become queries derived from the property path. Under the hood the repository still uses an `EntityManager` bound to the current transaction.

Boot's auto-configuration is the quiet hero here. With a JDBC driver and the JPA starter present, Boot builds a `DataSource`, a Hibernate `EntityManagerFactory`, and a `JpaTransactionManager`. Entity scanning picks up `@Entity` classes. You override when your schema or dialect is special. You do not hand-assemble the factory for the common case.

One failure mode to name early: treating JPA as "annotations until the red squiggles vanish." If you only memorize `@Entity` and `JpaRepository`, you do not own persistence yet. The idea is a mapped domain model with identity and a unit of work that translates field changes into SQL. Another failure mode is writing entities that are anemic copies of every table column with no thought for keys, nullability, or invariants — then wondering why the database fills with garbage.

So we answered why JPA shows up after MVC: objects and tables need a disciplined bridge. We separated JPA, Hibernate, and Spring Data JPA. We mapped a `Product` and declared a repository without a hand-written DAO.

But annotations alone do not explain what happens when you call `save`. Who builds the SQL? Who tracks which fields changed? Who decides when an `INSERT` becomes an `UPDATE`?

That pressure takes us into Hibernate's internals — Episode Thirty-Nine.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 38 (*JPA Fundamentals*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
