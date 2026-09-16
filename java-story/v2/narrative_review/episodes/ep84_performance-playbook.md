# Episode 84 — Performance Playbook

| Field | Value |
|---|---|
| Episode | 84 |
| Title | Performance Playbook |
| Catalog handbook column | 84 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You have APIs, caches, events, and GC knowledge. Someone says the system is "slow." Performance is a loop: measure, hypothesize, change one thing, remeasure. Without a baseline, tuning is superstition — the same lesson as JVM flags, now applied across the stack.

Define SLOs and percentiles first. Which percentile fails under what load? p50 pride means nothing if p99 burns the error budget. Capture baseline percentiles under a load test that resembles production mix — not a synthetic hammer on one endpoint with empty caches. Include dependency percentiles, GC pause percentiles, allocation rate, and pool saturation. A single number called "latency" hides which layer moved. Label graphs with life stage: cold start versus steady state after JIT warmup — Episode Sixty-Five's distinction returns here.

```text
// 1) capture baseline percentiles
// 2) profile under load
// 3) change one variable
// 4) remeasure
```

JFR and profilers show where CPU and allocation go — under the load that violates the SLO, not at idle. Allocation and locks are frequent villains in Java services. High allocation rates drive GC pressure; hot locks show up in JFR contention events and thread dumps. Fix algorithms and contention before micro-tuning flags. Avoid premature micro-opts on cold paths — escape analysis and JIT may already help, and readability still matters. Hypothesize in mechanism language: "I think the lock on inventory reservation is contended under this SKU skew," not "I think we need more pods."

A worked loop helps. Baseline: checkout p99 is 900ms at 200 RPS. Hypothesis: inventory HTTP calls dominate. Tracing shows 700ms in the inventory client. Change: cache inventory availability with a thirty-second TTL and stampede control. Remeasure: p99 drops to 350ms, hit rate 92%, staleness acceptable per product rules. Jumping straight to rewriting JSON serialization would have optimized a cold path. Change one variable — collector flag, cache TTL, query, pool size — so results are attributable. Remeasure against the same load recipe; store load scripts beside the service like tests.

Load tests must resemble reality: cache warmth, data shape, authentication, and dependency latency. Include failure injection — dependency slow, dependency down — because resilience and speed share a budget. A test against empty tables with auth disabled will green-light fantasies.

Close with a refusal list. Refuse to tune without a baseline. Refuse to optimize code paths that traces never enter. Refuse load tests that skip auth and caches. Refuse multi-variable changes. A developer wants to switch collectors because a blog promised lower pauses — ask which percentile fails under what load, open GC logs and traces from a production-like test, and refuse if pauses are not on the critical path. The playbook protects the system from fashionable fixes.

First performance question? Which percentile or error budget fails under what load? Then profile under that load, change one variable, remeasure. When allocation dominates, ask whether the design creates too many temporary objects, whether caching helps, or whether a representation change beats micro-edits. When locks dominate, ask whether shardable state from the concurrency arc applies. Measure, hypothesize, change one thing, remeasure — that loop is the answer.

Performance readiness is necessary but not sufficient. Production readiness also means ownership, rollback, and runbooks — the socio-technical layer that decides whether a fast system stays alive at 3 a.m.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Performance Playbook (Episode 84).

Narration technique: "slow" → measure loop → SLOs/percentiles → worked checkout loop → refusal list → bridge to capstone.

Teaching points preserved: define SLOs/percentiles; JFR/profilers; allocation and locks; avoid premature micro-opts; production-like load tests.
