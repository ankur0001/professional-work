# Episode 76 — Spring Security

| Field | Value |
|---|---|
| Episode | 76 |
| Title | Spring Security |
| Catalog handbook column | 76 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Your API can create orders and read users. Then someone asks, "Who is allowed to call this?" Security is not a controller `if` you remember to paste. In Spring, security is a filter chain — requests pass through filters that authenticate and authorize before your controller runs. Authentication asks who you are. Authorization asks what you can do. Never invent crypto for passwords or tokens when maintained libraries exist.

```java
@Bean
SecurityFilterChain filter(HttpSecurity http) throws Exception {
  return http.authorizeHttpRequests(a -> a
      .requestMatchers("/actuator/health").permitAll()
      .anyRequest().authenticated())
    .build();
}
```

A `SecurityFilterChain` bean defines the rules. Permit health checks for orchestrators. Require authentication elsewhere. Password encoders hash credentials correctly — plaintext passwords are not a "temporary shortcut," they are a breach waiting for a calendar date. CSRF protection matters for browser session cookie flows; APIs using tokens have a different threat model — learn which one you are building. Least privilege means roles and authorities that match real job functions, not one `ROLE_ADMIN` for everything.

Disabling security "temporarily" forever is how staging configurations reach production. Authorize checks only on the UI is how raw API clients bypass your SPA's pretty buttons. Security must enforce on the server.

AuthN versus AuthZ? Authentication: who are you? Authorization: what can you do? Keep them distinct in design conversations. Then mention the filter chain so it is clear enforcement happens before controllers — not only in frontend routes.

Picture a practical breach path. The SPA hides admin buttons. A curious user calls `/api/admin/refunds` with a stolen session cookie or a token. If authorization lives only in the UI, the API complies. Server-side authorization in the filter chain or method security is the real door lock.

Password encoders exist because hashing is easy to get wrong. Use the framework-supported encoder factories. Never store plaintext. Never roll a custom hash "for simplicity." Rotate and migrate encodings when algorithms age.

CSRF matters when browsers automatically attach session cookies to requests. Token-based APIs used by non-browser clients have different defaults — understand your clients before copying a Stack Overflow snippet that disables CSRF. Disabling security filters "so we can finish the demo" is how demo config becomes production config through a forgotten profile.

Least privilege shows up in role design. `ROLE_USER` versus `ROLE_FINANCE` versus `ROLE_ADMIN` should map to real capabilities. Broad admin for everyone is not speed; it is shared blast radius.

AuthN versus AuthZ remains the interview staple — answer cleanly, then mention filter chains and method security as enforcement points so the answer is operational, not only definitional.

Picture a practical breach path. The SPA hides admin buttons. A curious user calls an admin API with a stolen cookie or token. If authorization lives only in the UI, the API complies. Server-side authorization in the filter chain or method security is the real door lock.

Password encoders exist because hashing is easy to get wrong. Use framework-supported encoders. Never store plaintext. Never roll a custom hash for simplicity. Rotate encodings when algorithms age.

CSRF matters when browsers automatically attach session cookies. Token-based APIs used by non-browser clients have different defaults — understand your clients before copying a snippet that disables CSRF. Disabling security filters so we can finish the demo is how demo config becomes production config through a forgotten profile.

Least privilege shows up in role design. Roles should map to real capabilities. Broad admin for everyone is shared blast radius. AuthN versus AuthZ remains the interview staple — answer cleanly, then mention filter chains as enforcement points.

Method security annotations can complement the filter chain for deeper authorization — for example, checking whether this user owns this order id. Filters decide whether you are authenticated at all; method security can decide whether this particular action on this particular resource is allowed. Use both thoughtfully. Duplicating contradictory rules in filter matchers and method annotations creates gaps.

Never invent crypto also covers tokens and cookies. Prefer maintained JWT libraries or session mechanisms your platform supports. Home-grown encryption of auth tokens is a recurring breach story. SecurityFilterChain configuration is where those choices become enforceable policy rather than wiki advice.

Build a minimal mental checklist before merge. Is authentication happening at the edge? Are authorization rules enforced on the server for every sensitive route? Are passwords encoded with a modern encoder? Is CSRF configured for the actual client type? Are Actuator and admin endpoints locked down? Did anyone disable security in a profile that could be active in production? This checklist is less glamorous than novel crypto, and it prevents novel outages.

SecurityFilterChain beans make the checklist visible in code review. Prefer readable matchers over clever regex. Prefer least privilege defaults — deny by default, permit explicitly — when the application's risk profile warrants it.

Remember the distinction one more time in incident language. Authentication failures mean we do not know who you are — bad credentials, missing token, expired session. Authorization failures mean we know who you are and you may not do this — wrong role, wrong resource owner. Mixing those in logs and HTTP statuses confuses both users and on-call engineers. Spring Security gives you the hooks; your configuration and error mapping have to keep the meanings straight.

Also reconnect to testing: security rules without tests drift. Anonymous access tests and forbidden-role tests belong beside happy-path controller tests, which Episode Seventy-Seven will make systematic.

You can wire secure APIs and still ship regressions if tests are slow, flaky, or missing. Episode Seventy-Seven is Spring testing — slices before full context, and realism when you need it.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Security (Episode 76).

Narration technique: who can call this → filter chain thesis → SecurityFilterChain example → AuthN/AuthZ/encoders/CSRF/least privilege → misconceptions → interview woven → bridge to testing.

Teaching points preserved: SecurityFilterChain; AuthN vs AuthZ; password encoders; CSRF for browsers; least privilege.
