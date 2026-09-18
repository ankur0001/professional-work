# Episode 89 — Circuit Breaker

| Field | Value |
|---|---|
| Episode | 89 |
| Title | Circuit Breaker |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 89 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Feign made `inventory.reserve(...)` look like a local method. Under load, that courtesy becomes a trap. Inventory is failing — timeouts, 503s, thread pool exhaustion on their side. Order service keeps calling. Every checkout thread blocks on a doomed HTTP call. Order’s own thread pool fills. Health checks fail. The gateway marks order unhealthy. Now a dependency outage has taken down a service that might have degraded gracefully. A circuit breaker exists to stop calling a failing dependency after a threshold, fail fast, and optionally run fallback logic while the dependency recovers.

The electrical metaphor is intentional. Closed circuit: calls flow to the remote system. Open circuit: calls short-circuit immediately without hitting the network. Half-open: a limited number of trial calls probe whether the dependency is healthy again; success closes the circuit, failure re-opens it. Spring Cloud CircuitBreaker provides an abstraction; Resilience4j is the common implementation on modern stacks. You can annotate methods with `@CircuitBreaker` from Spring Cloud CircuitBreaker or use Resilience4j annotations directly — same state machine idea.

Watch a failing remote call open the circuit with a concrete service sketch.

```java
@Service
public class PaymentFacade {
    private final PaymentClient paymentClient;

    public PaymentFacade(PaymentClient paymentClient) {
        this.paymentClient = paymentClient;
    }

    @CircuitBreaker(name = "payment", fallbackMethod = "chargeFallback")
    public PaymentResult charge(ChargeCommand cmd) {
        return paymentClient.charge(cmd); // Feign/WebClient — may time out or 503
    }

    private PaymentResult chargeFallback(ChargeCommand cmd, Throwable ex) {
        return PaymentResult.pendingRetry(cmd.orderId(), ex.getMessage());
    }
}
```

```yaml
resilience4j:
  circuitbreaker:
    instances:
      payment:
        slidingWindowSize: 10
        failureRateThreshold: 50
        waitDurationInOpenState: 5s
        permittedNumberOfCallsInHalfOpenState: 3
        automaticTransitionFromOpenToHalfOpenEnabled: true
```

Narrate a run. The first few `charge` calls hit payment and fail — timeouts count as failures when configured that way. Once ten calls sit in the sliding window and half or more have failed, the breaker opens. Call eleven does not wait on HTTP; it jumps to `chargeFallback` in milliseconds. Order can record a pending payment state instead of melting its threads. After `waitDurationInOpenState`, the breaker goes half-open. A few calls are allowed through. If payment is healthy again, the circuit closes. If they still fail, it opens once more.

Integrate with Feign carefully. You can wrap Feign calls inside a service method that carries the circuit annotation, or use Resilience4j Feign capabilities depending on your stack version. The important design rule: the breaker wraps the remote boundary, not your entire domain transaction, unless you intentionally want that scope. Fallback signatures must match the original method plus a trailing `Throwable` (or specific exception types) so the proxy can dispatch correctly.

Metrics and Actuator endpoints matter operationally. A breaker that opens should be visible — state transitions, failure rates — or on-call will only notice via customer complaints. Pair breakers with sensible timeouts; a breaker without timeouts still lets threads hang until the window fills slowly.

A misconception is setting thresholds so tight that normal blips permanently open the circuit, or so loose that the breaker never trips during a real outage. Another is a fallback that returns empty success and writes nothing durable — you have hidden data loss. A third is putting a circuit breaker on purely in-process calls “for consistency”; breakers earn their keep on unreliable boundaries: network, process, or shared resource contention.

Today we watched a payment remote call fail until a circuit opened, fail-fast to a fallback, and probe half-open for recovery — protecting order capacity when a dependency burns.

When the breaker trips, you know *that* payment is unhealthy. You still may not know *which* hop across six services first slowed down for a single customer request. Logs without shared context will not tell you.

That cross-process story is Distributed Tracing.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 89 (*Circuit Breaker*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
