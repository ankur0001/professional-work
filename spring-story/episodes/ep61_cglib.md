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

Many harbor beans are concrete classes with no interface. A `@Service` that prints gate passes, a `@Component` that scores tide windows — injected by their own type. JDK’s `Proxy` cannot wrap those: it only implements interfaces. Spring’s answer is a class-based proxy via CGLIB (and related subclass generation in modern Spring). Runtime bytecode creates a subclass of your concrete class, overrides methods, and weaves interceptor calls into those overrides. The object you inject is-a your class — a subclass instance — while still delegating through the advice chain.

Use a concrete gate helper on purpose — no interface in sight.

```java
@Service
public class GatePassPrinter {

    public byte[] render(ReleaseReceipt receipt) {
        return PassPdf.of(receipt).bytes();
    }

    public boolean canReprint(CargoId cargoId) {
        return ReprintPolicy.allows(cargoId);
    }
}
```

```java
@Aspect
@Component
public class GatePassAuditAspect {

    private static final Logger log = LoggerFactory.getLogger(GatePassAuditAspect.class);

    @Before("execution(* com.harbor.gate.GatePassPrinter.render(..)) && args(receipt)")
    public void auditRender(ReleaseReceipt receipt) {
        log.info("gate pass render cargo={}", receipt.cargoId());
    }
}
```

Collaborators inject `GatePassPrinter`. With CGLIB, the runtime type might be `GatePassPrinter$$SpringCGLIB$$0` — a subclass. `instanceof GatePassPrinter` is true. Casting to the concrete type works. `render` is overridden so entering it runs the audit `@Before`, then the original body. Same class shape for injection; extra behavior in overridden methods.

Trade-offs arrive immediately. Final classes cannot be subclassed — proxy creation fails. Final methods cannot be overridden — calls go straight to the original implementation without advice. Private methods are not overridden either. Constructors run for the subclass; side effects in constructors can surprise you when the proxy is created. Equals and hashCode sometimes need care because proxy and target are distinct objects.

Compared with JDK proxies: interface wrapper versus subclass wrapper. `GateService` programmed to an interface fits JDK. `GatePassPrinter` programmed as a concrete `@Service` fits CGLIB. Neither is “more Spring.” They are two strategies for the same AOP idea. Forcing `proxyTargetClass = true` prefers CGLIB even when interfaces exist — useful when code casts to concrete types, costly when you wanted interface-only wrappers.

Your debugging questions stay stable across Spring versions. Is this bean a JDK proxy or a CGLIB subclass? Which methods are actually overridden? Did I call through the proxy or via `this`?

A misconception is believing CGLIB “enhances the original class in place.” It creates a new subclass instance. Another is assuming every method call on that instance is advised — final and private paths punch holes. A third is ignoring constructor cost when thousands of class proxies materialize at startup.

We know how the wrapper is built. Next is what kinds of logic you hang on it — the shapes of advice themselves.

Before, after, around, on throw, on return — that vocabulary is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 61 (*CGLIB*).
