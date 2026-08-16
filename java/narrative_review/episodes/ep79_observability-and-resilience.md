# Episode 79 — Observability and Resilience

| Field | Value |
|---|---|
| Episode | 79 |
| Title | Observability and Resilience |
| Catalog handbook column | 79 |
| Narration source script | `make_episode_79.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Eight framed microservices — boundaries, data, and operational cost.
2. Distributed systems do not fail cleanly — they fail partially and intermittently.
3. Observability tells you what is happening — resilience limits blast radius.
4. Without both, on-call becomes guesswork and cascading outages.
5. Spring Boot Actuator, Micrometer, and Resilience4j show up in many stacks.
6. Today — logs, metrics, traces, timeouts, and circuit breakers.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Nine.
2. Observability and Resilience.

### Scene `pillars` (renderer: `pillars`)

1. Three observability pillars — use them together.
2. Logs — event narratives with correlation IDs across services.
3. Metrics — RED and USE signals — rate, errors, duration, saturation.
4. Traces — request paths across process boundaries via spans.
5. OpenTelemetry is becoming the portable instrumentation layer.
6. If you cannot answer why latency spiked, your pillars have gaps.

### Scene `actuator` (renderer: `actuator`)

1. Spring Boot operations surface.
2. Actuator health endpoints feed load balancers and orchestrators.
3. Micrometer binds timers and counters to Prometheus or similar backends.
4. Structured JSON logs beat free-text grepping under load.
5. Propagate trace and span IDs on every outbound call.
6. Alert on symptoms users feel — error rate and latency — not only CPU.

### Scene `timeouts` (renderer: `timeouts`)

1. Resilience starts with timeouts and limits.
2. Every remote call needs a timeout — infinite waits hold threads hostage.
3. Bulkheads isolate pools so one dependency cannot starve others.
4. Rate limits protect you from stampeding clients and buggy loops.
5. Retries need jitter and budgets — blind retries amplify outages.
6. Idempotent APIs make safe retries possible — design for them.

### Scene `breakers` (renderer: `breakers`)

1. Circuit breakers stop calling a sick dependency.
2. Closed — calls flow — open — fail fast — half-open — probe recovery.
3. Resilience4j integrates cleanly with Spring Boot.
4. Combine with fallbacks — cached responses or degraded features.
5. Failing fast is kinder than queueing until thread pools die.
6. Tune thresholds from real SLOs — not copy-pasted defaults forever.

### Scene `degrade` (renderer: `degrade`)

1. Graceful degradation is a product skill.
2. Show partial results when recommendations are down — still take checkout.
3. Feature flags shut off expensive paths during incidents.
4. Read-only mode can save a write-path outage from becoming total failure.
5. Document dependency criticality — which outages are SEV-one.
6. Practice game days — resilience untested is resilience imagined.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — logs without correlation IDs — cannot stitch a single request.
3. Two — retries without backoff — turn a blip into a self-DDoS.
4. Three — health checks that always return up while the DB is down.
5. Also — paging on raw CPU — ignore saturation of thread pools and queues.
6. Observe what users feel — defend what users need.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you keep a distributed Spring system reliable?
2. Instrument logs, metrics, and traces with correlation across services.
3. Timeout every dependency — bulkhead and rate-limit shared resources.
4. Circuit-break sick calls — degrade features instead of failing entirely.
5. Alert on SLOs — error rate and latency — with runnable runbooks.
6. Prove it with load tests and failure injection, not slideware.

### Scene `teaser` (renderer: `teaser`)

1. The platform story is complete — next we wrap the interview arc.
2. Episode Eighty — Architecture Interview Wrap.
3. How to structure system-design answers using everything from this series.
4. See you in the finale.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **79** — *Observability and Resilience*.
- **Series catalog:** Episode 79 ↔ handbook lesson 79 — *Observability and Resilience*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Eight framed microservices — boundaries, data, and operational cost._
- **`title`** — starts from: _Episode Seventy-Nine._
- **`pillars`** — starts from: _Three observability pillars — use them together._
- **`actuator`** — starts from: _Spring Boot operations surface._
- **`timeouts`** — starts from: _Resilience starts with timeouts and limits._
- **`breakers`** — starts from: _Circuit breakers stop calling a sick dependency._
- **`degrade`** — starts from: _Graceful degradation is a product skill._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you keep a distributed Spring system reliable?_
- **`teaser`** — starts from: _The platform story is complete — next we wrap the interview arc._
