# Episode 84 — Performance Playbook

| Field | Value |
|---|---|
| Episode | 84 |
| Title | Performance Playbook |
| Catalog handbook column | S2 |
| Narration source script | `make_episode_84.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Eighty-Three covered event-driven flows and the transactional outbox.
2. Performance work without a method becomes random tuning theater.
3. Users feel latency percentiles — not average CPU on a quiet afternoon.
4. Java gives you JFR, async profilers, GC logs, and Micrometer — use them.
5. Fix the hottest path first — then re-measure.
6. Today — a performance playbook from symptom to verified fix.

### Scene `title` (renderer: `title`)

1. Episode Eighty-Four.
2. Performance Playbook.

### Scene `measure` (renderer: `measure`)

1. Start with measurement — never with a hunch.
2. Define the SLO — p95 latency, error rate, throughput under load.
3. Reproduce with realistic data volumes and concurrency.
4. Capture RED metrics — rate, errors, duration — per endpoint.
5. Add traces for the slow requests — see where time goes.
6. Without a baseline, you cannot claim an improvement.

### Scene `find` (renderer: `find`)

1. Find the bottleneck before changing code.
2. CPU-bound — profile methods — hot loops, JSON, crypto, regex.
3. IO-bound — watch DB time, remote calls, thread pool waits.
4. Allocation pressure — GC logs and allocation profilers tell the story.
5. Lock contention — thread dumps and JFR synchronization events.
6. One primary bottleneck at a time — resist shotgun refactors.

### Scene `fix_app` (renderer: `fix_app`)

1. Application-level fixes that often win.
2. Cut N-plus-one queries — fetch joins or DTO projections.
3. Cache correct hot reads — with invalidation from Episode Eighty-One.
4. Shrink payloads — less JSON, fewer columns, pagination.
5. Reuse connections and HTTP clients — connection setup is not free.
6. Move heavy work off the request thread — async or queues when product allows.

### Scene `fix_runtime` (renderer: `fix_runtime`)

1. Runtime and platform levers.
2. Size heaps and pick collectors from GC evidence — Episode Sixty-Two.
3. Tune thread and pool sizes to measured concurrency — not folklore.
4. Warm up JIT before load tests that claim peak performance.
5. Watch container CPU throttling — limits can fake a slow app.
6. Native images and AOT help startup — steady-state still needs profiling.

### Scene `verify` (renderer: `verify`)

1. Verify like a scientist.
2. One change, then re-run the same load scenario.
3. Compare p95 and p99 — not only averages.
4. Watch error rate — a faster endpoint that five-hundreds is not a win.
5. Keep a short performance note — what changed, what improved.
6. Automate a smoke performance check in CI for critical paths when feasible.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — optimizing before measuring — classic premature work.
3. Two — load testing with tiny datasets — missing real index and GC behavior.
4. Three — celebrating mean latency while p99 burns.
5. Also — changing five knobs at once — no attribution.
6. Method beats folklore — every time.

### Scene `interview` (renderer: `interview`)

1. Interview question — an endpoint's p99 doubled after a release — what do you do?
2. Confirm blast radius — which endpoint, since when, which region.
3. Compare metrics and traces before versus after the deploy.
4. Profile or pull JFR — classify CPU, IO, GC, or lock wait.
5. Fix the top offender — re-measure under the same load.
6. Ship with a rollback plan — performance incidents need escape hatches.

### Scene `teaser` (renderer: `teaser`)

1. Speed is one production virtue — readiness is the checklist.
2. Episode Eighty-Five — Production Readiness Capstone.
3. The Season Two finale — ship checklist and staff-level wrap.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Episode 84** is a **Season 2 production-systems bonus** track. It is **not** one of the handbook’s 80 lessons.
- Topic framing for the video: **Performance Playbook** (continuity after Episode 80’s architecture interview wrap).
- Narration was **original written for the video** (scene-synced beats), not copied verbatim from the handbook.
