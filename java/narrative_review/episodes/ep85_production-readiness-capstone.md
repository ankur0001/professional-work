# Episode 85 — Production Readiness Capstone

| Field | Value |
|---|---|
| Episode | 85 |
| Title | Production Readiness Capstone |
| Catalog handbook column | S2 |
| Narration source script | `make_episode_85.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Eighty-Four gave a performance playbook from symptom to fix.
2. Shipping is not merging — production readiness is a deliberate gate.
3. Season Two ends with a checklist staff engineers actually use.
4. Security, data, ops, and rollback belong in the same conversation.
5. Interviews love candidates who think past the happy-path demo.
6. Today — the production readiness capstone for The Java Story Season Two.

### Scene `title` (renderer: `title`)

1. Episode Eighty-Five.
2. Production Readiness Capstone.

### Scene `checklist` (renderer: `checklist`)

1. A practical readiness checklist.
2. SLOs defined — latency, availability, freshness where it matters.
3. Dashboards and alerts with runnable runbooks — not vanity graphs.
4. Authn, authz, secrets, and dependency upgrades on a cadence.
5. Backups, migrations, and a tested rollback or forward-fix path.
6. Load and failure tests for the hottest user journeys.

### Scene `release` (renderer: `release`)

1. Release engineering that reduces fear.
2. Small, reversible deploys — feature flags for risky paths.
3. Canaries and health probes before full traffic.
4. Migrations expand then contract — never lock the fleet on a long DDL.
5. Config changes are releases — review them like code.
6. If you cannot roll back, you have not finished the design.

### Scene `oncall` (renderer: `oncall`)

1. On-call is part of architecture.
2. Every critical dependency has an owner and an alert.
3. Pages should be rare, actionable, and tied to user impact.
4. Incident reviews blame process and design — not the person awake at three.
5. Game days practice breaker and degrade paths from Episode Seventy-Nine.
6. Handoffs need written context — tribal knowledge pages the wrong people.

### Scene `staff_lens` (renderer: `staff_lens`)

1. Staff-level interview lens — connect the whole series.
2. Language and JVM — correct and efficient under load.
3. Spring platform — IoC, Boot, data, security, tests.
4. Distributed design — boundaries, events, caches, APIs.
5. Operate what you propose — observe, degrade, recover.
6. Judgment — boring operable designs beat clever fragile ones.

### Scene `capstone` (renderer: `capstone`)

1. Capstone narrative — launch a payments-backed checkout.
2. Clarify consistency for money — strong where it counts.
3. Sync authorize payment — async notify fulfillment via outbox.
4. Cache catalog reads — never cache ledger balances casually.
5. Secure APIs, trace every request, break circuits on payment timeouts.
6. Ship behind a flag — canary, watch SLOs, keep a rollback.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — calling a demo production — no alerts, no rollback.
3. Two — toil-heavy on-call — noisy pages nobody can act on.
4. Three — architecture slides without a migration or data plan.
5. Also — ignoring security until the week before launch.
6. Readiness is continuous — not a single checkbox meeting.

### Scene `interview` (renderer: `interview`)

1. Final interview framing — are you production-ready?
2. State SLOs, risks, and the hottest user journey.
3. Explain auth, data ownership, and failure modes briefly.
4. Describe how you will observe, alert, and roll back.
5. Name what you would not build yet — scope is judgment.
6. That is the Season Two standard — ship with eyes open.

### Scene `teaser` (renderer: `teaser`)

1. Season Two complete — production systems from cache to readiness.
2. The Java Story now spans handbook plus production bonus track.
3. Rebuild any episode from its script when you need a refresher.
4. Go ship something measurable — and operate it well.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Episode 85** is a **Season 2 production-systems bonus** track. It is **not** one of the handbook’s 80 lessons.
- Topic framing for the video: **Production Readiness Capstone** (continuity after Episode 80’s architecture interview wrap).
- Narration was **original written for the video** (scene-synced beats), not copied verbatim from the handbook.
