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

Advice without aim is a firehose. Attach a logging `@Around` to `execution(* *(..))` and you will drown in noise, wrap infrastructure methods you never meant to touch, and pay proxy costs on hot paths that did not need them. Pointcuts are the aiming language: predicates that select join points so advice runs only where you intend.

In Spring AOP the dominant join point is method execution. The dominant expression language is AspectJ’s pointcut syntax, interpreted by Spring for proxy-based weaving.

```java
@Aspect
@Component
public class InventoryPointcutAspect {

    @Pointcut("execution(* com.example.inventory..*Service.*(..))")
    public void inventoryServices() {}

    @Pointcut("@annotation(com.example.audit.Audited)")
    public void auditedMethods() {}

    @Pointcut("inventoryServices() && auditedMethods()")
    public void auditedInventory() {}

    @Around("auditedInventory()")
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
public class StockService {

    @Audited
    public void allocate(Sku sku, int qty) {
        // ...
    }

    public int available(Sku sku) {
        // not annotated — pointcut misses this method on purpose
        return stockDao.count(sku);
    }
}
```

Design the expressions like you design APIs. `execution` selects by method signature — return type, type pattern, name pattern, parameters. Double-dot `..` in a package pattern means any subpackage. `within(com.example.inventory..*)` restricts by type. `@annotation` selects methods carrying a given annotation — excellent when you want opt-in auditing instead of package-wide wrapping. `@within` matches types annotated with a marker. `bean(stockService)` can select by Spring bean name when that style fits. Combine with `&&`, `||`, and `!`. Named `@Pointcut` methods keep complex expressions readable and reusable — the example composes `inventoryServices` and `auditedMethods` into `auditedInventory`.

Args binding ties matched parameters into advice parameters when types line up: `execution(* allocate(..)) && args(sku, qty)` lets advice declare `Sku sku, int qty`. Binding mistakes fail loudly at startup or at match time — better than silent no-ops if you notice early.

What Spring AOP will not do: advise join points that proxies cannot see. Field access, constructor execution, and private method calls are AspectJ-complete features outside Spring’s proxy subset. Keep expectations matched to the weaving model you actually enabled.

Pointcut mistakes show up as “my advice never runs” or “my advice runs too often.” Too narrow: wrong package, forgot `public`, mismatched argument patterns. Too wide: `execution(* *(..))` across the classpath. Another failure mode is matching self-invocations that never enter the proxy — the pointcut is fine; the call path is wrong. Test advice with integration tests that call through the Spring bean, not by constructing the target with `new`.

So advice aims through pointcuts, and named compositions keep that aim maintainable. When two aspects both match the same method — security and transactions, metrics and auditing — a new problem appears: which advice runs first, and which runs closer to the target?

That sequencing problem is aspect ordering.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 63 (*Pointcuts*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
