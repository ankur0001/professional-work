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

You can wire controllers, validation, advice, filters, and uploads and still ship an API that fights its clients. REST best practices are the craft layer: idempotent parcel create, honest pagination of tracking events, and boundaries that keep persistence out of the wire format.

Start with resource naming. Use nouns and plural collections: `/parcels`, `/parcels/{id}`, `/parcels/{id}/events`. Avoid verby paths like `/createParcel`. Let HTTP verbs carry the action. Keep identifiers opaque in URLs.

Idempotent create matters the moment a trucker’s mobile app retries a POST after a timeout. Without an idempotency key, you register the same parcel twice. With one, the second call returns the original resource:

```java
@PostMapping("/parcels")
public ResponseEntity<ParcelResponse> create(
        @RequestHeader("Idempotency-Key") String idempotencyKey,
        @Valid @RequestBody CreateParcelRequest body) {
    ParcelResponse created = parcels.createIdempotent(idempotencyKey, body);
    return ResponseEntity
            .created(URI.create("/parcels/" + created.id()))
            .body(created);
}
```

Store the key with the created parcel id. On replay, return the same body and the same `Location`. Do not invent a second parcel. Clients must send the key; document that requirement as part of the contract.

Pagination keeps tracking-event lists honest:

```java
@GetMapping("/parcels/{id}/events")
public Page<TrackingEventResponse> events(
        @PathVariable String id,
        @PageableDefault(size = 50, sort = "occurredAt") Pageable pageable) {
    return parcels.events(id, pageable);
}
```

Return `Page` when the UI needs total counts; return `Slice` when "has next" is enough and count queries hurt. Cap `size` so a client cannot ask for a million events. Stable sort keys matter — without them, page two drifts under concurrent inserts.

DTO boundaries close the loop. Request and response types are not your JPA entities. Entities grow lazy associations and persistence annotations; JSON serializers will happily walk them into N+1 territory and leak columns you never meant to publish. Map explicitly at the edge.

Status discipline stays non-negotiable: `201` for creates, `204` for empty successful deletes, `404` for missing parcels, `409` for conflicts, `400` for validation. One error envelope from your advice keeps mobile parsers sane.

Caching headers on pure GETs of immutable snapshots can help; do not cache personalized or rapidly changing gate state without thought. Prefer ISO-8601 timestamps and explicit money types. Empty collections are `200` with `[]`, not `404`.

RPC-in-disguise paths (`/parcels/doCheckIn`) fight every HTTP tool you adopt later. Returning entities "just for now" becomes forever. Skipping idempotency because "retries are rare" guarantees duplicate parcels on the first flaky pier Wi-Fi day.

Phase Three gave you the HTTP front door and the habits to speak it carefully. The next pressure is storage: vessels, manifests, and cargo lines that must survive process restarts. Mapping those as entities — instead of hand-written JDBC for every vessel column — is where Spring Data JPA begins.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 37 (*REST Best Practices*).
