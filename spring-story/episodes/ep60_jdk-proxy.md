# Episode 60 — JDK Proxy

| Field | Value |
|---|---|
| Episode | 60 |
| Title | JDK Proxy |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 60 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Program the harbor gate to an interface and the JDK already knows how to wrap it. `java.lang.reflect.Proxy` implements that interface at runtime and funnels every call through one `InvocationHandler`. Spring AOP leans on that when an interface-based proxy is enough. No subclass of your concrete class. A brand-new type that only promises the interface methods.

Interface-oriented design and JDK proxies fit cleanly. You inject `GateService`, not `HarborGateService`, and Spring can substitute a proxy that still is-a `GateService`. Callers never need the concrete class — which is exactly what the yard crane console and the trucker API both depend on when metrics and transactions wrap `release`.

```java
public interface GateService {
    ReleaseReceipt release(CargoId cargoId);
    GateStatus status(GateId gateId);
}

@Service
public class HarborGateService implements GateService {

    private final BoomController boom;
    private final CargoRepository cargo;

    public HarborGateService(BoomController boom, CargoRepository cargo) {
        this.boom = boom;
        this.cargo = cargo;
    }

    @Override
    public ReleaseReceipt release(CargoId cargoId) {
        CargoItem item = cargo.requireOpen(cargoId);
        boom.open(item.gateId());
        return ReleaseReceipt.open(cargoId);
    }

    @Override
    public GateStatus status(GateId gateId) {
        return boom.read(gateId);
    }
}
```

```java
@Aspect
@Component
public class GateMetricsAspect {

    @Around("execution(* com.harbor.gate.GateService.release(..))")
    public Object timeRelease(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            Metrics.timer("gate.release")
                    .record(System.nanoTime() - start, TimeUnit.NANOSECONDS);
        }
    }
}
```

Walk a `release` call at runtime. Collaborators hold a field of type `GateService`. After context refresh with matching advisors, the injected object is often a JDK proxy implementing `GateService` (and possibly other interfaces the target exposes), holding `HarborGateService` as the target inside Spring's AOP infrastructure. The trucker API calls `gateService.release(cargoId)`. The call enters the proxy's `InvocationHandler`, not `HarborGateService` directly. The interceptor chain runs — here the metrics `@Around` records nanos, and any transactional advisor would begin/commit around `proceed`. `pjp.proceed()` eventually reflects into `HarborGateService.release`, which loads cargo and opens the boom. Return value flows back through the same chain. The concrete class is not the type of the injected field — and that is fine for every caller that programmed to the interface.

Failure mode that shows up in code review and production. Someone injects or casts to `HarborGateService` while Spring published a JDK proxy. The proxy is not an instance of `HarborGateService`. It implements the interface only. `instanceof HarborGateService` is false. `(HarborGateService) gateService` throws `ClassCastException` at the edge that assumed the impl type — often a `@Autowired HarborGateService` field that fails at injection with an unsatisfied dependency or a wrong-type match depending on how candidates were filtered. Self-invocation inside `HarborGateService` — `this.status(gateId)` from `release` — never enters the proxy, so advice on `status` does not run for that path; metrics and transactions skip. Pointcuts written against the concrete class name may not match the way you expect when the public entry is the interface proxy. Final methods on the concrete class are irrelevant to the JDK proxy type because callers should not see the concrete class through the proxy reference — only interface methods are dispatched through the handler.

JDK proxies can implement multiple interfaces. If `HarborGateService` also implements `HealthIndicator`, the proxy can expose both, and injectors typed to either interface may receive the same proxy instance. Only interface methods are advised through this mechanism. Package-private or protected methods on the impl are not part of the proxy's public contract.

Selection rule of thumb: when the target implements at least one interface (other than marker-only cases Spring may ignore), JDK proxy is eligible. Force class-based proxies with `spring.aop.proxy-target-class=true` or `@EnableAspectJAutoProxy(proxyTargetClass = true)` and you push toward CGLIB even when interfaces exist. Boot defaults have shifted over versions — verify what you actually get instead of assuming a textbook JDK proxy. Debug with `AopUtils.isJdkDynamicProxy(bean)` or glance at the class name — `$Proxy12` is a clue you are in interface-proxy land; `$$SpringCGLIB$$` means class proxy.

Trade-offs. JDK proxies need no bytecode subclassing of your concrete type, play well with final classes that still implement interfaces, and keep the API surface honest. They punish concrete-type injection and are unavailable when there is no interface to implement. Prefer interface injection everywhere gate collaborators are wired; reserve concrete types for the `@Service` implementation class itself.

Misconception unique to JDK proxies: "The proxy is a subclass of `HarborGateService`." It is not. It is a sibling stand-in that shares the interface, generated by `Proxy.newProxyInstance`. Another misconception: "If I have an interface, Boot always uses JDK proxies." Configuration and Boot version may choose CGLIB anyway — check before writing casts or `instanceof` against the impl.

The limitation is the next engineering wall. What if there is no interface? What if the bean is a concrete `@Service` injected by its class type? JDK `Proxy` cannot subclass that concrete type.

You need CGLIB.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 60 (*JDK Proxy*).
