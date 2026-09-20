# Episode 69 — JWT

| Field | Value |
|---|---|
| Episode | 69 |
| Title | JWT |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 69 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Truckers do not live inside your VPN. Their mobile app hits the harbor API from a highway shoulder, proves identity without a sticky HTTP session store shared across pods, and moves on. Session cookies that assume one browser and one server get awkward fast. A common answer is a bearer token — and the usual format is JWT.

A JSON Web Token is three Base64url segments: header, payload, signature. The payload carries claims — subject, expiry, issuer, scopes, custom fields like trucker id. The signature binds those claims to a key so a resource server can validate the token without calling the issuer on every request. That is the appeal and the danger: validation is local and fast, but a leaked token is a stolen identity until it expires.

Spring Security’s OAuth2 Resource Server support treats JWTs as first-class credentials. On each request, a filter looks for `Authorization: Bearer ...`, parses the JWT, validates signature and claims, and builds an `Authentication` — often a `JwtAuthenticationToken` — into the `SecurityContext`. Authorization rules then run against authorities mapped from scopes or roles in the token.

```java
@Bean
SecurityFilterChain truckerApi(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/admin/**").hasAuthority("SCOPE_admin")
            .requestMatchers("/api/gates/**").hasAuthority("SCOPE_gates.write")
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
    return http.build();
}

// spring.security.oauth2.resourceserver.jwt.jwk-set-uri=
//   https://issuer.harbor.example/.well-known/jwks.json

// Incoming request from mobile app
//   GET /api/gates/G-12/status
//   Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.<payload>.<sig>
//
// BearerTokenAuthenticationFilter → JwtDecoder.decode(token)
//   verify signature with JWK set
//   check exp / iss / aud as configured
//   map scope → SCOPE_gates.write
// SecurityContext ← JwtAuthenticationToken(principal=Jwt, authorities=...)
```

Narrate failure modes as carefully as the happy path. Missing header → 401. Malformed JWT → 401. Bad signature → 401. Expired `exp` → 401. Valid token but wrong scope for `/api/admin/**` → 403. Those statuses still mean what they meant in authorization; only the credential shape changed.

Do not treat JWTs as encrypted blobs. The payload is readable to anyone who holds the token. Put secrets in the token only if you accept that readers can see them — which means do not. Prefer opaque references or short-lived access tokens with minimal claims. Rotate signing keys through a JWKS endpoint so resource servers refresh keys without redeploy theater.

A topic-specific misconception is “we use JWT, so we are doing OAuth2.” JWT is a token format. OAuth2 is a delegation protocol that often issues JWTs as access tokens. You can validate JWTs without the full OAuth2 dance, and you can run OAuth2 with opaque tokens. Another misconception is stuffing every trucker attribute into the access token until it rivals a session record — then wondering why logout and permission changes feel impossible. Short TTL plus refresh (when you have a real authorization server) beats a forever token with a giant claim set.

The bearer path is now concrete: `Authorization` header → parse → signature and claim checks → `SecurityContext` → authority matchers. Format alone does not finish the story. Who issues these tokens? How does a trucker consent? How does a client obtain them without embedding passwords?

That is the OAuth2 conversation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 69 (*JWT*).
