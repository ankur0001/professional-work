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

Define SLOs and percentiles. Which percentile fails under what load? p50 pride means nothing if p99 burns the error budget. Capture baseline percentiles under a load test that resembles production mix — not a synthetic hammer on one endpoint with empty caches.

```text
// 1) capture baseline percentiles
// 2) profile under load
// 3) change one variable
// 4) remeasure
```

JFR and profilers show where CPU and allocation go. Allocation and locks are frequent villains in Java services. Avoid premature micro-opts on cold paths — escape analysis and JIT may already help hot ones, and readability still matters. Load tests that are not production-like teach false confidence.

First performance question? Which percentile or error budget fails under what load? Then profile under that load, change one variable, remeasure. Tuning without baseline, optimizing cold paths, and unrealistic load tests are the anti-patterns.

A worked loop helps. Baseline: checkout p99 is 900ms at 200 RPS. Hypothesis: inventory HTTP calls dominate. JFR or tracing shows 700ms in the inventory client. Change: cache inventory availability with a thirty-second TTL and stampede control. Remeasure: p99 drops to 350ms, hit rate 92%, staleness acceptable per product rules. That story is performance engineering. Jumping straight to rewriting JSON serialization would have optimized a cold path.

Allocation and locks reconnect to the JVM arc. High allocation rates drive GC pressure. Hot locks show up in JFR contention events and thread dumps. Fix algorithms and contention before micro-tuning flags. Avoid premature micro-opts that muddy code without profiles.

Load tests must resemble reality: cache warmth, data shape, authentication, and dependency latency. A test against empty tables with auth disabled will green-light fantasies. Include failure injection — dependency slow, dependency down — as part of performance, because resilience and speed share a budget.

First question remains which percentile fails under what load. Everything else hangs from that needle.

JFR under load is the bridge between "the service is slow" and "this method allocates" or "this lock contends." Profilers without load show startup or idle fantasies. Always profile the scenario that violates the SLO.

Change one variable — collector flag, cache TTL, query, pool size — so results are attributable. Changing five things and declaring victory teaches nothing for the next incident.

Avoid premature micro-opts also means refusing to rewrite clear code for imaginary allocations when Episode Fifty-Nine's escape analysis may already apply. Measure first. Performance playbooks that skip measurement are fashion magazines.

Define SLOs and percentiles before tools. Tools without goals produce pretty flame graphs of the wrong fire.

Expand the baseline step. Capture not only HTTP percentiles but dependency percentiles, GC pause percentiles, allocation rate, and saturation of pools and CPUs. A single number called "latency" hides which layer moved. The playbook is a differential diagnosis across the stack you have been building all series long.

Hypothesize in mechanism language: "I think the lock on inventory reservation is contended under this SKU skew," not "I think we need more pods." Pods may still be the fix after the mechanism is confirmed — but mechanism-first prevents expensive wrong scaling.

Remeasure against the same load recipe. Changing the load recipe between baseline and candidate confounds the experiment. Store load scripts beside the service like tests.

Performance is a loop. Interviews that ask how you approach slowness want that loop, not a favorite flag.

Allocation and locks connect to earlier episodes explicitly. High allocation may be real heap traffic or may be mitigated by escape analysis — profile to know. Hot locks may be safepoint-adjacent or pure contention — JFR distinguishes. The playbook reuses the diagnostic toolkit rather than inventing a parallel religion of performance.

Load tests that resemble reality include authentication, cache state, and noisy neighbors if those exist in production. Synthetic perfection is a different product.

Measure, hypothesize, change one thing, remeasure — when someone asks for your performance philosophy, that loop is the answer. Tools are how you execute steps two and sometimes three.

Close the loop with a refusal list. Refuse to tune without a baseline. Refuse to optimize code paths that traces never enter. Refuse load tests that skip auth and caches. Refuse multi-variable changes. The playbook is as much about what you will not do as about flame graphs. Which percentile fails under what load — ask it every time — then earn the next change with evidence.

A final worked refusal: a developer wants to switch collectors because a blog promised lower pauses. Ask which percentile fails under what load. Open GC logs and traces from a production-like test. If pauses are not on the critical path, refuse the change. The playbook protects the system from fashionable fixes. Measure, hypothesize, change one thing, remeasure — then ship the improvement that earned its place against the SLO.

Production-like load tests should also include a warm-up window when JIT matters, so you do not confuse cold-start behavior with steady-state SLOs — Episode Sixty-Five's distinction returns here. Label your graphs with life stage. Mislabelled graphs create wrong hypotheses and wasted flags.

When allocation dominates, ask whether the design creates too many temporary objects on the hot path, whether caching helps, or whether a representation change beats micro-edits. When locks dominate, ask whether shardable state or lock-free structures from the concurrency arc apply. The playbook ends where good engineering judgment begins: use evidence to pick the next design move, not the next superstition.

Performance readiness is necessary but not sufficient. Production readiness also means ownership, rollback, and runbooks — Episode Eighty-Five closes the series there.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Performance Playbook (Episode 84).

Narration technique: "slow" → measure loop thesis → SLOs/percentiles → profile steps → allocation/locks → misconceptions → interview woven → bridge to capstone.

Teaching points preserved: define SLOs/percentiles; JFR/profilers; allocation and locks; avoid premature micro-opts; production-like load tests.
