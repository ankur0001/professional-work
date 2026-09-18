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

If your bean type is an interface, the JDK already has a built-in way to wrap it. `java.lang.reflect.Proxy` can implement that interface at runtime and funnel every call through one `InvocationHandler`. Spring AOP leans on that when it decides an interface-based proxy is enough. No subclass of your concrete class. A brand-new class that only promises the interface methods.

Why start here? Because interface-oriented design and JDK proxies fit together cleanly. You program to `NotificationGateway`, inject `NotificationGateway`, and Spring can substitute a proxy that still is-a `NotificationGateway`. Callers never need the concrete class.

```java
public interface NotificationGateway {
    void send(UserId userId, String template, Map<String, String> vars);
}

@Service
public class EmailNotificationGateway implements NotificationGateway {

    private final EmailClient emailClient;

    public EmailNotificationGateway(EmailClient emailClient) {
        this.emailClient = emailClient;
    }

    @Override
    public void send(UserId userId, String template, Map<String, String> vars) {
        emailClient.dispatch(userId, template, vars);
    }
}
```

```java
@Aspect
@Component
public class NotificationMetricsAspect {

    @Around("execution(* com.example.notify.NotificationGateway.send(..))")
    public Object timeSend(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            Metrics.timer("notification.send")
                    .record(System.nanoTime() - start, TimeUnit.NANOSECONDS);
        }
    }
}
```

In this setup, collaborators depend on `NotificationGateway`. At runtime the injected object is often a JDK proxy implementing `NotificationGateway`, holding `EmailNotificationGateway` as the target. `send` enters the proxy, the metrics `@Around` runs, `proceed` hits `EmailNotificationGateway.send`. The concrete class is never the type of the injected field — and that is fine.

Contrast this with a mistake teams make: injecting or casting to `EmailNotificationGateway` while Spring published a JDK proxy. The proxy is not an instance of `EmailNotificationGateway`. It implements the interface only. `instanceof EmailNotificationGateway` is false. `(EmailNotificationGateway) bean` throws `ClassCastException`. Prefer the interface type everywhere you inject.

JDK proxies can implement multiple interfaces. If your bean implements `NotificationGateway` and `HealthIndicator`, the proxy can expose both. Only interface methods are advised through this mechanism — there is no “class method” on a JDK proxy beyond what the interfaces declare. Final methods on the concrete class are irrelevant to the proxy type because callers should not see the concrete class through the proxy reference.

Spring’s selection rule of thumb: when the target implements interfaces, JDK proxy is eligible. You can force class-based proxies with `spring.aop.proxy-target-class=true` or `@EnableAspectJAutoProxy(proxyTargetClass = true)`, which pushes you toward CGLIB even when interfaces exist. Boot’s defaults have shifted over versions toward class proxies in many apps — so always verify what you actually get instead of assuming a textbook JDK proxy.

Debugging tip: log `AopUtils.isJdkDynamicProxy(bean)` and `AopUtils.isCglibProxy(bean)`, or inspect the class name — JDK proxies often look like `$Proxy12`. Seeing `$Proxy` in a stack trace is a clue you are in interface-proxy land.

The limitation is the point of the next episode. What if there is no interface? What if the bean is a concrete `@Service` class injected by its class type? JDK `Proxy` cannot subclass that concrete type. You need a different machinery that generates a subclass at runtime.

That machinery is CGLIB.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 60 (*JDK Proxy*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
