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

Theory becomes judgment when trucks, legacy berth schemas, and on-call rotations enter the room. This closing episode is not a new framework feature. It is three condensed postmortems that force you to pick from everything this series taught — IoC and Boot, MVC and data, security and cloud, tests, observability, and architecture — and leave you with a synthesis you can reuse on Monday.

### Case 1 — Gate latency without a villain

A harbor gate API met its error SLO and missed its latency SLO. The first proposal was “move gate to WebFlux.” Grafana showed HTTP p99 high; the `harbor.gate.release.duration` timer was elevated; OpenTelemetry showed ten sequential billing quote spans per multi-container truck. The fix was a bulk quote endpoint and a single span — evidence from the performance episode, not a programming-model fashion. Heap and GC were innocent. Architecture diagrams did not need redrawing.

Takeaway: instrument business hops, read the trace before changing stacks, optimize the algorithm the spans reveal.

### Case 2 — The god service that could not test release

A monolith package named `service` imported web DTOs, JPA entities, and the billing Feign client into one class. Unit tests booted half of Spring. The team carved a hexagonal slice around gate release: `ReleaseGateUseCase` in the core, MVC and Feign adapters outside, ArchUnit guarding imports. They did not rewrite every admin CRUD screen. Release rules became testable with a fake `BillingPort` and `DutyProvider`; production wiring stayed Boot’s job.

Takeaway: ports and adapters where change and risk concentrate; layered pragmatism elsewhere; dependency direction over folder cosmetics.

### Case 3 — Schedule board choking the write model

Operator boards joined berth reservations, vessel names, and billing state live against normalized write tables under row locks from `reserve`. The team introduced mild CQRS: `schedule_board_view` updated after commit from `BerthReserved`, query controller separate from command controller. They added a Prometheus gauge on projection lag. When lag spiked, on-call checked the projector before blaming Postgres primary CPU alone.

Takeaway: separate read models when screens and invariants diverge; emit domain events you can project; observe the projection itself.

### Synthesis — a working order of attack

When a Spring harbor system hurts, walk a deliberate path instead of grabbing a buzzword:

1. **See** — Actuator, Micrometer, Prometheus, Grafana, traces. If you cannot see it, you cannot rank it.
2. **Stabilize** — readiness probes, timeouts, pools, memory bounds, graceful shutdown. Survive the week.
3. **Simplify the hot path** — fix N+1, batch chatty Feign calls, cache only with hit metrics.
4. **Draw boundaries** — layers first; hex/clean rings where frameworks invade the core; DDD where language and invariants are rich (`Berth`, gate release).
5. **Decouple in time** — `BerthReserved` and outbox when sync fan-out couples availability.
6. **Split read/write** — CQRS when one model cannot serve both honesty and the schedule board.
7. **Prove** — JUnit and Mockito at the tariff core, slices for gate controllers, Testcontainers for `VesselRepository`, contracts for gate↔billing, dashboards and alerts as part of the change.

Spring’s through-line across the catalog is unchanged from the opening lesson: keep business logic in POJOs you can reason about; let the container and ecosystem handle assembly, infrastructure, and cross-cutting concerns. Boot accelerates the outer rings. Cloud patterns and messaging address multi-service quay reality. Observability closes the feedback loop so architecture debates meet production numbers.

### What you should be able to do now

Explain why a bean is created and where a request enters `DispatcherServlet`. Choose JPA fetch strategies with SQL evidence. Secure a resource with the filter chain you can narrate. Test slices without booting the world. Scrape gate meters, find a slow span on check-in, and decide whether the next move is a pool change, a port/adapter carve-out, or a schedule-board read model. That combination — mechanism plus judgment — is the series’ real deliverable.

There is no next handbook episode waiting behind a curtain. The next lesson is the system you own: pick one bottleneck on your quay, name the Spring mechanism that addresses it, measure before and after, and keep the dependency arrows pointing toward the domain. The handbook ends here; the work does not.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 112 (*Production Case Studies*).
