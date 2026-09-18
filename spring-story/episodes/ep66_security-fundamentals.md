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

Ship a harbor API on the public internet and the first reviewer question is not about JPA mappings. It is: who can call `/gates/release`? Controllers, repositories, and transactions can all be correct while the door stays open. Security fundamentals are the shared vocabulary for closing that door without scattering `if (user == null)` through every method.

Two questions appear on every request, and they are not the same. First: who is calling? That is authentication — establishing identity. Second: given that identity, may they perform this action on this resource? That is authorization. Teams that blur the words build filters that “check the token” and then forget ownership, or build role checks with no trustworthy identity behind them. On the quay that confusion shows up as a trucker JWT that validates, yet still releases cargo that belongs to another carrier, or as an admin berth UI that only checked “logged in” and never “is ADMIN.”

Spring Security models the pipeline as a filter chain in front of your servlets (and a WebFilter chain for WebFlux later). A request enters. Filters may attempt authentication, build a `SecurityContext`, enforce authorization rules, handle logout, or reject the call before a controller runs. When authentication succeeds, the context holds an `Authentication` — principal, authorities, authenticated flag — typically stored via `SecurityContextHolder` on a thread for servlet apps. Controllers and `@PreAuthorize` methods read that context; they should not invent a parallel “current user” stash in a request attribute unless you have a deliberate reason and a clear owner for clearing it.

```java
@Bean
SecurityFilterChain harborApi(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf.disable()) // token API sketch; browser apps revisit CSRF
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        .httpBasic(Customizer.withDefaults());
    return http.build();
}
```

Read that as policy, not decoration. Health may stay public for probes — Kubernetes needs a cheap answer without credentials. Admin berth routes demand an admin role; Spring’s `hasRole("ADMIN")` expects authority `ROLE_ADMIN`. Everything else demands an authenticated principal. Walk a failure: an anonymous `POST /gates/G12/check-ins` never reaches `GateController`. The authorization filter short-circuits with `401` (or a challenge, depending on the entry point). An authenticated crane operator without `ROLE_ADMIN` hitting `/api/admin/berths` gets `403` — identity existed; permission did not. That distinction is the whole point of separating authn from authz. A controller for gate status can then assume identity already exists — or it should not be public.

Runtime symptoms when the vocabulary is wrong: actuators open on the public gateway because someone copied `permitAll` too widely; Basic auth left on for browsers that needed CSRF; method security enabled in config but never annotated, so “we thought services were protected”; or a custom filter that sets a principal but forgets `SecurityContextHolder.clearContext()` on the thread pool path and leaks identity across requests. Those are not exotic exploits. They are everyday miswirings that fundamentals language helps you name in review.

A misconception that shows up early: “Spring Security is just annotations.” Method security matters, but the foundation is the filter chain and the security context. Another: enabling default form login means the harbor API is safe. Defaults are a starting point, not a threat model. You still decide which paths are public, how credentials are presented, where passwords live, and how sessions or tokens travel. A third: treating “HTTPS at the load balancer” as application authorization. TLS protects the pipe; it does not decide whether Alice may release Bob’s container.

Trade-offs sit in the open once vocabulary is shared. Session cookies fit browser ops consoles and force CSRF discipline. Stateless bearer tokens fit trucker mobile clients and force careful validation and expiry. Coarse URL rules are fast to audit; fine-grained ownership checks need method security or domain checks inside the use case. Pick deliberately per surface — public gate API versus internal berth admin — instead of one default for the whole harbor.

Once the vocabulary is clear — authentication versus authorization, filters versus controllers, security context versus ad-hoc request attributes — the engineering problem is unavoidable. How does a request actually prove identity for a crane operator? Basic credentials? A form login? A bearer token?

That is where authentication mechanisms begin.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 66 (*Security Fundamentals*).
