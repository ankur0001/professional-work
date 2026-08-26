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

Observability rests on three pillars. Logs tell stories about particular requests and errors. Metrics tell aggregate truths — rates, saturations, latencies, error percentages. Traces show a request's path across services so "slow checkout" becomes "inventory took 800ms." Emit metrics for latency and errors; propagate a trace id across hops. Without correlation, you have three museums instead of one investigation. Cardinality discipline matters: a metric label for every user id will explode your monitoring bill. Structured logs with correlation ids beat novel-length unstructured dumps.

Resilience begins with a blunt rule: set timeouts. Unbounded waits become outages. An HTTP client with absurdly long waits piles up threads under dependency slowness until your own health check fails — even though your code was "fine." Explicit timeouts on every remote call, including DNS and connection establishment, turn an unbounded risk into a bounded error. Timeouts everywhere includes message consumers and database calls; one unbounded call undoes the rest.

```java
// pseudo: call dependency with timeout + retry + circuit breaker
// emit metrics for latency/errors; propagate trace id
```

Retries need jitter and idempotency. Blind retries amplify an outage into a retry storm. One hundred pods retrying ten times with no jitter can stampede a dependency exactly when it tries to recover. Exponential backoff with jitter turns a stampede into a trickle. Retries without idempotency double-charge cards and double-create orders. Circuit breakers stop calling a sick dependency for a cool-down so your service can fail fast. They need clear fallbacks: cached reads may be fine; silent success for a write is not. Open on error rates and latency, half-open carefully, alert when circuits stay open.

SLOs drive alerts. Alerting on raw CPU because it is easy produces pages nobody respects. Alert on error budget burn and latency percentiles that users feel. Copy-pasted "three nines" without traffic math creates either constant pages or never pages. Dashboards should answer questions: is user success healthy, which dependency hurts, are we near a limit?

Walk an incident with the toolkit. Checkout p99 rises. The dashboard shows inventory latency rising. A trace confirms time in the inventory client. Inventory's metrics show DB pool exhaustion. Inventory's thread dump shows threads waiting on connections. Timeout on the checkout-to-inventory call saved checkout from total collapse, but the circuit breaker should have opened earlier — the alert on inventory error budget was missing. Traces get you to the guilty service; thread dumps and JFR from Episode Fifty-Eight finish the diagnosis inside that process. Resilience without observability is flying blind; observability without resilience is watching the crash in high definition.

First resilience rule in an interview? Set timeouts; unbounded waits become outages. Then mention retries with jitter plus idempotency, circuit breakers, and SLO-based alerts so the answer sounds like a system, not a single flag.

Seeing and surviving make distribution operable. Next we wrap architecture talk for interviews: trade-offs under constraints, with JVM awareness in the story. Episode Eighty.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Observability and Resilience (Episode 79).

Narration technique: network admission → see + survive → logs/metrics/traces → timeouts/retries/circuits → SLOs → incident walk → bridge to architecture wrap.

Teaching points preserved: logs/metrics/traces; timeouts; retries with jitter+idempotency; circuit breakers; SLOs drive alerts.
