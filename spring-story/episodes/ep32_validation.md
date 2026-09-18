# Episode 32 — Validation

| Field | Value |
|---|---|
| Episode | 32 |
| Title | Validation |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 32 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A request body that parses as JSON can still be garbage. Validation belongs at the API boundary so bad data never becomes half-written state.

Without bean validation, controllers grow hand-written checks: null tests, length tests, regex tests, nested `if` blocks that return ad-hoc error maps. Rules drift between endpoints. Services re-check the same fields because they do not trust the controller. Spring’s integration with Jakarta Bean Validation gives you declarative constraints on DTOs and a standard failure path when those constraints fail.

The pattern is simple to say and easy to miswire. Annotate the DTO. Put `@Valid` on the `@RequestBody` parameter. Let the framework run the validator before your method body executes. When validation fails, Spring throws `MethodArgumentNotValidException` instead of calling your method. You then map that exception to a 400-level response — often through `@ExceptionHandler` or a `@ControllerAdvice`, which the next episode owns in depth.

```java
public class CreateOrderRequest {

    @NotNull
    private Long customerId;

    @NotBlank
    private String sku;

    @Min(1)
    private int quantity;

    // getters/setters or a compact constructor + accessors
}

@RestController
@RequestMapping("/orders")
public class OrderController {

    @PostMapping
    public ResponseEntity<OrderResponse> create(
            @Valid @RequestBody CreateOrderRequest body) {
        // only runs when constraints pass
        return ResponseEntity.ok(orders.create(body));
    }
}
```

Constraints compose. `@NotNull` rejects a missing reference. `@NotBlank` rejects null, empty, and whitespace-only strings. `@Min` and `@Max` bound numbers. `@Email`, `@Size`, and `@Pattern` cover common formats. For nested objects, put `@Valid` on the nested field so the cascade continues. For collections of nested DTOs, the same idea applies: validate elements, not only the list reference.

Boot usually auto-configures a `LocalValidatorFactoryBean` when a validation implementation such as Hibernate Validator is on the classpath — typically via `spring-boot-starter-validation`. If `@Valid` appears to do nothing, check that dependency first. Also distinguish `@Validated` on a class (method-level validation with groups) from `@Valid` on a parameter (argument validation for MVC binding). For request bodies, `@Valid` on the parameter is the everyday tool.

When `MethodArgumentNotValidException` fires, the exception carries a `BindingResult` with field errors: which property failed, which code, which default message. That is gold for building a consistent error payload — `field`, `rejectedValue`, `message` — instead of a stack trace. Do not catch it inside every controller method. Centralize the translation once.

Groups and custom constraints appear when the same DTO is used in more than one operation. Create might require `sku`; patch might allow partial fields. Validation groups let you activate different constraint sets. Custom annotations backed by a `ConstraintValidator` capture domain rules that `@Pattern` cannot express cleanly — for example, "quantity must be a multiple of pack size." Keep those rules readable; a validator that opens a database connection on every request is usually the wrong layer for uniqueness checks that belong in the service transaction.

Also separate binding errors from validation errors in your head. Type mismatches — sending `"abc"` for an `int` — fail during binding and surface as related but distinct exceptions. Constraint violations assume the value was bound and then judged. Clients experience both as "bad request," but your logs and tests should know which stage failed.

A topic-specific misconception is validating only in the service and calling the controller "done." Services should still protect invariants, but transport-level shape belongs at the edge so HTTP clients get fast, uniform 400s. Another misconception is using `@Valid` without a validator on the classpath and concluding "annotations are decorative." A third is returning 200 with an errors array in the body for constraint failures — that fights every HTTP client convention.

So today we put declarative constraints on DTOs, required `@Valid` at the controller parameter, and named `MethodArgumentNotValidException` as the failure signal when the body is structurally wrong.

That raises the broader question: validation is only one failure mode. Controllers and services throw many others — missing resources, conflicts, unexpected bugs. How does Spring turn those exceptions into a coherent HTTP error model instead of a container stack page?

Exception handling is next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 32 (*Validation*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
