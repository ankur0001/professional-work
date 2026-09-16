# Episode 29 — DispatcherServlet

| Field | Value |
|---|---|
| Episode | 29 |
| Title | DispatcherServlet |
| Phase | Phase 3 — Spring MVC |
| Catalog handbook lesson | 29 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Every HTTP request needs a front door. In Spring MVC, that front door is DispatcherServlet.

Here is the pain this lesson exists to remove. Multiple servlets duplicate: encoding, security, exception handling, content negotiation. DispatcherServlet centralizes the pipeline so controllers focus on business logic only.

So the natural question becomes: what does Spring give us so we do not keep paying that cost? The answer we need is DispatcherServlet.

Key methods: doDispatch , getHandler , processHandlerException . Boot: DispatcherServletAutoConfiguration registers servlet with order and path. Reading the Source — Suggested Entry Points AbstractApplicationContext.refresh() — orchestrates context startup; read this once to see the big picture. DefaultListableBeanFactory.preInstantiateSingletons() — eager singleton creation pass. AutowiredAnnotationBeanPostProcessor.postProcessProperties() — where injection metadata becomes field/constructor values. ConfigurationClassParser.parse() — turns @Configuration into bean definitions at runtime.

A little context helps the idea stick. Spring MVC 1.0 (2003) introduced DispatcherServlet as evolution of Struts/Tapestry front-controller models. Spring 3.0 added annotation-driven @RequestMapping . Spring 4.0 improved REST support. Boot embeds Tomcat and registers DispatcherServlet automatically — no web.xml required.

Spring's design choice here is deliberate. Pluggable strategy interfaces (HandlerMapping, HandlerAdapter) allow extension without modifying core servlet. Same DispatcherServlet powers traditional MVC (JSP/Thymeleaf) and REST (@RestController returns body directly).

Once you accept the feature, the next honest question is how it works under the hood. Check multipart → MultipartResolver 2. getHandler() → HandlerExecutionChain (handler + interceptors) 3. getHandlerAdapter() → supports(handler)? applyPreHandle() on interceptors 5. ha.handle() → invoke controller method 6. processDispatchResult() → view or @ResponseBody 7. applyPostHandle / triggerAfterCompletion Application startup

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

Today we walked through DispatcherServlet inside Phase 3 — Spring MVC. The next natural question is waiting in Episode 30 — Controllers.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 29 (*DispatcherServlet*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
