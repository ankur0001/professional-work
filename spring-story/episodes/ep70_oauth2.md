# Episode 70 — OAuth2

| Field | Value |
|---|---|
| Episode | 70 |
| Title | OAuth2 |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 70 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

JWT told you how a resource server trusts a bearer token. OAuth2 answers a different question: how did the client get permission to hold that token in the first place?

Think about a calendar app that wants to read a user’s Google events. You do not want the calendar app to collect the Google password. You want the user to log in at Google, approve a scope like `calendar.readonly`, and send the calendar app an access token that represents that limited grant. OAuth2 is that delegation protocol. Roles have names: resource owner (the user), client (the app), authorization server (issues tokens), resource server (accepts tokens).

The authorization code flow is the one you should be able to narrate for browser and confidential clients. The client redirects the user to the authorization server with client id, redirect URI, scopes, and a state value. The user authenticates and consents. The authorization server redirects back with a short-lived code. The client exchanges that code — plus its client secret, for confidential clients — at the token endpoint for an access token (and often a refresh token). The client then calls APIs with `Authorization: Bearer ...`. PKCE adds a code challenge so public clients (mobile, SPA) are safer even without a secret.

Spring Security supports both sides you usually build. As a **resource server**, you validate access tokens — the JWT path from the previous episode, or opaque token introspection. As an **OAuth2 client**, Boot can drive the redirect, code exchange, and authorized `WebClient` / RestClient calls. As an **authorization server**, Spring Authorization Server is a separate project when you issue tokens yourself instead of buying Okta, Auth0, Keycloak, or a cloud IdP.

```java
@Bean
SecurityFilterChain clientApp(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/", "/error").permitAll()
            .anyRequest().authenticated()
        )
        .oauth2Login(Customizer.withDefaults())       // sign-in via IdP
        .oauth2Client(Customizer.withDefaults());     // outbound token use
    return http.build();
}

// application.yml (client registration sketch)
// spring:
//   security:
//     oauth2:
//       client:
//         registration:
//           google-calendar:
//             provider: google
//             client-id: ${GOOGLE_CLIENT_ID}
//             client-secret: ${GOOGLE_CLIENT_SECRET}
//             scope: openid, profile, email, https://www.googleapis.com/auth/calendar.readonly
//             redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
```

When the user hits a protected page, `oauth2Login` sends them to the provider. After callback success, Spring establishes a local `Authentication` (often an `OAuth2AuthenticationToken`) and can store authorized client tokens for later API calls. Separately, your API microservice might only enable `oauth2ResourceServer` and never redirect browsers at all — it only trusts bearer tokens. Pick the hat your process is wearing.

Grant types matter in interviews and in production. Authorization code (+ PKCE) for user-delegated access. Client credentials when a service talks to another service with no user present — the token represents the client, not Alice. Implicit and password grants are legacy for most new work; prefer code + PKCE or client credentials.

A frequent misunderstanding is treating "we added oauth2Login" as the same as securing a JSON API for mobile. Login redirect flows are for interactive clients. Machine APIs usually want resource-server validation of access tokens. Another misunderstanding is confusing the access token with proof of *who the user is* for your own profile screen — access tokens authorize API calls; identity claims for login UX are the OpenID Connect layer we open next.

Today we placed JWT inside a protocol: clients obtain tokens through redirects and token endpoints; resource servers consume them; scopes limit the grant. The remaining gap is login itself — when you need a standardized ID token that says "this browser session is Alice," not only "this client may call these APIs."

That is OpenID Connect.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 70 (*OAuth2*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
