# Episode 54 — Isolation Levels

| Field | Value |
|---|---|
| Episode | 54 |
| Title | Isolation Levels |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 54 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Transactions do not only commit or roll back. Isolation levels decide what concurrent readers and writers can see.

Here is the pain this lesson exists to remove. Without mastering Isolation Levels , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Isolation Levels misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Isolation Levels.

Isolation Levels — READ_UNCOMMITTED, READ_COMMITTED, REPEATABLE_READ, SERIALIZABLE. This lesson is part of Phase 5 — TRANSACTION MANAGEMENT . By Lesson 54, you should see how Isolation Levels fits into the transaction and consistency boundary and the broader application architecture. Primary API Dirty read Related classes Isolation , @Transactional(isolation=...) , database default vs explicit Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Isolation Levels in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. Dirty read, non-repeatable read, phantom read trade-offs. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Isolation Levels to well-tested components: Isolation , @Transactional(isolation=...) , database default vs explicit Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Isolation Levels Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases).

As you practice Isolation Levels, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Isolation Levels inside Phase 5 — Transaction Management. The next natural question is waiting in Episode 55 — Rollback Rules.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 54 (*Isolation Levels*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
