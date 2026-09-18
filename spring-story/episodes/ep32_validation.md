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

Customs will reject a declaration long before a crane moves. Your API should do the same: a request body that parses as JSON can still be garbage, and that garbage must die at the edge.

Without bean validation, customs controllers grow hand-written checks — null tests, HS-code length tests, nested `if` blocks that return ad-hoc error maps. Rules drift between "create declaration" and "amend declaration." Services re-check the same fields because they do not trust the controller. Spring’s integration with Jakarta Bean Validation gives you declarative constraints on DTOs and a standard failure path when those constraints fail.

Put the rules on the request type the controller accepts:

```java
public record CustomsDeclarationRequest(
        @NotBlank @Size(max = 32) String parcelId,
        @NotBlank @Pattern(regexp = "\\d{6,10}") String hsCode,
        @NotNull @DecimalMin("0.01") BigDecimal declaredValue,
        @NotBlank @Size(min = 2, max = 2) String originCountry,
        @NotEmpty List<@NotBlank String> contents
) {}
```

```java
@RestController
@RequestMapping("/customs/declarations")
public class CustomsDeclarationController {

    private final CustomsDesk desk;

    public CustomsDeclarationController(CustomsDesk desk) {
        this.desk = desk;
    }

    @PostMapping
    public ResponseEntity<DeclarationResponse> submit(
            @Valid @RequestBody CustomsDeclarationRequest body) {
        DeclarationResponse saved = desk.accept(body);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }
}
```

`@Valid` is the switch that turns annotations into enforcement. Without it, Spring binds the JSON and your method runs even when `hsCode` is blank. With it, the `HandlerAdapter` validates before your method body executes. Failure throws `MethodArgumentNotValidException`. That exception is your signal — later lessons turn it into Problem+JSON; today, know that the edge rejected the payload before `CustomsDesk` saw it.

Nested objects and collections need care. Annotate nested beans with `@Valid` so constraints cascade. Use `@NotEmpty` on lists that must contain at least one content line. Group constraints when create and update rules differ. For query parameters and path variables, `@Validated` on the controller plus constraint annotations on method parameters covers the non-body cases.

```java
@GetMapping("/customs/declarations")
public List<DeclarationResponse> search(
        @RequestParam @NotBlank @Size(max = 32) String parcelId) {
    return desk.findByParcel(parcelId);
}
```

Validation is structural honesty, not business policy. "HS code format looks right" belongs on the DTO. "This parcel is already cleared and cannot be redeclared" belongs in the domain service and should surface as a conflict, not as a bean-validation failure. Mixing those layers produces error messages nobody can route.

People forget `@Valid` and then blame Bean Validation for "not working." Others put `@NotNull` on entity fields and expect every repository write to be protected — entities are not the API boundary. A third mistake is returning raw binding errors as a pile of field names with no stable envelope, so mobile customs apps cannot render a single error screen.

Malformed declarations now die at the controller. Controllers and services still throw other failures — unknown parcel ids, conflicts, unexpected bugs. The open craft is turning those exceptions into one coherent HTTP error model instead of a container HTML error page for a JSON client.

That craft is exception handling.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 32 (*Validation*).
