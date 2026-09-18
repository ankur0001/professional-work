# Episode 72 — Method Security

| Field | Value |
|---|---|
| Episode | 72 |
| Title | Method Security |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 72 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

URL matchers catch coarse gates: authenticated, has role ADMIN, permit health checks. They struggle with rules that need the method arguments — "cancel this order only if the principal owns it," "export payroll only if the account id in the path matches a claim." Method security moves those decisions onto the service layer with the same `Authentication` you already established.

Spring enables it with `@EnableMethodSecurity` (modern) or older `@EnableGlobalMethodSecurity`. Under the hood, Spring AOP proxies the bean. Before the target method runs, an interceptor evaluates annotations like `@PreAuthorize`, `@PostAuthorize`, `@Secured`, or JSR-250 `@RolesAllowed`. SpEL expressions can reach `authentication`, method parameters by name, and beans you expose for custom checks.

```java
@Configuration
@EnableMethodSecurity
class MethodSecurityConfig {}

@Service
public class OrderService {

    @PreAuthorize("hasRole('ADMIN') or @orderSecurity.isOwner(authentication, #orderId)")
    public void cancel(long orderId) {
        // mutual fund / shop domain work
    }

    @PostAuthorize("returnObject.ownerId == authentication.name or hasRole('ADMIN')")
    public Order get(long orderId) {
        return repo.findById(orderId).orElseThrow();
    }
}

@Component("orderSecurity")
class OrderSecurity {
    private final OrderRepository repo;

    boolean isOwner(Authentication auth, long orderId) {
        return repo.findById(orderId)
            .map(o -> o.getOwnerId().equals(auth.getName()))
            .orElse(false);
    }
}

// Authenticated Alice (ROLE_USER), owns order 42:
//   cancel(42) → @PreAuthorize true → method runs
// Authenticated Alice, order 99 owned by Bob:
//   cancel(99) → @PreAuthorize false → AccessDeniedException → typically 403
```

`@PreAuthorize` runs before the call — use it to block work that should never start. `@PostAuthorize` runs after and can veto based on the return value — useful for read paths where you load then confirm visibility, with care about side effects. `@PreFilter` / `@PostFilter` trim collections in place; know they mutate return values and can surprise callers.

Method security does not replace HTTP security. Filters still authenticate and apply path rules. Method rules add defense in depth and express domain authorization where the arguments live. If someone invokes `OrderService.cancel` from a scheduled job or another bean inside the JVM, the HTTP matcher never ran — the method annotation still can, as long as the call goes through the Spring proxy. Self-invocation inside the same class bypasses the proxy, same AOP footgun you met earlier in the series.

A misconception is annotating controllers only and believing services are safe when called from messaging listeners or other adapters. Put the rule on the service that owns the invariant when multiple entry points exist. Another misconception is writing SpEL so complex nobody can audit it — extract `@orderSecurity.isOwner(...)` style beans so security reviews stay readable.

We can now deny an authenticated user on a specific business operation, not only on a URL prefix. Browser-based apps that use cookies for the session still have a different attack to respect: a forged request from another site that rides the user’s cookies. That attack is CSRF — and it needs its own defense, not another `@PreAuthorize`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 72 (*Method Security*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
