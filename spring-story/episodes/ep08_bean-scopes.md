# Episode 08 — Bean Scopes

| Field | Value |
|---|---|
| Episode | 08 |
| Title | Bean Scopes |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 8 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Incident channel, 19:40. Two guests booking the Harborview Hotel on different laptops somehow share a cart. Guest A selects a king ocean-view; Guest B refreshes and sees A's room with A's loyalty rate. Support screenshots prove it. Engineering finds `BookingCart` registered as the default singleton — one instance for the whole JVM — stuffed into a `@Controller` that was never meant to hold per-user state.

Scope is the answer to "how many instances, and over what boundary?" Spring's built-in scopes include singleton (one per container), prototype (new instance every retrieval), and, in web-aware contexts, request, session, and application. Default is singleton. That default is correct for stateless services and wrong for a mutable cart.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class BookingCart {
    private final List<RoomHold> holds = new ArrayList<>();

    public void add(RoomHold hold) { holds.add(hold); }
    public List<RoomHold> holds() { return List.copyOf(holds); }
    public void clear() { holds.clear(); }
}

@RestController
public class BookingController {
    private final BookingCart cart;
    private final ReservationService reservations;

    public BookingController(BookingCart cart, ReservationService reservations) {
        this.cart = cart;
        this.reservations = reservations;
    }

    @PostMapping("/cart/rooms")
    public CartView addRoom(@RequestBody RoomHold hold) {
        cart.add(hold);
        return CartView.from(cart);
    }
}
```

Runtime for session scope with a scoped proxy. On context refresh Spring does not put one shared `BookingCart` into the controller. It injects a proxy. On each HTTP call, when the controller touches `cart.add`, the proxy resolves the real cart for the current HTTP session — creating one on first use — and delegates. Guest A's session id maps to cart instance A; Guest B gets cart instance B. When the session expires, that cart becomes eligible for destruction callbacks. Singleton `ReservationService` stays one shared instance, which is what you want for a stateless booking API client.

Prototype scope would create a new cart on every `getBean` or injection point resolution — usually wrong for a cart you mutate across several requests. Request scope lives for one HTTP request only; useful for per-request buffers, useless for a multi-step booking wizard.

Misconception unique to scopes: "Annotating `@Scope("session")` without a proxy is enough when injecting into a singleton." If a singleton controller receives a session-scoped object without `proxyMode` (or ObjectFactory/Provider), it may capture one session's instance at injection time and share it forever — the Harborview bug in a tuxedo. The proxy (or lookup API) re-resolves per call.

Carts are isolated again. The next outage is different: Redis connections for rate caching are created lazily on the first booking spike after deploy, and the pool warms under traffic instead of before it. Creation timing — not instance count — is now the problem.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 8 (*Bean Scopes*).
