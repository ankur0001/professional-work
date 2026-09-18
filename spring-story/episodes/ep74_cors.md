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

CSRF was about a browser silently using cookies against your site. CORS is about a browser *refusing* to let JavaScript on one origin read responses from another — unless your API opts in.

Origins are scheme + host + port. `https://app.example` and `https://api.example` are different origins. A SPA on the app origin that calls `fetch('https://api.example/orders')` is cross-origin. Simple GETs may be sent, but the browser hides the response from JS unless the API returns the right `Access-Control-Allow-Origin` (and related) headers. For requests that the browser classifies as "not simple" — custom headers like `Authorization`, JSON content types, or certain methods — the browser first sends a **preflight**: `OPTIONS` with `Access-Control-Request-Method` and `Access-Control-Request-Headers`. Your API must answer the preflight successfully before the real request runs.

Without CORS configuration, local development feels haunted: Postman works, curl works, the SPA console shows a CORS error. Nothing is wrong with your controller mapping — the browser enforced the same-origin policy.

Spring MVC lets you declare CORS with `@CrossOrigin`, `WebMvcConfigurer#addCorsMappings`, or a `CorsConfigurationSource` bean. When Spring Security is on the classpath, you must also integrate CORS into the security filter chain — otherwise Security may reject or ignore the preflight before MVC’s CORS handling helps you.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http
        .cors(Customizer.withDefaults())
        .csrf(csrf -> csrf.disable()) // bearer API example
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
    return http.build();
}

@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}

// Browser on https://app.example:
//   1) OPTIONS https://api.example/api/orders
//      Access-Control-Request-Method: POST
//      Access-Control-Request-Headers: authorization, content-type
//   2) API responds 200 with
//      Access-Control-Allow-Origin: https://app.example
//      Access-Control-Allow-Methods: ...
//      Access-Control-Allow-Headers: authorization, content-type
//   3) Real POST with Authorization: Bearer ... proceeds; JS may read the response
```

Narrate credentials carefully. If you set `Allow-Credentials: true`, you cannot use `Allow-Origin: *`. You must echo an explicit origin. Cookie-based SPAs and credentialed XHR need that pairing. Bearer-token SPAs often send `Authorization` explicitly and may not need cookies — still list `Authorization` in allowed headers so preflight passes.

CORS is not an authentication mechanism. Allowing an origin does not authenticate the user. It only tells the browser which frontends may read responses. A non-browser client can still call your API; protect with authentication and authorization as before.

A misconception is fixing CORS by disabling browser security or reflecting arbitrary `Origin` headers in production. Reflecting every origin with credentials is an open door. Another is confusing CORS errors with 401/403 from Spring Security — check the Network tab: failed preflight vs failed bearer validation look different.

We have now secured identity, access, tokens, methods, CSRF, and cross-origin browser access. Those behaviors are not scattered magic — they are ordered filters. The next episode names that chain and shows how a request walks it.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 74 (*CORS*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
