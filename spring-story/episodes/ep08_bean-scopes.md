# Episode 08 — Bean Scopes

| Field | Value |
|---|---|
| Episode | 08 |
| Title | Bean Scopes |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 8 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Bean definitions tell Spring what to build. They also need to say how long each instance should live — and how widely it should be shared.

Here is a bug that teaches scope better than a definition list. A team stores the current user's cart on a `@Component` service field. In development, one tester clicks around and everything looks fine. In production, two customers share a JVM. Cart lines bleed across sessions. Someone "fixed" it with `synchronized`, which only serialized the corruption. The object was a singleton — one instance for the whole container — pretending to be per-user state.

What goes wrong without scopes is lifetime mismatch. Stateless services want one shared instance. Per-request scratchpads want a fresh object each HTTP call. Rare cases want a new instance every injection. If everything is accidentally singleton, mutable state becomes a cross-talk hazard. If everything is prototype, you waste memory and lose shared caches you actually needed.

So the engineer asks: how does Spring control whether a definition yields one shared object or many?

That control is bean scope. The default scope is singleton: one shared instance per container for that definition. Prototype creates a new instance every time the bean is retrieved or injected. In web-aware contexts, request scope gives one instance per HTTP request, session scope one per HTTP session, and application scope one per `ServletContext`. Spring also supports custom scopes when you need conversation or tenant boundaries.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST,
       proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestCart {
    private final List<LineItem> lines = new ArrayList<>();

    public void add(LineItem item) {
        lines.add(item);
    }

    public List<LineItem> lines() {
        return List.copyOf(lines);
    }
}

@Service
public class CheckoutFacade {
    private final RequestCart cart; // injected singleton-safe via scoped proxy

    public CheckoutFacade(RequestCart cart) {
        this.cart = cart;
    }

    public void addItem(LineItem item) {
        cart.add(item);
    }
}
```

Watch what happens at runtime. `CheckoutFacade` is a singleton, created once at startup. It cannot hold a raw request-scoped object created at startup — that request does not exist yet. Spring injects a scoped proxy instead. On each HTTP request, method calls on `cart` delegate to the `RequestCart` instance bound to that request. Customer A's `add` never touches Customer B's list. When the request ends, the request-scoped bean is discarded. Scope just saved you from shared mutable state without forcing `CheckoutFacade` itself to become request-scoped.

Choose scopes with intent. Prefer singleton for thread-safe, stateless services and shared expensive resources like connection pools. Use request or session only for state that truly follows the web lifecycle. Use prototype sparingly — and remember a hard edge: when a singleton depends on a prototype without a proxy or `ObjectFactory`/`Provider`, it may capture one prototype instance at injection time and never see a fresh one again.

A scope-specific misconception is "prototype means Spring destroys the instance for me." It does not fully manage prototype destruction the way it manages singleton destroy callbacks; you are closer to owning cleanup. Another is marking everything request-scoped "to be safe," which multiplies objects and breaks non-web use of the same types.

Scope answers how many instances and for how long they are visible. It does not answer what Spring calls on the way in and out of that life — init hooks, post-processors, destroy callbacks. When your bean opens a file handle or registers a listener, you need the lifecycle sequence next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 8 (*Bean Scopes*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
