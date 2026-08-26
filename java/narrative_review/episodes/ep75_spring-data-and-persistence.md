# Episode 75 — Spring Data and Persistence

| Field | Value |
|---|---|
| Episode | 75 |
| Title | Spring Data and Persistence |
| Catalog handbook column | 75 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Your REST controller needs to load a user by email. You could write JDBC by hand. You could write a full EntityManager repository. Spring Data says: declare an interface, get a repository. That speed is real — and so is the bill that arrives later if you forget SQL, transactions, and fetch behavior.

```java
interface UserRepo extends JpaRepository<User, Long> {
  List<User> findByEmail(String email);
}
```

`JpaRepository` gives you CRUD and paging helpers. Query methods derive queries from names — convenient until the method name becomes a novel. Custom `@Query` methods appear when derivation is not enough. Transaction boundaries matter: where does a unit of work start and end? Service-layer `@Transactional` is a common pattern so controllers stay thin and repositories do not each invent their own transaction story.

N+1 queries are the pitfall that turns demos into outages. You load a list of orders, then touch `order.getLines()` per order, and each touch fires another query. Lazy loading surprises outside a session throw `LazyInitializationException`. Fetch strategies — join fetch, entity graphs — must be chosen deliberately. God repositories that know every query in the company become dumpsters; split by aggregate or use cases when the interface grows without bound.

Migrations matter. Auto-ddl in production is not a strategy. Flyway or Liquibase — or your team's equivalent — version schema changes beside code. Spring Data speeds repositories; you still own SQL and schema reality.

Biggest JPA pitfall? Lazy loading surprises and N+1 queries. Say it, then say how you detect it: logging SQL in staging, metrics on query counts per request, and refusing to return entities across layers that close the session.

Query methods are wonderful until `findByAccountIdAndStatusInAndCreatedAtBetweenOrderByCreatedAtDesc` becomes unreadable. At that point a named `@Query` or a criteria/API approach can be clearer. Spring Data did not remove SQL thinking; it deferred it. Explain plans still matter. Indexes still matter.

Transaction boundaries decide consistency. A service method that updates an order and records an outbox event should succeed or fail together. Marking every repository method transactional can create chatty transactions and surprises around lazy loading. Prefer coarse enough service transactions with clear read-only flags for query paths.

N+1 detection should be part of Definition of Done for list endpoints. Enable SQL logging in a test profile, hit the endpoint, count statements. If count scales with list size, fix fetch strategy or reshape the query into a join or a dedicated read model. `LazyInitializationException` outside the session often means the view or DTO mapper touched lazy fields after the transaction closed — another reason not to spill entities into web layers.

God repositories appear when every query in the system lands on one interface. Split by aggregate roots or by bounded read/write use cases. Migrations keep schema evolution reviewable; pair them with expand/contract practices when zero downtime matters.

Biggest pitfall remains lazy loading and N+1 — because the code looks clean while the database burns.

Query methods are wonderful until method names become novels. At that point a named query can be clearer. Spring Data did not remove SQL thinking; it deferred it. Explain plans still matter. Indexes still matter.

Transaction boundaries decide consistency. A service method that updates an order and records an outbox event should succeed or fail together. Marking every repository method transactional can create chatty transactions and surprises around lazy loading. Prefer service-level transactions with clear read-only flags for query paths.

N+1 detection should be part of Definition of Done for list endpoints. Enable SQL logging in a test profile, hit the endpoint, count statements. If count scales with list size, fix fetch strategy or reshape the query. LazyInitializationException outside the session often means a mapper touched lazy fields after the transaction closed — another reason not to spill entities into web layers.

God repositories appear when every query lands on one interface. Split by aggregate or use case. Migrations keep schema evolution reviewable; pair them with expand/contract practices when zero downtime matters.

Read-write splitting and routing datasources appear as you scale, but the first victory is simpler: know which queries your page runs. Spring Data makes it easy to accidentally hide a dozen queries behind a tidy method name. Logging and metrics bring them back into view. Persistence literacy is still database literacy — repositories are a dialect, not an escape hatch.

If interviewers ask the biggest JPA pitfall, answer lazy loading and N+1, then briefly say how you would catch it in CI with SQL counting tests on critical list endpoints. That turns a trivia answer into an engineering answer.

Connect transactions to the outbox teaser you will meet later in event-driven design. If you update a row and publish a message in two separate steps without a shared transactional story, you will lose messages or double-apply effects under failure. Spring's transaction boundaries are part of that story even before you introduce messaging libraries. Persistence is not only CRUD; it is where consistency policies become real.

Migrations matter because code and schema are a pair. A repository method that assumes a new column will fail until the migration lands. Treat schema changes as reviewed artifacts. Auto-ddl in production hides drift until a catastrophic recreate fantasy meets real data.

Spring Data speeds repositories — keep saying the second half aloud — you still own SQL and N+1 reality.

Persistence without security is an open door. Episode Seventy-Six is Spring Security — filter chains, authentication versus authorization, and never inventing crypto.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Data and Persistence (Episode 75).

Narration technique: need load-by-email → Spring Data speed + bill → JpaRepository example → transactions → N+1/lazy → migrations → interview woven → bridge to security.

Teaching points preserved: JpaRepository; query methods; transaction boundaries; N+1/fetch; migrations.
