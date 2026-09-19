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

URL matchers catch coarse gates: authenticated, has role ADMIN, permit health checks. They struggle with rules that need method arguments — “release this cargo only if the principal owns it,” “export the manifest only if the vessel id matches a claim.” Method security moves those decisions onto the service layer with the same `Authentication` you already established.

Spring enables it with `@EnableMethodSecurity` (modern) or older `@EnableGlobalMethodSecurity`. Under the hood, Spring AOP proxies the bean. Before the target method runs, an interceptor evaluates `@PreAuthorize`, `@PostAuthorize`, `@Secured`, or JSR-250 `@RolesAllowed`. SpEL expressions can reach `authentication`, method parameters by name, and beans you expose for custom checks.

For harbor gate release, ownership is the rule that path matchers cannot express cleanly.

```java
@Configuration
@EnableMethodSecurity
class MethodSecurityConfig {}

@Service
public class GateReleaseService {

    @PreAuthorize("hasRole('ADMIN') or @gateSecurity.isOwner(authentication, #cargoId)")
    public ReleaseReceipt releaseGate(CargoId cargoId) {
        return boom.open(cargoId);
    }

    @PostAuthorize("returnObject.ownerId == authentication.name or hasRole('ADMIN')")
    public CargoView getCargo(CargoId cargoId) {
        return cargo.findById(cargoId).orElseThrow();
    }
}

@Component("gateSecurity")
class GateSecurity {
    private final CargoRepository cargo;

    boolean isOwner(Authentication auth, CargoId cargoId) {
        return cargo.findById(cargoId)
            .map(c -> c.getOwnerId().equals(auth.getName()))
            .orElse(false);
    }
}

// Authenticated Alice (ROLE_USER), owns cargo C-42:
//   releaseGate(C-42) → @PreAuthorize true → method runs
// Authenticated Alice, cargo C-99 owned by Bob:
//   releaseGate(C-99) → @PreAuthorize false → AccessDeniedException → typically 403
```

`@PreAuthorize` runs before the call — use it to block work that should never start, like opening someone else’s boom. `@PostAuthorize` runs after and can veto based on the return value — useful for read paths where you load then confirm visibility, with care about side effects. `@PreFilter` / `@PostFilter` trim collections in place; know they mutate return values and can surprise callers.

Method security does not replace HTTP security. Filters still authenticate and apply path rules. Method rules add defense in depth and express domain authorization where the arguments live. If someone invokes `releaseGate` from a messaging listener or another bean inside the JVM, the HTTP matcher never ran — the method annotation still can, as long as the call goes through the Spring proxy. Self-invocation inside the same class bypasses the proxy, same AOP footgun you met earlier.

A misconception is annotating controllers only and believing services are safe when called from adapters. Put the rule on the service that owns the invariant when multiple entry points exist. Another is writing SpEL so complex nobody can audit it — extract `@gateSecurity.isOwner(...)` style beans so security reviews stay readable.

We can now deny an authenticated user on a specific business operation, not only on a URL prefix. Browser-based harbor consoles that use cookies for the session still have a different attack to respect: a forged request from another site that rides the user’s cookies to release cargo.

That attack is CSRF — and it needs its own defense, not another `@PreAuthorize`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 72 (*Method Security*).
