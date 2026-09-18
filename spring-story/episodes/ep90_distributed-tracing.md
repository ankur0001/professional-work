# Episode 90 — Distributed Tracing

| Field | Value |
|---|---|
| Episode | 90 |
| Title | Distributed Tracing |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 90 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A circuit breaker told you payment was failing. A customer still opens a ticket: “Checkout hung for eight seconds, then said try again.” Order logs show a slow call. Inventory logs show nothing obvious. Gateway logs show 200s. Without a shared request identity across those processes, you are correlating by timestamp and prayer. Distributed tracing gives each request a trace id, each hop a span, and a timeline you can render in Zipkin, Jaeger, or another backend.

In modern Spring, Micrometer Tracing is the façade, often with Brave or OpenTelemetry as the bridge, and Spring Boot Actuator plus a reporter shipping spans somewhere useful. Older materials say Spring Cloud Sleuth; the ideas — trace id, span id, baggage, propagation over HTTP headers — remain. When order calls inventory over Feign or WebClient, instrumentation injects headers such as `traceparent` (W3C) or B3 headers. Inventory’s filter reads them and continues the same trace. Your log pattern should include the trace id so a single grep stitches the story.

```yaml
# order-service
management:
  tracing:
    sampling:
      probability: 1.0   # demos; use lower in hot prod
  zipkin:
    tracing:
      endpoint: http://zipkin:9411/api/v2/spans

logging:
  pattern:
    level: "%5p [${spring.application.name:},%X{traceId:-},%X{spanId:-}]"
```

Walk one checkout. Gateway creates a root span for `POST /api/orders`. It forwards to order-service with propagation headers. Order starts a child span for the controller, then another for `InventoryClient.reserve`, then another for `PaymentClient.charge`. Payment slows for 2.4 seconds — that span’s timing lights up in the UI. You see the critical path without SSH into three boxes. If the circuit breaker opens, you still see spans that failed fast versus spans that timed out, which is how you distinguish “protected” from “still hanging.”

```java
@Service
public class CheckoutService {
    private final InventoryClient inventory;
    private final PaymentClient payment;
    private final Tracer tracer; // Micrometer Tracing API

    public CheckoutService(InventoryClient inventory,
                           PaymentClient payment,
                           Tracer tracer) {
        this.inventory = inventory;
        this.payment = payment;
        this.tracer = tracer;
    }

    public void checkout(CheckoutCommand cmd) {
        Span span = tracer.nextSpan().name("checkout-domain").start();
        try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
            inventory.reserve(cmd.toReserve());
            payment.charge(cmd.toCharge());
        } finally {
            span.end();
        }
    }
}
```

Most HTTP and messaging instrumentation is automatic once dependencies are on the classpath. Manual spans are for domain phases that matter to you — “fraud-check”, “allocate-inventory” — when the auto spans are too coarse. Baggage can carry business keys like `customerId` across services; use it sparingly, and never put secrets in baggage or logs.

Sampling is an operational dial. One hundred percent sampling is perfect for a demo and expensive at peak traffic. Production often samples a fraction of successful requests and keeps error traces more aggressively. Wrong sampling makes traces look healthy while customers burn.

Messaging needs the same discipline. When Spring Cloud Stream publishes `OrderPlaced`, the binder instrumentation should continue the producer’s trace into the consumer’s process; otherwise async hops become orphan roots and your timeline lies. Clock skew across hosts can also make span waterfalls look impossible — trust relative durations inside a service more than absolute wall clocks across regions.

A misconception is equating tracing with logging. Logs are event text; traces are timed directed graphs of spans. You want both, linked by trace id. Another is enabling tracing without propagating headers through the gateway — then every service starts a new root and the graph shatters. A third is collecting traces but never opening the UI during incidents; unused observability is décor.

Today we followed one checkout across gateway, order, inventory, and payment as a single trace, propagated ids over HTTP, and tied breaker behavior to what spans reveal about fail-fast versus timeout.

Tracing shows pain. The next step is a fuller toolkit for preventing that pain at the call boundary — retries, rate limiters, bulkheads, and the circuit breaker you already met — under one library name you will see in Spring docs constantly.

That library is Resilience4j.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 90 (*Distributed Tracing*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
