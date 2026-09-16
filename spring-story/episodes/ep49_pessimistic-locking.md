# Episode 49 — Pessimistic Locking

| Field | Value |
|---|---|
| Episode | 49 |
| Title | Pessimistic Locking |
| Phase | Phase 4 — Spring Data JPA |
| Catalog handbook lesson | 49 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Sometimes rare conflict is still too risky. Pessimistic locking holds the row while you finish the work.

Here is the pain this lesson exists to remove. Without mastering Pessimistic Locking , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Pessimistic Locking misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Pessimistic Locking.

Pessimistic Locking — SELECT FOR UPDATE row-level locks in transactions. This lesson is part of Phase 4 — SPRING DATA JPA . It builds on Phase 1–3 (IoC, Boot, MVC). By Lesson 49, you should see how Pessimistic Locking fits into the persistence and data-access layer and the broader application architecture. Primary API LockModeType.PESSIMISTIC_WRITE Related classes EntityManager.lock() , @Lock , PessimisticLockException Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Pessimistic Locking in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. LockModeType.PESSIMISTIC_WRITE , lock timeout, deadlock risks. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Pessimistic Locking to well-tested components: EntityManager.lock() , @Lock , PessimisticLockException Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Pessimistic Locking Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Pessimistic Locking, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Pessimistic Locking inside Phase 4 — Spring Data JPA. The next natural question is waiting in Episode 50 — Performance Tuning.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 49 (*Pessimistic Locking*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
