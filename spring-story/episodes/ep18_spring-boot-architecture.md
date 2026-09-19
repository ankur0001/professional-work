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

Breakpoint on `SpringApplication.run` for the bike-share API. One docking-station service, one fat jar, one `main`. You step over the call and watch phases fire: bootstrap listeners, Environment prepared, ApplicationContext created, beans refreshed, embedded Tomcat started, `ApplicationRunner` beans executed. Cold start is not a blur — it is a pipeline. Boot's architecture is that pipeline plus the opinions that fill it in.

Spring Boot is not a separate DI container. It is an opinionated layer on Spring Framework that builds an `ApplicationContext` for you, auto-configures common infrastructure when the classpath looks right, embeds a web server when you need HTTP, and packages runnable artifacts. `SpringApplication` is the conductor. Auto-configuration classes are the sheet music that plays only when conditions match. Starters are curated dependency sets that make those conditions true on purpose.

```java
@SpringBootApplication
public class BikeShareApi {
    public static void main(String[] args) {
        SpringApplication app = new SpringApplication(BikeShareApi.class);
        app.addListeners(event -> {
            if (event instanceof ApplicationEnvironmentPreparedEvent e) {
                System.out.println("env ready, active=" +
                    Arrays.toString(e.getEnvironment().getActiveProfiles()));
            }
            if (event instanceof ContextRefreshedEvent) {
                System.out.println("context refreshed — beans ready");
            }
        });
        app.run(args);
    }
}
```

Walk the experiment. `new SpringApplication(BikeShareApi.class)` records the primary source — your `@SpringBootApplication` class — without starting anything yet. `addListeners` hooks the pipeline so you can observe phases; `ApplicationEnvironmentPreparedEvent` fires once profiles and property sources exist but before most beans. `app.run(args)` executes the full cold-start sequence and blocks until the embedded server is up (for a web app) or until non-web runners finish.

Runtime cold-start timeline for a docking lookup, slower on purpose. First, `SpringApplication` deduces web application type from the classpath: servlet stack present → SERVLET; WebFlux without servlet → REACTIVE; neither → NONE. It starts a bootstrap context for early logging configuration and `SpringApplicationRunListener`s. It prepares the Environment: loads `application.yml`, applies profile documents, attaches command-line args from `args`, publishes environment-prepared events — this is when your listener can print active profiles. It prints the banner. It creates the matching `ApplicationContext` implementation (`AnnotationConfigServletWebServerApplicationContext` for servlet). It loads sources: `BikeShareApi` plus auto-configuration imports triggered by `@EnableAutoConfiguration` inside `@SpringBootApplication`. It refreshes the context: bean definition loading, `BeanFactoryPostProcessor`s, singleton pre-instantiation — DataSource, MVC infrastructure, your `StationDirectory` if scanned. It creates and starts the embedded web server, publishing started/ready events. `ApplicationRunner` / `CommandLineRunner` beans run. Only then does `GET /stations/{id}` hit a `DispatcherServlet` backed by beans Boot mostly assembled without an XML file from 2012.

Failure mode with symptoms on cold start: classpath includes a JDBC driver and Hikari, but no `spring.datasource.url`. Auto-config registers a DataSource bean; refresh fails with `Failed to configure a DataSource: 'url' attribute is not specified`. The stack points at auto-configuration, not your application package — which is the architecture lesson: Boot inserted a definition you did not write because the classpath signaled "database." Another failure: wrong web type deduction after accidentally adding both servlet and reactive starters — confusing context type and "which stack am I on?" debugging. Listeners that throw during environment prepare abort startup before any controller exists; symptom is a short log ending at bootstrap, no Tomcat port bind.

Trade-offs. The pipeline removes dozens of manual assembly steps and standardizes startup across services; it also concentrates "magic" into phases you must learn to observe (`--debug`, condition reports, startup events). Hand-building an `AnnotationConfigApplicationContext` is clearer for teaching BeanFactory, but slower for shipping APIs. Boot's opinions (embedded server, auto-config, fat jar) are defaults you can override — excluding auto-config, providing your own `SpringApplication` customizers, switching to WAR deployment — each override costs knowledge of which phase you are interrupting.

Misconception unique to Boot architecture: "Boot replaces Spring Framework — learning Framework concepts is optional." Boot orchestrates Framework. When auto-config surprises you, you debug bean definitions, conditions, and the context — Framework vocabulary — not a magical Boot-only machine.

The bike-share API is up in seconds on a laptop. A developer adds `postgresql` driver "just for later" and suddenly a DataSource bean appears and fails startup because no URL is set. Who created that bean without a `@Bean` method in the application package?

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 18 (*Spring Boot Architecture*).
