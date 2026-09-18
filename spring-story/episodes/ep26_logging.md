# Episode 26 — Logging

| Field | Value |
|---|---|
| Episode | 26 |
| Title | Logging |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 26 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

02:00. Ferry-booking logs in the aggregator. Four pods. A customer says checkout charged twice. You search the booking reference and get fragments: one line from pod A at payment start, nothing from the gateway callback, an ERROR on pod C without a booking id, a stack trace on pod B for an unrelated sailing. Missing correlation IDs turn a distributed request into archaeology. Boot's default console pattern is fine for a laptop; it is not an incident strategy for multi-pod ferry checkout.

Boot's default logging uses Logback behind SLF4J, with `logging.level.*` and `logging.pattern.*` properties, and optional `logback-spring.xml` for profiles and advanced appenders. The framework lesson is not "how to print." It is structured, correlatable output that survives multi-pod reality — and the MDC (Mapped Diagnostic Context) as the carrier for per-request identifiers on a thread.

```xml
<!-- logback-spring.xml -->
<configuration>
  <springProperty scope="context" name="app" source="spring.application.name"/>
  <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
      <providers>
        <timestamp/>
        <pattern>
          <pattern>
            {"app":"${app}","level":"%level","corr":"%X{correlationId}","msg":"%message"}
          </pattern>
        </pattern>
        <stackTrace/>
      </providers>
    </encoder>
  </appender>
  <root level="INFO">
    <appender-ref ref="JSON"/>
  </root>
</configuration>
```

```java
@Component
public class CorrelationFilter extends OncePerRequestFilter {
    public static final String HEADER = "X-Correlation-Id";

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        String cid = Optional.ofNullable(req.getHeader(HEADER))
            .filter(s -> !s.isBlank())
            .orElse(UUID.randomUUID().toString());
        MDC.put("correlationId", cid);
        res.setHeader(HEADER, cid);
        try {
            chain.doFilter(req, res);
        } finally {
            MDC.remove("correlationId");
        }
    }
}
```

Walk the filter and encoder. `OncePerRequestFilter` guarantees one execution per dispatch. Read `X-Correlation-Id` if a gateway already set it; otherwise mint a UUID. `MDC.put("correlationId", cid)` stores the value on the current thread. `res.setHeader` returns the id to clients and support tools. `try/finally` with `MDC.remove` prevents leaks onto pooled threads — a classic bug where later requests inherit someone else's correlation id. The Logback pattern `%X{correlationId}` pulls from MDC into JSON as `corr`. `springProperty` reads `spring.application.name` so every line names the ferry service.

Runtime for one checkout. Request enters pod A; filter assigns id `c-9f3`. Payment service logs "charging" with `corr=c-9f3`. WebClient/Feign to the payment gateway should forward `X-Correlation-Id` — if it does not, the callback lands on pod C with a *new* id and your aggregator cannot join charge and callback. With propagation, refund decision logs share `c-9f3` across pods. Without MDC, Boot's nice default console pattern still leaves you string-matching timestamps and booking refs that half the lines omit. `logging.level.com.ferry=DEBUG` raises detail for one package without recompiling; Actuator's loggers endpoint can change levels live when secured — useful at 02:00 if you already have correlation.

Failure mode symptoms: duplicate charge investigation finds four unrelated `corr` values for one customer journey — header not propagated on outbound calls, or MDC cleared too early, or async work (`@Async`, reactive) lost MDC because it changed threads without copying context. Symptom of MDC leak: support searches one id and sees fragments of other customers' checkouts on the same pod. Symptom of `logging.level.root=DEBUG` in prod during panic: disk full, log pipeline lag, real ERROR lines drowned — and sometimes added latency from logging volume.

Trade-offs. JSON + correlation costs a dependency and filter discipline; it buys queryable incidents. Text patterns are easier to read in a terminal and worse in aggregators. Putting booking ids only in free-text messages fails when the message format changes; first-class MDC fields stay stable. Sampling debug logs or using traces (later episodes) handles volume better than permanent DEBUG.

One ferry-specific discipline: log the booking reference as an MDC field too (`MDC.put("bookingRef", ...)` once the ref exists), not only inside message strings. Aggregators index fields; they do not reliably parse prose. Correlation id joins hops; booking ref joins business. Together they turn "charged twice" from four pods into two queries instead of a scavenger hunt.

Misconception unique to logging in Boot: "Setting `logging.level.root=DEBUG` in production is the responsible way to 'get more detail' during an incident." It floods disks, hides the signal, and can itself cause latency. Prefer targeted packages, already-correlated IDs, and metrics/traces for volume.

Checkout archaeology becomes a single query on `corr`. Finance still deploys the same ferry artifact to staging and prod with different payment merchant IDs — and last week staging charged the prod merchant because the Boot profile document never activated. Profile-specific YAML in Boot packaging is the next seam to tighten.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 26 (*Logging*).
