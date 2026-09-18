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

One `releaseGate` call. Three aspects. Security must reject unauthorized operators before anything else runs. Transactions must begin before business work and commit after. Metrics want to time the call — ideally without opening a database transaction for callers who were going to be denied anyway. If the order is accidental, you open connections for rejected trucks, or you time only the inner fragment and lie on the dashboard.

Aspect ordering makes that sequence intentional. Spring uses `Ordered` / `@Order` on aspect beans (and on some infrastructure advisors). Lower order values mean higher precedence. For `@Around` advice, higher precedence is outer: enters first, exits last. Think nested wrappers.

For harbor gate releases, prefer security → transaction → metrics from outside in.

```java
@Aspect
@Component
@Order(1) // outer: security first on the way in
public class GateSecurityAspect {

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
public class GateTxStyleAspect {

    // teaching stand-in — real @Transactional uses Spring's own advisor
    @Around("@annotation(com.harbor.tx.AppTransactional)")
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
@Order(3) // inner among these three: closest to the target
public class GateMetricsAspect {

    @Around("execution(* com.harbor.gate..*Service.*(..))")
    public Object time(ProceedingJoinPoint pjp) throws Throwable {
        Timer.Sample sample = Timer.start();
        try {
            return pjp.proceed();
        } finally {
            sample.stop(Timer.builder("gate.service").register(meterRegistry));
        }
    }
}
```

Narrate the enter path. Client hits the proxy. Security (order 1) checks permission, calls `proceed`. Transactional-style advice (order 2) begins work, calls `proceed`. Metrics (order 3) starts a timer, calls `proceed`, hits the target. On the way out: metrics stop, transaction commits, security exits. Unauthorized callers fail in security and never open a transaction — usually what you want. Swap carelessly and you hold database connections for operators who were never allowed to release the gate.

Spring’s own `@Transactional` and `@Async` advisors live in the same precedence world. Custom aspects that must run outside or inside transactions should declare `@Order` explicitly. When two aspects share the same order value, relative order is effectively undefined — do not depend on class-name sorting luck.

Within one aspect class, advice-type precedence has its own rules; cross-aspect problems are what `@Order` on the aspect bean solves. Prefer one clear responsibility per aspect so ordering stays reviewable.

Misconception: “`@Order` on any `@Component` controls method call order in the app.” Here it controls advisor precedence in the AOP chain, not general bean initialization. Another: expecting `@After` from a lower-precedence aspect to run before `@After` from a higher-precedence aspect without drawing the enter/exit nest. Draw the nest. Speak the nest. Then the numbers make sense.

Ordered aspects keep security, transactions, and metrics from tripping over each other. They do not erase the cost of every proxy hop and advice invocation.

When does that cost matter on a busy gate? That is AOP performance.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 64 (*Aspect Ordering*).
