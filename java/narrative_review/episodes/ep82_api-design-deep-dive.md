# Episode 82 — API Design Deep Dive

| Field | Value |
|---|---|
| Episode | 82 |
| Title | API Design Deep Dive |
| Catalog handbook column | S2 |
| Narration source script | `make_episode_82.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Eighty-One covered caching layers, invalidation, and stampedes.
2. APIs are long-lived contracts — harder to change than internal classes.
3. Good API design reduces client breakage and on-call pages.
4. Idempotency, pagination, and versioning show up in every senior interview.
5. Spring MVC skills matter — contract thinking matters more.
6. Today — resources, versioning, idempotency, errors, and evolution.

### Scene `title` (renderer: `title`)

1. Episode Eighty-Two.
2. API Design Deep Dive.

### Scene `resources` (renderer: `resources`)

1. Model the API around resources and use cases — not your tables.
2. Stable nouns — orders, payments, customers — with HTTP verbs for actions.
3. Prefer coarse resources that match user intents over chatty micro-gets.
4. DTOs are public — never leak JPA entities or internal IDs carelessly.
5. Explicit fields beat magic maps when clients generate code.
6. Design for the reader of the OpenAPI — that reader is a future teammate.

### Scene `versioning` (renderer: `versioning`)

1. Versioning is how you change without stranding clients.
2. URL versions — slash v-one — are obvious and cache-friendly.
3. Header versions keep paths clean — require disciplined clients.
4. Additive changes are safest — new optional fields, new endpoints.
5. Breaking changes need a migration window and dual-run support.
6. Deprecate loudly — metrics on old versions tell you when to cut.

### Scene `idempotency` (renderer: `idempotency`)

1. Idempotency makes retries safe.
2. PUT and DELETE should be naturally idempotent — POST often is not.
3. Idempotency-Key headers dedupe creates across at-least-once clients.
4. Store the key with the result — replay the same response on retry.
5. Timeouts without idempotency cause double charges — design for it.
6. Document which endpoints are safe to retry — clients will guess otherwise.

### Scene `pagination` (renderer: `pagination`)

1. Pagination and filtering keep collections operable.
2. Cursor pagination scales better than large offsets on hot tables.
3. Always bound page size — never allow unbounded find-all dumps.
4. Stable sort keys prevent missing or duplicated rows across pages.
5. Filter and sort parameters belong in the contract — validate them.
6. Return totals only when cheap — expensive counts need their own path.

### Scene `errors` (renderer: `errors`)

1. Error contracts are part of the API.
2. Use correct status codes — four-hundred validation, four-oh-nine conflict.
3. Problem Details or a stable error schema beats ad-hoc message strings.
4. Include a machine-readable code — human text can be localized later.
5. Never leak stack traces or SQL to public clients.
6. Trace IDs in error bodies connect support tickets to logs.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — breaking JSON field types without a version bump.
3. Two — POST create with no idempotency — double submits in production.
4. Three — offset pagination on huge tables — p99 death by skip.
5. Also — returning different shapes for the same status code.
6. Contracts are product — treat changes like migrations.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you evolve a public REST API safely?
2. Prefer additive changes — optional fields and new endpoints first.
3. Version when you must break — dual-run with metrics on old clients.
4. Idempotency keys on creates — pagination that scales with data.
5. Stable error schema with correlation IDs.
6. Publish OpenAPI and changelog — silence is how clients break.

### Scene `teaser` (renderer: `teaser`)

1. Request-response is one style — events are another.
2. Episode Eighty-Three — Event-Driven Architecture.
3. Topics, outbox, consumers, and when async wins.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Episode 82** is a **Season 2 production-systems bonus** track. It is **not** one of the handbook’s 80 lessons.
- Topic framing for the video: **API Design Deep Dive** (continuity after Episode 80’s architecture interview wrap).
- Narration was **original written for the video** (scene-synced beats), not copied verbatim from the handbook.
