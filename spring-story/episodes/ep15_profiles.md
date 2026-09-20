# Episode 15 — Profiles

| Field | Value |
|---|---|
| Episode | 15 |
| Title | Profiles |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 15 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Friday deploy of the tolling-adjacent reporting service. Same JAR that developers ran against H2 on laptops. Staging expected Postgres. Someone forgot the active profile. The app started, Auto-DDL touched the wrong assumptions, and the first health check looked "up" while queries failed with dialect errors. Three environments — local H2, staging Postgres, prod Postgres with read replicas — one artifact. Profiles exist so bean definitions and properties can differ without forking the codebase into `reporting-local` and `reporting-prod` repositories.

A profile is a named gate on definitions and property sources. Activate with `spring.profiles.active`, the `SPRING_PROFILES_ACTIVE` environment variable, or programmatic API on the context. Beans annotated `@Profile("…")` or XML `profile=` attributes register only when that profile is on. `@Profile("!prod")` excludes production. Multiple profiles can be active at once; the set is a bag, not a single enum, unless ops enforces one-at-a-time in the Deployment.

```java
@Configuration
public class PersistenceProfiles {

    @Bean
    @Profile("local")
    DataSource localDataSource() {
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .addScript("schema-local.sql")
            .build();
    }

    @Bean
    @Profile({"staging", "prod"})
    DataSource postgresDataSource(Environment env) {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(env.getRequiredProperty("app.datasource.url"));
        ds.setUsername(env.getRequiredProperty("app.datasource.username"));
        ds.setPassword(env.getRequiredProperty("app.datasource.password"));
        return ds;
    }

    @Bean
    @Profile("prod")
    DataSource routingDataSource(
            @Qualifier("postgresDataSource") DataSource primary,
            @Value("${app.datasource.replica-url}") String replicaUrl,
            Environment env) {
        HikariDataSource replica = new HikariDataSource();
        replica.setJdbcUrl(replicaUrl);
        replica.setUsername(env.getRequiredProperty("app.datasource.username"));
        replica.setPassword(env.getRequiredProperty("app.datasource.password"));
        return new ReadWriteRoutingDataSource(primary, replica);
    }
}
```

Walk the gates. `@Profile("local")` on `localDataSource` means that bean definition is registered only when `local` is active — H2 plus `schema-local.sql`. `@Profile({"staging", "prod"})` on `postgresDataSource` registers the same factory method for either staging or prod; JDBC URL still comes from Environment so the two envs differ by property, not by a third method. `@Profile("prod")` on `routingDataSource` adds a read/write splitter only in production: it injects the postgres bean by qualifier and builds a replica pool from `app.datasource.replica-url`. In staging you get a single Postgres DataSource; in prod you get routing on top.

Runtime with `spring.profiles.active=prod`. Spring prepares the Environment, marks `prod` active, and while parsing configuration classes only accepts `@Bean` methods whose profiles match. `localDataSource` never enters the registry. `postgresDataSource` and `routingDataSource` do. If something `@Autowired DataSource` without a qualifier in prod, you still need clarity — often mark the routing bean `@Primary` so repositories get the splitter. Wrong or missing profile changes which definitions exist: unsatisfied dependencies can fail fast, or — worse — a leftover `local` in `spring.profiles.active=local,prod` can register H2 *and* Postgres and then lose on primary selection.

Step through a staging boot with `spring.profiles.active=staging` once more, slower. Environment marks only `staging`. `PersistenceProfiles` is parsed; `localDataSource`'s `@Profile("local")` does not match, so that definition is skipped entirely — not created-and-disabled, skipped. `postgresDataSource` matches the staging/prod set and registers. `routingDataSource` requires `prod`, so staging never builds the replica pool. Repositories that `@Autowired DataSource` receive the single Postgres bean. First query uses the staging JDBC URL from Environment. If ops meant prod and typed `production` instead of `prod`, none of the postgres profile annotations match either — and if nothing else defines a DataSource, refresh fails with `NoSuchBeanDefinitionException` for `DataSource`, which is painful but clearer than talking to the wrong cluster.

Failure mode from that Friday: `SPRING_PROFILES_ACTIVE` unset in the staging Deployment. Only default property sources load; if a default `DataSource` auto-config or an unprofiled bean still builds something, startup may succeed. Symptom: SQLGrammarException or wrong dialect messages on first query; H2 file in `/tmp` on a staging pod; `Environment.getActiveProfiles()` empty in an actuator env dump. Another failure: `application-prod.yml` present in the JAR but profile never activated — people assume the filename alone selects prod. It does not; activation is mandatory.

Trade-offs. Profiles keep one artifact and branch bean graphs cleanly; they also hide behavior behind an env var that must be set correctly in every cluster. Too many fine-grained profiles (`local`, `local-h2`, `local-postgres`, `qa1`…) explode combinatorial testing. Prefer coarse profiles for infrastructure (local/staging/prod) and property overlays for small differences (URLs, pool sizes). Profile-specific *beans* for incompatible implementations (H2 vs Postgres); profile-specific *properties* for the same bean shape with different values.

Misconception unique to profiles: "Setting `spring.profiles.active=prod` replaces `application.properties` entirely with `application-prod.properties`." No. Profile-specific documents add and override; the default `application.properties` (or `.yml`) still loads. Forgetting that is how a shared default URL leaks into prod beside your overrides.

Profiles select which beans exist. The tolling ops team still needs a single API to ask "what is the feature flag value and which DB URL won after env vars, files, and CLI flags fought?" That unified view is the Environment abstraction.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 15 (*Profiles*).
