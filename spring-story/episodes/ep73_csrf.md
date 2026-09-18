# Episode 73 — CSRF

| Field | Value |
|---|---|
| Episode | 73 |
| Title | CSRF |
| Phase | Phase 7 — Spring Security |
| Catalog handbook lesson | 73 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Method security answered domain rules for an already-authenticated principal. CSRF answers a browser-shaped attack that never needs to steal the password — it only needs the browser to attach cookies automatically.

Here is the forged-POST story. Alice is logged into `https://shop.example` with a session cookie. While her session is alive, she visits `https://evil.example`. That page contains a hidden form that POSTs to `https://shop.example/api/transfer` with Alice’s account numbers in the body. Alice’s browser sends the shop’s session cookie on that cross-site POST because that is how cookies work for the target domain. The shop server sees a authenticated session and executes the transfer. Alice never clicked "Transfer" on the real site. That is cross-site request forgery.

APIs that use `Authorization: Bearer` headers from JavaScript are usually not vulnerable in the same way — browsers do not auto-attach arbitrary bearer tokens the way they attach cookies. Cookie-session browser apps are the classic CSRF victims. Spring Security enables CSRF protection by default for browser-oriented configurations precisely because of that model.

The defense is a synchronizer token. The server issues a CSRF token bound to the session. Legitimate forms and AJAX calls from your origin include that token in a header or form field. The forged page on `evil.example` cannot read your token (same-origin policy). Spring’s `CsrfFilter` rejects state-changing requests that lack a valid token.

```java
@Bean
SecurityFilterChain browserApp(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf
            .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
        )
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}

// Legitimate page (same origin) includes token:
// <form method="post" action="/transfer">
//   <input type="hidden" name="_csrf" th:value="${_csrf.token}"/>
//   ...
// </form>
//
// Or AJAX:
//   headers: { "X-XSRF-TOKEN": readCookie("XSRF-TOKEN") }
//
// Forged evil.example POST /transfer with cookies attached but no valid CSRF token
//   → CsrfFilter → 403 Forbidden
```

Walk the denial: session cookie may be present; authentication may succeed; CSRF check still fails without the token. That ordering matters when you debug — you can be logged in and still get 403 on POST, PUT, PATCH, DELETE.

For pure stateless bearer-token APIs with no cookie session, teams often disable CSRF in the security DSL because the browser cookie attack does not apply. Disabling it on a Thymeleaf form-login app because "it was noisy in Postman" is how you reopen the forged-POST hole. Match the protection to the credential style.

SameSite cookie attributes reduce some CSRF variants but are not a complete replacement for token checks on sensitive actions, especially across older browsers and complex subdomain setups. Defense in depth: SameSite where appropriate, CSRF tokens for cookie sessions, and never rely on the UI alone.

A misconception is "CSRF is an XSS problem." They interact — XSS can steal tokens — but CSRF is specifically about abuse of ambient authority (cookies). Fixing XSS does not remove the need for CSRF tokens in cookie apps. Another misconception is protecting only `/login` — protect every state-changing endpoint that trusts the session.

Today we watched a cross-site forged POST ride a session cookie and saw Spring’s CSRF token stop it. Browsers bring another cross-origin concern that is not forgery of cookie POSTs but controlled access to your API from JavaScript on another origin. That policy surface is CORS.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 73 (*CSRF*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
