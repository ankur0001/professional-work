# Episode 63 — Pointcuts

| Field | Value |
|---|---|
| Episode | 63 |
| Title | Pointcuts |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 63 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Someone ships a logging `@Around` with `execution(* com.harbor..*(..))`. Overnight the metrics bus melts. Repository `findById` calls, mapper methods, and gate services all sprout advice. Latency climbs. The advice body was harmless. The aim was not.

Pointcuts are the aiming language: predicates that select join points so advice runs only where you intend. In Spring AOP the dominant join point is method execution. The dominant expression language is AspectJ pointcut syntax, interpreted for proxy-based weaving.

Narrow the harbor story so advice hits gate services — not repositories.

```java
@Aspect
@Component
public class GatePointcutAspect {

    @Pointcut("execution(* com.harbor.gate..*Service.*(..))")
    public void gateServices() {}

    @Pointcut("@annotation(com.harbor.audit.Audited)")
    public void auditedMethods() {}

    @Pointcut("gateServices() && auditedMethods() && !within(com.harbor.gate..*Repository+)")
    public void auditedGateOps() {}

    @Around("auditedGateOps()")
    public Object audit(ProceedingJoinPoint pjp) throws Throwable {
        AuditTrail.enter(pjp.getSignature().toShortString(), pjp.getArgs());
        try {
            Object result = pjp.proceed();
            AuditTrail.exit(pjp.getSignature().toShortString(), result);
            return result;
        } catch (Throwable ex) {
            AuditTrail.fail(pjp.getSignature().toShortString(), ex);
            throw ex;
        }
    }
}
```

```java
public class GateReleaseService {

    @Audited
    public ReleaseReceipt release(CargoId cargoId) {
        // advised
        return boom.open(cargoId);
    }

    public int queueDepth(GateId gateId) {
        // not @Audited — pointcut misses on purpose
        return queues.depth(gateId);
    }
}
```

Design expressions like APIs. `execution` selects by method signature. Double-dot `..` in a package pattern means any subpackage. `within` restricts by type. `@annotation` selects opt-in methods — excellent when you want auditing without wrapping every repository. `@within` matches types carrying a marker. `bean(gateReleaseService)` selects by bean name when that style fits. Combine with `&&`, `||`, and `!`. Named `@Pointcut` methods keep compositions readable — here `gateServices` and `auditedMethods` meet, and repositories are excluded so advice does not hit persistence methods by accident.

Args binding ties matched parameters into advice when types line up: `execution(* release(..)) && args(cargoId)` lets advice declare `CargoId cargoId`. Binding mistakes fail loudly — better than silent no-ops if you notice early.

What Spring AOP will not do: advise join points proxies cannot see. Field access, constructors, and private method calls are AspectJ-complete features outside the proxy subset. Keep expectations matched to the weaving model you enabled.

Pointcut bugs show up as “advice never runs” or “advice runs too often.” Too narrow: wrong package, forgot `public`, mismatched arguments. Too wide: `execution(* *(..))` across the classpath. Another failure mode is matching self-invocations that never enter the proxy — the expression is fine; the call path is wrong. Test advice by calling through the Spring bean, not by constructing the target with `new`.

So advice aims through pointcuts, and named compositions keep that aim maintainable. When security, transactions, and metrics all match the same gate method, a new problem appears: which advice runs first, and which runs closer to the target?

That sequencing problem is aspect ordering.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 63 (*Pointcuts*).
