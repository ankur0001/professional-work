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

A trucker app asks for parcel `PRC-90210`. The id does not exist. What should the JSON look like — and will every other missing-id path in the harbor API look the same?

Without a shared approach, each controller invents an answer. One returns a string. Another returns a Map. A third lets Tomcat render an HTML error page to a JSON client. Operators cannot alert on status codes consistently. Spring MVC gives you structured hooks: `@ExceptionHandler` on a controller, `@RestControllerAdvice` for application-wide handlers, and `ResponseEntityExceptionHandler` as a base when you want to customize framework exceptions such as bind failures.

Start from a domain signal and a stable error shape — Problem+JSON style fields work well even if you keep a simple record:

```java
public class ParcelNotFoundException extends RuntimeException {
    private final String parcelId;

    public ParcelNotFoundException(String parcelId) {
        super("Unknown parcel: " + parcelId);
        this.parcelId = parcelId;
    }

    public String getParcelId() {
        return parcelId;
    }
}
```

```java
public record ApiProblem(
        String type,
        String title,
        int status,
        String detail,
        String instance
) {}
```

```java
@RestControllerAdvice
public class HarborExceptionAdvice {

    @ExceptionHandler(ParcelNotFoundException.class)
    public ResponseEntity<ApiProblem> unknownParcel(ParcelNotFoundException ex,
                                                    HttpServletRequest request) {
        ApiProblem body = new ApiProblem(
                "https://api.harbor.example/problems/parcel-not-found",
                "Parcel not found",
                404,
                ex.getMessage(),
                request.getRequestURI());
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(body);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiProblem> invalid(MethodArgumentNotValidException ex,
                                              HttpServletRequest request) {
        String detail = ex.getBindingResult().getFieldErrors().stream()
                .map(err -> err.getField() + ": " + err.getDefaultMessage())
                .collect(Collectors.joining("; "));
        ApiProblem body = new ApiProblem(
                "https://api.harbor.example/problems/validation",
                "Request validation failed",
                400,
                detail,
                request.getRequestURI());
        return ResponseEntity.badRequest().body(body);
    }
}
```

Controllers stay thin: throw `ParcelNotFoundException` when a lookup misses; do not build error maps inline. Advice owns status and envelope. Validation failures from the previous lesson become first-class citizens of the same bridge — clients parse one shape for "bad customs JSON" and "unknown parcel id."

`@ResponseStatus` on an exception type can set the code, but a status without a body is a weak contract for mobile clients. Prefer advice that always returns the shared problem type. Local `@ExceptionHandler` methods on a single controller are fine for controller-specific cases; application-wide policy belongs on `@RestControllerAdvice` so luggage, parcels, and customs do not diverge.

Wrapping every controller method in try/catch "for safety" scatters policy and guarantees inconsistency. Returning different JSON shapes per exception type with no shared fields forces every client to write N parsers. Swallowing exceptions and returning 200 with `"success": false` teaches clients to ignore HTTP — reverse that habit early.

Failures now have a deliberate model. Some concerns still must wrap the request *before* Spring MVC even picks a handler — encoding, security filters, correlation ids at the servlet boundary. That layer is the servlet `Filter` chain.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 33 (*Exception Handling*).
