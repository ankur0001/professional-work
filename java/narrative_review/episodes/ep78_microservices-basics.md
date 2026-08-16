# Episode 78 — Microservices Basics

| Field | Value |
|---|---|
| Episode | 78 |
| Title | Microservices Basics |
| Catalog handbook column | 78 |
| Narration source script | `make_episode_78.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Seven covered testing Spring apps from unit to containers.
2. Architecture interviews often jump next — should this be microservices?
3. Microservices are independently deployable services collaborating over the network.
4. They buy team autonomy and scale axes — they cost operational complexity.
5. The wrong split creates a distributed monolith — worst of both worlds.
6. Today — when to split, boundaries, communication, data, and failure modes.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Eight.
2. Microservices Basics.

### Scene `when_split` (renderer: `when_split`)

1. Split when forces demand it — not for fashion.
2. Independent deploy cadence across teams is a real force.
3. Different scale or technology needs per subdomain.
4. Strong module boundaries already exist — services formalize them.
5. If one team owns everything and deploys weekly together — a modular monolith may win.
6. Start cohesive — extract services when pain is measured, not imagined.

### Scene `boundaries` (renderer: `boundaries`)

1. Boundaries follow business capabilities — not technical layers.
2. Think Order Service and Payment Service — not Controller Service and Repository Service.
3. Domain-driven contexts help — a bounded context is a candidate service.
4. Avoid chatty cross-service calls inside one user request when possible.
5. Shared libraries for DTOs can couple release trains — version carefully.
6. Clear ownership beats perfect purity — every service needs an owning team.

### Scene `communication` (renderer: `communication`)

1. Communication styles define failure shapes.
2. Synchronous HTTP or gRPC — simple mental model, tight runtime coupling.
3. Asynchronous messaging — Kafka or queues — temporal decoupling, harder flows.
4. Idempotency keys matter when at-least-once delivery retries.
5. Timeouts, retries, and backoff are part of the interface contract.
6. Prefer async for fan-out and sync for queries that must return now.

### Scene `data` (renderer: `data`)

1. Data ownership is the hard part of microservices.
2. Each service owns its database — no shared tables across services.
3. Cross-service joins become APIs or materialized read models.
4. Sagas or outbox patterns coordinate multi-service changes.
5. Dual writes without a pattern are how distributed inconsistency starts.
6. Eventual consistency is a product decision — set user expectations.

### Scene `cost` (renderer: `cost`)

1. Operational cost you must budget for.
2. More deployables — more pipelines, dashboards, and on-call surfaces.
3. Distributed tracing and correlation IDs become mandatory.
4. Local development needs compose files or remote stubs.
5. Network latency and partial failure replace in-process method calls.
6. If you cannot operate it, you do not have microservices — you have hope.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — splitting by technical layer — distributed presentation and data tiers.
3. Two — shared database across services — invisible coupling at the schema.
4. Three — chatty sync chains — one click fans into a latency hairball.
5. Also — no idempotency — retries create double charges and duplicate rows.
6. Architecture must match team and ops maturity — not a conference talk.

### Scene `interview` (renderer: `interview`)

1. Interview question — monolith or microservices for a new product?
2. Default to a modular monolith until deploy or scale forces argue otherwise.
3. Define domain boundaries first — extract services along those lines later.
4. Budget for observability, CI, and on-call before multiplying deployables.
5. Call out data ownership and consistency model explicitly.
6. Optimize for change — pick the shape that lets the team ship safely.

### Scene `teaser` (renderer: `teaser`)

1. Distributed systems fail in partial ways — next we harden them.
2. Episode Seventy-Nine — Observability and Resilience.
3. Logs, metrics, traces, timeouts, circuit breakers, and graceful degradation.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **78** — *Microservices Basics*.
- **Series catalog:** Episode 78 ↔ handbook lesson 78 — *Microservices Basics*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Seven covered testing Spring apps from unit to containers._
- **`title`** — starts from: _Episode Seventy-Eight._
- **`when_split`** — starts from: _Split when forces demand it — not for fashion._
- **`boundaries`** — starts from: _Boundaries follow business capabilities — not technical layers._
- **`communication`** — starts from: _Communication styles define failure shapes._
- **`data`** — starts from: _Data ownership is the hard part of microservices._
- **`cost`** — starts from: _Operational cost you must budget for._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — monolith or microservices for a new product?_
- **`teaser`** — starts from: _Distributed systems fail in partial ways — next we harden them._
