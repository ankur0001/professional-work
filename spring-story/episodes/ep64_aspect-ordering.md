# Episode 64 — Aspect Ordering

| Field | Value |
|---|---|
| Episode | 64 |
| Title | Aspect Ordering |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 64 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

One method. Three aspects. Security wants to reject unauthorized callers before anything else runs. Transactions want to begin before business work and commit after. Metrics want to time the whole thing, including security failures — or maybe only successful business calls. If the order is accidental, you get accidental behavior: a transaction that opens before the auth check, a timer that excludes the expensive part, an audit entry that claims success for a call that never authorized.

Aspect ordering is how you make that sequence intentional.

Spring uses `Ordered` / `@Order` on aspect beans (and on some infrastructure advisors). Lower order values run with higher precedence. For `@Around` advice, higher precedence means outer: it enters first and exits last. Think nested wrappers. The outermost advice calls `proceed`, which enters the next advice, which eventually reaches the target, then unwinds back out.

```java
@Aspect
@Component
@Order(1) // outer: runs first on the way in
public class SecurityAspect {

    @Around("@annotation(secured)")
    public Object authorize(ProceedingJoinPoint pjp, Secured secured) throws Throwable {
        security.assertHas(secured.value());
        return pjp.proceed();
    }
}
```

```java
@Aspect
@Component
@Order(2)
public class TransactionalStyleAspect {

    // teaching stand-in — real @Transactional uses Spring's own advisor
    @Around("@annotation(com.example.tx.AppTransactional)")
    public Object aroundTx(ProceedingJoinPoint pjp) throws Throwable {
        tx.begin();
        try {
            Object result = pjp.proceed();
            tx.commit();
            return result;
        } catch (RuntimeException ex) {
            tx.rollback();
            throw ex;
        }
    }
}
```

```java
@Aspect
@Component
@Order(3) // inner: closest to the target among these three
public class MetricsAspect {

    @Around("execution(* com.example.shop..*Service.*(..))")
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        Timer.Sample sample = Timer.start();
        try {
            return pjp.proceed();
        } finally {
            sample.stop(Timer.builder("service.method").register(meterRegistry));
        }
    }
}
```

Narrate the enter path with these orders. Client calls the proxy. `SecurityAspect` (order 1) enters, checks permission, calls `proceed`. `TransactionalStyleAspect` (order 2) begins a transaction, calls `proceed`. `MetricsAspect` (order 3) starts a timer, calls `proceed`, hits the target. On the way out, metrics stop, transaction commits, security exits. Unauthorized callers fail in security and never open a transaction — which is usually what you want. Swap orders carelessly and you hold database connections for callers who were going to be rejected anyway.

Spring’s own `@Transactional` and `@Async` advisors participate in the same precedence world. Documentation and source set default orders for infrastructure; custom aspects that must run outside or inside transactions should declare `@Order` explicitly instead of relying on undefined relative order between your aspects. When two aspects share the same order value, relative order is effectively undefined — do not depend on class name sorting luck.

Within a single aspect class, advice ordering among `@Before` / `@After` / `@Around` methods follows Spring’s precedence rules for advice types; cross-aspect problems are the ones `@Order` on the aspect bean is meant to solve. Prefer one clear responsibility per aspect so ordering decisions stay reviewable.

Misconception: “`@Order` on a `@Component` always controls method call order in the app.” Here it controls advisor precedence in the AOP chain, not general bean initialization order — related annotation, different meaning in this context. Another misconception: expecting `@After` advice from a lower-precedence aspect to run before `@After` from a higher-precedence aspect without drawing the enter/exit nesting. Draw the nest. Speak the nest. Then the annotation values make sense.

Ordered aspects keep security, transactions, and metrics from tripping over each other. They do not erase the fact that every proxy hop and every advice invocation costs CPU and allocations.

When does that cost matter, and how do you keep AOP from becoming a latency tax? That is the performance episode next — and after it, the series turns toward securing the application itself.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 64 (*Aspect Ordering*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
