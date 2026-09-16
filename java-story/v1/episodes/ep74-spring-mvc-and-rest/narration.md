# Episode 74 — Spring MVC and REST

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Three covered Spring Boot starters and auto-configuration. Most Boot services speak HTTP — Spring MVC is the classic request stack. REST controllers map URLs to methods and convert JSON with HttpMessageConverters.

Clean API design separates transport from business rules. Interviews love status codes, validation, and exception handling details. Today — controllers, mapping, validation, advice, and REST design tips.

Episode Seventy-Four. Spring MVC and REST. RestController combines Controller and ResponseBody. Methods return objects — Spring writes JSON to the response. RequestMapping family — GetMapping, PostMapping, PutMapping, DeleteMapping.

Path variables, request params, and headers bind method arguments. Keep controllers thin — validate input, call a service, map the result. Business rules belong in services — not in mapping methods.

The request-response pipeline. DispatcherServlet is the front controller for Spring MVC. Handler mapping finds the controller method for the request. Argument resolvers bind parameters — body, path, query, principal.

Return value handlers write the body or negotiate a view. Filters and interceptors wrap cross-cutting HTTP concerns. Validation belongs at the edge of the API. Jakarta Validation annotations — NotNull, Size, Email — on DTOs.

Valid on a request body triggers validation before your method runs. BindException or MethodArgumentNotValidException carry field errors. Return structured four-hundred responses — not stack traces.

Validate again in the domain when rules are more than bean annotations. Consistent error handling builds client trust. ControllerAdvice centralizes exception-to-response mapping. Map domain not-found to four-oh-four — conflicts to four-oh-nine.

Never leak internal exception messages to public clients. Problem Details or a small error JSON schema keeps clients stable. Log with correlation IDs — respond with safe, actionable messages.

REST design habits that interviewers look for. Nouns for resources — verbs for HTTP methods, not URL paths. Idempotent PUT and DELETE — careful POST semantics. Use proper status codes — two-oh-one for create, two-oh-four for empty.

Version deliberately — URL or header — do not break clients silently. Pagination and filtering for collections — never dump unbounded lists. Three common mistakes. One — fat controllers with transactions and SQL inside mapping methods.

Two — returning entities directly — overexposes persistence fields. Three — swallowing exceptions and always returning two-hundred OK. Also — ignoring Content-Type and Accept — surprising clients with wrong formats.

Treat the HTTP layer as a translation boundary — not the business core. Interview question — how does a request reach your RestController? Embedded server hands the request to DispatcherServlet.

Handler mapping selects the controller method by path and verb. Argument resolvers bind body and params — validation may run. Service executes business logic — return value becomes the HTTP body.

Advice and filters can reshape errors and cross-cutting concerns. HTTP is handled — next we persist data. Episode Seventy-Five — Spring Data and Persistence. Repositories, JPA mapping, transactions, and N-plus-one awareness.

See you there.
