# Episode 76 — Spring Security

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Five covered Spring Data, transactions, and N-plus-one pitfalls. Persistence without security is an open door — every API needs an access story. Spring Security is the standard filter chain for authentication and authorization.

Modern apps mix sessions, JWTs, OAuth two, and method-level rules. Interviews expect you to separate who you are from what you may do. Today — authn versus authz, the filter chain, securing REST, and common traps.

Episode Seventy-Six. Spring Security. Authentication answers who you are — authorization answers what you may do. Credentials become a SecurityContext with an Authentication principal.

Roles and authorities express permissions — ROLE_USER is a convention, not magic. Fail closed — deny by default, grant explicitly. Never conflate logged-in with allowed — that is the classic auth bug.

Say authn and authz separately in interviews — interviewers listen for the split. Spring Security is a filter chain in front of your servlet stack. SecurityFilterChain beans declare which paths need auth and which are public.

UsernamePasswordAuthenticationFilter, BearerTokenAuthenticationFilter — specialized links. Once authenticated, AuthorizationFilter enforces request matchers and rules. Order matters — mis-ordered filters create confusing allow or deny behavior.

Debug with spring-security DEBUG logs when a path is unexpectedly open. Securing REST APIs in practice. Stateless JWT or opaque tokens for services — sessions for browser apps. CSRF protection matters for cookie sessions — often disabled for pure bearer APIs.

CORS is not security — it only relaxes browser same-origin rules. Use HTTPS everywhere — tokens on the wire are credentials. Resource servers validate tokens — authorization servers issue them.

Method security complements URL rules. EnableMethodSecurity unlocks PreAuthorize and PostAuthorize. Express domain rules — hasRole, hasAuthority, or custom PermissionEvaluator. URL rules catch coarse paths — method rules protect service operations.

SpEL in annotations is powerful — keep expressions readable and tested. Defense in depth — never rely on the UI alone to hide forbidden actions. Security practices that survive production.

Least privilege — grant the smallest authority that works. Rotate secrets and signing keys — store them outside the repo. Log auth failures without leaking whether a username exists when policy forbids it.

Test both positive and negative authorization paths in CI. Threat-model new endpoints — every PostMapping is an attack surface. Three common mistakes. One — permitAll on a broad ant pattern that swallows admin routes.

Two — trusting client-sent roles inside an unsigned JWT payload. Three — disabling CSRF for cookie apps without understanding the risk. Also — putting authorization only in the frontend — backends must enforce.

Security is a server responsibility — clients are untrusted. Interview question — how do you secure a Spring Boot REST API? Declare a SecurityFilterChain — authenticate requests, authorize paths.

Prefer bearer tokens for stateless services — validate signatures and expiry. Map authorities to endpoints and critical service methods. Keep secrets external — HTTPS in transit, least privilege in design.

Prove it with tests that assert four-oh-one and four-oh-three outcomes. Security holds the line — next we prove the system. Episode Seventy-Seven — Spring Testing. Unit, slice, and full-context tests that keep Spring apps honest.

See you there.
