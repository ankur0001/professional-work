# Episode 66 — Security Fundamentals

| Field | Value |
|---|---|
| Episode | 66 |
| Title | Security Fundamentals |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 66 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You can build MVC controllers, JPA repositories, and transactional services and still ship an open door. A `GET /orders/42` that anyone on the network can call is not "done." Security fundamentals are the shared vocabulary for closing that door without scattering `if (user == null)` checks through every method.

Start from a concrete request. A browser or mobile client hits your API. Two questions appear immediately, and they are not the same question. First: who is calling? That is authentication — establishing identity. Second: given that identity, may they perform this action on this resource? That is authorization. Teams that blur the two words build filters that "check the token" and then forget to check ownership, or build role checks with no trustworthy identity behind them.

Spring Security models that pipeline as a filter chain in front of your servlets (and a WebFilter chain for WebFlux later). A request enters the chain. Filters may attempt authentication, build a `SecurityContext`, enforce authorization rules, handle logout, or reject the call before a controller runs. When authentication succeeds, the context holds an `Authentication` object — principal, authorities, and authenticated flag — typically stored in a `SecurityContextHolder` strategy bound to the thread for servlet apps.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf.disable()) // example API; revisit CSRF for browsers
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        .httpBasic(Customizer.withDefaults());
    return http.build();
}
```

Read that as policy, not as decoration. `/actuator/health` may be public for probes. `/api/admin/**` demands an admin role. Everything else demands an authenticated principal. The controller for `/api/orders/42` can then assume identity already exists — or it should not be public.

A misconception that shows up early: "Spring Security is just annotations." Annotations and method security matter, but the foundation is the filter chain and the security context. Another misconception: enabling a default form login means the API is safe. Defaults are a starting point, not a threat model. You still decide which paths are public, how credentials are presented, where passwords are stored, and how sessions or tokens travel.

Once the vocabulary is clear — authentication versus authorization, filters versus controllers, security context versus ad-hoc request attributes — the next engineering problem is unavoidable. How does a request actually prove identity? Cookies? Basic credentials? A bearer token? That is where authentication mechanisms begin.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 66 (*Security Fundamentals*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
