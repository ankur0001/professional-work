# Episode 65 — Performance

| Field | Value |
|---|---|
| Episode | 65 |
| Title | Performance |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 65 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Proxies are an elegant way to modularize cross-cutting concerns. They are not free. Each advised call pays for entering the proxy, walking an interceptor chain, evaluating whatever remains of matching work, and only then running your method. On a cold path that hits the database for forty milliseconds, a few microseconds of AOP vanish into noise. On a tight in-memory loop advised by three `@Around` aspects with fat pointcut expressions, the abstraction becomes a tax you can measure.

AOP performance is about knowing where that tax is worth paying.

Startup cost comes first. Auto-proxy creators scan advisors, build candidate sets, and generate JDK or CGLIB proxy classes for matching beans. Hundreds of beans times class-based proxy generation shows up in boot time and metaspace. Narrow pointcuts and fewer blanket aspects reduce how many beans get wrapped. If only ten services need auditing, an `@annotation(Audited)` pointcut beats `execution(* com.example..*(..))` across the entire tree.

```java
@Aspect
@Component
public class ExpensiveVsCheapAspect {

    // wide — tempting, costly if it matches hundreds of beans/methods
    @Around("execution(* com.example..*Service.*(..))")
    public Object wide(ProceedingJoinPoint pjp) throws Throwable {
        return pjp.proceed();
    }
}
```

```java
@Aspect
@Component
public class OptInAuditAspect {

    // narrow — opt-in methods only
    @Around("@annotation(com.example.audit.Audited)")
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

Runtime cost sits in the call path. Prefer cheap advice bodies. An `@Around` that allocates format strings, serializes arguments to JSON, and writes synchronous network audit on every call can dominate a service that used to be a few field updates. Sample, bound, or async the observability side effects. Avoid advising trivial getters called thousands of times per request. Remember self-invocation: people sometimes “fix” performance by moving logic to public advised methods and accidentally create extra proxy hops — or conversely wonder why removing an annotation did nothing because calls never hit the proxy.

Pointcut shape matters more than many teams expect. Complex runtime matching is cheaper when Spring can cache and when static structure dominates. Extremely wide expressions force more proxying and more interceptor evaluations. Named composed pointcuts that fail fast — type first, then annotation — keep intent clear and matching bounded.

Measure before you blame AOP. Use a profiler or micrometer timers around representative endpoints with aspects enabled and disabled. Check allocation rates, not only average latency. Watch for CGLIB proxy class explosion in metaspace on apps that create many advised beans dynamically. And distinguish framework advisors you want — transactions, security — from accidental custom aspects on hot loops.

A misconception is “remove all AOP for speed.” You would reintroduce copy-pasted logging and transaction demarkation, usually with worse bugs and similar overhead in handwritten form. Another is enabling `exposeProxy = true` and calling `AopContext.currentProxy()` everywhere to “fix” self-invocation — correct sometimes, but a design smell that also adds cost and thread-local coupling. Prefer restructuring so external calls enter through the proxy naturally.

We have now walked AOP from concepts through proxies, advice, pointcuts, ordering, and cost. Cross-cutting concerns are under control in the service layer. The next pressure is different: who is allowed to call those services at all, how credentials travel with a request, and what “authenticated” means inside a Spring application.

That opens security fundamentals — the natural continuation beyond AOP.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 65 (*Performance*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
