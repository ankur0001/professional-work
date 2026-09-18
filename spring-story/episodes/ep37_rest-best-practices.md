# Episode 37 — REST Best Practices

| Field | Value |
|---|---|
| Episode | 37 |
| Title | REST Best Practices |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 37 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Shipping endpoints is easy. Shipping an API a team can live with for years is a set of habits — naming, status discipline, error shape, pagination, and honest versioning.

By now you have the mechanics: dispatcher, controllers, validation, advice, filters, interceptors, uploads. The pain that remains is entropy. Two squads invent two error formats. Collection endpoints return unbounded lists. Resources expose persistence fields. Breaking changes ship without a migration story. Best practices are not decorations on Spring. They are constraints that keep Spring MVC features pointed in one direction.

Start with resource naming. Use nouns and plural collections: `/orders`, `/orders/{id}`, `/orders/{id}/attachments`. Avoid verby paths like `/createOrder`. Let HTTP verbs carry the action. Keep identifiers opaque in URLs; do not leak storage keys you are not willing to support forever.

Status codes should be boring and consistent. `200` for successful reads and many updates. `201` plus `Location` for creates. `204` when a delete or update has no body. `400` for validation and malformed input. `401`/`403` for authn/authz. `404` for missing resources. `409` for conflicts. `429` when you throttle. Do not invent a private meaning for `200` that actually means failure.

```java
@GetMapping("/orders")
public ResponseEntity<PageResponse<OrderSummary>> list(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size) {

    if (size > 100) {
        size = 100;
    }
    Page<OrderSummary> result = orders.list(page, size);
    return ResponseEntity.ok(PageResponse.from(result));
}

public record PageResponse<T>(
        List<T> items,
        int page,
        int size,
        long totalElements,
        int totalPages) {

    static <T> PageResponse<T> from(Page<T> page) {
        return new PageResponse<>(
                page.getContent(),
                page.getNumber(),
                page.getSize(),
                page.getTotalElements(),
                page.getTotalPages());
    }
}
```

Pagination and filtering belong on collections by default. Unbounded `findAll()` over HTTP is how you create an accidental denial-of-service against your own database. Cap `size`. Document sort parameters. Prefer stable cursors for deep pages when offset pagination gets expensive — but even simple page/size is better than returning everything.

Keep a single error envelope across the API — the `ApiError` idea from exception handling — so clients parse one schema. Include a machine-readable `code`, a human `message`, and optionally a `correlationId` that matches logs. Do not return JPA entities as payloads. Map to request/response DTOs so renaming a column does not become a breaking API change and so lazy associations cannot trigger accidental queries during serialization.

Idempotency and concurrency deserve explicit design on write endpoints. For creates that clients may retry, consider an `Idempotency-Key` header stored server-side. For updates to contested resources, use ETags or a version field and answer with `412`/`409` when the client’s view is stale. Document these rules; silent uniqueness constraints that only appear as SQL exceptions are not an API.

Version only when you must, and pick one strategy. URI versioning (`/v1/...`) is obvious to operators and gateways. Media-type versioning is more precise but harder to debug. Running two versions temporarily is fine; running five forever is a tax. Deprecate with headers or docs, then remove on a published schedule.

Observability is part of API craft. Propagate correlation ids from filters into logs. Expose latency and error-rate metrics per route. Treat 5xx spikes as product incidents, not only ops noise. Contract tests — consumer-driven or snapshot OpenAPI diffs in CI — catch accidental breaking changes before clients do. Spring MVC gives you the endpoints; the surrounding discipline keeps them trustworthy.

A topic-specific misconception is chasing "perfect REST purity" while shipping inconsistent statuses and unbounded lists. Another is equating OpenAPI generation with API design — generated docs help, but they cannot invent pagination or error discipline for you. A third is exposing internal exception messages as the public contract and calling it transparency.

So today we tightened the craft around the MVC stack you already have: resource-oriented URLs, disciplined statuses, paginated collections, DTO boundaries, and a single error shape.

That closes the core Spring MVC pass. The next practical pressure is persistence: how those order resources are stored, loaded, and related in a database without turning controllers into SQL.

JPA fundamentals are waiting on the other side of that door.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 37 (*REST Best Practices*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
