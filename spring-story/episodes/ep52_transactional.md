# Episode 52 — @Transactional

| Field | Value |
|---|---|
| Episode | 52 |
| Title | @Transactional |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 52 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Multiple database steps often need one all-or-nothing outcome. @Transactional declares that boundary.

Here is the pain this lesson exists to remove. Problem Statement Manual transaction code: try { conn.setAutoCommit(false); ... conn.commit(); } catch { rollback(); } Duplicated everywhere, easy to forget rollback, connection leaks, inconsistent across team.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is @Transactional.

Concept @Transactional is Spring's declarative transaction management annotation. It tells Spring: "Wrap this method in a database transaction — begin before, commit on success, rollback on failure." Without it, each JPA save() might auto-commit independently — breaking atomicity across multiple operations.

Spring's design choice here is deliberate. Same annotation works for JDBC, JPA, MyBatis when PlatformTransactionManager is configured. Integrates with @Rollback in tests. Design Principles Behind Spring Principle How Spring Applies It Inversion of Control Container controls object creation and wiring Dependency Injection Dependencies supplied via constructor/setter/field Separation of Concerns Config, cross-cutting (AOP), and domain logic separated Program to Interfaces Beans wired by type/name; swap impls without code change Convention over Configuration Boot defaults; sensible @Component scanning Non-invasive No framework classes required in domain model (POJOs) Spring vs Solving It Yourself Custom DI container Spring Framework

Once you accept the feature, the next honest question is how it works under the hood. Internal Working TransactionInterceptor + BeanFactoryTransactionAttributeSourceAdvisor create JDK/CGLIB proxy. Attributes parsed from @Transactional → RuleBasedTransactionAttribute . TransactionSynchronizationManager binds Connection/EntityManager to current thread. Container Refresh Sequence (High Level) Application startup

As you practice @Transactional, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through @Transactional inside Phase 5 — Transaction Management. The next natural question is waiting in Episode 53 — Propagation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 52 (*@Transactional*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
