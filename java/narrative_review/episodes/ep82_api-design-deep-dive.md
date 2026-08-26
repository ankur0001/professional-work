# Episode 82 — API Design Deep Dive

| Field | Value |
|---|---|
| Episode | 82 |
| Title | API Design Deep Dive |
| Catalog handbook column | 82 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Caches and services only help if clients can depend on your HTTP contract for years. APIs are long-term contracts — idempotency and errors matter as much as happy paths. A beautiful endpoint that double-charges on retry is not beautiful.

Resource modeling comes first. Prefer nouns and HTTP verbs that match: `POST /orders` creates, `GET /orders/{id}` reads, `POST /orders/{id}/cancel` may be justified when cancel is a real action. Prefer `/users/{id}/orders` over `/getUserOrders`. An endpoint named `/doCreateOrder` that always returns 200 is a remote procedure call wearing a thin disguise. Breaking changes casually — renaming fields, changing meaning, removing properties without versioning — punish every client. Prefer additive evolution when you can; reserve hard versions for true breaks. Deprecate before removal.

```java
@PostMapping("/orders")
ResponseEntity<OrderResponse> create(@Valid @RequestBody OrderRequest req) {
  return ResponseEntity.created(uri).body(service.create(req));
}
```

Validation at the edge keeps the domain cleaner. Consistent error shapes let clients automate handling — `code`, `message`, `fields`, `traceId`. Clients branch on `code`; humans read `message`; support uses `traceId`. Changing that shape later is itself a breaking change. Prefer problem-details or a documented JSON envelope over free-text. Recycling an error code to mean something new is a silent break.

Pagination and filtering prevent "return the entire table" accidents. Cursor pagination often ages better than deep offset pages. State max page size server-side; clients asking for a million rows should fail loudly. Filter parameters should be documented, capped, and preferably indexed.

Idempotency keys on POSTs that matter mean a client can retry safely after a timeout without creating two orders. Why idempotency? Clients retry; servers must not double-apply side effects. Walk a payment POST: client sends Idempotency-Key; server charges once and stores the response; network drops; client retries with the same key; server returns the stored response without charging again. Without TTL, the idempotency table grows forever. Without uniqueness scoped correctly, different users collide. Money, bookings, and side-effecting POSTs earn this machinery; pure GETs do not. Document keys in public API docs with examples — server support without client education is half a solution.

Leaky entities as DTOs couple clients to persistence and leak lazy-loading problems from Episode Seventy-Five into public JSON. Keep entities inward. Public API docs should show happy paths and failure paths side by side — an OpenAPI file that only lists 200 responses lies by omission. Include validation failures, auth failures, and idempotent replays.

Mature POST behavior: validate, apply once, return consistent bodies on replay, and never return 500 with a half-applied side effect without a recovery story. Status codes are part of the contract: 201 or 200 on success, 409 when a key reuses different bodies, 400 when validation fails before charge. Breaking changes casually — renaming amount fields from cents to dollars without versioning — cause real financial events. Treat API changes with the seriousness of schema migrations.

Interview answers should stress contracts, idempotency, and error consistency — not only annotation trivia. When APIs need to fan work out asynchronously, events enter. Episode Eighty-Three is event-driven architecture.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — API Design Deep Dive (Episode 82).

Narration technique: long-term contract → resource modeling → create endpoint → validation/errors/pagination → idempotency payment walk → bridge to events.

Teaching points preserved: resource modeling; idempotency keys; consistent errors; versioning/compatibility; pagination/filtering.
