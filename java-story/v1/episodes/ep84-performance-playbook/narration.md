# Episode 84 — Performance Playbook

**Cut:** v1 (original)

## Transcript (from captions)

Episode Eighty-Three covered event-driven flows and the transactional outbox. Performance work without a method becomes random tuning theater. Users feel latency percentiles — not average CPU on a quiet afternoon.

Java gives you JFR, async profilers, GC logs, and Micrometer — use them. Fix the hottest path first — then re-measure. Today — a performance playbook from symptom to verified fix. Episode Eighty-Four.

Performance Playbook. Start with measurement — never with a hunch. Define the SLO — p95 latency, error rate, throughput under load. Reproduce with realistic data volumes and concurrency.

Capture RED metrics — rate, errors, duration — per endpoint. Add traces for the slow requests — see where time goes. Without a baseline, you cannot claim an improvement. Find the bottleneck before changing code.

CPU-bound — profile methods — hot loops, JSON, crypto, regex. IO-bound — watch DB time, remote calls, thread pool waits. Allocation pressure — GC logs and allocation profilers tell the story.

Lock contention — thread dumps and JFR synchronization events. One primary bottleneck at a time — resist shotgun refactors. Application-level fixes that often win. Cut N-plus-one queries — fetch joins or DTO projections.

Cache correct hot reads — with invalidation from Episode Eighty-One. Shrink payloads — less JSON, fewer columns, pagination. Reuse connections and HTTP clients — connection setup is not free.

Move heavy work off the request thread — async or queues when product allows. Runtime and platform levers. Size heaps and pick collectors from GC evidence — Episode Sixty-Two. Tune thread and pool sizes to measured concurrency — not folklore.

Warm up JIT before load tests that claim peak performance. Watch container CPU throttling — limits can fake a slow app. Native images and AOT help startup — steady-state still needs profiling.

Verify like a scientist. One change, then re-run the same load scenario. Compare p95 and p99 — not only averages. Watch error rate — a faster endpoint that five-hundreds is not a win.

Keep a short performance note — what changed, what improved. Automate a smoke performance check in CI for critical paths when feasible. Three common mistakes. One — optimizing before measuring — classic premature work.

Two — load testing with tiny datasets — missing real index and GC behavior. Three — celebrating mean latency while p99 burns. Also — changing five knobs at once — no attribution. Method beats folklore — every time.

Interview question — an endpoint's p99 doubled after a release — what do you do? Confirm blast radius — which endpoint, since when, which region. Compare metrics and traces before versus after the deploy.

Profile or pull JFR — classify CPU, IO, GC, or lock wait. Fix the top offender — re-measure under the same load. Ship with a rollback plan — performance incidents need escape hatches.

Speed is one production virtue — readiness is the checklist. Episode Eighty-Five — Production Readiness Capstone. The Season Two finale — ship checklist and staff-level wrap. See you there.
