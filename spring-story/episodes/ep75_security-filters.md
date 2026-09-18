# Episode 75 — Security Filters

| Field | Value |
|---|---|
| Episode | 75 |
| Title | Security Filters |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 75 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Every security feature in this phase eventually lands in the same place: a filter chain that runs before your harbor controllers. If you can narrate that chain, configuration stops feeling like folklore.

Servlet containers have a filter chain. Spring Security installs `DelegatingFilterProxy` (named `springSecurityFilterChain`) into that chain. The proxy forwards to `FilterChainProxy`, which selects a `SecurityFilterChain` bean for the request — useful when you have separate chains for `/api/**` and browser ops consoles. Inside the chosen chain, a list of security filters runs in a deliberate order: channel security, CORS, CSRF, authentication mechanisms, session management, authorization, exception translation, and more.

Order is not academic. CORS must handle preflight early. CSRF must see the request before controllers mutate state. Authentication filters must populate the `SecurityContext` before authorization reads it. `ExceptionTranslationFilter` converts security exceptions into 401/403 responses or login redirects. Insert a custom filter in the wrong relative position and you will debug symptoms that look like “Spring is broken” when the chain is merely misordered.

```java
@Bean
@Order(1)
SecurityFilterChain harborApiChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/api/**")
        .cors(Customizer.withDefaults())
        .csrf(csrf -> csrf.disable())
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/admin/berths/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
    return http.build();
}

@Bean
@Order(2)
SecurityFilterChain harborBrowserChain(HttpSecurity http) throws Exception {
    http
        .securityMatcher("/**")
        .csrf(Customizer.withDefaults())
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/css/**").permitAll()
            .anyRequest().authenticated()
        )
        .formLogin(Customizer.withDefaults());
    return http.build();
}

// Conceptual walk for GET /api/gates/G-12/status with Bearer token:
// Servlet filter chain → DelegatingFilterProxy
//   → FilterChainProxy selects harborApiChain
//   → CorsFilter
//   → BearerTokenAuthenticationFilter (Authentication → SecurityContext)
//   → AuthorizationFilter (authenticated? scopes? admin berths?)
//   → ... → DispatcherServlet → controller
```

You can list the filters at runtime by enabling debug security or inspecting the chain bean — useful when a custom `OncePerRequestFilter` never fires. Relative placement APIs on `HttpSecurity` (`addFilterBefore`, `addFilterAfter`, `addFilterAt`) only make sense when you know the anchor filter’s job.

`SecurityContext` persistence deserves a beat. In classic servlet apps, persistence filters load and store context around the request, often tied to the HTTP session for form login. Stateless JWT APIs typically use a session-creation policy of stateless: authenticate from the bearer token every request, do not create an HTTP session. Mixing those modes accidentally is a common source of sticky sessions and surprising logouts on the harbor edge.

A misconception is treating `SecurityFilterChain` as “the servlet container’s only filters.” Your logging and correlation filters may still sit outside Spring Security. Another is adding ten custom filters that each re-parse the Authorization header — compose with providers and one authentication filter instead.

Phase 7 ends with a coherent servlet security story: credentials become `Authentication`, filters enforce CSRF/CORS/authorization, method security deepens domain rules. The stack so far assumes a thread-per-request servlet model. The next phase asks what changes when AIS vessel positions fan in faster than threads can wait — and why that model needs publishers instead of eager values.

That door is reactive programming.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 75 (*Security Filters*).
