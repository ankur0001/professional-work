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

Resource modeling comes first. Prefer nouns and HTTP verbs that match: `POST /orders` creates, `GET /orders/{id}` reads, `POST /orders/{id}/cancel` may be justified when cancel is a real action. Breaking changes casually — renaming fields, changing meaning, removing properties without versioning or negotiation — punish every client. Versioning and compatibility strategies differ by team; the requirement is intentionality.

```java
@PostMapping("/orders")
ResponseEntity<OrderResponse> create(@Valid @RequestBody OrderRequest req) {
  return ResponseEntity.created(uri).body(service.create(req));
}
```

Validation at the edge keeps the domain cleaner. Consistent error shapes let clients automate handling. Pagination and filtering prevent "return the entire table" accidents. Idempotency keys on POSTs that matter mean a client can retry safely after a timeout without creating two orders. Why idempotency? Clients retry; servers must not double-apply side effects. Store the key, return the original result on replay.

Leaky entities as DTOs couple clients to persistence. No idempotency for money-moving POSTs is an incident factory. Breaking changes without a plan force synchronized releases — a distributed monolith of contracts.

Idempotency keys need storage and TTL policy. The client sends a key; the server stores the first result; replays return the same response. Without TTL, the idempotency table grows forever. Without uniqueness scoped correctly, different users collide. Money, bookings, and side-effecting POSTs earn this machinery; pure GETs do not need it.

Consistent error shape might look like `code`, `message`, `fields`, `traceId`. Clients can branch on `code`. Humans read `message`. Support uses `traceId`. Changing that shape later is itself a breaking change — design it once with care.

Versioning options include URL versions, header versions, or compatible evolution with additive fields. Casual breaking changes force synchronized client releases. Prefer additive evolution when you can; reserve hard versions for true breaks.

Pagination and filtering protect the database as much as the contract. Cursor pagination often ages better than deep offset pages. Filter parameters should be documented and capped. Resource modeling that returns entire collections "for convenience" becomes an outage on a popular account.

Leaky entities as DTOs also leak lazy-loading problems from Episode Seventy-Five into public JSON. The API deep dive and the persistence episode are one seam — keep entities inward.

Compatibility is a social contract with other teams. Publish changelog discipline. Prefer additive JSON fields. Deprecate before removal. Provide dual-write or dual-read windows when renaming matters. Breaking changes casually destroy trust faster than outages — outages end; broken clients linger.

Pagination should state max page size server-side. Clients asking for a million rows should fail loudly. Filtering should use indexed columns where possible; document expensive filters. Resource modeling that ignores these operators pushes accidental denial-of-service into your own API.

Idempotency and errors together define mature POST behavior: validate, apply once, return consistent bodies on replay, and never return 500 with a half-applied side effect without a recovery story. That is API design as production design.

Resource modeling examples help. Prefer `/users/{id}/orders` over `/getUserOrders`. Prefer 404 for missing resources and 409 for conflicts like duplicate idempotency with different bodies if that is your rule. Prefer problem-details or a documented JSON error envelope over free-text. Clients should not parse English sentences to branch logic.

Versioning and compatibility also cover error codes. Recycling a code to mean something new is a silent break. Add new codes; deprecate old ones.

Idempotency keys for POSTs that matter — payments, bookings, submissions — should appear in public API docs with examples. If clients do not know to send them, they will not. Server support without client education is half a solution.

APIs are long-term contracts. Design them as if strangers will depend on them for years — because they will, including your future self.

Walk a payment POST with idempotency. Client sends Idempotency-Key. Server sees first request, charges once, stores response. Network drops the response. Client retries with the same key. Server returns the stored response without charging again. That story is why idempotency exists. Without it, support refunds duplicates all afternoon.

Consistent errors in that flow matter too: a 409 with a clear code when the key reuses different bodies; a 402 or 400 when validation fails before charge; a 201 or 200 with the payment representation on success. Status codes are part of the contract, not decoration.

Pagination for listing payments should be cursored when history is long. Filtering by date ranges should be bounded. Resource modeling keeps payment as a resource with subresources for refunds rather than a RPC soup.

Breaking changes casually — renaming amount fields from cents to dollars without versioning — cause real financial events. Treat API changes with the seriousness of schema migrations.

Public API docs should show happy paths and failure paths side by side. An OpenAPI file that only lists 200 responses lies by omission. Include validation failures, auth failures, and idempotent replays. Documentation is part of the contract — treat it with the same review rigor as code.

Idempotency, consistent errors, and compatible evolution are how APIs survive contact with retries, partial failures, and multiple client teams. Happy-path JSON is the easy part; the contract is the hard part — and the part this episode exists to elevate.

Interview answers should stress contracts, idempotency, and error consistency — not only annotation trivia. When APIs need to fan work out asynchronously, events enter. Episode Eighty-Three is event-driven architecture.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — API Design Deep Dive (Episode 82).

Narration technique: long-term contract thesis → resource modeling → create endpoint → validation/errors/pagination/idempotency → misconceptions → interview woven → bridge to events.

Teaching points preserved: resource modeling; idempotency keys; consistent errors; versioning/compatibility; pagination/filtering.
