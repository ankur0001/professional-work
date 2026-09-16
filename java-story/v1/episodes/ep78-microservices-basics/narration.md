# Episode 78 — Microservices Basics

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Seven covered testing Spring apps from unit to containers. Architecture interviews often jump next — should this be microservices? Microservices are independently deployable services collaborating over the network.

They buy team autonomy and scale axes — they cost operational complexity. The wrong split creates a distributed monolith — worst of both worlds. Today — when to split, boundaries, communication, data, and failure modes.

Episode Seventy-Eight. Microservices Basics. Split when forces demand it — not for fashion. Independent deploy cadence across teams is a real force. Different scale or technology needs per subdomain.

Strong module boundaries already exist — services formalize them. If one team owns everything and deploys weekly together — a modular monolith may win. Start cohesive — extract services when pain is measured, not imagined.

Boundaries follow business capabilities — not technical layers. Think Order Service and Payment Service — not Controller Service and Repository Service. Domain-driven contexts help — a bounded context is a candidate service.

Avoid chatty cross-service calls inside one user request when possible. Shared libraries for DTOs can couple release trains — version carefully. Clear ownership beats perfect purity — every service needs an owning team.

Communication styles define failure shapes. Synchronous HTTP or gRPC — simple mental model, tight runtime coupling. Asynchronous messaging — Kafka or queues — temporal decoupling, harder flows.

Idempotency keys matter when at-least-once delivery retries. Timeouts, retries, and backoff are part of the interface contract. Prefer async for fan-out and sync for queries that must return now.

Data ownership is the hard part of microservices. Each service owns its database — no shared tables across services. Cross-service joins become APIs or materialized read models. Sagas or outbox patterns coordinate multi-service changes.

Dual writes without a pattern are how distributed inconsistency starts. Eventual consistency is a product decision — set user expectations. Operational cost you must budget for. More deployables — more pipelines, dashboards, and on-call surfaces.

Distributed tracing and correlation IDs become mandatory. Local development needs compose files or remote stubs. Network latency and partial failure replace in-process method calls.

If you cannot operate it, you do not have microservices — you have hope. Three common mistakes. One — splitting by technical layer — distributed presentation and data tiers. Two — shared database across services — invisible coupling at the schema.

Three — chatty sync chains — one click fans into a latency hairball. Also — no idempotency — retries create double charges and duplicate rows. Architecture must match team and ops maturity — not a conference talk.

Interview question — monolith or microservices for a new product? Default to a modular monolith until deploy or scale forces argue otherwise. Define domain boundaries first — extract services along those lines later.

Budget for observability, CI, and on-call before multiplying deployables. Call out data ownership and consistency model explicitly. Optimize for change — pick the shape that lets the team ship safely.

Distributed systems fail in partial ways — next we harden them. Episode Seventy-Nine — Observability and Resilience. Logs, metrics, traces, timeouts, circuit breakers, and graceful degradation.

See you there.
