# Episode 74 — CORS

| Field | Value |
|---|---|
| Episode | 74 |
| Title | CORS |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 74 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

CSRF was about a browser silently using cookies against your harbor site. CORS is about a browser refusing to let JavaScript on one origin read responses from another — unless your API opts in. Different attack, different headers, different failure mode. Do not blur them.

Origins are scheme + host + port. `https://ops.example` and `https://api.example` are different origins. A SPA on the ops origin that calls `fetch('https://api.example/api/gates/status')` is cross-origin. Simple GETs may be sent, but the browser hides the response from JS unless the API returns the right `Access-Control-Allow-Origin` (and related) headers. For requests the browser classifies as “not simple” — custom headers like `Authorization`, JSON content types, or certain methods — the browser first sends a **preflight**: `OPTIONS` with `Access-Control-Request-Method` and `Access-Control-Request-Headers`. Your API must answer the preflight successfully before the real request runs.

Without CORS configuration, local development feels haunted: Postman works, curl works, the SPA console on `https://ops.example` shows a CORS error. Nothing is wrong with your controller mapping — the browser enforced the same-origin policy.

Spring MVC lets you declare CORS with `@CrossOrigin`, `WebMvcConfigurer#addCorsMappings`, or a `CorsConfigurationSource` bean. When Spring Security is on the classpath, you must also integrate CORS into the security filter chain — otherwise Security may reject or ignore the preflight before MVC’s CORS handling helps you.

```java
@Bean
SecurityFilterChain harborApi(HttpSecurity http) throws Exception {
    http
        .cors(Customizer.withDefaults())
        .csrf(csrf -> csrf.disable()) // bearer API example — not a CSRF fix via CORS
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
    return http.build();
}

@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://ops.example"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}

// Browser on https://ops.example:
//   1) OPTIONS https://api.example/api/gates/status
//      Access-Control-Request-Method: GET
//      Access-Control-Request-Headers: authorization, content-type
//   2) API responds 200 with
//      Access-Control-Allow-Origin: https://ops.example
//      Access-Control-Allow-Methods: ...
//      Access-Control-Allow-Headers: authorization, content-type
//   3) Real GET with Authorization: Bearer ... proceeds; JS may read the response
```

Narrate credentials carefully. If you set `Allow-Credentials: true`, you cannot use `Allow-Origin: *`. You must echo an explicit origin. Cookie-based SPAs and credentialed XHR need that pairing. Bearer-token SPAs often send `Authorization` explicitly and may not need cookies — still list `Authorization` in allowed headers so preflight passes.

CORS is not an authentication mechanism. Allowing `https://ops.example` does not authenticate the user. It only tells the browser which frontends may read responses. A non-browser client can still call your API; protect with authentication and authorization as before. CORS also does not stop CSRF — a forged cookie POST is a different problem with a different defense.

A misconception is fixing CORS by reflecting arbitrary `Origin` headers in production. Reflecting every origin with credentials is an open door. Another is confusing CORS errors with 401/403 from Spring Security — check the Network tab: failed preflight vs failed bearer validation look different. A third is “we enabled CORS, so CSRF is handled” — that blurs two distinct browser policies.

We have secured identity, access, tokens, methods, CSRF, and cross-origin browser access. Those behaviors are not scattered magic — they are ordered filters. The next episode names that chain and shows how a harbor request walks it.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 74 (*CORS*).
