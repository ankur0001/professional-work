# Episode 01 — Why Spring?

| Field | Value |
|---|---|
| Episode | 01 |
| Title | Why Spring? |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 1 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Before we talk about annotations or Boot starters, let's start with a situation teams kept hitting in enterprise Java.

Imagine you are building a banking or logistics backend in the early two-thousands. You already have Java. You already have servlets. You may even have an application server. And yet every new feature feels heavier than the business logic itself. You need an object that talks to payments, another that talks to orders, another that logs, another that starts a transaction. So where do you create them? Inside constructors with `new`? In a giant factory class? Through JNDI lookups that only work inside the server?

That is not a syntax problem. That is an assembly problem.

Before Spring became the default answer, many teams paid the same bill every week. Enterprise JavaBeans asked for remote and local interfaces, home objects, and container callbacks. Deployment descriptors grew until XML dwarfed the domain code. Redeploys took minutes, so feedback loops died. Tests were awkward because code reached into `InitialContext` lookups. And switching app servers was never "just a deploy" — vendor lock-in hid in the corners.

So a practical question appears: can we keep Java's strengths, keep POJOs readable, and still get transactions, wiring, and web integration without drowning in ceremony?

That question is why Spring exists.

Spring Framework is an application framework for Java that simplifies enterprise development by providing Inversion of Control, Dependency Injection, and Aspect-Oriented Programming on top of plain Java objects. The shift is easy to say and easy to underestimate. Instead of your code hunting for collaborators, the Spring container assembles, configures, and manages the object graph. You describe what a type needs. The container decides how the graph comes alive.

Hold the three pillars in your head as promises, not buzzwords. IoC means the container owns object creation and lifecycle. DI means dependencies are supplied — usually through constructors — instead of looked up. AOP means cross-cutting concerns like logging, security, and transactions can be modularized instead of copy-pasted into every service method. We will deepen each pillar in later episodes. Today we only need the shape of the stack.

A little history makes the design less mysterious. Rod Johnson published *Expert One-on-One J2EE Design and Development* in 2002. The book included tens of thousands of lines of educational framework code. That code became Spring. The thesis was blunt: J2EE had over-engineered everyday problems. Many teams did not need EJB-heavy solutions for wiring and cross-cutting concerns. Interfaces, factories, and a lightweight container could carry enterprise features while staying testable.

Now separate three names people mash together. Spring Framework is the core IoC and DI engine plus modules for data access, web, AOP, and testing. Spring Boot is an opinionated layer on top that removes boilerplate — auto-configuration, embedded servers, starters. Spring Cloud adds distributed-system patterns on top of Boot. You can use the Framework alone. In modern delivery, Boot is the usual on-ramp. Cloud is for multi-service systems. Lesson one is still Framework thinking: who owns creation, wiring, and lifecycle?

Let's make the before-and-after concrete. In a pre-Spring style, an `OrderService` might construct a `StripePaymentGateway` with an environment variable inside the field initializer, then construct a JDBC repository the same way. It works on one laptop. It fails in tests. It resists swapping implementations. It hides dependencies inside `new`.

In a Spring style, `OrderService` declares what it needs in the constructor — a payment gateway port and an order repository. The container supplies implementations. In a test, you pass fakes. In production, you pass real adapters. The business method stays about orders, not about construction.

```java
public class OrderService {
    private final PaymentGateway gateway;
    private final OrderRepository repo;

    public OrderService(PaymentGateway gateway, OrderRepository repo) {
        this.gateway = gateway;
        this.repo = repo;
    }

    public Order place(Cart cart) {
        PaymentResult paid = gateway.charge(cart.total());
        return repo.save(Order.from(cart, paid));
    }
}
```

Read that again slowly. There is no Spring import in the domain class. That is the point. Spring is invasive to configuration and assembly, not to every business type. The framework earns trust when your domain can still be reasoned about as plain Java.

Under the hood, at the highest level, Spring splits into a core container, data access, web, AOP, and test modules. The container reads bean definitions — metadata about classes, scope, properties, and dependencies — registers them in a `BeanFactory`, and materializes objects on demand or at startup. `ApplicationContext` extends that foundation with events, internationalization, and resource loading. Most applications talk to an `ApplicationContext`, not to the lowest-level factory API. We will open those layers in the next episodes. For now, remember the pipeline: metadata in, managed object graph out.

A common misunderstanding is to treat Spring as "annotations you sprinkle until the red lines go away." If you only memorize `@Component` and `@Autowired`, you do not own the idea yet. The idea is control inversion: your code stops being the composer of the orchestra and becomes one musician with a clear part. Another misunderstanding is thinking Spring replaces Java or the servlet model. It does not. It composes them with less glue code and more testability.

So today we answered why Spring showed up: assembly pain, testability pain, and cross-cutting duplication in enterprise Java. We named the three pillars. We separated Framework, Boot, and Cloud. And we saw a tiny service that depends on interfaces instead of constructing concrete collaborators.

The next natural question is unavoidable. If Spring is a container that builds object graphs, what are the moving parts of that container — and how do they fit together?

That is Episode Two — Spring Architecture.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 1 (*Why Spring?*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
