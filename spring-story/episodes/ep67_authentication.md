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

You finished AOP with proxies and advice. Cross-cutting concerns are modular. Security is the next one that cannot stay as a few `if` checks scattered through controllers — because identity has to be established before business code runs, on every request, the same way.

A client hits your orders API. The HTTP request carries something that claims who they are: a session cookie from an earlier login, an `Authorization: Basic ...` header, or — more often in APIs — `Authorization: Bearer eyJ...`. Until something in your process turns that claim into a trusted principal, every downstream authorization rule is guessing. Authentication is that step: prove identity, then remember it for the rest of the request.

Without a shared mechanism, teams invent private patterns. One filter parses Basic auth. Another servlet reads a custom header. A controller method hashes passwords with a hand-rolled salt. Session fixation, plaintext credentials in logs, and "forgot to check on this endpoint" become weekly incidents. The question is not "should we secure the app?" It is "where does identity get established once, so controllers can assume it?"

Spring Security answers with a filter chain and an `AuthenticationManager`. On a typical form or HTTP-basic flow, a filter extracts credentials from the request, builds an unauthenticated `Authentication` token, and asks the manager to authenticate it. The manager delegates to one or more `AuthenticationProvider` implementations — often a `DaoAuthenticationProvider` that loads a `UserDetails` and checks a password with a `PasswordEncoder`. On success, the result is an authenticated `Authentication` stored in the `SecurityContext`, usually held by `SecurityContextHolder` on a `ThreadLocal` for servlet apps.

Walk one request out loud. `POST /api/orders` arrives with `Authorization: Bearer <access-token>`. A bearer-token filter (or resource-server filter) pulls the token from the header. A provider validates it and builds an `Authentication` whose principal might be a username or a JWT subject, with authorities derived from claims or a user store. That object goes into the `SecurityContext`. Later filters and the controller can call `SecurityContextHolder.getContext().getAuthentication()` and know who is calling — without parsing headers again.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf.disable()) // API example; browser apps need CSRF — later episode
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .anyRequest().authenticated()
        )
        .httpBasic(Customizer.withDefaults());
    return http.build();
}

// Request: GET /api/me
// Header:  Authorization: Basic YWxpY2U6c2VjcmV0
// After UsernamePasswordAuthenticationFilter / BasicAuthenticationFilter:
//   SecurityContext holds Authentication
//     principal = User(username=alice, ...)
//     authenticated = true
```

That configuration says: health is open; everything else needs an authenticated principal. Basic auth is only one mechanism. The same `SecurityContext` contract works when the credentials are a form POST, a session already established, or a bearer token validated elsewhere. Controllers should not re-implement login. They should consume the principal.

A topic-specific trap is conflating "the user sent a password" with "the user is authenticated." Credentials on the wire are a claim. Authentication is the successful verification of that claim and the recording of the result. Another trap is stuffing identity checks into every service method by hand while leaving the HTTP layer wide open — or the reverse: locking HTTP and forgetting that internal callers bypass the filter chain. Establish identity at the boundary you trust; propagate the principal inward.

So today we treated authentication as request-scoped identity: credentials or token in, verified `Authentication` in the `SecurityContext` out. Knowing *who* is calling is necessary — and still not enough. The next pressure is obvious: Alice is authenticated, Bob is authenticated, and both want `/admin/refunds`. Who is allowed?

That question is authorization.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 67 (*Authentication*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
