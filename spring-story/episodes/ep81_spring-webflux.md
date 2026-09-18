# Episode 81 — Spring WebFlux

| Field | Value |
|---|---|
| Episode | 81 |
| Title | Spring WebFlux |
| Phase | Phase 8 — Reactive Spring |
| Catalog handbook lesson | 81 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Reactor gave us `Mono`, `Flux`, schedulers, and backpressure. Spring WebFlux is how those types become HTTP servers and clients on a non-blocking stack — typically Netty with Boot’s WebFlux starter, not an embedded Tomcat servlet container.

Contrast the center of gravity. Spring MVC: `DispatcherServlet`, thread-per-request style, blocking signatures returning objects or `ResponseEntity`. WebFlux: reactive HTTP, handlers that return `Mono` / `Flux`, and a choice of programming model — annotated `@RestController` familiar from MVC, or functional `RouterFunction` / `HandlerFunction` beans. Same application for JSON APIs; different concurrency contract.

```java
@RestController
@RequestMapping("/api/orders")
class OrderController {
    private final OrderService orders;

    @GetMapping("/{id}")
    Mono<Order> byId(@PathVariable String id) {
        return orders.findById(id); // Mono from reactive repo / WebClient
    }

    @GetMapping(produces = MediaType.APPLICATION_NDJSON_VALUE)
    Flux<Order> stream(@RequestParam String tenant) {
        return orders.streamOpen(tenant);
    }
}

// Functional style alternative:
@Bean
RouterFunction<ServerResponse> routes(OrderHandler handler) {
    return route(GET("/api/orders/{id}"), handler::byId)
        .andRoute(GET("/api/orders"), handler::stream);
}

// Client side (non-blocking):
WebClient client = WebClient.create("https://inventory.example");
Mono<Stock> stock = client.get()
    .uri("/sku/{sku}", sku)
    .retrieve()
    .bodyToMono(Stock.class);
```

`WebClient` replaces blocking `RestTemplate` in this world. It returns publishers; you compose them with the same operators you already learned. Connecting WebFlux to a blocking DataSource without offloading will stall Netty event loops — pair WebFlux with R2DBC or wrap blocking JDBC on `boundedElastic` at a clear boundary.

Boot chooses the stack from the classpath. `spring-boot-starter-web` pulls MVC. `spring-boot-starter-webflux` pulls WebFlux. Putting both on the classpath makes Boot prefer MVC unless you force a reactive application type. Be explicit in multi-module builds so you do not accidentally ship a servlet stack while writing `Mono` return types that never get a reactive runtime.

Error handling and validation have reactive-aware variants, but the teaching point for this episode is the request pipeline: channel reads bytes, decoding produces objects, your handler returns a publisher, encoding writes when items arrive, cancellation propagates when clients disconnect. That is why returning `Flux` for SSE is natural here and awkward under a blocking servlet mindset.

A misconception is "WebFlux is always faster than MVC." For modest concurrency and blocking drivers, MVC is often simpler and plenty fast. WebFlux shines when concurrency and I/O wait dominate and the whole stack is non-blocking. Another misconception is using WebFlux only because it looks modern while calling `.block()` in every handler — that is the worst of both models.

We can serve reactive HTTP. Security still matters — identity and authorization cannot vanish because we changed the server. The filter story must move to the reactive channel.

That is reactive security.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 81 (*Spring WebFlux*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
