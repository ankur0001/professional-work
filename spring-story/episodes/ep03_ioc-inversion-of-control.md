# Episode 03 — IoC (Inversion of Control)

| Field | Value |
|---|---|
| Episode | 03 |
| Title | IoC (Inversion of Control) |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 3 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We know Spring is modular. Now look at what happens inside the container modules when an application starts — because that is where control quietly changes hands.

Open a checkout flow written the old way. `CheckoutService` constructs a `StripeClient`, an `InventoryClient`, and an `EmailNotifier` in its fields. Each collaborator opens connections, reads secrets from environment variables, and maybe starts a background thread. The service thinks it is "just business logic," but it has become the composer, the configurator, and the lifecycle owner of half the system. Unit tests either hit real Stripe or invent brittle subclasses. Swapping email for a queue means editing the service. Shutdown is somebody's afterthought.

What goes wrong is not Java syntax. What goes wrong is who holds the baton. The application code is conducting creation, wiring, and teardown. That is the cost Inversion of Control exists to remove.

An engineer staring at that class usually asks: can something else own construction and lifecycle so my service only owns checkout rules?

Inversion of Control, in Spring's sense, means yes. The container — not your constructors — decides when objects are created, how long they live, and when they are destroyed. Your types declare what they are and what they need. The framework runs the assembly line. Hollywood principle, said plainly: don't call the framework to look things up; the framework calls you into existence when the graph is ready.

```java
public class CheckoutService {
    private final PaymentClient payments;
    private final InventoryClient inventory;
    private final EmailNotifier email;

    // No `new` of collaborators. IoC: the container constructs this
    // after it has already constructed the dependencies.
    public CheckoutService(PaymentClient payments,
                           InventoryClient inventory,
                           EmailNotifier email) {
        this.payments = payments;
        this.inventory = inventory;
        this.email = email;
    }

    public Receipt checkout(Cart cart) {
        inventory.reserve(cart.lines());
        PaymentResult paid = payments.charge(cart.total());
        email.sendReceipt(paid);
        return Receipt.of(paid);
    }
}
```

Watch the runtime story. On context refresh, Spring reads bean definitions, instantiates `PaymentClient`, `InventoryClient`, and `EmailNotifier` according to their definitions, then calls the `CheckoutService` constructor with those instances. Your `checkout` method never asks a registry where payment lives. Control of creation inverted: the container called your constructor; you did not call `new` on the world.

IoC is broader than Dependency Injection. DI is the usual mechanism Spring uses to supply collaborators once the container owns creation. You can have inversion without calling it DI — think template methods or callback-driven frameworks — but in Spring day-to-day work, IoC shows up as the container owning the object graph. People blur the words. Keep them stacked: IoC is who is in charge; DI is how dependencies arrive.

A misconception specific to IoC is "if I still write `new` for a value object, I broke Spring." You did not. Inversion targets application components with lifecycle and wiring needs — services, repositories, gateways — not every `Money` or `LineItem` record. Another misconception is that IoC means your code never runs first. Your `main` method still starts the process; after that, the container takes over the component graph.

So the container owns creation. That still leaves a sharp follow-up: once the container creates objects, how do those objects actually receive the collaborators they declare? That mechanism — Dependency Injection — is the everyday skill we open next.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 3 (*IoC (Inversion of Control)*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
