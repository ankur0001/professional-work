# Episode 68 — Authorization

| Field | Value |
|---|---|
| Episode | 68 |
| Title | Authorization |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 68 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Authentication told you the caller is Alice. Authorization decides whether Alice may touch this resource, with this method, right now.

Picture two authenticated users hitting the same API. Alice has role `ROLE_USER`. Bob has `ROLE_ADMIN`. Both send valid credentials. `GET /api/orders/42` should succeed for Alice if she owns order 42. `POST /api/admin/refunds` should succeed for Bob and return 403 for Alice — not 401. A 401 means "we do not know who you are." A 403 means "we know who you are, and you are not allowed." That distinction is the heartbeat of authorization debugging.

Before a central model, teams sprinkle `if (!user.isAdmin()) throw ...` through controllers and services. Rules drift. One endpoint checks a role string; another checks a group in LDAP; a third forgets the check entirely. The failure mode is not theoretical — it is an authenticated user reaching a destructive operation because the guard lived only on the UI.

Spring Security separates the concerns on purpose. Authentication fills the `SecurityContext`. Authorization consumes it. At the HTTP layer, `authorizeHttpRequests` (or older `authorizeRequests`) declares which paths need authentication, which roles, which authorities, or custom matchers. The decision runs in the filter chain — typically via `AuthorizationFilter` — before your controller method executes.

```java
@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth
        .requestMatchers("/api/public/**").permitAll()
        .requestMatchers(HttpMethod.GET, "/api/orders/**").hasAnyRole("USER", "ADMIN")
        .requestMatchers("/api/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated()
    );
    return http.build();
}

// Authenticated Alice (ROLE_USER) → POST /api/admin/refunds
// AuthorizationFilter: hasRole("ADMIN")? false → 403 Forbidden
//
// Authenticated Bob (ROLE_ADMIN) → POST /api/admin/refunds
// AuthorizationFilter: hasRole("ADMIN")? true  → controller runs
```

Read the denial path carefully. Alice is authenticated. The security context is populated. The matcher for `/api/admin/**` demands `ROLE_ADMIN`. Spring prefixes `ROLE_` when you use `hasRole("ADMIN")`. Alice lacks it, so the filter short-circuits with forbidden. Bob passes the same rule and reaches the refund controller. Same login machinery; different authorization outcome.

Authorities are the finer grain: strings like `orders:read` or `refunds:write` that you attach to the `Authentication`. Roles are a convention — authorities with a `ROLE_` prefix — not a separate type system. Prefer explicit authorities when product permissions do not map cleanly to a handful of roles. Prefer roles when the org already thinks in USER / ADMIN / SUPPORT.

URL rules are not the whole story. A path matcher cannot easily express "Alice may read only her own orders." Object-level rules need method security or a custom `AuthorizationManager` that loads the order and compares `order.getOwnerId()` to the principal. We will open method security soon. Today, own the HTTP decision: authenticated is not the same as authorized, and 401 is not the same as 403.

A common misunderstanding is enabling `anyRequest().authenticated()` and believing the app is locked down. That only requires a valid identity. Another is checking roles in the UI and assuming the API is safe — browsers are not your enforcement point. Enforce on the server, on every request that mutates or reveals data.

We established identity last episode. Today we enforced access on paths and saw an authenticated user correctly denied. APIs that span many services often stop carrying server sessions and start carrying signed claims instead. How do you authenticate and authorize with a token the client sends on every call?

That pressure leads straight into JWT.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 68 (*Authorization*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
