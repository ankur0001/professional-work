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

When Spring says it will run your advice around a service method, it does not sprinkle invisible hooks into the class file by default. It hands out a different object than the one you wrote — an object that looks like your bean to callers, holds a reference to the real instance, and decides what to do when a method is invoked. That stand-in is a proxy. Dynamic proxies are built at runtime, not handwritten as `FooProxy extends Foo` for every type in the app.

Without a proxy, AOP has no place to stand. A client calls `billingService.charge(…)`. If `billingService` is the raw target, your `@Around` never runs. If `billingService` is a proxy, the call enters the proxy’s invocation handler, the interceptor chain runs matching advice, and only then does `proceed` reach the target method.

```java
public interface PricingService {
    Quote quote(Sku sku, int qty);
}

public class PricingServiceImpl implements PricingService {
    @Override
    public Quote quote(Sku sku, int qty) {
        return Quote.of(sku, qty * 10);
    }
}
```

```java
// Illustrative: JDK dynamic proxy shape (Spring builds this for you)
PricingService target = new PricingServiceImpl();

PricingService proxy = (PricingService) Proxy.newProxyInstance(
        PricingService.class.getClassLoader(),
        new Class<?>[] { PricingService.class },
        (proxyObj, method, args) -> {
            System.out.println("before " + method.getName());
            Object result = method.invoke(target, args);
            System.out.println("after " + method.getName());
            return result;
        });

Quote q = proxy.quote(Sku.of("ABC"), 3); // advice runs; target.quote does the math
```

That JDK snippet is the teaching skeleton. `Proxy.newProxyInstance` needs a class loader, the interfaces to implement, and an `InvocationHandler`. Every interface method call becomes `invoke` on the handler. Spring’s AOP runtime is the industrial version of this idea: an advisor chain, pointcut matching, `ReflectiveMethodInvocation` calling `proceed` through interceptors — including transaction and security interceptors you did not author by hand.

Two proxy families matter inside Spring. If the bean exposes at least one interface, Spring may create a JDK dynamic proxy that implements those interfaces and delegates to the target. If the bean is a concrete class with no interface — or you force class-based proxies — Spring uses CGLIB to subclass the concrete type and override methods. Same idea from the caller’s perspective: you talk to a wrapper. Different mechanics under the floor.

Why “dynamic”? Because the proxy class is synthesized at runtime. You do not maintain `PricingServiceProxy.java`. The JVM (or CGLIB’s generator) creates the type as the context refreshes and eligible beans are wrapped by auto-proxy creators.

Operational consequences follow. The object injected into collaborators is the proxy, not the raw target — which is what you want for advice to fire. Casting the injected bean to a concrete class can fail when the runtime chose a JDK interface proxy. Self-calls inside the target (`this.helper()`) never enter the proxy, so annotated advice on `helper` is skipped. `@Async`, `@Transactional`, and custom `@Aspect` advice all share that proxy requirement.

People sometimes imagine AOP as a compiler plugin rewriting every `.class` in `target/`. Full AspectJ can weave that way. Spring AOP’s everyday path is proxy-based. Confusing the two leads to surprise when private methods or field access are not advised.

So a proxy is the runtime seat of Spring AOP: an object in front of your bean that runs interceptor logic, then delegates. The next split is which proxy technology Spring picks — and what breaks when you assume the wrong one.

Start with the interface-based path: JDK Proxy.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 59 (*Dynamic Proxies*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
