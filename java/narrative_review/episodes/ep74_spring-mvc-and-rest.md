# Episode 74 — Spring MVC and REST

| Field | Value |
|---|---|
| Episode | 74 |
| Title | Spring MVC and REST |
| Catalog handbook column | 74 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Boot gave you an executable web app. Now a product manager asks for an HTTP API: create orders, fetch orders, return sensible errors. The practical situation is mapping HTTP into method calls without turning controllers into dumping grounds. Spring MVC maps HTTP to methods — be intentional about DTOs, validation, and status codes.

```java
@RestController
class HelloController {
  @GetMapping("/hello")
  String hello() { return "hi"; }
}
```

`@RestController` combines controller semantics with response-body conversion. `@GetMapping` binds a path and verb. Behind the scenes, `DispatcherServlet` is the front controller: it receives the request, finds a handler, invokes it, and works with message converters and exception resolvers. You do not need to recite every class in that flow on day one, but you need the picture: one entry servlet, many handler methods.

Validation belongs at the edge. Annotate request bodies with constraints and trigger validation deliberately so bad input fails with 400-class responses instead of corrupting the domain. `ResponseEntity` lets you control status codes and headers when a bare return type is too blunt. Controller return types — body, `ResponseEntity`, or reactive types in reactive stacks — should be chosen with status and error shape in mind.

Do not expose entities blindly. Returning JPA entities with lazy fields is a classic production footgun: serialization triggers lazy loads, or worse, `LazyInitializationException` after the session closes. DTOs or dedicated response types keep the API contract stable and the persistence graph private. Inconsistent error shapes — sometimes a string, sometimes a random JSON blob — punish clients. Agree on an error document and stick to it.

Walk a create-order endpoint mentally. Validate the request DTO. Call the service. Return `201` with a `Location` header and a response DTO. On domain conflict, return `409` with the shared error shape. Ignoring validation, returning entities, and improvising errors are the misunderstandings that make APIs brittle.

Controller return types in an interview? Body for simple success, `ResponseEntity` when status and headers matter, reactive types when you are on a reactive stack — always choose status and errors deliberately.

DispatcherServlet flow in slightly more detail helps debugging. Request arrives. Handler mapping selects a controller method. Argument resolvers bind path variables, query params, and bodies. Your method runs. Return value handlers write the response. Exception resolvers translate failures into status codes. When a response looks wrong, ask which stage failed — binding, handler logic, conversion, or exception translation — instead of randomly tweaking annotations.

Validation annotations on DTOs only help if validation runs. `@Valid` / `@Validated` at the right parameter, plus a clear 400 response body, prevent "null pointer deep in the service" as your input checker. Inconsistent error shapes force every client to special-case. Pick a structure: code, message, fields, correlation id — and reuse it.

Entity exposure hurts in two ways. Lazy fields and session boundaries cause runtime failures. Schema leakage causes API churn when columns change. Map to response DTOs at the boundary. Pagination and filtering deserve explicit parameters rather than loading entire tables into JSON.

For status codes, be boring and correct: 201 for creation with Location when applicable, 204 for empty success deletes if that is your style, 404 when the resource is missing, 409 for conflicts. Controllers that always return 200 with an error flag reinvent HTTP poorly.

Interview answers on controller return types should mention deliberate status and error handling, not only "we return the object and Spring Jacksonifies it."

Be intentional about DTOs means mapping both ways with care. Request DTOs validate input. Response DTOs shape output. Domain entities stay inward. Controllers that accept entities invite over-posting — clients setting fields they should never touch.

Error handling can be centralized with controller advice so every controller does not invent its own try/catch theater. Central advice should still produce the consistent error shape you promised clients. Inconsistent errors across endpoints are a contract bug.

DispatcherServlet flow knowledge pays off when filters and interceptors enter the story — security filters run around this world. Knowing where your controller sits in the chain prevents confusion about who decided status codes and headers first.

REST is not only JSON over HTTP. Resource modeling matters: nouns for resources, verbs as HTTP methods, status codes as outcomes. An endpoint named `/doCreateOrder` that always returns 200 is a remote procedure call wearing a thin disguise. Prefer `/orders` with POST and a 201. That modeling choice reduces client ambiguity and matches the intentional DTO and error practices already discussed.

When validation fails, do not leak stack traces. When authorization fails, do not reveal whether a resource exists if that revelation is itself sensitive. Controllers sit at a trust boundary; MVC skill is partly security hygiene.

Walk one more failure from production. A list endpoint returns entities. Under load, Hibernate session closes, Jackson serializes, lazy collection triggers, and the API throws five hundred. The fix is not "open session in view forever" as a silent default without debate — that pattern has its own costs. The cleaner fix is a DTO query or an explicit fetch tailored to the response. MVC and JPA meet at this seam; Episode Seventy-Five will deepen the persistence side, but the controller already should have refused to spill entities.

Status codes and ResponseEntity are how you make HTTP speak honestly when creation succeeds, validation fails, or a resource is missing. Bare strings are fine for hello world; production APIs need deliberate envelopes.

APIs need durable data. Spring Data speeds repositories, but you still own SQL reality, transactions, and N+1 — Episode Seventy-Five.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring MVC and REST (Episode 74).

Narration technique: product API ask → MVC thesis → RestController example → DispatcherServlet → validation/ResponseEntity/DTOs → misconceptions → interview woven → bridge to Spring Data.

Teaching points preserved: DispatcherServlet flow; @RestController mappings; validation; ResponseEntity/status; don't expose entities blindly.
