# Episode 83 — Event-Driven Architecture

| Field | Value |
|---|---|
| Episode | 83 |
| Title | Event-Driven Architecture |
| Catalog handbook column | 83 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Synchronous APIs couple latency: your checkout waits on inventory. Sometimes you need facts to propagate without blocking the caller. Events are facts — something that happened — and consumers must tolerate at-least-once delivery. Assuming exactly-once is how systems lie to themselves.

Distinguish facts from commands. `OrderCreated` is a fact. `CreateOrder` is a command. Facts let multiple consumers react — email, analytics, inventory — without the producer knowing each one. Ordering is partial: across partitions or consumers, time is not a single global line. Schema evolution matters because old consumers and new producers coexist during deploys.

Dual writes without an outbox are a classic failure. You write the order row, then publish to the broker, and crash between. The message is lost. Or you publish first and fail to write. The outbox pattern records the state change and the event in one transaction; a publisher relays outbox rows to the bus.

```java
// transactionally write Order + OutboxEvent
// publisher relays outbox to the bus
// consumers handle OrderCreated idempotently
```

Why outbox? Atomically record state change plus event to avoid lost messages. Idempotent consumers handle duplicates from at-least-once delivery — using event ids or natural keys. Fat events that couple everything — dumping entire object graphs — make schema change painful; prefer necessary facts with clear versioning.

At-least-once delivery means duplicates are normal. Consumers must treat redelivery as expected, not as a broker bug. Idempotency keys, dedupe tables, or natural unique constraints turn duplicates into no-ops. Exactly-once end-to-end across independent systems is a marketing phrase more often than an engineering guarantee — be precise in interviews.

Outbox versus dual write is the reliability fork. Dual write looks shorter in a demo. Outbox looks like extra tables and a publisher. Under failure injection, outbox wins. Transactional outbox plus a relay process is boring infrastructure that prevents silent data loss.

Schema evolution needs compatibility rules: additive fields, careful renames, consumers that ignore unknowns. Fat events that embed every nested entity make evolution and PII handling harder. Prefer identifiers plus essential attributes, with consumers fetching details when needed — balancing chatty reads against coupling.

Partial ordering means you design for "inventory update may arrive before the email consumer is ready" and for partition-level order only when you key messages carefully. If your business needs strong global order, events may be the wrong primary tool for that slice.

Facts versus commands keep producers honest. Emitting commands disguised as events couples producers to consumer intent. Emit what happened; let consumers decide what to do.

Connect events to the observability episode. Every event should carry correlation ids so a checkout trace includes the async legs that fire after the HTTP response. Without that, event-driven systems become un-debuggable fog.

Outbox publishers need their own monitoring: lag, failure counts, poison messages. An outbox that stops draining is a silent outage — the API looks healthy while downstream consumers starve. Production readiness later will call this ownership; start the habit now.

Schema evolution pairs with consumer deployment order. Prefer expand/contract: add fields, deploy consumers that tolerate them, then switch producers, then remove old fields later. Fat events fight this discipline by making every change large.

Idempotent consumers plus outbox plus partial-order awareness is the minimum responsible set for event-driven Java services. Skip any one and the architecture interview should dock you — and production will too.

A concrete dual-write failure seals the lesson. Transaction commits the order. Process crashes before Kafka send returns. Customer sees success; inventory never hears. Support tickets multiply. Outbox would have left a row to relay on restart. That single story converts skeptics faster than abstract diagrams.

Consumers handle OrderCreated idempotently by remembering processed event ids or by upserting state keyed by order id. Choose the approach that matches your domain. Test redelivery in CI. Untested idempotency is hopeful naming.

Ordering is partial — design workflows that tolerate inventory-before-email or email-before-inventory unless you intentionally serialize through a single key and partition. When business truly needs a saga with orchestration, say so; do not pretend a firehose of events gives you global transaction semantics for free.

Events are facts; consumers must tolerate at-least-once; outbox protects producers from dual-write loss. That triad is the episode in one breath.

Schema evolution example: add an optional `shippingMethod` field to OrderCreated. Old consumers ignore it. New consumers use it. Later remove a deprecated field only after all consumers deploy. That expand/contract rhythm is how events age without stop-the-world upgrades.

Fat events that couple everything tempt producers to embed customer, inventory, and pricing snapshots. Then every consumer breaks when pricing shape changes. Prefer essential facts; let consumers query what they need or maintain their own read models from smaller events.

At-least-once plus outbox plus idempotent consumers is not optional garnish for "serious" companies only — it is the baseline for any event-driven path that moves money or inventory. Demoing Kafka without those pieces is a demo of risk.

When events cross team boundaries, ownership of schema becomes political. Decide who may add fields, how compatibility is tested, and where the schema registry lives if you use one. Technology alone does not solve governance; name the owners like production readiness will demand in the final episode.

Tolerate at-least-once, record facts through an outbox, and evolve schemas additively. That sentence is enough to start a design review. The rest of the episode exists so you can defend each clause when someone proposes skipping one for speed.

Event-driven designs shine when they reduce coupling and absorb load spikes. They punish teams that skip idempotency, outbox, and observability. Performance across sync and async paths still needs a disciplined loop — Episode Eighty-Four.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Event-Driven Architecture (Episode 83).

Narration technique: sync coupling pain → events as facts → facts vs commands → dual write failure → outbox code → idempotent consumers → interview woven → bridge to performance.

Teaching points preserved: facts vs commands; idempotent consumers; outbox; partial ordering; schema evolution.
