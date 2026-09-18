# Episode 61 — CGLIB

| Field | Value |
|---|---|
| Episode | 61 |
| Title | CGLIB |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 61 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Many Spring beans are concrete classes with no interface. A `@Service` report generator, a `@Component` price calculator — injected by their own type. JDK’s `Proxy` cannot wrap those: it only implements interfaces. Spring’s answer is a class-based proxy via CGLIB (and, in modern Spring, related subclass-generation support). Runtime bytecode creates a subclass of your concrete class, overrides methods, and weaves interceptor calls into those overrides. The object you inject is-a your class — a subclass instance — while still delegating to the original target logic through the advice chain.

Use a different example than the notification gateway. Here the component is a concrete class on purpose.

```java
@Service
public class TaxComputationService {

    public TaxResult compute(Money net, TaxRegion region) {
        Rate rate = Rates.forRegion(region);
        Money tax = net.multiply(rate);
        return new TaxResult(net, tax, net.plus(tax));
    }

    public boolean isExempt(CustomerId id) {
        return Exemptions.contains(id);
    }
}
```

```java
@Aspect
@Component
public class TaxAuditAspect {

    private static final Logger log = LoggerFactory.getLogger(TaxAuditAspect.class);

    @Before("execution(* com.example.tax.TaxComputationService.compute(..)) && args(net, region)")
    public void auditCompute(Money net, TaxRegion region) {
        log.info("tax compute net={} region={}", net, region);
    }
}
```

Collaborators inject `TaxComputationService`. With CGLIB, the runtime type might be something like `TaxComputationService$$SpringCGLIB$$0` — a subclass. `instanceof TaxComputationService` is true. Casting to the concrete type works. `compute` is overridden so that entering it runs the audit `@Before` advice, then the original method body. That is the subclass-proxy story: same class shape for injection, extra behavior in overridden methods.

Trade-offs arrive immediately. Final classes cannot be subclassed — CGLIB proxy creation fails. Final methods cannot be overridden — calls to them go straight to the original implementation without advice. Private methods are not overridden either. Constructors run for the subclass; side effects in constructors can surprise you when the proxy is created. Equals and hashCode sometimes need care because the proxy and target are distinct objects.

Compared with JDK proxies from the previous episode: interface proxy versus subclass proxy. Notification gateways programmed to interfaces fit JDK. Tax services programmed as concrete types fit CGLIB. Neither is “more Spring.” They are two implementation strategies for the same AOP idea. Forcing `proxyTargetClass = true` makes Spring prefer CGLIB even when interfaces exist — useful when code casts to concrete types, costly when you wanted interface-only wrappers.

Spring Framework 6 / Boot 3 still expose the same conceptual choice even as the bytecode library details evolve; your debugging questions stay stable. Is this bean a JDK proxy or a CGLIB subclass? Which methods are actually overridden? Did I call through the proxy or via `this`?

A misconception is believing CGLIB “enhances the original class in place.” It creates a new subclass instance. Another is assuming every method call on that instance is advised — final and private paths punch holes in that assumption. A third is ignoring constructor cost: creating thousands of CGLIB proxies at startup has a real bill, which we will revisit when we talk performance.

We now know how the wrapper is built — interface proxy or subclass proxy. The next question is what kinds of logic you hang on that wrapper: the shapes of advice themselves.

Before, after, around, on throw, on return — that vocabulary is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 61 (*CGLIB*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
