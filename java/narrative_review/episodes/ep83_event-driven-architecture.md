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

Distinguish facts from commands. `OrderCreated` is a fact. `CreateOrder` is a command. Facts let multiple consumers react — email, analytics, inventory — without the producer knowing each one. Emitting commands disguised as events couples producers to consumer intent. Emit what happened; let consumers decide what to do.

Dual writes without an outbox are a classic failure. Transaction commits the order. Process crashes before Kafka send returns. Customer sees success; inventory never hears. The outbox pattern records the state change and the event in one transaction; a publisher relays outbox rows to the bus.

```java
// transactionally write Order + OutboxEvent
// publisher relays outbox to the bus
// consumers handle OrderCreated idempotently
```

Why outbox? Atomically record state change plus event to avoid lost messages. Dual write looks shorter in a demo; under failure injection, outbox wins. Outbox publishers need their own monitoring: lag, failure counts, poison messages. An outbox that stops draining is a silent outage — the API looks healthy while downstream consumers starve.

At-least-once delivery means duplicates are normal. Consumers must treat redelivery as expected. Idempotency keys, dedupe tables, or natural unique constraints — upserting state keyed by order id — turn duplicates into no-ops. Test redelivery in CI. Untested idempotency is hopeful naming. Exactly-once end-to-end across independent systems is a marketing phrase more often than an engineering guarantee.

Ordering is partial: across partitions or consumers, time is not a single global line. Design workflows that tolerate inventory-before-email unless you intentionally serialize through a single key and partition. If your business needs strong global order or a saga with orchestration, say so — do not pretend a firehose of events gives you global transaction semantics for free.

Schema evolution needs compatibility rules: additive fields, careful renames, consumers that ignore unknowns. Prefer expand/contract: add fields, deploy consumers that tolerate them, then switch producers, then remove old fields later. Fat events that embed every nested entity make evolution and PII handling harder — every consumer breaks when pricing shape changes. Prefer identifiers plus essential attributes; let consumers query details or maintain their own read models from smaller events.

Connect events to observability. Every event should carry correlation ids so a checkout trace includes the async legs that fire after the HTTP response. When events cross team boundaries, ownership of schema becomes political — decide who may add fields and how compatibility is tested. Technology alone does not solve governance.

Events are facts; consumers must tolerate at-least-once; outbox protects producers from dual-write loss. That triad is the episode in one breath. Event-driven designs shine when they reduce coupling and absorb load spikes. They punish teams that skip idempotency, outbox, and observability. Performance across sync and async paths still needs a disciplined loop — Episode Eighty-Four.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Event-Driven Architecture (Episode 83).

Narration technique: sync coupling → events as facts → dual-write failure → outbox → idempotent consumers → partial order/schema → bridge to performance.

Teaching points preserved: facts vs commands; idempotent consumers; outbox; partial ordering; schema evolution.
