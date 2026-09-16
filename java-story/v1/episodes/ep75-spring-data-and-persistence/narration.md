# Episode 75 — Spring Data and Persistence

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Four covered Spring MVC and REST boundaries. Most services persist state — Spring Data makes repositories a first-class idea. JPA and Hibernate remain the common relational stack under Spring Data JPA.

Transactions define consistency boundaries — get them wrong and data lies. Performance interviews often land on lazy loading and N-plus-one queries. Today — repositories, entities, transactions, and persistence pitfalls.

Episode Seventy-Five. Spring Data and Persistence. Spring Data repositories declare persistence intent as interfaces. JpaRepository gives CRUD, paging, and sorting with almost no boilerplate.

Query methods derive SQL from method names — findByEmail, existsById. Query annotation or specs handle complex predicates deliberately. Keep repositories focused on persistence — not business workflows.

Custom fragments extend repositories when derived queries run out. Entities map tables to objects — carefully. Id and GeneratedValue define identity — equals should respect it thoughtfully.

Relationships — OneToMany, ManyToOne — model cardinality and ownership. FetchType lazy is the default for many associations — for good reason. DTOs or projections keep API models separate from persistence models.

Schema migrations belong in Flyway or Liquibase — not hope and hibernate-ddl. Transactional marks a consistency boundary. On a service facade — one use case, one transaction, by default.

Propagation and isolation settings change when nested calls join or suspend. Read-only transactions can help readers — still measure before assuming. Checked exceptions do not roll back by default — RuntimeException does.

Keep transactions short — no remote calls while holding DB locks. The N-plus-one problem — classic interview and production trap. One query loads parents — N more queries load each child collection.

Symptoms — fine in tests with two rows, painful with thousands. Fixes — join fetch, entity graphs, or dedicated query DTOs. Open Session in View can hide the issue until you disable it.

Log SQL in staging — count queries for critical endpoints. Practical persistence practices. Index for the queries you run — not for every column. Paginate at the database — not in memory after findAll.

Optimistic locking with Version prevents silent overwrites. Separate read models when query shapes diverge from write models. Measure with realistic data volumes — microbenchmarks lie.

Three common mistakes. One — calling findAll and filtering in Java — database should filter. Two — lazy loads in JSON serialization — accidental query storms. Three — huge transactional methods that call other services.

Also — exposing entities over REST — persistence leaks into clients. Persistence is a boundary — protect it with clear services and DTOs. Interview question — how do you avoid N-plus-one with Spring Data JPA?

Detect it — enable SQL logging and watch query counts under load. Fetch joins or entity graphs load required associations deliberately. DTO projections query exactly the columns the use case needs.

Avoid Open Session in View masking lazy loads during rendering. Fix the query shape — do not just raise the connection pool size. Data is safe — next we lock the doors. Episode Seventy-Six — Spring Security.

Authentication, authorization, filters, and securing REST APIs. See you there.
