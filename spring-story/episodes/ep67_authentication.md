# Episode 67 — Authentication

| Field | Value |
|---|---|
| Episode | 67 |
| Title | Authentication |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 67 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A crane operator taps “release gate” on a handheld. The HTTP request carries a claim of identity: a session cookie from an earlier login, `Authorization: Basic ...`, or — more often for APIs — `Authorization: Bearer eyJ...`. Until something in your process turns that claim into a trusted principal, every downstream authorization rule is guessing. Authentication is that step: prove identity, then remember it for the rest of the request in the `SecurityContext`.

Without a shared mechanism, teams invent private patterns. One filter parses Basic auth. Another servlet reads a custom header. A controller hashes passwords with a hand-rolled salt. Session fixation, plaintext credentials in logs, and “forgot this endpoint” become weekly incidents. The question is not whether the harbor app should be secured. It is where identity gets established once so controllers can assume it.

Spring Security answers with a filter chain that runs before your controllers. Walk one crane-operator request as a sequence, not a class list.

`POST /api/gates/release` arrives with `Authorization: Basic Y3JhbmU6c2VjcmV0` (or a bearer token). The servlet container enters the `SecurityFilterChain`. A mechanism-specific filter — Basic, form-login, or bearer — extracts the claim from the request and builds an unauthenticated `Authentication` object (credentials present, `authenticated=false`). That filter asks the `AuthenticationManager` to authenticate the token. The manager does not check passwords itself; it delegates to an `AuthenticationProvider` that understands this kind of token — often a `DaoAuthenticationProvider` that loads `UserDetails` and verifies the password with a `PasswordEncoder`, or a JWT provider that validates a signature and claims. On success, the provider returns an authenticated `Authentication` (principal + authorities, `authenticated=true`). The filter stores it in the `SecurityContext`, held by `SecurityContextHolder` (typically thread-local on servlet apps). Downstream filters and the controller call `SecurityContextHolder.getContext().getAuthentication()` and know who is calling — without parsing headers again.

Say the flow once: request → security filter chain → authentication filter → `AuthenticationManager` → `AuthenticationProvider` → authenticated principal in `SecurityContext` → controller. Authorization comes later; this episode stops at “who is this?”

```java
@Bean
SecurityFilterChain craneApi(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf.disable()) // API example; browser apps need CSRF later
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .anyRequest().authenticated()
        )
        .httpBasic(Customizer.withDefaults());
    return http.build();
}

// Request: GET /api/me
// Header:  Authorization: Basic Y3JhbmU6c2VjcmV0
// After BasicAuthenticationFilter:
//   SecurityContext holds Authentication
//     principal = User(username=crane.ops, ...)
//     authenticated = true
```

That configuration says: health is open; everything else needs an authenticated principal. Basic auth is only one mechanism. The same `SecurityContext` contract works when credentials are a form POST, a session already established, or a bearer token validated elsewhere. Controllers should not re-implement login. They should consume the principal.

A topic-specific trap is conflating “the operator sent a password” with “the operator is authenticated.” Credentials on the wire are a claim. Authentication is successful verification of that claim and recording of the result. Another trap is stuffing identity checks into every service method by hand while leaving the HTTP layer wide open — or the reverse: locking HTTP and forgetting internal callers bypass the filter chain. Establish identity at the boundary you trust; propagate the principal inward.

So authentication is request-scoped identity: credentials or token in, verified `Authentication` in the `SecurityContext` out. Knowing who is calling is necessary — and still not enough. Alice and Bob can both authenticate and still disagree about `/admin/berths`.

That pressure is authorization.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 67 (*Authentication*).
