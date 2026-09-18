# Episode 112 — Production Case Studies

| Field | Value |
|---|---|
| Episode | 112 |
| Title | Production Case Studies |
| Phase | Phase 12 — Enterprise Architecture |
| Catalog handbook lesson | 112 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Theory becomes judgment when traffic, legacy schemas, and on-call rotations enter the room. This last episode is not a new framework feature. It is three condensed case studies that force you to pick from everything this series taught — IoC and Boot, MVC and data, security and cloud, tests, observability, and architecture — and leave you with a synthesis you can reuse on Monday.

### Case 1 — Checkout latency without a villain

A retail checkout API met its error SLO and missed its latency SLO. The team’s first proposal was "move to WebFlux." Grafana showed HTTP p99 high; the payment timer from Micrometer was fine; OpenTelemetry showed ten sequential inventory spans per cart. The fix was a batch reserve endpoint and a single span — Episode 103’s lesson. Heap and GC were innocent. Architecture diagrams did not need redrawing. Evidence beat fashion.

Takeaway: instrument business hops, read the trace before changing programming models, optimize the algorithm that the spans reveal.

### Case 2 — The god service that could not test payments

A monolith package named `service` imported web DTOs, JPA entities, and Stripe’s SDK into one class. Unit tests booted half of Spring. The team carved a hexagonal slice around payment and order placement: `PlaceOrderUseCase` in the core, MVC and Stripe adapters outside, ArchUnit guarding imports. They did not rewrite the admin CRUD screens. Payment rules became testable with fakes; production wiring stayed Boot’s job.

Takeaway: ports and adapters where change and risk concentrate; layered pragmatism elsewhere; dependency direction over folder cosmetics.

### Case 3 — Support screens choking the write model

Customer support queries joined orders, shipments, and loyalty live against normalized write tables under row locks from authorize/capture. The team introduced mild CQRS: `order_support_view` updated after commit from `OrderAuthorized` and `OrderShipped`, query controller separate from command controller. They added Prometheus gauges on projection lag. When lag spiked, on-call checked the projector before blaming Postgres primary CPU alone.

Takeaway: separate read models when screens and invariants diverge; emit domain events you can project; observe the projection itself.

### Synthesis — a working order of attack

When a Spring system hurts, walk a deliberate path instead of grabbing a buzzword:

1. **See** — Actuator, Micrometer, Prometheus, Grafana, traces. If you cannot see it, you cannot rank it.
2. **Stabilize** — readiness probes, timeouts, pools, memory bounds, graceful shutdown. Survive the week.
3. **Simplify the hot path** — fix N+1, batch chatty calls, cache only with hit metrics.
4. **Draw boundaries** — layers first; hex/clean rings where frameworks invade the core; DDD where language and invariants are rich.
5. **Decouple in time** — events and outbox when sync fan-out couples availability.
6. **Split read/write** — CQRS when one model cannot serve both honesty and screens.
7. **Prove** — tests at the right layer, contracts between services, dashboards and alerts as part of the change.

Spring’s through-line across the catalog is unchanged from Episode 01: keep business logic in POJOs you can reason about; let the container and ecosystem handle assembly, infrastructure, and cross-cutting concerns. Boot accelerates the outer rings. Cloud patterns and messaging address multi-service reality. Observability closes the feedback loop so architecture debates meet production numbers.

### What you should be able to do now

Explain why a bean is created and where a request enters `DispatcherServlet`. Choose JPA fetch strategies with SQL evidence. Secure a resource with the filter chain you can narrate. Test slices without booting the world. Scrape meters, find a slow span, and decide whether the next move is a pool change, a port/adapter carve-out, or a read model. That combination — mechanism plus judgment — is the series’ real deliverable.

There is no Episode 113 waiting behind a curtain. The next lesson is the system you own: pick one bottleneck, name the Spring mechanism that addresses it, measure before and after, and keep the dependency arrows pointing toward the domain. The handbook ends here; the work does not.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 112 (*Production Case Studies*).

Narration technique: three production case studies → numbered synthesis → Spring through-line back to Episode 01 → capability checklist → series close without a fake next episode.
