# Episode 82 — Reactive Security

| Field | Value |
|---|---|
| Episode | 82 |
| Title | Reactive Security |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 82 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

WebFlux changed the HTTP engine under `/positions/stream`. Spring Security still has to authenticate and authorize — but it cannot assume `ThreadLocal` and servlet filters the way the MVC chain did. Reactive security adapts the same ideas to WebFlux’s `WebFilter` chain and a context that rides with the reactive subscription — including JWT validation on that chain for harbor APIs.

In servlet apps, `SecurityContextHolder` defaulted to `ThreadLocal` storage. In WebFlux, the security context is typically stored in Reactor’s `Context` and retrieved with reactive adapters so it survives thread hops from `publishOn` / Netty event loops. You configure a `SecurityWebFilterChain` instead of a servlet `SecurityFilterChain`. Method security has reactive-aware expressions when return types are publishers.

```java
@Bean
SecurityWebFilterChain harborReactiveSecurity(ServerHttpSecurity http) {
    return http
        .csrf(ServerHttpSecurity.CsrfSpec::disable) // bearer API example
        .authorizeExchange(ex -> ex
            .pathMatchers("/actuator/health").permitAll()
            .pathMatchers("/api/admin/**").hasRole("ADMIN")
            .pathMatchers("/positions/stream").hasAuthority("SCOPE_ais.read")
            .anyExchange().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
        .build();
}

@GetMapping("/api/me")
Mono<Map<String, Object>> me(@AuthenticationPrincipal Mono<Jwt> jwt) {
    return jwt.map(token -> Map.of(
        "sub", token.getSubject(),
        "scopes", token.getClaimAsStringList("scope")
    ));
}

// Request: GET /positions/stream?quayId=7
// Header:  Authorization: Bearer <jwt>
// AuthenticationWebFilter / JWT decoder validates → reactive SecurityContext
// AuthorizationWebFilter checks exchange matchers → handler Flux runs
```

Mirror the earlier JWT walk, now on the reactive chain: bearer token extracted, decoded without blocking the event loop, authentication placed in Reactor context, authorization decision on the exchange, then the controller’s `Flux` streams positions. CSRF and form login exist for browser-oriented WebFlux apps too — use cookie sessions only when you accept the same CSRF obligations you learned on the servlet side.

Watch blocking habits. A custom `ReactiveAuthenticationManager` that calls blocking JDBC inside `authenticate` without `subscribeOn(boundedElastic)` will stall the event loop under AIS load. Prefer reactive user stores or explicit offloads. Similarly, `@PreAuthorize` on methods returning `Mono` / `Flux` must use reactive method-security support so the decision participates in the publisher chain instead of blocking for a context that is not on the thread.

A misconception is copying a servlet `HttpSecurity` config class into a WebFlux project unchanged — types differ (`ServerHttpSecurity`, `authorizeExchange`). Another is reading `SecurityContextHolder.getContext()` imperatively inside a WebFlux handler after a thread hop and wondering why it is empty — use reactive context propagation and `@AuthenticationPrincipal Mono<...>`. A third is assuming JWT on WebFlux is “just a filter bean” with no context story — without Reactor context, identity vanishes across schedulers.

Phase 8 closes the reactive web and security loop: publishers, WebFlux, and a filter chain that respects Reactor’s context with JWT. Many production harbor systems are not one reactive service — they are many deployables that must discover each other, share config, and fail partially without taking the whole product down.

That organizational jump is microservices with Spring.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 82 (*Reactive Security*).
