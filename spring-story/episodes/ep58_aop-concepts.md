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

Open a typical service class before aspects arrive and you can predict the clutter. At the top of every method: log entry with arguments. Then a security check. Then maybe a timer. Then the real business lines. At the bottom: log exit, or log error in a catch that rethrows. Change the audit format and you edit two hundred methods. Forget the security check on one new endpoint and you ship a hole. The domain logic was never the hard part — the repeated rim around it was.

Those repeated rims are cross-cutting concerns. Logging, security, transactions, metrics — they cut across modules instead of belonging to one feature package. Aspect-oriented programming exists to pull them into their own modules and apply them systematically.

Spring AOP does that with proxies and a small AspectJ-inspired programming model. You write an aspect: a class that packages pointcuts — where to intervene — and advice — what to run. At runtime, calls into a Spring bean hit a proxy first. If the join point matches, advice runs before, after, or around the real method.

```java
@Aspect
@Component
public class ServiceGuardAspect {

    private static final Logger log = LoggerFactory.getLogger(ServiceGuardAspect.class);

    private final PermissionChecker permissions;

    public ServiceGuardAspect(PermissionChecker permissions) {
        this.permissions = permissions;
    }

    @Around("@within(org.springframework.stereotype.Service) && execution(public * *(..))")
    public Object guard(ProceedingJoinPoint pjp) throws Throwable {
        String name = pjp.getSignature().toShortString();
        log.info("enter {}", name);
        permissions.assertAllowed(name);

        long start = System.nanoTime();
        try {
            Object result = pjp.proceed();
            log.info("exit {} in {} ms", name, (System.nanoTime() - start) / 1_000_000);
            return result;
        } catch (Throwable ex) {
            log.warn("fail {}: {}", name, ex.toString());
            throw ex;
        }
    }
}
```

Speak the example. `@Aspect` marks the module. `@Around` advice wraps matching service methods. Before `proceed`, we log and enforce a permission check. After `proceed`, we log timing. On failure, we log and rethrow. The service methods themselves stay about invoices or reservations — no copy-pasted security or timing boilerplate. Transactions fit the same story: `@Transactional` is implemented with AOP infrastructure even when you never write `@Aspect` yourself.

Hold a few vocabulary words so later episodes stay crisp. Join point: a moment you could intervene — in Spring AOP, primarily method execution. Pointcut: the predicate that selects join points. Advice: the code that runs. Aspect: the unit combining pointcut and advice. Weaving: applying aspects to targets — Spring usually weaves at runtime via proxies, not compile-time bytecode rewriting like full AspectJ.

History helps expectations. AspectJ at Xerox PARC aimed at a rich join-point model. Spring AOP, arriving with the framework’s early years, chose a pragmatic subset: proxy-based, method-centric, friendly to plain Java config and annotations. You enable it with `@EnableAspectJAutoProxy` or, in Boot, by having spring-aop and aspectjweaver on the classpath with aspects as beans. `AnnotationAwareAspectJAutoProxyCreator` notices `@Aspect` beans and wraps matching targets.

What AOP is not: a replacement for clean module boundaries, or a place to hide core business rules. If the “aspect” is really domain policy that only one aggregate cares about, keep it in the domain. Use aspects for true cross-cuts. Also, Spring AOP will not advise private methods, self-invocations, or calls that never pass through the proxy — limits that become vivid once you see how proxies work.

We modularized logging, security, and transactional-style wrapping with an `@Aspect`. The remaining mystery is mechanical: what object actually sits in front of your bean and intercepts the call?

That object is a dynamic proxy — and understanding it unlocks the next episodes.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 58 (*AOP Concepts*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
