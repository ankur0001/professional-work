# Episode 59 — Dynamic Proxies

| Field | Value |
|---|---|
| Episode | 59 |
| Title | Dynamic Proxies |
| Phase | Phase 6 — Spring AOP |
| Catalog handbook lesson | 59 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Debug a transactional gate release and print the runtime class of the injected collaborator. You expected `GateReleaseServiceImpl`. You see something like `$Proxy147` or `GateReleaseServiceImpl$$SpringCGLIB$$0`. The method still opens the boom. Transactions still commit. So what object did Spring actually inject?

A proxy — a runtime stand-in that looks like your bean to callers, holds the real target, and decides what happens on each invocation. Dynamic proxies are synthesized at runtime, not handwritten as `GateReleaseServiceProxy` for every type.

Without that stand-in, AOP has nowhere to stand. A client calls `gateService.release(cargoId)`. If `gateService` is the raw target, `@Transactional` and your `@Around` never run. If it is a proxy, the call enters the invocation handler, the interceptor chain runs, and only then does `proceed` reach the target.

```java
public interface GateService {
    ReleaseReceipt release(CargoId cargoId);
}

public class GateServiceImpl implements GateService {
    @Override
    public ReleaseReceipt release(CargoId cargoId) {
        return ReleaseReceipt.open(cargoId);
    }
}
```

```java
// Teaching skeleton — Spring builds the industrial version for you
GateService target = new GateServiceImpl();

GateService proxy = (GateService) Proxy.newProxyInstance(
        GateService.class.getClassLoader(),
        new Class<?>[] { GateService.class },
        (proxyObj, method, args) -> {
            System.out.println("before " + method.getName());
            Object result = method.invoke(target, args);
            System.out.println("after " + method.getName());
            return result;
        });

ReleaseReceipt receipt = proxy.release(CargoId.of("C-902"));
```

`Proxy.newProxyInstance` needs a class loader, the interfaces to implement, and an `InvocationHandler`. Every interface method becomes `invoke` on the handler. Spring’s AOP runtime is that idea with an advisor chain, pointcut matching, and `ReflectiveMethodInvocation` calling `proceed` through interceptors — including transaction and security interceptors you did not author by hand.

Two families matter. If the bean exposes at least one interface, Spring may create a JDK dynamic proxy that implements those interfaces and delegates to the target. If the bean is a concrete class with no interface — or you force class-based proxies — Spring uses CGLIB to subclass the concrete type and override methods. Same idea for callers: talk to a wrapper. Different mechanics under the floor.

Why “dynamic”? The proxy class is generated as the context refreshes. You do not maintain `GateServiceProxy.java`. Auto-proxy creators wrap eligible beans when advisors match.

Operational consequences follow. Collaborators receive the proxy, which is what you want for advice to fire. Casting to the concrete impl can fail when the runtime chose a JDK interface proxy. Self-calls inside the target (`this.release(...)`) never enter the proxy, so annotated advice on that path is skipped. `@Async`, `@Transactional`, and custom `@Aspect` advice all share that requirement.

People sometimes imagine AOP as a compiler plugin rewriting every `.class`. Full AspectJ can weave that way. Spring AOP’s everyday path is proxy-based. Confusing the two leads to surprise when private methods or field access are not advised.

So the injected object for a transactional gate service is a proxy: interceptor logic first, then the target. The next split is which technology Spring picks — and what breaks when you assume the wrong one.

Start with the interface-based path: JDK Proxy.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 59 (*Dynamic Proxies*).
