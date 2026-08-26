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

A `SecurityFilterChain` bean defines the rules. Permit health checks for orchestrators. Require authentication elsewhere. Prefer readable matchers over clever regex. Prefer least privilege defaults — deny by default, permit explicitly — when the application's risk profile warrants it.

Picture a practical breach path. The SPA hides admin buttons. A curious user calls `/api/admin/refunds` with a stolen session cookie or token. If authorization lives only in the UI, the API complies. Server-side authorization in the filter chain or method security is the real door lock. Disabling security "temporarily" forever is how staging configurations reach production. Authorize checks only on the UI is how raw API clients bypass your SPA's pretty buttons.

Password encoders hash credentials correctly — plaintext passwords are not a "temporary shortcut," they are a breach waiting for a calendar date. Use framework-supported encoder factories. Never roll a custom hash "for simplicity." Rotate and migrate encodings when algorithms age. Never invent crypto also covers tokens and cookies — prefer maintained JWT libraries or session mechanisms your platform supports.

CSRF protection matters for browser session cookie flows; APIs using tokens have a different threat model. Understand your clients before copying a snippet that disables CSRF. Disabling security filters "so we can finish the demo" is how demo config becomes production config through a forgotten profile.

Least privilege shows up in role design. `ROLE_USER` versus `ROLE_FINANCE` versus `ROLE_ADMIN` should map to real capabilities. Broad admin for everyone is shared blast radius. Method security annotations can complement the filter chain for deeper checks — whether this user owns this order id. Filters decide whether you are authenticated at all; method security can decide whether this particular action on this resource is allowed. Duplicating contradictory rules in filter matchers and method annotations creates gaps.

AuthN versus AuthZ remains the interview staple. Authentication: who are you? Authorization: what can you do? Keep them distinct — then mention filter chains and method security as enforcement points so the answer is operational. In incident language: authentication failures mean we do not know who you are; authorization failures mean we know who you are and you may not do this. Mixing those in logs and HTTP statuses confuses users and on-call engineers.

Build a minimal checklist before merge. Is authentication happening at the edge? Are authorization rules enforced on the server for every sensitive route? Are passwords encoded with a modern encoder? Is CSRF configured for the actual client type? Are Actuator and admin endpoints locked down? Did anyone disable security in a profile that could be active in production? Also reconnect to testing: security rules without tests drift. Anonymous access tests and forbidden-role tests belong beside happy-path controller tests.

You can wire secure APIs and still ship regressions if tests are slow, flaky, or missing. Episode Seventy-Seven is Spring testing — slices before full context, and realism when you need it.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Security (Episode 76).

Narration technique: who can call this → filter chain → SecurityFilterChain → breach path → encoders/CSRF/least privilege → AuthN/AuthZ → checklist → bridge to testing.

Teaching points preserved: SecurityFilterChain; AuthN vs AuthZ; password encoders; CSRF for browsers; least privilege.
