# Episode 80 — Architecture Interview Wrap

| Field | Value |
|---|---|
| Episode | 80 |
| Title | Architecture Interview Wrap |
| Catalog handbook column | 80 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Architecture interviews do not reward buzzword bingo. They reward trade-off stories under constraints. Someone asks you to design an order system. A weak answer sprays Kafka, Kubernetes, CQRS, and mesh until the whiteboard fills. A strong answer clarifies requirements and SLOs first — write throughput, read latency, consistency needs, team size, cost ceiling — then draws boundaries and data flow that fit those constraints.

```text
// Scaffold: requirements -> API/data -> runtime -> failures -> observability
```

Walk that scaffold as speech. Requirements and SLOs: what must never be lost, what may be eventually consistent, what percentile matters. Ask questions — interviewers reward candidates who surface constraints instead of inventing infinity. API and data: resources, ownership, sync versus async edges. Runtime as a Java engineer: JVM heap sizing, GC pause budgets, thread models, cold start if scale-to-zero. Failure modes: dependency down, duplicate messages, partial deploy. Observability: metrics, traces, alerts on SLOs. Evolve complexity: start modular, extract a service when a boundary earns independence. Stage deliberately — single region before multi-region, monolith modules before services, cache before CQRS — and name the pain each step removes.

Practice a short design aloud. "Design a URL shortener" clarifies read/write ratio, redirect latency SLO, consistency on create, and analytics needs. Maybe a modular monolith is enough at small scale. Maybe reads need caching with TTL. Maybe writes append events for analytics. JVM notes: heap for cache, GC pause budget versus redirect SLO, connection pools to the store. Failure modes: cache stampede, DB outage, duplicate short-code generation. Observability: redirect latency histogram, error rate, dependency health. That answer is coherent without naming twelve products.

Draw boundaries with words if you lack a whiteboard. "Clients hit an API gateway; the orders service owns the orders database; inventory is a separate service reached synchronously for reservation and asynchronously for restock events." Then pressure-test: gateway timeout policy, reservation idempotency, event outbox, read-your-writes needs. Each pressure-test adds a box or arrow you missed. Architecture is iterative speech, not a single perfect diagram.

Bring JVM awareness as a differentiator: you know that "just add instances" still meets GC, metaspace, and thread limits per process. If you propose caching, mention invalidation. If you propose events, mention at-least-once and idempotency. Ignoring ops — how it deploys, migrates, rolls back, and pages — is how architecture answers sound academic. A design that needs a two-hour migration with no expand/contract plan is not a senior design.

Tie this wrap to the JVM wrap from Episode Sixty-Six. Same scaffold spirit: define, mechanism, failure mode, diagnose — now scaled to systems. For "why not microservices here?" define the trade-off, explain network failure modes, name the small-team failure mode of premature distribution, and say how you would revisit with metrics on deploy friction and scaling pain. Buzzword bingo fails because follow-ups expose missing mechanisms. Trade-off stories survive follow-ups because they already admitted what hurts.

How to answer as a Java engineer? Requirements, design, JVM and runtime concerns, failure modes, observability — practice until the order is muscle memory, then let the specific domain fill the blanks. Admit trade-offs: microservices versus modular monolith, consistency versus availability, freshness versus cache hit rate.

This wrap sets you up for deeper production topics that still show up in senior conversations: caching, API contracts, events, performance loops, and readiness. Caching comes first — latency bought with correctness risk.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Architecture Interview Wrap (Episode 80).

Narration technique: buzzword vs trade-off → scaffold as continuous teaching → URL shortener rehearsal → JVM/ops awareness → bridge to caching.

Teaching points preserved: clarify requirements/SLOs; boundaries/data flow; failure modes; evolve complexity; JVM awareness.
