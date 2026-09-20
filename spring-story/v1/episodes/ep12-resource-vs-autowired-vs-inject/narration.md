# Episode 12 — @Resource vs @Autowired vs @Inject

| Field | Value |
|---|---|
| Episode | 12 |
| Title | @Resource vs @Autowired vs @Inject |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 12 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

PR review, cargo finance module. Author injects with `@Autowired DataSource dataSource` and marks the OLTP pool `@Primary`. Reviewer insists on `@Resource(name = "reportingDataSource")` for the nightly export job. A third engineer pastes `@Inject` from a Jakarta tutorial and claims it is "more standard." The app has two beans of type `DataSource`: `oltpDataSource` and `reportingDataSource`. Which annotation wins is not taste — it is injection algorithm. Pick the wrong algorithm and the export job hammers the OLTP pool during a full-table manifest dump.

Short rules of engagement. `@Autowired` (Spring) and `@Inject` (Jakarta/JSR-330) are type-driven first. If multiple candidates exist, Spring narrows with `@Qualifier`, `@Primary`, or — in some configurations — parameter/field names. `@Resource` (Jakarta/JSR-250) is name-driven first: default name is the field or setter name, then it falls back to type. For two DataSources, name-based selection is often the honest intent for "I want the reporting pool," while `@Primary` expresses "when someone asks for a DataSource without narrowing, give them OLTP."

```java
@Configuration
public class CargoDataConfig {

    @Bean
    @Primary
    DataSource oltpDataSource() {
        return DataSourceBuilder.create().url("jdbc:postgresql://oltp/cargo").build();
    }

    @Bean
    DataSource reportingDataSource() {
        return DataSourceBuilder.create().url("jdbc:postgresql://report/cargo").build();
    }
}

@Service
public class ManifestExportJob {
    @Resource(name = "reportingDataSource")
    private DataSource reportingDataSource;

    public void run(LocalDate day) {
        try (Connection c = reportingDataSource.getConnection()) {
            // export manifests for day
        } catch (SQLException e) {
            throw new ExportFailedException(day, e);
        }
    }
}
```

Walk the config. `oltpDataSource` method name becomes the default bean name; `@Primary` marks it as the preferred candidate for ambiguous type matches. `reportingDataSource` is a second bean of the same type without primary. On `ManifestExportJob`, `@Resource(name = "reportingDataSource")` skips the primary game: look up that exact name in the factory, inject that instance into the field. The `run` method opens a connection from whatever was injected — if you got reporting, heavy reads stay off OLTP; if you got OLTP by mistake, you will see lock contention and slow checkouts while exports run.

Modern Spring style for the same intent uses constructor injection plus `@Qualifier` — type match, then name, without field injection:

```java
@Service
public class ManifestExportJob {
    private final DataSource reporting;

    public ManifestExportJob(@Qualifier("reportingDataSource") DataSource reporting) {
        this.reporting = reporting;
    }
}
```

Here `@Autowired` is often implicit on a single constructor. Spring finds all `DataSource` beans, filters to those matching qualifier `reportingDataSource`, and injects that one. The field name `reporting` no longer has to match the bean name — the qualifier carries intent. That is clearer in reviews than relying on field-name defaults.

Runtime resolution, step by step, for three common mistakes. Case A: `@Autowired DataSource dataSource` on the export job, no qualifier. Spring collects both beans by type, sees `@Primary` on OLTP, injects OLTP. Symptom: export traffic on the primary DB, `pg_stat_activity` shows long `SELECT` from the export user on oltp host, checkout latency climbs — no Spring error at startup. Case B: `@Resource` on a field named `reportingDataSource` without an explicit `name` attribute — still resolves by field name first, gets reporting even when OLTP is primary. Case C: `@Inject` with `@Named("reportingDataSource")` — behaves like type-plus-qualifier, similar to `@Autowired` + `@Qualifier`. Case D: `@Autowired` with field name `reportingDataSource` but no `@Qualifier` and multiple candidates — depending on Spring version and `spring.main`-era defaults, you may still get primary or an ambiguity failure; do not bet production on name fallback for `@Autowired`.

Failure mode to drill in demos: ship Case A to staging. Startup is green. First nightly export coincides with peak booking. On-call sees OLTP CPU spike, not "wrong bean" in logs. Fix is `@Qualifier` or `@Resource(name=...)`, plus maybe removing accidental `@Primary` misuse if primary was only added to silence `NoUniqueBeanDefinitionException` without thinking about export jobs.

Trade-offs. `@Autowired`/`@Inject` + `@Qualifier` keep constructor injection and Spring idioms; you must remember to qualify when duplicates exist. `@Primary` reduces noise for the common DataSource but is dangerous when secondary uses are silent. `@Resource` makes name-first intent obvious for fields/setters but pushes teams toward field injection and JSR-250 semantics that newcomers confuse with `@Autowired`. Prefer one house style: constructors + `@Qualifier` for multiple beans of one type; reserve `@Primary` for a true default; use `@Resource` when aligning with Jakarta name-based injection in mixed stacks.

Misconception unique to these annotations: "`@Inject` and `@Autowired` are identical, and `@Resource` is just the Jakarta spelling of `@Autowired`." `@Inject` is close to `@Autowired` but lacks some Spring-specific features (for example `required` flag semantics differ). `@Resource` is not a synonym — name-first matching changes which bean you get when duplicates exist.

Finance exports finally hit the reporting replica. A cinema ticketing team wants the opposite extreme: no component scan at all, only explicit `@Configuration` classes wiring the full-screen box office. How those configuration classes themselves are processed — enhanced, intercepted, singleton-guaranteeing — is the next mechanism to open.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 12 (*@Resource vs @Autowired vs @Inject*).
