# Episode 71 — OpenID Connect

| Field | Value |
|---|---|
| Episode | 71 |
| Title | OpenID Connect |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 71 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

OAuth2 delegates access. It does not, by itself, define how a client learns the user’s identity in a standard way. OpenID Connect (OIDC) sits on top of OAuth2 and adds that identity layer.

The short version: OIDC keeps the authorization code flow you already know, and adds an **ID token** — a JWT that asserts who authenticated — plus a UserInfo endpoint for profile claims. Scopes like `openid`, `profile`, and `email` are the handshake that you want login, not only API access. If you request `openid`, a conformant provider returns an ID token alongside the access token.

Why teams care in Spring apps: you want "Sign in with Okta / Google / Azure AD" without inventing a proprietary profile JSON for every IdP. OIDC standardizes `sub`, `iss`, `aud`, `exp`, `nonce`, and optional profile claims. Your app verifies the ID token, establishes a local session or security context, and optionally still uses the access token to call APIs.

```java
@Bean
SecurityFilterChain oidcLogin(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/css/**", "/login").permitAll()
            .anyRequest().authenticated()
        )
        .oauth2Login(oauth2 -> oauth2
            .userInfoEndpoint(userInfo -> userInfo
                .oidcUserService(this.oidcUserService())
            )
        );
    return http.build();
}

private OAuth2UserService<OidcUserRequest, OidcUser> oidcUserService() {
    final OidcUserService delegate = new OidcUserService();
    return userRequest -> {
        OidcUser user = delegate.loadUser(userRequest);
        // ID token claims: sub, email, ...
        String email = user.getEmail();
        // Map IdP groups/roles → GrantedAuthority for your app
        Set<GrantedAuthority> mapped = mapAuthorities(user);
        return new DefaultOidcUser(mapped, user.getIdToken(), user.getUserInfo());
    };
}

// Browser flow (sketch):
// 1) GET /oauth2/authorization/okta
// 2) Redirect to IdP → user authenticates + consents (scope includes openid)
// 3) Callback with code → token endpoint returns access_token + id_token
// 4) Spring validates id_token (sig, iss, aud, exp, nonce) → OidcUser in SecurityContext
```

Hold the token types apart. The **ID token** is for the client application to know who logged in. The **access token** is for calling a resource server. Your SPA should not send the ID token as an API bearer credential just because it is also a JWT. Resource servers validate access tokens (and audience/scope). Login apps validate ID tokens.

Nonce and state are not decorative. State ties the callback to the browser session that started the redirect (CSRF-ish protection on the OAuth redirect). Nonce binds the ID token to that authentication attempt so replayed ID tokens are harder to abuse. Spring’s OAuth2 login support handles the common case when you use the client starter correctly — still know why those parameters exist when something fails in production.

A topic-specific misconception is saying "OIDC replaces OAuth2." It extends it. Another is assuming every JWT from the IdP is interchangeable: access tokens and ID tokens have different audiences and purposes. A third is mapping `email` to your local admin role without an explicit claim-to-authority policy — that is how contractors inherit god mode from a misconfigured IdP group.

So today we added identity assertions on top of delegation: `openid` scope, ID token validation, `OidcUser` in the security context, and a clear split between login tokens and API tokens. HTTP and login rules still live at the edge. Many domain rules — "only the owner may cancel this order" — want to sit next to the service method itself.

That is where method security earns its place.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 71 (*OpenID Connect*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
