# Episode 19 — Auto Configuration

| Field | Value |
|---|---|
| Episode | 19 |
| Title | Auto Configuration |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 19 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Boot's architecture told you that auto-configuration is imported during startup. Now open that box. Why does adding a JDBC driver suddenly produce a `DataSource` bean you never declared?

Without auto-configuration, every service repeats the same platform wiring. You write a `@Configuration` class for Jackson. Another for the datasource. Another for MVC message converters. Copy those classes across ten microservices and you have ten slightly different "standard" setups — and a week of merge pain when the standard changes.

The question that follows is precise: can the framework notice what is on the classpath and wire the obvious beans — unless the application already defined its own?

Auto-configuration is Boot's answer. It is not magic beans appearing from nowhere. It is ordinary `@Configuration` classes packaged inside Boot, registered through `AutoConfiguration.imports` (or the older `spring.factories` entry), and guarded by conditions. `@ConditionalOnClass` checks that a type exists on the classpath. `@ConditionalOnMissingBean` backs off when you already defined that bean. `@ConditionalOnProperty` keys off configuration. Matching conditions activate the config class; failing conditions skip it.

Picture a simplified slice of what Boot does for JDBC:

```java
@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(DataSource.class)
@EnableConfigurationProperties(DataSourceProperties.class)
public class DataSourceAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    DataSource dataSource(DataSourceProperties properties) {
        return properties.initializeDataSourceBuilder().build();
    }
}
```

Read it as a contract. If `DataSource` is on the classpath, consider this configuration. If the user has not already declared a `DataSource` bean, create one from properties. Define your own `DataSource` `@Bean`, and Boot steps aside. That back-off is the design — opinionated defaults that yield to explicit application beans.

Runtime behavior matches the contract. Start an app with `spring-boot-starter-web` and no database driver: you do not get a pool. Add H2 or Postgres drivers plus `spring.datasource.url`, and datasource auto-config can activate. Turn on debug for auto-config — `debug=true` or `--debug` — and Boot prints a condition evaluation report: positive matches, negative matches, and exclusions. That report is how you debug "why is this bean missing?" without guessing.

```yaml
# application.yml — feeds DataSourceProperties used by auto-config
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/orders
    username: orders
    password: secret
```

Those properties do not create a datasource by themselves. Auto-configuration reads them when its conditions pass. Change the classpath or define a competing bean, and the outcome changes even if the YAML stays the same.

People often treat auto-config as an all-or-nothing spell. It is a set of conditional configuration classes. You can exclude one with `spring.autoconfigure.exclude` or `@SpringBootApplication(exclude = ...)`. You can replace a bean and rely on `@ConditionalOnMissingBean`. You cannot "turn off Spring" by being confused — you override deliberately at the condition boundary.

Another wrong mental model is "auto-config replaces my `@Configuration` classes." Your configuration still wins for product-specific beans. Auto-config covers the repetitive platform layer — ObjectMapper defaults, dispatcher setup, datasource scaffolding — so you spend attention on domain wiring.

Once you see that classpath clues drive which auto-config runs, a packaging question appears. Who decides which libraries land on that classpath in a coherent set of versions — so the conditions have something sensible to detect?

That is the job of starter dependencies.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 19 (*Auto Configuration*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
