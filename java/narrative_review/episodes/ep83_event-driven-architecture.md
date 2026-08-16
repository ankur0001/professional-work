# Episode 83 — Event-Driven Architecture

| Field | Value |
|---|---|
| Episode | 83 |
| Title | Event-Driven Architecture |
| Catalog handbook column | S2 |
| Narration source script | `make_episode_83.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Eighty-Two covered API contracts — versioning, idempotency, pagination.
2. Not every collaboration should be a synchronous HTTP call.
3. Event-driven architecture decouples producers from consumers in time.
4. Kafka, queues, and the transactional outbox appear constantly in designs.
5. Async is powerful — and a great way to lose data if you skip patterns.
6. Today — events versus commands, outbox, consumers, and failure handling.

### Scene `title` (renderer: `title`)

1. Episode Eighty-Three.
2. Event-Driven Architecture.

### Scene `why_async` (renderer: `why_async`)

1. Why teams reach for events.
2. Fan-out — one fact notifies many interested services.
3. Temporal decoupling — producer stays up when a consumer is down.
4. Smooth load — buffers absorb spikes that would melt sync chains.
5. Auditability — a log of facts becomes a product feature.
6. Cost — more moving parts, harder end-to-end debugging — earn it.

### Scene `events_commands` (renderer: `events_commands`)

1. Events and commands are not the same speech act.
2. A command asks a specific service to do work — often expects a reply.
3. An event states a fact that already happened — OrderPlaced.
4. Name events in past tense — consumers decide their own reactions.
5. Do not hide commands inside topics without clear ownership.
6. Schema evolution — additive fields, careful compatibility rules.

### Scene `outbox` (renderer: `outbox`)

1. Dual-write is the classic distributed bug.
2. Writing the database and publishing a message separately can diverge.
3. Transactional outbox — same DB transaction stores business row and outbox row.
4. A publisher relay reads the outbox and emits to Kafka reliably.
5. Inbox or idempotent consumers handle at-least-once delivery.
6. If you cannot explain outbox, do not claim exactly-once in interviews.

### Scene `consumers` (renderer: `consumers`)

1. Consumer design decides whether async helps or hurts.
2. Make handlers idempotent — duplicates will arrive.
3. Poison messages need a dead-letter path — not infinite retries.
4. Lag is a first-class metric — silent lag is silent outage.
5. Ordering — partition keys preserve per-entity order when required.
6. Backpressure — slow consumers must not silently drop work.

### Scene `when_not` (renderer: `when_not`)

1. When not to go event-driven.
2. A single team, single deployable, simple CRUD — sync may be enough.
3. User needs an immediate answer — keep the request-response path.
4. You lack ops for brokers, schemas, and lag alerts — defer the split.
5. Chatty pseudo-events that are really RPC over topics — worst of both.
6. Choose async for clear fan-out or durability needs — not for resume keywords.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — dual-write without outbox — lost or double events under failure.
3. Two — non-idempotent consumers — retries corrupt state.
4. Three — no lag alerts — discover backlog when customers complain.
5. Also — giant event payloads that couple every consumer to internals.
6. Publish stable facts — keep fat details behind APIs when needed.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you publish OrderPlaced safely?
2. Write order and outbox row in one database transaction.
3. Relay publishes to the topic — at-least-once delivery.
4. Consumers key on event ID — idempotent processing.
5. Dead-letter poison messages — alert on consumer lag.
6. That is a senior answer — mechanisms, not buzzwords.

### Scene `teaser` (renderer: `teaser`)

1. Architecture moves data — performance keeps users happy.
2. Episode Eighty-Four — Performance Playbook.
3. Measure, find bottlenecks, and fix the hottest path first.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Episode 83** is a **Season 2 production-systems bonus** track. It is **not** one of the handbook’s 80 lessons.
- Topic framing for the video: **Event-Driven Architecture** (continuity after Episode 80’s architecture interview wrap).
- Narration was **original written for the video** (scene-synced beats), not copied verbatim from the handbook.
