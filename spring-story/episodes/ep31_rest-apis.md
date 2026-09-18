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

A `@RestController` that returns objects is not yet a REST API. REST is a contract style: resources, verbs, representations, and status codes that clients can trust.

Teams often start with "JSON endpoints" and discover the pain later. One method returns 200 with an error string in the body. Another returns 200 for create. Paths look like `/getOrder` and `/createOrder` — RPC painted with HTTP. Content types are inconsistent. Clients cannot cache, cannot tell success from failure without parsing bodies, and cannot evolve without breaking every caller. Spring does not force good REST on you. It gives you the tools to express a deliberate contract.

Think in resources, not in procedure names. An order is a resource at `/orders/{id}`. A collection lives at `/orders`. Creating an order is `POST /orders` with a body. Updating is `PUT` or `Patch` depending on your semantics. Deleting is `DELETE`. Reading is `GET`. The Java method names can be `create` or `get`; the public contract is the URL plus the verb.

```java
@RestController
@RequestMapping("/orders")
public class OrderApi {

    private final OrderService orders;

    public OrderApi(OrderService orders) {
        this.orders = orders;
    }

    @PostMapping(consumes = MediaType.APPLICATION_JSON_VALUE,
                 produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<OrderResponse> create(@RequestBody CreateOrderRequest body) {
        OrderResponse created = orders.create(body);
        return ResponseEntity
                .created(URI.create("/orders/" + created.id()))
                .body(created);
    }

    @GetMapping(value = "/{id}", produces = MediaType.APPLICATION_JSON_VALUE)
    public OrderResponse get(@PathVariable long id) {
        return orders.findById(id);
    }
}
```

`ResponseEntity` is how you own status and headers without leaving the controller. A create that returns `201 Created` plus a `Location` header is more honest than a bare `200` with a body. `consumes` and `produces` make content negotiation explicit: the client must send JSON, and you promise JSON back. Jackson message converters handle serialization when the classpath and configuration agree.

Idempotency and safety are part of the spoken contract. Safe methods like `GET` should not change server state. Idempotent methods like `PUT` and `DELETE` should be repeatable with the same outcome. `POST` is the usual non-idempotent create. When you blur those lines — a `GET` that deducts inventory — caches and retries become landmines.

Versioning and representation design deserve a short honest take. Prefer stable resource names and evolve fields carefully. If you must version, pick a strategy and stick to it — URI prefix like `/v1/orders` or a version media type — but do not invent three strategies in one codebase. Separate request DTOs from response DTOs when the shapes diverge; exposing your JPA entity as the API body couples persistence to every client.

Hypermedia is optional; honesty is not. You do not need a full HATEOAS graph on day one. You do need documented fields, predictable nullability, and stable enum strings. Prefer ISO-8601 timestamps and explicit money representations over ambiguous doubles. When a collection is empty, return `200` with an empty list, not `404` — `404` means the collection resource itself is missing, which is rare for `/orders`.

Message conversion is the quiet machinery behind REST in Spring. `HttpMessageConverter` implementations turn Java objects into JSON, XML, or other representations based on `Accept` and `Content-Type`. If conversion fails, you get framework exceptions that your advice can map. If you never set `produces`/`consumes`, defaults usually still work for JSON-first APIs — until a client sends `text/plain` and you are surprised. Explicit media types make that surprise a 415 instead of a mystery.

A topic-specific misconception is "REST means JSON over HTTP." JSON is a common representation, not the definition. Another is treating every successful method as HTTP 200. Creates, deletes, and empty results have better status vocabulary. A third is returning domain entities directly and then wondering why lazy-loading and password hashes appear in API payloads.

So today we moved from "controller methods exist" to "HTTP as a resource contract": verbs, status codes, media types, and `ResponseEntity` as the deliberate response tool.

But a contract that accepts a body still has a hole. What happens when the JSON is well-formed yet the fields are missing, blank, or nonsense — and who should reject that before the service layer runs?

Validation is that boundary.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 31 (*REST APIs*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
