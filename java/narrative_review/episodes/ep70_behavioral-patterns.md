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

Every new promotion type edits this spine. Strategy replaces it with a common interface and swappable implementations. The caller depends on `DiscountPolicy`, not on a growing `if` tower. Strategy essence: swap algorithms behind a common interface without rewriting callers. The failure mode is Strategy interfaces with one implementation forever — pure ceremony. Use Strategy when variation is real and expected to grow. Keep a simple switch when few stable variants live local and no extension is expected. Admitting the non-pattern choice is part of pattern literacy.

A `DiscountPolicy` functional interface can be implemented by classes or lambdas. The important part is the seam: checkout depends on the interface. Unit tests inject a fixed policy; production wires seasonal policies from configuration. The pattern is the seam, not the ceremony of anonymous inner classes from 2005.

Observer fits events. Something interesting happens — order placed, user registered — and multiple listeners react. The subject notifies observers without hard-coding each reaction. Useful. Also leaky: forgotten observers are the listener leaks from Episode Fifty-Seven wearing a pattern name. Register and unregister with clear lifetimes. A component that registers on a long-lived bus and is never removed keeps its graph alive; heaps climb. The pattern did not cause the leak — unbounded lifetime did. In modern systems, message buses play Observer at a larger scale, with the same lifetime discipline — plus at-least-once delivery and idempotency that later episodes treat seriously.

Template Method uses inheritance to fix an algorithm skeleton while subclasses fill steps. Composition with Strategy-like hooks often ages better in Java than deep template hierarchies, but you will still meet Template Method in frameworks — learn the hooks rather than fighting the skeleton.

Command turns a request into an object — useful for queues, undo stacks, and audit trails. `RefundOrder` carries the data needed to perform and to record. Retries become re-execution; undo becomes a compensating command. If you never retry, never audit, and never undo, a method call may suffice. Command explosion without need is busywork.

Walk a checkout flow. Pricing uses Strategy for discount policies. Placing an order publishes an event; email and inventory observe. A Command representing "cancel order" sits on an admin undo stack. Each pattern appears because a problem appeared — not because a chapter checklist demanded coverage. That necessity test is the same one Episode Sixty-Seven taught.

Behavioral patterns also meet concurrency. Strategy objects should usually be stateless or immutable so they can be shared across threads. Observers that mutate shared collections need the discipline from the concurrency arc. Commands on queues must be serializable or mappable if they cross process boundaries. The pattern sketch is single-threaded; production choreography is not.

Do not over-abstract one-off code. Behavioral patterns shine when communication or algorithm variation is a recurring pain. They dull when every method becomes an interface hierarchy "for testing" without a second implementation in sight. Prefer the smallest structure that keeps change local. Interviewers who ask for a behavioral pattern you used want a story: we replaced a switch with Strategy because marketing added three discount types in a quarter. Mechanisms plus timeline beat trivia.

Behavioral patterns close the classical catalog arc. Next we enter the ecosystem where many of these ideas are industrialized for enterprise Java: Spring — dependency injection, portable abstractions, and a container mindset. Episode Seventy-One begins that story with a practical situation, not a feature brochure.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Behavioral Patterns (Episode 70).

Narration technique: choreography framing → conditional → Strategy → Observer leaks → Template/Command → checkout walk → concurrency note → bridge to Spring.

Teaching points preserved: Strategy; Observer; Template vs composition; Command; don't over-abstract one-offs.
