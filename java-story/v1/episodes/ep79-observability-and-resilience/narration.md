# Episode 79 — Observability and Resilience

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Eight framed microservices — boundaries, data, and operational cost. Distributed systems do not fail cleanly — they fail partially and intermittently. Observability tells you what is happening — resilience limits blast radius.

Without both, on-call becomes guesswork and cascading outages. Spring Boot Actuator, Micrometer, and Resilience4j show up in many stacks. Today — logs, metrics, traces, timeouts, and circuit breakers.

Episode Seventy-Nine. Observability and Resilience. Three observability pillars — use them together. Logs — event narratives with correlation IDs across services. Metrics — RED and USE signals — rate, errors, duration, saturation.

Traces — request paths across process boundaries via spans. OpenTelemetry is becoming the portable instrumentation layer. If you cannot answer why latency spiked, your pillars have gaps.

Spring Boot operations surface. Actuator health endpoints feed load balancers and orchestrators. Micrometer binds timers and counters to Prometheus or similar backends. Structured JSON logs beat free-text grepping under load.

Propagate trace and span IDs on every outbound call. Alert on symptoms users feel — error rate and latency — not only CPU. Resilience starts with timeouts and limits. Every remote call needs a timeout — infinite waits hold threads hostage.

Bulkheads isolate pools so one dependency cannot starve others. Rate limits protect you from stampeding clients and buggy loops. Retries need jitter and budgets — blind retries amplify outages.

Idempotent APIs make safe retries possible — design for them. Circuit breakers stop calling a sick dependency. Closed — calls flow — open — fail fast — half-open — probe recovery. Resilience4j integrates cleanly with Spring Boot.

Combine with fallbacks — cached responses or degraded features. Failing fast is kinder than queueing until thread pools die. Tune thresholds from real SLOs — not copy-pasted defaults forever.

Graceful degradation is a product skill. Show partial results when recommendations are down — still take checkout. Feature flags shut off expensive paths during incidents. Read-only mode can save a write-path outage from becoming total failure.

Document dependency criticality — which outages are SEV-one. Practice game days — resilience untested is resilience imagined. Three common mistakes. One — logs without correlation IDs — cannot stitch a single request.

Two — retries without backoff — turn a blip into a self-DDoS. Three — health checks that always return up while the DB is down. Also — paging on raw CPU — ignore saturation of thread pools and queues.

Observe what users feel — defend what users need. Interview question — how do you keep a distributed Spring system reliable? Instrument logs, metrics, and traces with correlation across services.

Timeout every dependency — bulkhead and rate-limit shared resources. Circuit-break sick calls — degrade features instead of failing entirely. Alert on SLOs — error rate and latency — with runnable runbooks.

Prove it with load tests and failure injection, not slideware. The platform story is complete — next we wrap the interview arc. Episode Eighty — Architecture Interview Wrap. How to structure system-design answers using everything from this series.

See you in the finale.
