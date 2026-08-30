# Episode 73 — Spring Boot Basics

| Field | Value |
|---|---|
| Episode | 73 |
| Title | Spring Boot Basics |
| Catalog handbook column | 73 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You understand DI. You can wire a service and a repository by hand in a configuration class. Then you spend a day configuring an embedded server, JSON converters, a DataSource, logging levels, and health endpoints — for every new service. The practical pain is boilerplate and decision fatigue. Spring Boot makes the happy path executable: auto-configuration, starters, and opinions so you ship with less ceremony.

```java
@SpringBootApplication
public class App {
  public static void main(String[] args) {
    SpringApplication.run(App.class, args);
  }
}
```

`@SpringBootApplication` bundles common setup: component scanning, auto-configuration enablement, and configuration class semantics. `SpringApplication.run` boots the context and, for web apps, the embedded server. Starters are dependency bill-of-materials flavored for jobs — web, data JPA, security — so you pull a coherent set of libraries instead of assembling versions by folklore. Each starter is a capability decision, not a badge collection. Prefer a thin classpath for faster startup — Episode Sixty-Five's lesson returns inside Boot apps.

Walk a first Boot service. You add `spring-boot-starter-web`, write a controller, run the main class, hit `localhost:8080`. Boot configured a server and JSON converters because the web starter was present. You add Actuator, hit `/actuator/health`, and readiness becomes visible to an orchestrator. When you need a custom DataSource bean, you define it and understand that you are overriding auto-config on purpose.

Auto-configuration is classpath-conditioned opinion. If Tomcat is present and you have not defined a conflicting bean, Boot sets up a server. If a DataSource URL is present, Boot may configure a pool. Read the auto-config report when something surprises you — what kicked in and what backed off. Blind acceptance is how a test dependency on a database driver suddenly changes runtime wiring. Override intentionally with a custom `@Bean` when the default does not fit, and document why — including exclusions so the next engineer does not clean them up by accident.

`application.yaml` needs structure: shared defaults, profile overlays, secrets kept out of git. A giant flat file with every environment mixed together becomes an incident factory. Walk a misconfiguration: JDBC URL in the wrong profile, Boot auto-configures a pool in prod against an empty default. Profile-specific configuration and fail-fast validation of required properties turn Boot from cozy to safe.

Actuator exposes health, metrics, and info that operations need. Lock it down in production — expose health for the platform, protect more sensitive endpoints. "No Actuator" and "Actuator wide open" are both failure modes. Health shows liveness; metrics show HTTP timers. You still need JFR and dumps for deep incidents, but Actuator is how the platform notices you are sick before customers complain.

What does Boot add? Opinionated auto-configuration so you ship with less boilerplate. The humility line follows: auto-config is classpath-driven; add a jar and behavior may change. What it does not add is permission to skip understanding DI, MVC, and persistence underneath. A team needing an internal API by Friday picks web and validation starters, writes controllers with constructor injection, externalizes the database URL, and exposes a health endpoint — opinions removed undecidable trivia so hours go to domain rules. That Friday story only works if the team still understands DI underneath.

A practical Boot day ends with: main class runs, one controller answers, config externalized, health endpoint protected appropriately, and auto-config overrides documented. Then you are ready to deepen MVC rather than collect more starters.

Boot is the executable face of Spring for most modern teams. Next we aim that executable app at HTTP: MVC, REST controllers, validation, and status codes — where the wrong return type or a spilled entity turns a clean Boot app into a production incident.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Boot Basics (Episode 73).

Narration technique: boilerplate pain → Boot thesis → @SpringBootApplication walk → starters/yaml/actuator → override intentionally → bridge to MVC/REST.

Teaching points preserved: @SpringBootApplication; starters; application.yaml; Actuator; override auto-config intentionally.
