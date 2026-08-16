# Episode 75 — Spring Data and Persistence

| Field | Value |
|---|---|
| Episode | 75 |
| Title | Spring Data and Persistence |
| Catalog handbook column | 75 |
| Narration source script | `make_episode_75.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Four covered Spring MVC and REST boundaries.
2. Most services persist state — Spring Data makes repositories a first-class idea.
3. JPA and Hibernate remain the common relational stack under Spring Data JPA.
4. Transactions define consistency boundaries — get them wrong and data lies.
5. Performance interviews often land on lazy loading and N-plus-one queries.
6. Today — repositories, entities, transactions, and persistence pitfalls.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Five.
2. Spring Data and Persistence.

### Scene `repositories` (renderer: `repositories`)

1. Spring Data repositories declare persistence intent as interfaces.
2. JpaRepository gives CRUD, paging, and sorting with almost no boilerplate.
3. Query methods derive SQL from method names — findByEmail, existsById.
4. Query annotation or specs handle complex predicates deliberately.
5. Keep repositories focused on persistence — not business workflows.
6. Custom fragments extend repositories when derived queries run out.

### Scene `entities` (renderer: `entities`)

1. Entities map tables to objects — carefully.
2. Id and GeneratedValue define identity — equals should respect it thoughtfully.
3. Relationships — OneToMany, ManyToOne — model cardinality and ownership.
4. FetchType lazy is the default for many associations — for good reason.
5. DTOs or projections keep API models separate from persistence models.
6. Schema migrations belong in Flyway or Liquibase — not hope and hibernate-ddl.

### Scene `transactions` (renderer: `transactions`)

1. Transactional marks a consistency boundary.
2. On a service facade — one use case, one transaction, by default.
3. Propagation and isolation settings change when nested calls join or suspend.
4. Read-only transactions can help readers — still measure before assuming.
5. Checked exceptions do not roll back by default — RuntimeException does.
6. Keep transactions short — no remote calls while holding DB locks.

### Scene `nplusone` (renderer: `nplusone`)

1. The N-plus-one problem — classic interview and production trap.
2. One query loads parents — N more queries load each child collection.
3. Symptoms — fine in tests with two rows, painful with thousands.
4. Fixes — join fetch, entity graphs, or dedicated query DTOs.
5. Open Session in View can hide the issue until you disable it.
6. Log SQL in staging — count queries for critical endpoints.

### Scene `practices` (renderer: `practices`)

1. Practical persistence practices.
2. Index for the queries you run — not for every column.
3. Paginate at the database — not in memory after findAll.
4. Optimistic locking with Version prevents silent overwrites.
5. Separate read models when query shapes diverge from write models.
6. Measure with realistic data volumes — microbenchmarks lie.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — calling findAll and filtering in Java — database should filter.
3. Two — lazy loads in JSON serialization — accidental query storms.
4. Three — huge transactional methods that call other services.
5. Also — exposing entities over REST — persistence leaks into clients.
6. Persistence is a boundary — protect it with clear services and DTOs.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you avoid N-plus-one with Spring Data JPA?
2. Detect it — enable SQL logging and watch query counts under load.
3. Fetch joins or entity graphs load required associations deliberately.
4. DTO projections query exactly the columns the use case needs.
5. Avoid Open Session in View masking lazy loads during rendering.
6. Fix the query shape — do not just raise the connection pool size.

### Scene `teaser` (renderer: `teaser`)

1. Data is safe — next we lock the doors.
2. Episode Seventy-Six — Spring Security.
3. Authentication, authorization, filters, and securing REST APIs.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **75** — *Spring Data and Persistence*.
- **Series catalog:** Episode 75 ↔ handbook lesson 75 — *Spring Data and Persistence*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Four covered Spring MVC and REST boundaries._
- **`title`** — starts from: _Episode Seventy-Five._
- **`repositories`** — starts from: _Spring Data repositories declare persistence intent as interfaces._
- **`entities`** — starts from: _Entities map tables to objects — carefully._
- **`transactions`** — starts from: _Transactional marks a consistency boundary._
- **`nplusone`** — starts from: _The N-plus-one problem — classic interview and production trap._
- **`practices`** — starts from: _Practical persistence practices._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you avoid N-plus-one with Spring Data JPA?_
- **`teaser`** — starts from: _Data is safe — next we lock the doors._
