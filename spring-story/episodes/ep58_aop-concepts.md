# Episode 58 — AOP Concepts

| Field | Value |
|---|---|
| Episode | 58 |
| Title | AOP Concepts |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 58 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Open `GateReleaseService` before anyone introduces aspects and you can predict the clutter. Log entry with truck plate and cargo id. Start a timer. Check that the operator may release this gate. Then — finally — the three lines that actually open the boom and stamp the release. On the way out: log duration, log errors, maybe write an audit row. Change the audit format and you edit every gate method. Forget the permission check on one overload and you ship a hole. The domain was never the hard part. The repeated rim was.

Those rims are cross-cutting concerns. Timing, audit, security, transactions — they cut across modules instead of belonging to one feature package. Aspect-oriented programming pulls them into their own modules and applies them systematically.

Spring AOP does that with proxies and a small AspectJ-inspired model. You write an aspect: pointcuts for where to intervene, advice for what to run. At runtime, calls into a Spring bean hit a proxy first. If the join point matches, advice runs before, after, or around the real method.

```java
@Aspect
@Component
public class HarborGateAspect {

    private static final Logger log = LoggerFactory.getLogger(HarborGateAspect.class);

    private final GateAudit audit;

    public HarborGateAspect(GateAudit audit) {
        this.audit = audit;
    }

    @Around("execution(* com.harbor.gate..*Service.release*(..))")
    public Object timeAndAudit(ProceedingJoinPoint pjp) throws Throwable {
        String name = pjp.getSignature().toShortString();
        long start = System.nanoTime();
        audit.enter(name, pjp.getArgs());
        try {
            Object result = pjp.proceed();
            audit.exit(name, (System.nanoTime() - start) / 1_000_000);
            return result;
        } catch (Throwable ex) {
            audit.fail(name, ex);
            throw ex;
        }
    }
}
```

Speak the example. `@Aspect` marks the module. `@Around` wraps matching gate service release methods. Before `proceed`, we record entry. After, we record timing. On failure, we audit and rethrow. `GateReleaseService` methods stay about cargo and booms — no copy-pasted timers. `@Transactional` fits the same story: you may never write `@Aspect` yourself, yet transactions still ride AOP infrastructure.

Hold the vocabulary so later episodes stay crisp. Join point: a moment you could intervene — in Spring AOP, primarily method execution. Pointcut: the predicate that selects join points. Advice: the code that runs. Aspect: pointcut plus advice. Weaving: applying aspects to targets — Spring usually weaves at runtime via proxies, not compile-time bytecode rewriting like full AspectJ.

History sets expectations. AspectJ aimed at a rich join-point model. Spring AOP chose a pragmatic subset: proxy-based, method-centric, friendly to Java config and annotations. Enable it with `@EnableAspectJAutoProxy` or, in Boot, by having spring-aop and aspectjweaver on the classpath with aspects as beans. `AnnotationAwareAspectJAutoProxyCreator` notices `@Aspect` beans and wraps matching targets.

What AOP is not: a dump for core gate business rules, or a license to advise everything. If the rule is really “this cargo’s seal must match,” keep it in the domain. Use aspects for true cross-cuts. Spring AOP will not advise private methods, self-invocations, or calls that never pass through the proxy — limits that become vivid once you see how proxies work.

We modularized timing and audit around harbor gate services. The mechanical mystery remains: what object actually sits in front of your transactional gate bean and intercepts the call?

That stand-in is a dynamic proxy.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 58 (*AOP Concepts*).
