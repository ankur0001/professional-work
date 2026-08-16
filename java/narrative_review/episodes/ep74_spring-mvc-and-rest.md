# Episode 74 — Spring MVC and REST

| Field | Value |
|---|---|
| Episode | 74 |
| Title | Spring MVC and REST |
| Catalog handbook column | 74 |
| Narration source script | `make_episode_74.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Seventy-Three covered Spring Boot starters and auto-configuration.
2. Most Boot services speak HTTP — Spring MVC is the classic request stack.
3. REST controllers map URLs to methods and convert JSON with HttpMessageConverters.
4. Clean API design separates transport from business rules.
5. Interviews love status codes, validation, and exception handling details.
6. Today — controllers, mapping, validation, advice, and REST design tips.

### Scene `title` (renderer: `title`)

1. Episode Seventy-Four.
2. Spring MVC and REST.

### Scene `controllers` (renderer: `controllers`)

1. RestController combines Controller and ResponseBody.
2. Methods return objects — Spring writes JSON to the response.
3. RequestMapping family — GetMapping, PostMapping, PutMapping, DeleteMapping.
4. Path variables, request params, and headers bind method arguments.
5. Keep controllers thin — validate input, call a service, map the result.
6. Business rules belong in services — not in mapping methods.

### Scene `request_response` (renderer: `request_response`)

1. The request-response pipeline.
2. DispatcherServlet is the front controller for Spring MVC.
3. Handler mapping finds the controller method for the request.
4. Argument resolvers bind parameters — body, path, query, principal.
5. Return value handlers write the body or negotiate a view.
6. Filters and interceptors wrap cross-cutting HTTP concerns.

### Scene `validation` (renderer: `validation`)

1. Validation belongs at the edge of the API.
2. Jakarta Validation annotations — NotNull, Size, Email — on DTOs.
3. Valid on a request body triggers validation before your method runs.
4. BindException or MethodArgumentNotValidException carry field errors.
5. Return structured four-hundred responses — not stack traces.
6. Validate again in the domain when rules are more than bean annotations.

### Scene `errors` (renderer: `errors`)

1. Consistent error handling builds client trust.
2. ControllerAdvice centralizes exception-to-response mapping.
3. Map domain not-found to four-oh-four — conflicts to four-oh-nine.
4. Never leak internal exception messages to public clients.
5. Problem Details or a small error JSON schema keeps clients stable.
6. Log with correlation IDs — respond with safe, actionable messages.

### Scene `design` (renderer: `design`)

1. REST design habits that interviewers look for.
2. Nouns for resources — verbs for HTTP methods, not URL paths.
3. Idempotent PUT and DELETE — careful POST semantics.
4. Use proper status codes — two-oh-one for create, two-oh-four for empty.
5. Version deliberately — URL or header — do not break clients silently.
6. Pagination and filtering for collections — never dump unbounded lists.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — fat controllers with transactions and SQL inside mapping methods.
3. Two — returning entities directly — overexposes persistence fields.
4. Three — swallowing exceptions and always returning two-hundred OK.
5. Also — ignoring Content-Type and Accept — surprising clients with wrong formats.
6. Treat the HTTP layer as a translation boundary — not the business core.

### Scene `interview` (renderer: `interview`)

1. Interview question — how does a request reach your RestController?
2. Embedded server hands the request to DispatcherServlet.
3. Handler mapping selects the controller method by path and verb.
4. Argument resolvers bind body and params — validation may run.
5. Service executes business logic — return value becomes the HTTP body.
6. Advice and filters can reshape errors and cross-cutting concerns.

### Scene `teaser` (renderer: `teaser`)

1. HTTP is handled — next we persist data.
2. Episode Seventy-Five — Spring Data and Persistence.
3. Repositories, JPA mapping, transactions, and N-plus-one awareness.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **74** — *Spring MVC and REST*.
- **Series catalog:** Episode 74 ↔ handbook lesson 74 — *Spring MVC and REST*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Seventy-Three covered Spring Boot starters and auto-configuration._
- **`title`** — starts from: _Episode Seventy-Four._
- **`controllers`** — starts from: _RestController combines Controller and ResponseBody._
- **`request_response`** — starts from: _The request-response pipeline._
- **`validation`** — starts from: _Validation belongs at the edge of the API._
- **`errors`** — starts from: _Consistent error handling builds client trust._
- **`design`** — starts from: _REST design habits that interviewers look for._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — how does a request reach your RestController?_
- **`teaser`** — starts from: _HTTP is handled — next we persist data._
