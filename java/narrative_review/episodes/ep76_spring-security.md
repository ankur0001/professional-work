# Episode 76 — Spring Security

| Field | Value |
|---|---|
| Episode | 76 |
| Title | Spring Security |
| Catalog handbook column | 76 |
| Narration source script | `make_episode_76.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Five covered Spring Data, transactions, and N-plus-one pitfalls.
2. Persistence without security is an open door — every API needs an access story.
3. Spring Security is the standard filter chain for authentication and authorization.
4. Modern apps mix sessions, JWTs, OAuth two, and method-level rules.
5. Interviews expect you to separate who you are from what you may do.
6. Today — authn versus authz, the filter chain, securing REST, and common traps.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Six.
2. Spring Security.

### Scene `authn_authz` (renderer: `authn_authz`)

1. Authentication answers who you are — authorization answers what you may do.
2. Credentials become a SecurityContext with an Authentication principal.
3. Roles and authorities express permissions — ROLE_USER is a convention, not magic.
4. Fail closed — deny by default, grant explicitly.
5. Never conflate logged-in with allowed — that is the classic auth bug.
6. Say authn and authz separately in interviews — interviewers listen for the split.

### Scene `filter_chain` (renderer: `filter_chain`)

1. Spring Security is a filter chain in front of your servlet stack.
2. SecurityFilterChain beans declare which paths need auth and which are public.
3. UsernamePasswordAuthenticationFilter, BearerTokenAuthenticationFilter — specialized links.
4. Once authenticated, AuthorizationFilter enforces request matchers and rules.
5. Order matters — mis-ordered filters create confusing allow or deny behavior.
6. Debug with spring-security DEBUG logs when a path is unexpectedly open.

### Scene `rest_apis` (renderer: `rest_apis`)

1. Securing REST APIs in practice.
2. Stateless JWT or opaque tokens for services — sessions for browser apps.
3. CSRF protection matters for cookie sessions — often disabled for pure bearer APIs.
4. CORS is not security — it only relaxes browser same-origin rules.
5. Use HTTPS everywhere — tokens on the wire are credentials.
6. Resource servers validate tokens — authorization servers issue them.

### Scene `method_security` (renderer: `method_security`)

1. Method security complements URL rules.
2. EnableMethodSecurity unlocks PreAuthorize and PostAuthorize.
3. Express domain rules — hasRole, hasAuthority, or custom PermissionEvaluator.
4. URL rules catch coarse paths — method rules protect service operations.
5. SpEL in annotations is powerful — keep expressions readable and tested.
6. Defense in depth — never rely on the UI alone to hide forbidden actions.

### Scene `practices` (renderer: `practices`)

1. Security practices that survive production.
2. Least privilege — grant the smallest authority that works.
3. Rotate secrets and signing keys — store them outside the repo.
4. Log auth failures without leaking whether a username exists when policy forbids it.
5. Test both positive and negative authorization paths in CI.
6. Threat-model new endpoints — every PostMapping is an attack surface.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — permitAll on a broad ant pattern that swallows admin routes.
3. Two — trusting client-sent roles inside an unsigned JWT payload.
4. Three — disabling CSRF for cookie apps without understanding the risk.
5. Also — putting authorization only in the frontend — backends must enforce.
6. Security is a server responsibility — clients are untrusted.

### Scene `interview` (renderer: `interview`)

1. Interview question — how do you secure a Spring Boot REST API?
2. Declare a SecurityFilterChain — authenticate requests, authorize paths.
3. Prefer bearer tokens for stateless services — validate signatures and expiry.
4. Map authorities to endpoints and critical service methods.
5. Keep secrets external — HTTPS in transit, least privilege in design.
6. Prove it with tests that assert four-oh-one and four-oh-three outcomes.

### Scene `teaser` (renderer: `teaser`)

1. Security holds the line — next we prove the system.
2. Episode Seventy-Seven — Spring Testing.
3. Unit, slice, and full-context tests that keep Spring apps honest.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **76** — *Spring Security*.
- **Series catalog:** Episode 76 ↔ handbook lesson 76 — *Spring Security*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Five covered Spring Data, transactions, and N-plus-one pitfalls._
- **`title`** — starts from: _Episode Seventy-Six._
- **`authn_authz`** — starts from: _Authentication answers who you are — authorization answers what you may do._
- **`filter_chain`** — starts from: _Spring Security is a filter chain in front of your servlet stack._
- **`rest_apis`** — starts from: _Securing REST APIs in practice._
- **`method_security`** — starts from: _Method security complements URL rules._
- **`practices`** — starts from: _Security practices that survive production._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how do you secure a Spring Boot REST API?_
- **`teaser`** — starts from: _Security holds the line — next we prove the system._
