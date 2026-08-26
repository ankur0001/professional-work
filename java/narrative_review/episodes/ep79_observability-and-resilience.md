# Episode 79 — Observability and Resilience

| Field | Value |
|---|---|
| Episode | 79 |
| Title | Observability and Resilience |
| Catalog handbook column | 79 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Seventy-Eight admitted the network is unreliable. That admission is useless without two capabilities: you must see what the system is doing, and you must survive when a dependency fails. If you cannot see it and cannot survive dependency failure, you are not production-ready — you are hosted.

Observability rests on three pillars that answer different questions. Logs tell stories about particular requests and errors. Metrics tell aggregate truths — rates, saturations, latencies, error percentages. Traces show a request's path across services so "slow checkout" becomes "inventory took 800ms." Emit metrics for latency and errors; propagate a trace id across hops. Without correlation, you have three museums instead of one investigation.

Resilience begins with a blunt rule: set timeouts. Unbounded waits become outages. A dependency that never answers should not hold your threads forever — platform threads or virtual threads, the product still stalls. Retries need jitter and idempotency. Blind retries amplify an outage into a retry storm that finishes the dependency off. Circuit breakers stop calling a sick dependency for a cool-down so your service can fail fast and recover when the dependency returns. Bulkheads isolate pools so one integration cannot exhaust the whole process.

```java
// pseudo: call dependency with timeout + retry + circuit breaker
// emit metrics for latency/errors; propagate trace id
```

SLOs drive alerts. Alerting on raw CPU because it is easy produces pages nobody respects. Alert on error budget burn and latency percentiles that users feel. Dashboards should answer questions: is user success healthy, which dependency hurts, are we near a limit?

Misunderstandings cluster. Retry storms from unbounded retries without backoff. No timeouts anywhere. Alerts on CPU instead of SLOs. Each one feels like diligence until the night it pages uselessly or fails to page at all.

First resilience rule in an interview? Set timeouts; unbounded waits become outages. Then mention retries with jitter plus idempotency, circuit breakers, and SLO-based alerts so the answer sounds like a system, not a single flag.

Make the timeout story concrete. An HTTP client defaults to infinite or absurdly long waits. Under dependency slowness, your threads pile up, your queue grows, your own health check fails, and the platform kills you — even though your code was "fine." Explicit timeouts on every remote call, including DNS and connection establishment, turn an unbounded risk into a bounded error you can handle.

Retries without idempotency double-charge cards and double-create orders. Retries without jitter synchronize thundering herds after an outage. Circuit breakers without metrics are guesswork; open the circuit based on error rates and latency, half-open carefully, and alert when circuits stay open.

Logs, metrics, and traces need cardinality discipline. A metric label for every user id will explode your monitoring bill and drown signal. Trace sampling strategies matter at high QPS. Structured logs with correlation ids beat novel-length unstructured dumps.

SLO-driven alerts change culture. Page on symptoms users feel — high error rate, high p99 — and use CPU as a diagnostic detail, not a primary pager. Runbooks linked from alerts close the loop so a page includes the next action.

If you cannot see it and cannot survive dependency failure, you are not production-ready — keep that sentence as the episode's spine when architecture interviews ask what "operable" means.

Correlate metrics with dumps when the problem is a single JVM — Episode Fifty-Eight's lesson still applies inside each microservice. Traces get you to the guilty service; thread dumps and JFR finish the diagnosis inside that process. Observability is layered: system graph first, process toolkit second.

Circuit breakers need clear fallbacks. Returning a cached read may be fine; returning a silent success for a write is not. Decide fallback semantics per use case. Retries belong on idempotent reads and carefully keyed writes — never on non-idempotent POSTs without keys.

SLOs drive alerts only if SLOs are real. Copy-pasted "three nines" without traffic math creates either constant pages or never pages. Compute error budgets from actual demand. Review budgets weekly as a product conversation, not only as an ops ritual.

Timeouts everywhere includes message consumers, database calls, and DNS. Partial stacks with one unbounded call undo the rest of your resilience work. First resilience rule stays: set timeouts; unbounded waits become outages. Build the rest of the toolkit on that floor.

Walk an incident with the toolkit. Checkout p99 rises. The dashboard shows inventory latency rising. A trace confirms time in the inventory client. Inventory's metrics show DB pool exhaustion. Inventory's thread dump shows threads waiting on connections. Timeout on the checkout-to-inventory call saved checkout from total collapse, but the circuit breaker should have opened earlier — the alert on inventory error budget was missing. That story uses logs, metrics, traces, timeouts, and SLOs together. Resilience without observability is flying blind; observability without resilience is watching the crash in high definition.

Retry storms deserve a numeric picture. One hundred pods retrying a sick dependency ten times with no jitter can produce a synchronized thundering herd exactly when the dependency tries to recover. Exponential backoff with jitter turns a stampede into a trickle. Idempotency turns a trickle of duplicates into safe no-ops.

Set timeouts; retries with care; break circuits; alert on SLOs — that is the spoken checklist to take into architecture interviews and on-call rotations alike.

Seeing and surviving make distribution operable. Next we wrap architecture talk for interviews: trade-offs under constraints, with JVM awareness in the story. Episode Eighty.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Observability and Resilience (Episode 79).

Narration technique: network admission → see + survive thesis → logs/metrics/traces → timeouts/retries/circuits → SLOs → misconceptions → interview woven → bridge to architecture wrap.

Teaching points preserved: logs/metrics/traces; timeouts; retries with jitter+idempotency; circuit breakers; SLOs drive alerts.
