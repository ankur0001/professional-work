# Episode 85 — Production Readiness Capstone

**Cut:** v1 (original)

## Transcript (from captions)

Episode Eighty-Four gave a performance playbook from symptom to fix. Shipping is not merging — production readiness is a deliberate gate. Season Two ends with a checklist staff engineers actually use.

Security, data, ops, and rollback belong in the same conversation. Interviews love candidates who think past the happy-path demo. Today — the production readiness capstone for The Java Story Season Two.

Episode Eighty-Five. Production Readiness Capstone. A practical readiness checklist. SLOs defined — latency, availability, freshness where it matters. Dashboards and alerts with runnable runbooks — not vanity graphs.

Authn, authz, secrets, and dependency upgrades on a cadence. Backups, migrations, and a tested rollback or forward-fix path. Load and failure tests for the hottest user journeys. Release engineering that reduces fear.

Small, reversible deploys — feature flags for risky paths. Canaries and health probes before full traffic. Migrations expand then contract — never lock the fleet on a long DDL. Config changes are releases — review them like code.

If you cannot roll back, you have not finished the design. On-call is part of architecture. Every critical dependency has an owner and an alert. Pages should be rare, actionable, and tied to user impact.

Incident reviews blame process and design — not the person awake at three. Game days practice breaker and degrade paths from Episode Seventy-Nine. Handoffs need written context — tribal knowledge pages the wrong people.

Staff-level interview lens — connect the whole series. Language and JVM — correct and efficient under load. Spring platform — IoC, Boot, data, security, tests. Distributed design — boundaries, events, caches, APIs.

Operate what you propose — observe, degrade, recover. Judgment — boring operable designs beat clever fragile ones. Capstone narrative — launch a payments-backed checkout. Clarify consistency for money — strong where it counts.

Sync authorize payment — async notify fulfillment via outbox. Cache catalog reads — never cache ledger balances casually. Secure APIs, trace every request, break circuits on payment timeouts.

Ship behind a flag — canary, watch SLOs, keep a rollback. Three common mistakes. One — calling a demo production — no alerts, no rollback. Two — toil-heavy on-call — noisy pages nobody can act on.

Three — architecture slides without a migration or data plan. Also — ignoring security until the week before launch. Readiness is continuous — not a single checkbox meeting. Final interview framing — are you production-ready?

State SLOs, risks, and the hottest user journey. Explain auth, data ownership, and failure modes briefly. Describe how you will observe, alert, and roll back. Name what you would not build yet — scope is judgment.

That is the Season Two standard — ship with eyes open. Season Two complete — production systems from cache to readiness. The Java Story now spans handbook plus production bonus track.

Rebuild any episode from its script when you need a refresher. Go ship something measurable — and operate it well.
