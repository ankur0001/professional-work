# Episode 02 — Spring Architecture

| Field | Value |
|---|---|
| Episode | 02 |
| Title | Spring Architecture |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 2 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Once you know why Spring exists, the next question is almost unavoidable: what pieces make up Spring itself?

Here is the pain this lesson exists to remove. Problem Statement Monolithic "framework JAR" dependencies cause classpath bloat and version skew. Without modular architecture, a REST API might accidentally pull ORM, JMS, and SOAP stacks. Spring's layered modules let libraries depend only on spring-context , not the entire web stack.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The idea we need next is Spring Architecture.

At a practical level, Spring Architecture is the Spring mechanism you reach for when this pain shows up in a real codebase. Treat it as a tool with a clear job — not as a checklist item.

Spring's design choice here is deliberate. Architectural styles give teams a shared language for boundaries, dependencies, and change.

Once you accept the feature, the next honest question is how it works under the hood. Dependency direction and boundary rules decide what can know about what — and what stays replaceable.

Let's make this concrete with a small example you can read aloud and still follow.

```java
public class OrderService {
 private final PaymentGateway gateway = new StripePaymentGateway(
 System.getenv("STRIPE_KEY") // fails in tests, hard to mock
 );
 private final OrderRepository repo = new JdbcOrderRepository(
 DriverManager.getConnection(...) // untestable, no pool
 );
}
```

Read it top to bottom once. Notice what your code declares versus what the framework takes over. The point of Spring is rarely "more annotations." The point is fewer decisions you must reinvent on every project.

A common misunderstanding is to memorize names without a mental model. If you can only recite an annotation or class name, you do not own the concept yet. If you can explain the problem it removes, the runtime piece that implements it, and one failure mode, you are ready for production conversations.

Today we walked through Spring Architecture inside Phase 1 — Spring Fundamentals. The next natural question is waiting in Episode 03 — IoC (Inversion of Control).

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 2 (*Spring Architecture*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
