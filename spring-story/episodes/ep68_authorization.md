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

Authentication told you the caller is Alice. Authorization decides whether Alice may touch this berth admin route, with this method, right now.

Picture two authenticated harbor users. Alice has role `ROLE_USER` — a clerk on the yard floor. Bob has `ROLE_ADMIN` — operations lead. Both send valid credentials. `GET /api/gates/status` may succeed for Alice. `GET /api/admin/berths` must succeed for Bob and return 403 for Alice — not 401. A 401 means “we do not know who you are.” A 403 means “we know who you are, and you are not allowed.” That distinction is the heartbeat of authorization debugging on admin berth routes.

Before a central model, teams sprinkle `if (!user.isAdmin()) throw ...` through controllers. Rules drift. One endpoint checks a role string; another checks an LDAP group; a third forgets the check. The failure mode is an authenticated clerk reaching a destructive berth reassignment because the guard lived only on the UI.

Spring Security separates the concerns on purpose. Authentication fills the `SecurityContext`. Authorization consumes it. At the HTTP layer, `authorizeHttpRequests` declares which paths need authentication, which roles, which authorities, or custom matchers. The decision runs in the filter chain — typically via `AuthorizationFilter` — before your controller method executes.

```java
@Bean
SecurityFilterChain harborApp(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth
        .requestMatchers("/api/public/**").permitAll()
        .requestMatchers(HttpMethod.GET, "/api/gates/**").hasAnyRole("USER", "ADMIN")
        .requestMatchers("/api/admin/berths", "/api/admin/berths/**").hasRole("ADMIN")
        .anyRequest().authenticated()
    );
    return http.build();
}

// Authenticated Alice (ROLE_USER) → GET /api/admin/berths
// AuthorizationFilter: hasRole("ADMIN")? false → 403 Forbidden
//
// Authenticated Bob (ROLE_ADMIN) → GET /api/admin/berths
// AuthorizationFilter: hasRole("ADMIN")? true  → controller runs
```

Read the denial path carefully. Alice is authenticated. The security context is populated. The matcher for the admin berth route demands `ROLE_ADMIN`. Spring prefixes `ROLE_` when you use `hasRole("ADMIN")`. Alice lacks it, so the filter short-circuits with forbidden. Bob passes the same rule and reaches the berth admin controller. Same login machinery; different authorization outcome.

Authorities are the finer grain: strings like `berths:write` or `gates:release` attached to the `Authentication`. Roles are a convention — authorities with a `ROLE_` prefix — not a separate type system. Prefer explicit authorities when product permissions do not map cleanly to a handful of roles. Prefer roles when the org already thinks in USER / ADMIN / SUPPORT.

URL rules are not the whole story. A path matcher cannot easily express “Alice may release only cargo she owns.” Object-level rules need method security or a custom `AuthorizationManager`. We will open method security soon. Today, own the HTTP decision: authenticated is not authorized, and 401 is not 403.

A common misunderstanding is enabling `anyRequest().authenticated()` and believing admin berths are locked down. That only requires a valid identity. Another is checking roles in the UI and assuming the API is safe — browsers are not your enforcement point. Enforce on the server, on every request that mutates or reveals berth data.

We established identity last. Today Alice is correctly denied and Bob is allowed on `/admin/berths`. APIs that span mobile clients often stop carrying server sessions and start carrying signed claims instead.

That pressure leads into JWT.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 68 (*Authorization*).
