# Episode 65 — AOP Performance

| Field | Value |
|---|---|
| Episode | 65 |
| Title | AOP Performance |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 65 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Multiply three milliseconds by a few million gate-status polls per day and you are no longer discussing elegance. You are discussing a latency tax. Someone aimed a wide pointcut at every public method under `com.harbor..*`, each `@Around` allocating strings and writing synchronous audit. On a cold path that already waits forty milliseconds on the database, a few microseconds of AOP vanish. On a hot status loop, the abstraction becomes measurable pain.

AOP performance is about knowing where that tax is worth paying.

Startup cost comes first. Auto-proxy creators scan advisors, build candidate sets, and generate JDK or CGLIB proxy classes for matching beans. Hundreds of beans times class-based proxy generation shows up in boot time and metaspace. Narrow pointcuts and fewer blanket aspects reduce how many beans get wrapped. If only ten gate operations need auditing, `@annotation(Audited)` beats `execution(* com.harbor..*(..))` across the tree.

```java
@Aspect
@Component
public class WideHarborAspect {

    // tempting — costly if it matches millions of hot calls
    @Around("execution(* com.harbor..*Service.*(..))")
    public Object wide(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            // 3ms of formatting + remote audit on every call adds up
            audit.remote(pjp.getSignature().toShortString(), System.nanoTime() - start);
        }
    }
}
```

```java
@Aspect
@Component
public class OptInGateAuditAspect {

    @Around("@annotation(com.harbor.audit.Audited)")
    public Object audit(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            long took = System.nanoTime() - start;
            if (took > 5_000_000L) {
                slowLog.warn("{} took {} µs", pjp.getSignature(), took / 1000);
            }
        }
    }
}
```

Runtime cost sits in the call path. Prefer cheap advice bodies. An `@Around` that serializes arguments to JSON and writes synchronous network audit on every call can dominate a method that used to be a few field updates. Sample, bound, or async the observability side effects. Avoid advising trivial getters called thousands of times per request. Remember self-invocation: moving logic to public advised methods can add proxy hops — or removing an annotation can change nothing because calls never hit the proxy.

Pointcut shape matters. Complex runtime matching is cheaper when Spring can cache and when static structure dominates. Extremely wide expressions force more proxying and more interceptor evaluations. Named composed pointcuts that fail fast — type first, then annotation — keep intent clear and matching bounded.

Measure before you blame AOP. Profile or time representative gate endpoints with aspects enabled and disabled. Check allocation rates, not only average latency. Watch for CGLIB proxy class explosion in metaspace. Distinguish framework advisors you want — transactions, security — from accidental custom aspects on hot loops.

A misconception is “remove all AOP for speed.” You would reintroduce copy-pasted logging and transaction demarkation, usually with worse bugs and similar overhead in handwritten form. Another is enabling `exposeProxy = true` and calling `AopContext.currentProxy()` everywhere to “fix” self-invocation — sometimes correct, often a design smell with thread-local coupling. Prefer restructuring so external calls enter through the proxy naturally.

We have walked AOP from concepts through proxies, advice, pointcuts, ordering, and cost. Cross-cutting concerns are under control in the service layer. The next pressure is different: who may call those services at all, how credentials travel with a request, and what “authenticated” means for an open harbor API.

That opens security fundamentals.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 65 (*AOP Performance*).
