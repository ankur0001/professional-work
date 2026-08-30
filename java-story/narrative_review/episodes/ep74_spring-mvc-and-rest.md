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

`@RestController` combines controller semantics with response-body conversion. `@GetMapping` binds a path and verb. Behind the scenes, `DispatcherServlet` is the front controller: it receives the request, finds a handler, invokes it, and works with message converters and exception resolvers. Request arrives; handler mapping selects a method; argument resolvers bind path variables, query params, and bodies; your method runs; return value handlers write the response; exception resolvers translate failures. When a response looks wrong, ask which stage failed — binding, handler logic, conversion, or exception translation — instead of randomly tweaking annotations.

Validation belongs at the edge. Annotate request bodies with constraints and trigger validation deliberately — `@Valid` / `@Validated` at the right parameter — so bad input fails with 400-class responses instead of corrupting the domain. Pick an error structure: code, message, fields, correlation id — and reuse it. Centralize with controller advice so every controller does not invent its own try/catch theater. When validation fails, do not leak stack traces. When authorization fails, do not reveal whether a resource exists if that revelation is itself sensitive. Controllers sit at a trust boundary.

`ResponseEntity` lets you control status codes and headers when a bare return type is too blunt. Be boring and correct: 201 for creation with Location when applicable, 404 when missing, 409 for conflicts. Controllers that always return 200 with an error flag reinvent HTTP poorly. Bare strings are fine for hello world; production APIs need deliberate envelopes.

Do not expose entities blindly. Returning JPA entities with lazy fields is a classic footgun: serialization triggers lazy loads, or `LazyInitializationException` after the session closes. Schema leakage causes API churn when columns change. Request DTOs validate input; response DTOs shape output; domain entities stay inward. Controllers that accept entities invite over-posting — clients setting fields they should never touch.

Walk a create-order endpoint. Validate the request DTO. Call the service. Return `201` with a `Location` header and a response DTO. On domain conflict, return `409` with the shared error shape. Walk one failure from production: a list endpoint returns entities; under load the session closes, Jackson serializes, a lazy collection triggers, and the API throws five hundred. The fix is not "open session in view forever" without debate — it is a DTO query or an explicit fetch tailored to the response. MVC and JPA meet at this seam; Episode Seventy-Five deepens persistence, but the controller already should have refused to spill entities.

REST is not only JSON over HTTP. Resource modeling matters: nouns for resources, verbs as HTTP methods, status codes as outcomes. An endpoint named `/doCreateOrder` that always returns 200 is a remote procedure call wearing a thin disguise. Prefer `/orders` with POST and a 201.

Controller return types in an interview? Body for simple success, `ResponseEntity` when status and headers matter, reactive types when you are on a reactive stack — always choose status and errors deliberately. Mention deliberate status and error handling, not only "we return the object and Spring Jacksonifies it."

APIs need durable data. Spring Data speeds repositories, but you still own SQL reality, transactions, and N+1 — and that ownership gap is the next pressure.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring MVC and REST (Episode 74).

Narration technique: product API ask → MVC thesis → RestController → DispatcherServlet → validation/DTOs/status → create-order walk → bridge to Spring Data.

Teaching points preserved: DispatcherServlet flow; @RestController mappings; validation; ResponseEntity/status; don't expose entities blindly.
