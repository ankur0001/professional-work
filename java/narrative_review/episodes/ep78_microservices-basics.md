# Episode 78 — Microservices Basics

| Field | Value |
|---|---|
| Episode | 78 |
| Title | Microservices Basics |
| Catalog handbook column | 78 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Your Spring monolith ships. Teams grow. Deploys queue behind each other. One noisy feature takes the whole process down. Someone says the word: microservices. That word is not a trophy. Microservices are a scalability and organization choice — and distributed failure is the price of admission. If you cannot name the organizational or scale problem you are solving, you are not ready to pay that price.

Start with boundaries by business capability. Orders are not "the database layer" and "the web layer" split into two repos that still share one schema and must deploy together. That split is a distributed monolith: network latency with none of the independence. Service A owns orders; Service B owns inventory. They communicate through APIs or events — not by reaching into each other's tables.

```java
// Service A owns orders; Service B owns inventory
// Communicate via API/events — not shared DB tables
```

Independent deployability is the test. Can the orders team release on Tuesday without a coordinated inventory release, as long as contracts hold? If every change still needs a lockstep release train, you have multiplied repos without multiplying autonomy. Data ownership follows the same honesty: each service owns its persistence. Shared databases feel convenient and couple you silently.

The network is unreliable. Calls time out, retry, duplicate, arrive reordered. What was a method call in a monolith becomes a failure mode you must design for. Ignoring observability in that world is negligence — you cannot debug a graph of services with stdout on one laptop. Later episodes will deepen resilience and events; today you need the humility: distribution makes everything harder on purpose, in exchange for team and scale leverage you must actually need.

Modular monolith first often wins. Keep module boundaries inside one deployable until the boundaries hurt for real — separate release cadence, separate scaling, separate failure isolation. Splitting by technical layers only — "controllers service," "service service," "repository service" — usually fails. Split where the business language already splits.

When not microservices? Small team, simple domain, early product — a modular monolith may win on focus and operability. Say that in interviews without embarrassment. Then say what would change your mind: independent scaling of a hotspot, team autonomy blocked by a single release train, or a clear bounded context ready to isolate.

Independent deployability deserves a sharper test than repo count. Two services that must change a shared library and a shared database migration in lockstep are one system wearing two costumes. Contracts — versioned APIs, consumer-driven tests, or event schemas — are what make independence real. Without contract discipline, microservices become a distributed waterfall.

Data ownership fights a common shortcut: the shared "reporting" schema everyone writes to. Reporting needs can be served by events, read replicas owned carefully, or a dedicated analytics pipeline that consumes facts. Crossing into another service's tables to "just join" recreates the monolith's coupling with weaker transactions.

Organizational scaling is a valid reason to split — Conway's law is not a joke — but only when teams already struggle to ship inside one codebase with clear modules. If one team owns everything, microservices mainly add operational tax. Fit the architecture to the org and the domain stage.

Network unreliability shows up as partial failure: inventory succeeded, billing timed out, the user clicked again. Idempotency and correlation ids are not optional extras; they are the price of distribution. Observability, next episode, is how you see those partial failures instead of guessing.

When someone sells microservices as the default for every Java shop, ask what modular monolith option was tried and what metric proved it insufficient. That question alone prevents entire classes of premature distribution.

Return to the monolith morning that started this episode. Deploys queue because every feature shares one release train. That organizational friction can justify extraction even before traffic demands it — if the domain boundary is real. Extract the inventory context behind an API, give it its own database, and keep the orders service talking through a client with timeouts. Measure whether deploy frequency actually rises. If it does not, you paid the network tax for nothing and should reconsider the cut.

Distributed failure is not only total outage. It is slow dependency, stale cache, duplicated request, and clock skew between nodes. Designing for those modes from day one is cheaper than bolting them on after the first major incident. That is why the next episode exists immediately after this one: observability and resilience are not "phase two." They are part of the microservice definition if you are honest.

Splitting by technical layers only creates chatty services: a "controller service" calling a "logic service" calling a "data service" for one user click. Prefer vertical slices of business capability that can answer meaningful requests with minimal synchronous fan-out. When fan-out is required, budgets and bulkheads become first-class.

Modular monolith first often means packages or Gradle modules with enforced boundaries, not a wish and a wiki diagram. Architecture fitness functions and code ownership inside one deployable train teams for the day a real split is needed. Microservices then become a relocation of an existing boundary, not an invention under panic.

One closing caution: microservices multiply JVM processes, each with its own heap, GC, metaspace, and startup profile. Everything from Episodes Fifty-Six through Sixty-Five becomes a fleet concern. If you cannot operate one JVM well, operating thirty will not teach you by magic — it will page you in parallel.

Microservices without visibility and without timeouts become a slower monolith with worse nights. Episode Seventy-Nine is observability and resilience — how you see the system and how you survive dependency failure.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Microservices Basics (Episode 78).

Narration technique: monolith pain → trade-off thesis → capability boundaries + code comment → independent deploy/data ownership → network unreliability → modular monolith first → interview woven → bridge to observability.

Teaching points preserved: boundaries by capability; independent deployability; network unreliable; data ownership; modular monolith first often.
