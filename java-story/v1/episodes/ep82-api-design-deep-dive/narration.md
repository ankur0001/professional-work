# Episode 82 — API Design Deep Dive

**Cut:** v1 (original)

## Transcript (from captions)

Episode Eighty-One covered caching layers, invalidation, and stampedes. APIs are long-lived contracts — harder to change than internal classes. Good API design reduces client breakage and on-call pages.

Idempotency, pagination, and versioning show up in every senior interview. Spring MVC skills matter — contract thinking matters more. Today — resources, versioning, idempotency, errors, and evolution.

Episode Eighty-Two. API Design Deep Dive. Model the API around resources and use cases — not your tables. Stable nouns — orders, payments, customers — with HTTP verbs for actions. Prefer coarse resources that match user intents over chatty micro-gets.

DTOs are public — never leak JPA entities or internal IDs carelessly. Explicit fields beat magic maps when clients generate code. Design for the reader of the OpenAPI — that reader is a future teammate.

Versioning is how you change without stranding clients. URL versions — slash v-one — are obvious and cache-friendly. Header versions keep paths clean — require disciplined clients. Additive changes are safest — new optional fields, new endpoints.

Breaking changes need a migration window and dual-run support. Deprecate loudly — metrics on old versions tell you when to cut. Idempotency makes retries safe. PUT and DELETE should be naturally idempotent — POST often is not.

Idempotency-Key headers dedupe creates across at-least-once clients. Store the key with the result — replay the same response on retry. Timeouts without idempotency cause double charges — design for it.

Document which endpoints are safe to retry — clients will guess otherwise. Pagination and filtering keep collections operable. Cursor pagination scales better than large offsets on hot tables.

Always bound page size — never allow unbounded find-all dumps. Stable sort keys prevent missing or duplicated rows across pages. Filter and sort parameters belong in the contract — validate them.

Return totals only when cheap — expensive counts need their own path. Error contracts are part of the API. Use correct status codes — four-hundred validation, four-oh-nine conflict.

Problem Details or a stable error schema beats ad-hoc message strings. Include a machine-readable code — human text can be localized later. Never leak stack traces or SQL to public clients.

Trace IDs in error bodies connect support tickets to logs. Three common mistakes. One — breaking JSON field types without a version bump. Two — POST create with no idempotency — double submits in production.

Three — offset pagination on huge tables — p99 death by skip. Also — returning different shapes for the same status code. Contracts are product — treat changes like migrations. Interview question — how do you evolve a public REST API safely?

Prefer additive changes — optional fields and new endpoints first. Version when you must break — dual-run with metrics on old clients. Idempotency keys on creates — pagination that scales with data.

Stable error schema with correlation IDs. Publish OpenAPI and changelog — silence is how clients break. Request-response is one style — events are another. Episode Eighty-Three — Event-Driven Architecture.

Topics, outbox, consumers, and when async wins. See you there.
