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

War story from the bike-share team, Tuesday. Diff adds one line to the Gradle build: the PostgreSQL JDBC driver. No Java changes. Restart. Startup dies: `Failed to configure a DataSource: 'url' attribute is not specified`. Nobody wrote a DataSource `@Bean`. Something else did — Boot auto-configuration — because a `DataSource` class became visible and no user bean of that type existed yet. The classpath spoke; Boot answered.

Auto-configuration is conditional bean registration shipped with Boot. Candidate classes are listed under `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` (older Boot: `spring.factories`). Annotations like `@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty` decide whether their `@Bean` methods fire. Your application code stays small; the classpath and Environment become signals. That is powerful and surprising in equal measure until you can read a condition evaluation report.

```java
// Simplified idea of what Boot ships (not your app code)
@AutoConfiguration
@ConditionalOnClass({ DataSource.class, HikariDataSource.class })
@EnableConfigurationProperties(DataSourceProperties.class)
public class DataSourceAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    DataSource dataSource(DataSourceProperties properties) {
        return properties.initializeDataSourceBuilder().build();
    }
}
```

```yaml
# auto-configured DataSource still needs properties
spring:
  datasource:
    url: jdbc:postgresql://bikeshare-db/stations
    username: share
    password: ${DB_PASSWORD}
```

Walk the simplified auto-config. `@ConditionalOnClass` means: only consider this configuration if `DataSource` and Hikari are loadable — adding the Postgres driver pulled those types onto the classpath (together with Boot's JDBC starter or transitive deps). `@EnableConfigurationProperties(DataSourceProperties.class)` binds `spring.datasource.*` into a typed properties object. `@Bean` + `@ConditionalOnMissingBean` means: create a DataSource *only if* the user did not already define one. `initializeDataSourceBuilder().build()` reads URL, username, password from those properties — empty URL is what triggered Tuesday's failure.

Runtime after the driver lands, step by step. During context refresh Boot loads auto-configuration import lists. Each candidate is evaluated against conditions. `DataSourceAutoConfiguration` matches on class presence. Inside, `@ConditionalOnMissingBean` searches the bean factory for an existing `DataSource` definition — none in the bike-share app — so the method is eligible. It builds from `DataSourceProperties`. Properties are empty for `url` → Boot fails fast with the familiar message. That fail-fast is kinder than a silent miswire to an in-memory default you did not want. Fixes: add `spring.datasource.url` (and credentials); or define your own `@Bean DataSource` so `@ConditionalOnMissingBean` skips; or exclude the auto-config class via `spring.autoconfigure.exclude` / `@SpringBootApplication(exclude=...)` if you truly have no database yet but need the driver for a batch tool on the same classpath. Debug with `--debug` or `ConditionEvaluationReport` logging to see matched and negative conditions.

Failure mode symptoms beyond missing URL: you define a custom DataSource bean, but still see Boot trying to configure JPA against a second implicit pool — often because another auto-config keyed off different types, or your bean was not visible yet when conditions ran (rare with proper user config ordering, more common with unusual `BeanDefinition` tricks). Symptom of successful override: condition report shows `DataSourceAutoConfiguration` beans skipped due to `@ConditionalOnMissingBean`. Symptom of accidental activation: adding `starter-data-jpa` "for later" pulls driver + Hibernate and suddenly entity scanning and DDL expectations appear.

Trade-offs. Auto-configuration collapses days of XML/Java infra into classpath conventions and keeps services consistent; it couples startup behavior to dependencies, so "just add a jar" is never free. Exclusions and custom beans restore control but require knowing which auto-config class owns the surprise. Prefer reading conditions over memorizing every `@Bean` Boot might create.

One more runtime detail the bike-share team used after Tuesday: start with `--debug` and search the log for `DataSourceAutoConfiguration`. Positive matches show which nested configurations fired; negative matches show why an exclude or `@ConditionalOnMissingBean` skipped a bean. That report is how you prove "our `@Bean DataSource` suppressed Boot" without guessing. Auto-configuration is not a black box once you treat conditions as the API.

Misconception unique to auto-configuration: "Auto-configuration runs before my `@Configuration` and always wins." Conditions like `@ConditionalOnMissingBean` are evaluated with user beans in mind; defining your own DataSource typically suppresses Boot's. The surprise is not that Boot overrides you — it is that Boot acts when you said nothing and the classpath said "database."

The team now understands why the driver created a bean. The new hire still stares at a `pom.xml` with twenty-seven versioned Spring jars fighting each other. Curated dependency sets — starters — are how Boot teams avoid that hell on purpose.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 19 (*Auto Configuration*).
