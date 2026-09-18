# Episode 101 — Grafana

| Field | Value |
|---|---|
| Episode | 101 |
| Title | Grafana |
| Phase | Phase 11 — Observability |
| Catalog handbook lesson | 101 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Prometheus can answer any PromQL question you type. At three in the morning nobody wants to invent the question from scratch. Grafana is where scrape data becomes a shared operational picture: panels, variables, alert rules hanging off the same queries your on-call already trusts.

Connect Grafana to Prometheus as a data source — URL of the Prometheus server, nothing Spring-specific there. Then build a dashboard around the meters you actually emit. For the checkout service from the Micrometer episode, start narrow. One row for traffic and success. One row for latency. One row for saturation. Resist the urge to paste thirty JVM panels on day one.

A practical starter layout for `checkout-service`:

| Panel | PromQL sketch | Why it exists |
|---|---|---|
| Requests in flight / rate | `sum(rate(http_server_requests_seconds_count{application="checkout-service"}[5m]))` | Are we busy? |
| Checkout success ratio | `sum(rate(checkout_succeeded_total[5m])) / sum(rate(checkout_started_total[5m]))` | Is business OK? |
| Payment p99 | `histogram_quantile(0.99, sum(rate(checkout_payment_duration_seconds_bucket[5m])) by (le))` | Where does time go? |
| JVM heap used | `jvm_memory_used_bytes{area="heap"}` | Are we near OOM? |
| Tomcat threads / DB pool | pool gauges from Boot | Are we saturated? |

Dashboard JSON in a repo beats click-ops. Export the dashboard, store it next to the service, and provision it so every environment sees the same panels. Variables for `application` and `env` keep one dashboard reusable across services that share naming conventions — which is why those Micrometer common tags mattered. A folder structure that mirrors your domain — `checkout`, `inventory`, `payments` — beats one endless list titled "Spring apps."

Walk an incident with the dashboard open. Traffic rate flat, success ratio down: look at error panels and logs. Success ratio fine, payment p99 up: open the latency row and jump to traces for that operation name. Heap climbing while latency is fine: you are early on a memory problem — Episode 104 territory — and the panel still earned its keep by showing the ramp.

Alerts belong next to panels, not in a separate tribal wiki. Example: page if payment p99 stays above two seconds for five minutes, or if success ratio drops below 0.95. Grafana can evaluate PromQL and notify Slack or PagerDuty. The skill is choosing signals that mean customer harm, not every blip on a CPU graph. Burn-rate alerts on SLOs beat "CPU > 80%" pages that train on-call to ignore noise.

Spring’s role here is upstream honesty. Grafana cannot invent a `checkout.payment.duration` timer you never registered. Bad tag cardinality makes every panel slow. Missing `application` tags make variables useless. When a panel is empty, debug in order: is the meter recorded, is `/actuator/prometheus` exposing it, is Prometheus scraping the right target, is the PromQL label matcher wrong? Units matter too — a panel that treats `_seconds` as milliseconds will invent a crisis.

A misconception is treating a pretty JVM dashboard as application observability. Heap graphs without business timers leave you knowing the GC ran while checkout failed for a different reason. Another misconception is one giant org-wide dashboard. Prefer service dashboards with a small RED/USE core — rate, errors, duration; utilization, saturation, errors — then deep-links into traces when latency spikes.

So today we turned scraped series into an operable checkout dashboard, tied alerts to the same queries, and put the burden back on good Micrometer names. Metrics answer "how much" and "how often." They still struggle with "what happened on this one request as it crossed four services?"

That request-shaped story is OpenTelemetry’s home ground.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 101 (*Grafana*).

Narration technique: PromQL at 3am → Grafana as shared picture → starter panel table → provisioning/alerts → Spring upstream honesty → bridge to distributed traces.
