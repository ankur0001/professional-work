# Episode 73 — Spring Boot Basics

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-Two covered IoC, injection styles, and bean scopes. Spring Boot is how most teams actually start a Spring application today. Boot is still Spring — it adds conventions, starters, and auto-configuration.

The goal — a production-ready app with less XML and less boilerplate. Misunderstanding Boot leads to fighting auto-config instead of using it. Today — starters, auto-configuration, properties, actuators, and the fat jar.

Episode Seventy-Three. Spring Boot Basics. Starters are curated dependency descriptors. spring-boot-starter-web pulls MVC, Tomcat, Jackson, and validation basics. starter-data-jpa brings Hibernate and repository support.

starter-test lands JUnit, Mockito, AssertJ, and Spring Test. You choose capabilities — Boot chooses compatible versions via the BOM. Prefer official starters over hand-picking twenty transitive jars.

Auto-configuration creates beans when conditions match. Classpath present — DataSource auto-config may engage. A user-defined bean of the same type usually wins — you can override. ConditionalOnClass and ConditionalOnMissingBean drive the decisions.

debug equals true or ConditionEvaluationReport shows what matched. Auto-config is opinionated defaults — not untouchable magic. Externalized configuration keeps code environment-agnostic.

application.properties or application.yaml hold defaults. Profile-specific files — application-prod.yaml — override per environment. Environment variables and command-line args outrank file values.

ConfigurationProperties maps typed settings into beans safely. Never hardcode secrets — inject them from the environment or a vault. The Boot run model in practice. SpringBootApplication enables scanning and auto-configuration.

SpringApplication.run boots the context and embedded server. Executable jar packaging ships dependencies — java -jar app.jar. Actuator exposes health, info, and metrics endpoints for operations.

Devtools and docker compose support speed local inner loops. Customization without abandoning Boot. Define your own Bean when defaults are wrong — Boot backs off. Exclude specific auto-config classes only with a clear reason.

Use application properties before writing custom configuration code. Keep SpringBootApplication on a root package so scanning sees your code. Read starter docs — each starter documents keys you can tune.

Three common mistakes. One — excluding auto-config to fix a symptom — hide the real conflict. Two — giant application.yaml with unused keys nobody understands. Three — putting SpringBootApplication in a nested package — components missed.

Also — mixing Boot versions manually — always use the BOM managed set. Work with Boot's conventions — override deliberately, not accidentally. Interview question — what does Spring Boot add on top of Spring?

Starters for curated dependencies and a managed BOM. Auto-configuration that wires common stacks from the classpath. Externalized config and production-ready Actuator endpoints. Embedded servers and executable jars for simple deployment.

Same Spring container underneath — Boot accelerates the path to production. Boot starts the app — next we handle HTTP. Episode Seventy-Four — Spring MVC and REST. Controllers, request mapping, validation, and clean API design.

See you there.
