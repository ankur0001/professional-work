# Episode 55 — Rollback Rules

| Field | Value |
|---|---|
| Episode | 55 |
| Title | Rollback Rules |
| Phase | Phase 5 — Transaction Management |
| Catalog handbook lesson | 55 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Not every exception should undo the work. Rollback rules encode which failures are fatal to the unit of work.

Here is the pain this lesson exists to remove. Without mastering Rollback Rules , teams encounter mysterious startup failures: beans missing from context, wrong implementation wired, duplicate definitions, or environment-specific code compiled into production. Concrete scenario: a @Service appears not to inject — often the root cause lies in Rollback Rules misconfiguration (scan path, missing @Bean , wrong profile, or scope proxy issue). Additional pain points: implicit copy-paste config, test drift from production scanning, and library conflicts from duplicate bean definitions.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Rollback Rules.

Rollback Rules — rollbackFor, noRollbackFor, checked vs unchecked exceptions. This lesson is part of Phase 5 — TRANSACTION MANAGEMENT . By Lesson 55, you should see how Rollback Rules fits into the transaction and consistency boundary and the broader application architecture. Core Ideas Idea Explanation Purpose rollbackFor, noRollbackFor, checked vs unchecked exceptions. Primary API Default: rollback on RuntimeException and Error; commit on checked Related classes RuleBasedTransactionAttribute , @Transactional(rollbackFor=...) Typical config Java @Configuration + annotations (Boot default) Architecture Placement BeanDefinition sources Container core Your code

Spring's design choice here is deliberate. Spring centralizes Rollback Rules in the container rather than scattering factory logic across the codebase. Benefits: Single composition root — all wiring visible in config layer. Consistent semantics — same rules in tests and production. Extension hooks — customize via post-processors without forking framework. Tooling — IDE support, Actuator /beans , condition reports. Default: rollback on RuntimeException and Error; commit on checked. This is preferable to ad-hoc Service Locator or manual singleton registries that grow unmaintainable.

Once you accept the feature, the next honest question is how it works under the hood. Internally, Spring delegates Rollback Rules to well-tested components: RuleBasedTransactionAttribute , @Transactional(rollbackFor=...) Processing order matters: BeanFactoryPostProcessor s run before bean instantiation; BeanPostProcessor s wrap creation. Misordered custom processors cause subtle bugs. Step-by-Step Internal Flow for Rollback Rules Parse — configuration class, XML, or scan result produces BeanDefinition objects. Register — definitions stored in DefaultListableBeanFactory registry (by name + aliases). Post-process definitions — modify property values, register extra beans.

As you practice Rollback Rules, keep one habit: explain the before-and-after. What did the team do manually, and which Spring mechanism now owns that step?

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Rollback Rules inside Phase 5 — Transaction Management. The next natural question is waiting in Episode 56 — Distributed Transactions.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 55 (*Rollback Rules*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
