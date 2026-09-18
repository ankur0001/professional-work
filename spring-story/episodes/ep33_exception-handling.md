# Episode 33 — Exception Handling

| Field | Value |
|---|---|
| Episode | 33 |
| Title | Exception Handling |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 33 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Failures will happen on live traffic. Exception handling decides whether clients see chaos or a deliberate error model.

Without a shared approach, each controller catches exceptions differently. One returns a string. Another returns a Map. A third lets Tomcat render an HTML error page to a JSON client. Operators cannot alert on status codes consistently. Spring MVC gives you structured hooks: `@ExceptionHandler` on a controller, `@ControllerAdvice` (or `@RestControllerAdvice`) for application-wide handlers, and `ResponseEntityExceptionHandler` as a base when you want to customize framework exceptions such as bind failures.

Start with a domain exception that means something. `OrderNotFoundException` is clearer than a bare `RuntimeException("missing")`. Throw it from the service when an id does not exist. Then translate it once to HTTP 404 with a stable body shape.

```java
public class OrderNotFoundException extends RuntimeException {
    private final long orderId;

    public OrderNotFoundException(long orderId) {
        super("Order not found: " + orderId);
        this.orderId = orderId;
    }

    public long getOrderId() {
        return orderId;
    }
}

@RestControllerAdvice
public class ApiExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    public ResponseEntity<ApiError> notFound(OrderNotFoundException ex) {
        ApiError body = new ApiError("ORDER_NOT_FOUND", ex.getMessage());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(body);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiError> invalid(MethodArgumentNotValidException ex) {
        String details = ex.getBindingResult().getFieldErrors().stream()
                .map(err -> err.getField() + ": " + err.getDefaultMessage())
                .collect(Collectors.joining("; "));
        ApiError body = new ApiError("VALIDATION_FAILED", details);
        return ResponseEntity.badRequest().body(body);
    }
}

public record ApiError(String code, String message) {}
```

`@RestControllerAdvice` combines `@ControllerAdvice` with `@ResponseBody` semantics, so returned objects become JSON like a REST controller. Handler methods can take the exception, the request, and other injectable arguments. Prefer a small catalog of problem codes your clients can switch on — not a dump of exception class names that change when you refactor packages.

Validation failures connect directly here. Episode 32 ended with `MethodArgumentNotValidException`. The advice above shows the natural home for that translation: one place, one 400 shape, every `@Valid` endpoint inherits it. Binding failures, missing path variables, and unsupported media types have related framework exceptions you can handle the same way.

Decide what must not leak. Stack traces, SQL text, and internal hostnames belong in logs, not in API bodies. Log the unexpected with a correlation id. Return a generic 500 payload to the client. For expected business conflicts — duplicate create, stale update — use 409 or 422 with a clear code rather than a generic 500.

Handler precedence matters when advice classes multiply. More specific exception types win over broader ones. `@RestControllerAdvice(assignableTypes = …)` or base-package filters can scope advice to one API surface if a monolith hosts several. Avoid a catch-all `Exception` handler that returns 400 for everything — that hides outages. Catch-all should be 500, logged loudly, and rare in healthy traffic.

`ResponseEntityExceptionHandler` is worth knowing when you customize Spring’s own exceptions — missing request body, method not supported, media type not acceptable — without reimplementing every case from scratch. Extend it in your advice and override only the methods you care about. That keeps framework errors and domain errors in one vocabulary.

A topic-specific misconception is wrapping every controller method in try/catch "for safety." That scatters policy and guarantees inconsistency. Another is using only `@ResponseStatus` on exception types and assuming the body will be useful — status alone is not a contract. A third is letting advice return different JSON shapes per exception type with no shared fields, so clients cannot write one error parser.

So today we built a central error bridge: domain and framework exceptions enter, stable `ApiError` payloads and status codes leave, with validation failures as a first-class citizen of that bridge.

Cross-cutting work is not only about failures after a controller runs. Some concerns must wrap the request before Spring MVC even picks a handler — encoding, security filters, correlation ids at the servlet boundary. That layer is the servlet `Filter` chain.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 33 (*Exception Handling*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
