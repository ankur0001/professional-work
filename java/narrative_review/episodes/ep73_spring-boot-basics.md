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

`@SpringBootApplication` is a bundle of common setup: component scanning, auto-configuration enablement, and configuration class semantics. `SpringApplication.run` boots the context and, for web apps, the embedded server. Starters are dependency bill-of-materials flavored for jobs — web, data JPA, security — so you pull a coherent set of libraries instead of assembling versions by folklore. `application.yaml` or properties hold externalized config: ports, URLs, feature flags. Actuator exposes health, metrics, and info endpoints that operations needs. Override auto-config intentionally when the opinion does not fit — do not fight the framework blindly, and do not accept every auto-config without reading what it did.

What does Boot add? Opinionated auto-configuration so you ship with less boilerplate. That is the interview line. The humility line follows: auto-config is classpath-driven. Add a jar, and behavior may change. Blindly accepting all auto-config is how surprise DataSources and security filters appear. Giant unstructured `application.yaml` files become a second codebase — structure them, profile them, and document non-obvious keys. Shipping production apps with no Actuator story when you need health and metrics is choosing darkness.

Walk a first Boot service. You add `spring-boot-starter-web`, write a controller, run the main class, hit `localhost:8080`. Boot configured a server and JSON converters because the web starter was present. You add Actuator, hit `/actuator/health`, and readiness becomes visible to an orchestrator. When you need a custom DataSource bean, you define it and understand that you are overriding or supplementing auto-config on purpose.

Auto-configuration is classpath-conditioned opinion. If Tomcat is present and you have not defined a conflicting bean, Boot sets up a server. If a DataSource URL is present, Boot may configure a pool. The practical habit is to read the auto-config report when something surprises you — Boot can show what kicked in and what backed off. Blind acceptance is how a test dependency on a database driver suddenly changes runtime wiring.

Starters reduce version archaeology. `spring-boot-starter-data-jpa` pulls a coherent set. You still own the choice to add it. Each starter is a capability decision, not a badge collection. Prefer a thin classpath for faster startup — Episode Sixty-Five's lesson returns inside Boot apps.

`application.yaml` needs structure: shared defaults, profile overlays, secrets kept out of git. A giant flat file with every environment mixed together becomes an incident factory. Actuator should be locked down in production — expose health for the platform, protect more sensitive endpoints. "No Actuator" and "Actuator wide open" are both failure modes.

Override intentionally with a custom `@Bean` when the default does not fit, and document why. Fighting Boot by disabling half of auto-config without understanding costs more than configuring the opinion it already offers.

What Boot adds is speed to a secure-enough happy path. What it does not add is permission to skip understanding DI, MVC, and persistence behavior underneath.

Walk a misconfiguration. You add a JDBC URL in the wrong profile. Boot auto-configures a pool in prod against an empty default. Startup fails late or connects to the wrong place. Profile-specific configuration and fail-fast validation of required properties turn Boot from cozy to safe. Opinions help; validated opinions help more.

Actuator and operations connect back to JVM diagnostics. Health shows liveness. Metrics show HTTP timers. You still need JFR and dumps for deep incidents, but Actuator is how the platform notices you are sick before customers complain. Leaving it out of production apps that need it is choosing silence.

Override auto-config intentionally also means documenting exclusions so the next engineer does not clean them up by accident.

Boot's opinions extend to testing and packaging. The same main class that runs locally can run as a fat jar in a container. That executable bias is why Boot won teams over XML-heavy setups. Still measure startup — fat jars and component scans cost time — and still keep configuration honest across environments.

A practical Boot day ends with: main class runs, one controller answers, config externalized, health endpoint protected appropriately, and auto-config overrides documented. If those are true, you are ready to deepen MVC rather than collect more starters.

Return to the thesis with a shipping story. A team needs a new internal API by Friday. Without Boot, they debate server choice, JSON library versions, and health check plumbing. With Boot, they pick web and validation starters, write controllers and services with constructor injection, externalize the database URL, and expose a health endpoint for Kubernetes. The framework opinions removed undecidable trivia so the team could spend hours on domain rules. That is what Boot adds when used with understanding rather than as a mystery box.

If auto-config ever surprises you, treat it like a failing test: reproduce, read the condition, adjust the classpath or define an overriding bean, document the decision. Mystery is optional.

That Friday-shipping story only works if the team still understands DI underneath Boot. Otherwise the happy path becomes a maze the first time auto-config disagrees with production reality.

Boot is the executable face of Spring for most modern teams. Next we aim that executable app at HTTP: MVC, REST controllers, validation, and status codes — Episode Seventy-Four.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Boot Basics (Episode 73).

Narration technique: boilerplate pain → Boot thesis → @SpringBootApplication walk → starters/yaml/actuator → override intentionally → misconceptions → interview woven → bridge to MVC/REST.

Teaching points preserved: @SpringBootApplication; starters; application.yaml; Actuator; override auto-config intentionally.
