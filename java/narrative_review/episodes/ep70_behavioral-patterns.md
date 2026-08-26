# Episode 70 — Behavioral Patterns

| Field | Value |
|---|---|
| Episode | 70 |
| Title | Behavioral Patterns |
| Catalog handbook column | 70 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Structural patterns assembled objects. Behavioral patterns organize algorithms and communication — how work varies, how events propagate, how requests become objects. If creational is birth and structural is anatomy, behavioral is choreography.

Start with a deep conditional that everyone regrets:

```java
if (type == Type.PERCENT) { ... }
else if (type == Type.FIXED) { ... }
else if (type == Type.BOGO) { ... }
```

Every new promotion type edits this spine. Strategy replaces that spine with a common interface and swappable implementations. The caller depends on `DiscountPolicy`, not on a growing `if` tower. Strategy essence, for interviews: swap algorithms behind a common interface without rewriting callers. The failure mode is the opposite extreme — Strategy interfaces with one implementation forever, pure ceremony. Use Strategy when variation is real and expected to grow.

Observer fits events. Something interesting happens — order placed, user registered — and multiple listeners react. The subject notifies observers without hard-coding each reaction into its own method list. Useful. Also leaky: forgotten observers are the listener leaks from Episode Fifty-Seven wearing a pattern name. Register and unregister with clear lifetimes. In modern systems, message buses and application events play Observer at a larger scale, with the same lifetime discipline.

Template Method uses inheritance to fix an algorithm skeleton while letting subclasses fill steps. Composition with Strategy-like hooks often ages better in Java than deep template hierarchies, but you will still meet Template Method in frameworks. Command turns a request into an object — useful for queues, undo stacks, and audit trails. `command.execute()` can be logged, retried, or stored. Command explosion without need — a class per trivial action with no replay or undo story — is busywork.

Do not over-abstract one-off code. Behavioral patterns shine when communication or algorithm variation is a recurring pain. They dull when every method becomes an interface hierarchy "for testing" without a second implementation in sight. Prefer the smallest structure that keeps change local.

Walk a checkout flow. Pricing uses Strategy for discount policies. Placing an order publishes an event; email and inventory observe. A Command object representing "cancel order" sits on an admin undo stack. Each pattern appears because a problem appeared — not because a chapter checklist demanded coverage. That necessity test is the same one Episode Sixty-Seven taught.

If an interview asks for Strategy essence, give the swap-behind-interface answer, then mention when you would keep a simple switch — few stable variants, local code, no extension expected. Admitting the non-pattern choice is part of pattern literacy.

Strategy pairs naturally with modern Java. A `DiscountPolicy` functional interface can be implemented by classes or lambdas. The important part remains the seam: checkout depends on the interface. Unit tests inject a fixed policy. Production wires seasonal policies from configuration. The pattern is the seam, not the ceremony of anonymous inner classes from 2005.

Observer at process scale becomes events. In-process observers are easy and dangerous for leaks. Across services, observers become consumers of messages — and then you inherit at-least-once delivery, idempotency, and schema evolution, which later episodes will treat seriously. Spot the lineage now: the behavioral idea scales, the failure modes scale harder.

Template Method shows up when you subclass `JdbcTemplate`-style workflows or framework base classes. Prefer composition when you control the design: pass strategies for the varying steps instead of forcing callers into inheritance. When you are subclassing a framework that already chose Template Method, learn the hooks rather than fighting the skeleton.

Command objects earn their keep in job queues and audit logs. `RefundOrder` carries the data needed to perform and to record. Retries become re-execution of the same command. Undo becomes a compensating command. If you never retry, never audit, and never undo, a method call may suffice.

Interviewers sometimes ask you to "name a behavioral pattern you used." Tell a story: we replaced a switch with Strategy because marketing added three discount types in a quarter. Mechanisms plus timeline beat trivia.

Replace deep conditionals with Strategy only when the conditional encodes algorithm choice. If the conditional encodes a simple two-branch guard, a plain if remains clearer. Pattern literacy includes knowing when not to swing the hammer.

Observer leaks deserve a second beat because they reconnect to JVM memory. A component registers on a long-lived bus and is never removed. The component graph stays. Heaps climb. The pattern did not cause the leak by itself; unbounded lifetime did. Pair Observer with explicit deregistration or weak listener policies where appropriate.

Command for undo and queues should stay tied to product needs. An undo stack in a document editor is a real Command win. A command class per controller endpoint with no queue is theater. Keep the necessity test from Episode Sixty-Seven pinned above your IDE.

Behavioral patterns also meet concurrency. Strategy objects should usually be stateless or immutable so they can be shared across threads. Observers that mutate shared collections need the same discipline you learned in the concurrency arc. Commands placed on queues must be serializable or mappable to messages if they cross process boundaries. The pattern sketch is single-threaded; production choreography is not. Carry the JVM and concurrency instincts forward when you apply catalog names.

Behavioral patterns close the classical catalog arc. Next we enter the ecosystem where many of these ideas are industrialized for enterprise Java: Spring — dependency injection, portable abstractions, and a container mindset. Episode Seventy-One begins that story with a practical situation, not a feature brochure.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Behavioral Patterns (Episode 70).

Narration technique: choreography framing → conditional → Strategy → Observer leaks → Template/Command → don't over-abstract → checkout walk → interview woven → bridge to Spring.

Teaching points preserved: Strategy; Observer; Template vs composition; Command; don't over-abstract one-offs.
