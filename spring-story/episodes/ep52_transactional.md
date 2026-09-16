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

Multiple database steps often need one all-or-nothing outcome. @Transactional is Spring's declaration of that boundary.

Here is the pain this lesson exists to remove. Manual transaction code: try { conn.setAutoCommit(false); ... conn.commit(); } catch { rollback(); } Duplicated everywhere, easy to forget rollback, connection leaks, inconsistent across team.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is @Transactional.

@Transactional is Spring's declarative transaction management annotation. It tells Spring: "Wrap this method in a database transaction — begin before, commit on success, rollback on failure." Without it, each JPA save() might auto-commit independently — breaking atomicity across multiple operations.

A little context helps the idea stick. Spring 1.2 introduced @Transactional (2007). Before that, programmatic TransactionTemplate or JTA APIs were required. Spring unified JDBC, JPA, and JTA under one annotation model.

Spring's design choice here is deliberate. Declarative TX keeps business code clean. Same annotation works for JDBC, JPA, MyBatis when PlatformTransactionManager is configured. Integrates with @Rollback in tests.

Once you accept the feature, the next honest question is how it works under the hood. TransactionInterceptor + BeanFactoryTransactionAttributeSourceAdvisor create JDK/CGLIB proxy. Attributes parsed from @Transactional → RuleBasedTransactionAttribute . TransactionSynchronizationManager binds Connection/EntityManager to current thread.

As you practice @Transactional, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through @Transactional inside Phase 5 — Transaction Management. The next natural question is waiting in Episode 53 — Propagation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 52 (*@Transactional*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
