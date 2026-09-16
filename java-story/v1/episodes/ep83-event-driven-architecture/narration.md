# Episode 83 — Event-Driven Architecture

**Cut:** v1 (original)

## Transcript (from captions)

Episode Eighty-Two covered API contracts — versioning, idempotency, pagination. Not every collaboration should be a synchronous HTTP call. Event-driven architecture decouples producers from consumers in time.

Kafka, queues, and the transactional outbox appear constantly in designs. Async is powerful — and a great way to lose data if you skip patterns. Today — events versus commands, outbox, consumers, and failure handling.

Episode Eighty-Three. Event-Driven Architecture. Why teams reach for events. Fan-out — one fact notifies many interested services. Temporal decoupling — producer stays up when a consumer is down.

Smooth load — buffers absorb spikes that would melt sync chains. Auditability — a log of facts becomes a product feature. Cost — more moving parts, harder end-to-end debugging — earn it.

Events and commands are not the same speech act. A command asks a specific service to do work — often expects a reply. An event states a fact that already happened — OrderPlaced. Name events in past tense — consumers decide their own reactions.

Do not hide commands inside topics without clear ownership. Schema evolution — additive fields, careful compatibility rules. Dual-write is the classic distributed bug. Writing the database and publishing a message separately can diverge.

Transactional outbox — same DB transaction stores business row and outbox row. A publisher relay reads the outbox and emits to Kafka reliably. Inbox or idempotent consumers handle at-least-once delivery.

If you cannot explain outbox, do not claim exactly-once in interviews. Consumer design decides whether async helps or hurts. Make handlers idempotent — duplicates will arrive. Poison messages need a dead-letter path — not infinite retries.

Lag is a first-class metric — silent lag is silent outage. Ordering — partition keys preserve per-entity order when required. Backpressure — slow consumers must not silently drop work.

When not to go event-driven. A single team, single deployable, simple CRUD — sync may be enough. User needs an immediate answer — keep the request-response path. You lack ops for brokers, schemas, and lag alerts — defer the split.

Chatty pseudo-events that are really RPC over topics — worst of both. Choose async for clear fan-out or durability needs — not for resume keywords. Three common mistakes. One — dual-write without outbox — lost or double events under failure.

Two — non-idempotent consumers — retries corrupt state. Three — no lag alerts — discover backlog when customers complain. Also — giant event payloads that couple every consumer to internals.

Publish stable facts — keep fat details behind APIs when needed. Interview question — how do you publish OrderPlaced safely? Write order and outbox row in one database transaction. Relay publishes to the topic — at-least-once delivery.

Consumers key on event ID — idempotent processing. Dead-letter poison messages — alert on consumer lag. That is a senior answer — mechanisms, not buzzwords. Architecture moves data — performance keeps users happy.

Episode Eighty-Four — Performance Playbook. Measure, find bottlenecks, and fix the hottest path first. See you there.
