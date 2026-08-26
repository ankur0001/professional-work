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

`JpaRepository` gives you CRUD and paging helpers. Query methods derive queries from names — convenient until `findByAccountIdAndStatusInAndCreatedAtBetweenOrderByCreatedAtDesc` becomes a novel. At that point a named `@Query` or a criteria approach can be clearer. Spring Data did not remove SQL thinking; it deferred it. Explain plans still matter. Indexes still matter.

Transaction boundaries decide consistency. A service method that updates an order and records an outbox event should succeed or fail together. Service-layer `@Transactional` is a common pattern so controllers stay thin and repositories do not each invent their own transaction story. Marking every repository method transactional can create chatty transactions and lazy-loading surprises. Prefer coarse enough service transactions with clear read-only flags for query paths. Connect this to the outbox teaser you will meet in event-driven design: update a row and publish a message in two separate steps without a shared transactional story, and you will lose messages or double-apply effects under failure.

N+1 queries are the pitfall that turns demos into outages. You load a list of orders, then touch `order.getLines()` per order, and each touch fires another query. Lazy loading outside a session throws `LazyInitializationException`. Make N+1 detection part of Definition of Done for list endpoints: enable SQL logging in a test profile, hit the endpoint, count statements. If count scales with list size, fix fetch strategy — join fetch, entity graphs — or reshape into a join or dedicated read model. The code looks clean while the database burns.

Do not spill entities into web layers. A mapper that touches lazy fields after the transaction closed is another reason Episode Seventy-Four refused to return entities. God repositories that know every query in the company become dumpsters; split by aggregate or use case when the interface grows without bound.

Migrations matter. Auto-ddl in production is not a strategy. Flyway or Liquibase — or your team's equivalent — version schema changes beside code. A repository method that assumes a new column will fail until the migration lands. Treat schema changes as reviewed artifacts. Pair with expand/contract practices when zero downtime matters.

Read-write splitting appears as you scale, but the first victory is simpler: know which queries your page runs. Spring Data makes it easy to hide a dozen queries behind a tidy method name. Logging and metrics bring them back into view. Persistence literacy is still database literacy — repositories are a dialect, not an escape hatch.

Biggest JPA pitfall? Lazy loading surprises and N+1 queries. Say it, then say how you detect it: SQL logging in staging, metrics on query counts per request, and SQL-counting tests on critical list endpoints in CI. That turns a trivia answer into an engineering answer. Spring Data speeds repositories — keep saying the second half aloud — you still own SQL and N+1 reality.

Persistence without security is an open door. Episode Seventy-Six is Spring Security — filter chains, authentication versus authorization, and never inventing crypto.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Data and Persistence (Episode 75).

Narration technique: need load-by-email → Spring Data speed + bill → JpaRepository → transactions → N+1/lazy → migrations → interview woven → bridge to security.

Teaching points preserved: JpaRepository; query methods; transaction boundaries; N+1/fetch; migrations.
