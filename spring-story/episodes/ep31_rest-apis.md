# Episode 31 — REST APIs

| Field | Value |
|---|---|
| Episode | 31 |
| Title | REST APIs |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 31 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

A `@RestController` that returns objects is not yet a REST API. REST is a contract style: resources, verbs, representations, and status codes that clients can trust — especially when the resource is a parcel moving through a harbor.

Teams often start with "JSON endpoints" and discover the pain later. One method returns 200 with an error string in the body. Another returns 200 for create. Paths look like `/getParcel` and `/createParcel` — RPC painted with HTTP. Content types drift. Trucking clients cannot cache, cannot tell success from failure without parsing bodies, and cannot evolve without breaking every scanner. Spring does not force good REST on you. It gives you the tools to express a deliberate contract.

Think in resources, not procedure names. A parcel is a resource at `/parcels/{id}`. A collection lives at `/parcels`. Creating a parcel is `POST /parcels` with a body. Updating is `PUT` or `PATCH` depending on your semantics. Deleting is `DELETE`. Reading is `GET`. Tracking events hang under the parcel: `/parcels/{id}/events`. The Java method names can be `create` or `get`; the public contract is the URL plus the verb.

```java
@RestController
@RequestMapping("/parcels")
public class ParcelApi {

    private final ParcelTracking tracking;

    public ParcelApi(ParcelTracking tracking) {
        this.tracking = tracking;
    }

    @PostMapping
    public ResponseEntity<ParcelResponse> create(@RequestBody CreateParcelRequest body) {
        ParcelResponse created = tracking.register(body);
        return ResponseEntity
                .created(URI.create("/parcels/" + created.id()))
                .body(created);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ParcelResponse> get(@PathVariable String id) {
        return tracking.find(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/{id}/events")
    public List<TrackingEventResponse> events(@PathVariable String id) {
        return tracking.eventsFor(id);
    }
}
```

`ResponseEntity` is deliberate response control. `201 Created` with a `Location` header tells clients where the new parcel lives. `404` for an unknown id is a status, not a soft null body with 200. `GET` stays safe and idempotent; `POST` creates. Media types matter too: declare `produces` and `consumes` when you support more than one representation, and fail loudly on mismatch instead of guessing.

Versioning and representation design deserve a short honest take. Prefer stable resource names and evolve fields carefully. If you must version, pick a strategy and stick to it — URI prefix like `/v1/parcels` or a version media type — but do not invent three strategies in one codebase. Separate request DTOs from response DTOs when the shapes diverge; exposing a JPA entity as the API body couples persistence to every trucking client.

Hypermedia is optional; honesty is not. You do not need a full HATEOAS graph on day one. You do need documented fields, predictable nullability, and stable enum strings for parcel states. Prefer ISO-8601 timestamps. When a collection of events is empty, return `200` with an empty list, not `404` — `404` means the parcel resource itself is missing.

A frequent wrong turn is treating every successful Java return as HTTP 200, including creates and deletes. Another is encoding actions in the path (`/parcels/{id}/markDelivered`) when a state transition could be a `PATCH` on the parcel or a POST to a subordinate resource. A third is leaking internal database ids in URLs you are not willing to support forever — prefer opaque public tracking ids.

Controllers can now claim paths. Claiming a path still leaves a hole: what happens when the JSON is well-formed yet the customs fields are missing, blank, or nonsense — and who should reject that before the tracking service runs?

That boundary is validation.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 31 (*REST APIs*).
