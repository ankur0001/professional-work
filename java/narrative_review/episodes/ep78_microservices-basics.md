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

Independent deployability is the test. Can the orders team release on Tuesday without a coordinated inventory release, as long as contracts hold? Two services that must change a shared library and a shared database migration in lockstep are one system wearing two costumes. Contracts — versioned APIs, consumer-driven tests, or event schemas — make independence real. Data ownership follows the same honesty: each service owns its persistence. The shared "reporting" schema everyone writes to couples you silently; serve reporting via events, careful read replicas, or a dedicated analytics pipeline.

The network is unreliable. Calls time out, retry, duplicate, arrive reordered. What was a method call in a monolith becomes a failure mode you must design for. Partial failure is the everyday case: inventory succeeded, billing timed out, the user clicked again. Idempotency and correlation ids are not optional extras. Ignoring observability in that world is negligence — you cannot debug a graph of services with stdout on one laptop.

Modular monolith first often wins. Keep module boundaries inside one deployable until the boundaries hurt for real — separate release cadence, separate scaling, separate failure isolation. That often means packages or Gradle modules with enforced boundaries, not a wish and a wiki diagram. Splitting by technical layers only — "controller service" calling "logic service" calling "data service" — creates chatty services with none of the autonomy. Prefer vertical slices of business capability that can answer meaningful requests with minimal synchronous fan-out.

Organizational scaling is a valid reason to split — Conway's law is not a joke — but only when teams already struggle to ship inside one codebase with clear modules. If one team owns everything, microservices mainly add operational tax. When not microservices? Small team, simple domain, early product — a modular monolith may win on focus and operability. Say that in interviews without embarrassment. Then say what would change your mind: independent scaling of a hotspot, team autonomy blocked by a single release train, or a clear bounded context ready to isolate.

Return to the monolith morning. Deploys queue because every feature shares one release train. That organizational friction can justify extraction even before traffic demands it — if the domain boundary is real. Extract the inventory context behind an API, give it its own database, keep orders talking through a client with timeouts. Measure whether deploy frequency actually rises. If it does not, you paid the network tax for nothing.

One closing caution: microservices multiply JVM processes, each with its own heap, GC, metaspace, and startup profile. Everything from Episodes Fifty-Six through Sixty-Five becomes a fleet concern. If you cannot operate one JVM well, operating thirty will not teach you by magic — it will page you in parallel.

Microservices without visibility and without timeouts become a slower monolith with worse nights. The next pressure is observability and resilience — how you see the system and how you survive dependency failure.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Microservices Basics (Episode 78).

Narration technique: monolith pain → trade-off thesis → capability boundaries → independent deploy/data ownership → network unreliability → modular monolith first → bridge to observability.

Teaching points preserved: boundaries by capability; independent deployability; network unreliable; data ownership; modular monolith first often.
