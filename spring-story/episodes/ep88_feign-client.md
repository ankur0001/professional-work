# Episode 88 — Feign Client

| Field | Value |
|---|---|
| Episode | 88 |
| Title | Feign Client |
| Phase | Phase 9 — Spring Cloud |
| Catalog handbook lesson | 88 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Load-balanced WebClient works. You still end up repeating URIs, verb choices, and DTO decoding in every caller. OpenFeign — via Spring Cloud OpenFeign — offers a different surface: declare a Java interface that mirrors the remote HTTP API, annotate methods like a controller in reverse, and let a runtime proxy turn method calls into HTTP requests. The interface becomes your anti-corruption layer for a remote service.

Enable it on the Boot application with `@EnableFeignClients`, then write a client interface. The `name` (or `value`) attribute is the service id used with discovery and load balancing. Method annotations use Spring MVC annotations in the Spring Cloud integration, so the vocabulary matches what you already know from controllers.

```java
@FeignClient(name = "inventory-service")
public interface InventoryClient {

    @GetMapping("/stock/{sku}")
    StockView getStock(@PathVariable("sku") String sku);

    @PostMapping("/reservations")
    ReservationResult reserve(@RequestBody ReserveRequest request);
}
```

```java
@Service
public class OrderService {
    private final InventoryClient inventory;
    private final OrderRepository orders;

    public OrderService(InventoryClient inventory, OrderRepository orders) {
        this.inventory = inventory;
        this.orders = orders;
    }

    public Order place(PlaceOrderCommand cmd) {
        StockView stock = inventory.getStock(cmd.sku());
        if (stock.available() < cmd.qty()) {
            throw new InsufficientStockException(cmd.sku());
        }
        inventory.reserve(new ReserveRequest(cmd.sku(), cmd.qty()));
        return orders.save(Order.from(cmd));
    }
}
```

Read that carefully. `OrderService` depends on `InventoryClient` the same way it would depend on a local port. There is no URL string in the service. At runtime, Feign creates a JDK proxy for the interface. A call to `getStock("SKU-9")` becomes an HTTP GET to a chosen `inventory-service` instance at `/stock/SKU-9`, with encoders and decoders handling JSON. If you set `url` on `@FeignClient` instead of relying on `name`, you bypass discovery — useful for third-party APIs, wrong for internal mesh services you want balanced.

Configuration hooks matter in production. You can set connect and read timeouts, log request/response bodies at a chosen level, and plug request interceptors that attach authorization headers. Error decoders map HTTP 404 or 409 into domain exceptions instead of generic Feign failures. Contract mismatches — client expects a field the server renamed — still fail at runtime; Feign does not invent schema evolution for you.

```java
@FeignClient(
        name = "inventory-service",
        configuration = InventoryFeignConfig.class,
        fallback = InventoryClientFallback.class)
public interface InventoryClient {
    // ...
}
```

Fallbacks hint at the next resilience story. A fallback class provides substitute behavior when the remote call fails. Treat fallbacks as deliberate degraded mode — cached stock, empty reservations queue, fail-soft — not as silent sweeps that hide outages from operators.

Testing Feign clients without the network usually means stubbing the interface in unit tests, or using WireMock / Spring Cloud Contract stubs in slice tests. Do not feel obligated to hit a real inventory process to prove that `OrderService` branches correctly — that is what the Mockito episode will formalize. Do feel obligated to verify the contract of the HTTP shape somewhere, or Friday’s rename will surprise you.

A misconception is generating dozens of Feign clients that mirror every internal controller method and then calling them in chatty loops. You still design APIs for remote use: coarser operations, fewer round trips. Another is sharing the server’s entity classes as Feign DTOs across jars until services cannot deploy independently; prefer dedicated client DTOs. A third is forgetting that Feign is blocking by default in many setups — if your stack is WebFlux-reactive end to end, evaluate whether Feign fits or whether WebClient should remain the client.

Today we replaced hand-built HTTP calls with a declarative Feign interface bound to a service id, wired it into an order service like a normal collaborator, and noted timeouts, error decoding, and fallbacks as the production knobs.

Declarative clients make remote calls easy — which means cascading failure becomes easy too. When inventory starts timing out, do order threads keep piling into a dead dependency until the whole checkout fleet saturates?

That failure mode is why Circuit Breaker exists.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 88 (*Feign Client*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
