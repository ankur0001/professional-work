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

Here is the pain this lesson exists to remove. Monolithic "framework JAR" dependencies cause classpath bloat and version skew. Without modular architecture, a REST API might accidentally pull ORM, JMS, and SOAP stacks. Spring's layered modules let libraries depend only on spring-context , not the entire web stack.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is Spring Architecture.

Spring Source Code Concepts (High Level) GitHub: spring-projects/spring-framework — multi-module Gradle build ( settings.gradle lists modules). Trace dependency: spring-webmvc → spring-context → spring-beans → spring-core . Reading the Source — Suggested Entry Points AbstractApplicationContext.refresh() — orchestrates context startup; read this once to see the big picture. DefaultListableBeanFactory.preInstantiateSingletons() — eager singleton creation pass. AutowiredAnnotationBeanPostProcessor.postProcessProperties() — where injection metadata becomes field/constructor values.

Spring's design choice here is deliberate. Modular architecture enables: Minimal transitive dependencies for libraries. Clear extension points ( BeanFactoryPostProcessor , ApplicationListener ). Replaceable implementations (Tomcat vs Jetty via Boot, JPA vs JDBC).

Once you accept the feature, the next honest question is how it works under the hood. Spring 1.0 shipped as a single dist with optional modules. Over time, Maven modularization enforced clear boundaries. Spring 2.5/3.0 moved configuration from XML namespaces toward annotations. Spring Boot repackaged modules into starters without changing the underlying architecture.

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
