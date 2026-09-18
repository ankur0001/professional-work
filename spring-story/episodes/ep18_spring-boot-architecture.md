# Episode 18 — Spring Boot Architecture

| Field | Value |
|---|---|
| Episode | 18 |
| Title | Spring Boot Architecture |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 18 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You already know why Boot exists. The next gap is sharper: when you call `SpringApplication.run`, what actually happens — in order — before your first controller can answer?

Teams that skip this map treat Boot like a black box. Something fails at startup, the log dumps a stack of auto-config class names, and nobody can say whether the Environment, the context, or the embedded server is the broken piece. Architecture is the antidote. It turns the shortcut into a pipeline you can reason about.

Ask it the way an engineer asks it on a bad Monday: if Boot is not a second framework, what are the moving parts of one Boot process, and who owns each phase?

Spring Boot's runtime architecture is a deliberate sequence layered on the Framework you already studied. `SpringApplication` is the orchestrator. It prepares an `Environment`, creates an `ApplicationContext`, imports auto-configuration, refreshes the context so beans exist, starts an embedded web server when the classpath says "web," and publishes lifecycle events so listeners can react. Your `@SpringBootApplication` class is the entry metadata. The Framework still owns beans, DI, and MVC. Boot owns the opinions and the startup choreography.

Walk the sequence without magic language. First the Environment: command-line args, `application.properties` or YAML, OS environment variables, and profile activation land in one property abstraction. Second, context creation: typically a `AnnotationConfigServletWebServerApplicationContext` for servlet apps, or a reactive equivalent. Third, sources and auto-configuration: Boot loads your configuration classes and conditionally imports auto-config classes discovered from the classpath. Fourth, refresh: bean definitions are processed, singletons are created, and injection happens — the same ApplicationContext refresh you already know, now with Boot's imported config in the mix. Fifth, the web server: if Tomcat, Jetty, or Undertow is present and web auto-config activates, Boot starts an embedded container and registers the dispatcher. Sixth, readiness: `ApplicationReadyEvent` and related events fire so you can run post-start hooks.

```java
@SpringBootApplication
public class OrdersApplication {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(OrdersApplication.class);
        app.addListeners(event -> {
            if (event instanceof ApplicationReadyEvent) {
                System.out.println("context ready — server listening");
            }
        });
        app.run(args);
    }
}
```

That snippet is not about printing a line. It shows that startup is evented. You can observe phases. You can also call `SpringApplication.run(OrdersApplication.class, args)` and get the same pipeline with less ceremony. Either way, the architecture is Environment → context → auto-config import → refresh → embedded server → ready.

Compare that to plain Spring. You might build a WAR, drop it into an external Tomcat, and wire a `DispatcherServlet` yourself. Boot inverts the packaging: the process is the unit of deployment, and the server is a library inside the JAR. Same servlet model underneath. Different ownership of bootstrap.

One trap is thinking "architecture" means memorizing every class in `org.springframework.boot`. You need the pipeline and the seams: where properties enter, where conditions decide beans, where the server starts, where you override. Another trap is blaming Boot when a bean fails to wire — often the Framework refresh is doing exactly what it always did; Boot only decided which definitions to import.

Hold that last seam carefully. The import step is where Boot stops looking like a launcher and starts looking like conditional configuration. If you cannot see which auto-config classes activated and why, the rest of Phase Two stays foggy.

That fog is the next lesson: auto-configuration itself — conditions, back-off, and how classpath clues become real beans.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 18 (*Spring Boot Architecture*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
