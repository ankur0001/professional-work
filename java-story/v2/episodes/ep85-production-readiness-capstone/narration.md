# Episode 85 — Production Readiness Capstone

| Field | Value |
|---|---|
| Episode | 85 |
| Title | Production Readiness Capstone |
| Catalog handbook column | 85 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We began with why Java exists and how a hello world runs on a JVM. We walked language, APIs, concurrency, the JVM's memory and execution machinery, design vocabulary, Spring, and distributed systems. The last question is not another feature. It is whether you would sleep the night after shipping. Production-ready means observable, recoverable, capacity-tested, and owned — not merely running.

```text
// checklist: SLO, dashboard, alert, runbook, rollback, load test, dependency timeouts
```

Observable means you can explain a bad minute with metrics, traces, and logs — and that the JVM toolkit from earlier episodes is reachable when the bad minute is a heap climb or a stuck thread. Recoverable means timeouts, retries done safely, circuit breakers, and a rollback you have rehearsed. Capacity-tested means load tests that look like production and SLOs you actually measure — you know the RPS at which p99 breaks and what you will do. Owned means names on runbooks and pages, not a distribution list nobody reads. A perfect dashboard with no human who can roll back is decoration. A runbook that has never been exercised in a game day is fiction.

SLOs and alerts come first. What does healthy mean in user terms, and who gets paged when error budgets burn? Write alerts in the language of user pain and attach the runbook link in the page itself. Review noisy alerts like flaky tests — fix or delete. Dashboards that answer questions beat vanity charts: is success rate healthy, which dependency hurts, are we near saturation? Three panels may be enough for a small service; more panels can wait until a question appears that they answer.

Rollback plan before deploy: can you revert quickly when the new version lies? Include database migrations — expand/contract so rollback does not require reverse mythology. Feature flags can help when coordinated with the same ownership model. Shipping without rollback turns every deploy into a one-way door. Prefer doors with handles on both sides.

Dependency limits — timeouts, bulkheads, circuit breakers — keep one slow friend from taking you down. Every added client is an added way to die. Those limits are part of the API of a good citizen service, not optional polish.

Walk a launch gate. Before traffic: SLO written, dashboard live, alert routed, runbook linked, rollback tested in staging, load test signed off, dependency timeouts set, security checks on. After traffic: watch error budgets for the first hours, keep a human near the rollback button, compare JVM and HTTP metrics to the baseline. That is production readiness as a practice, not a poster.

No owner for 3 a.m. is a management defect as much as an engineering one. Rotate ownership, compensate it, train it. Production readiness is socio-technical. The series taught mechanisms; this capstone insists on people and practice around those mechanisms. When a shiny new platform claims to make you production-ready automatically, ask it those four questions — observable, recoverable, capacity-tested, owned — and listen for silence.

This series does not end because Java ends. It ends because you now have a chain of thought: situation, problem, mechanism, evidence, trade-off. We refused syllabus dumps. We started from situations — portability pain, leaking references, cargo-cult flags, double charges on retry — and let Java's answers arrive as necessities. Carry that method into frameworks we never named and into systems you will invent. The final test remains: if you remove the headings, does your explanation still sound like one engineer thinking with a teammate? If yes, you learned the real curriculum.

There is no Episode Eighty-Six bridge. Your bridge is the next production system you touch. Take the chain of thought with you — situation, problem, question, mechanism, evidence, trade-off — and the Java Story keeps teaching after the narration ends. Welcome to building and operating Java systems with eyes open.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Production Readiness Capstone (Episode 85).

Narration technique: series arc callback → production-ready thesis → checklist/launch gate → ownership → series close (no next-episode bridge).

Teaching points preserved: SLOs/alerts; dashboards that answer questions; rollback; dependency limits; runbooks/ownership.
