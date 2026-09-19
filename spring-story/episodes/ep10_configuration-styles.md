# Episode 10 — Configuration Styles

| Field | Value |
|---|---|
| Episode | 10 |
| Title | Configuration Styles |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 10 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Before: `bank-batch-context.xml` at 2,400 lines, last touched in 2012, wiring a nightly clearing job with property placeholders nobody dares rename. After the first migration slice: a `@Configuration` class for the new ledger writer, still importing the old XML for the parts that work. The bank does not get a greenfield rewrite. It gets coexistence — and Spring has always been built for that mid-history reality.

Spring accepts multiple configuration styles because teams arrive mid-flight. XML bean definitions, Java `@Configuration` / `@Bean` methods, component scanning of stereotype annotations, and Groovy DSL in some stacks. They all produce bean definitions that land in the same `BeanDefinitionRegistry`. Style is presentation; the registry is the truth. Migrating means changing how definitions are *authored*, not inventing a second container.

```xml
<!-- still in production for the 2012 clearing reader -->
<bean id="clearingFileReader" class="com.bank.batch.ClearingFileReader">
    <property name="directory" value="${clearing.inbox}"/>
    <property name="charset" value="UTF-8"/>
</bean>
```

```java
@Configuration
@ImportResource("classpath:bank-batch-context.xml")
public class LedgerMigrationConfig {

    @Bean
    LedgerWriter ledgerWriter(DataSource dataSource) {
        return new JdbcLedgerWriter(dataSource);
    }

    @Bean
    ClearingJob clearingJob(ClearingFileReader reader, LedgerWriter writer) {
        return new ClearingJob(reader, writer);
    }
}
```

Walk the migration code. `@Configuration` marks `LedgerMigrationConfig` as a definition source. `@ImportResource("classpath:bank-batch-context.xml")` tells the context: while processing this Java config, also run an XML reader against that file and merge those definitions into the *same* registry. `ledgerWriter(DataSource dataSource)` is a factory method — Spring calls it when the `ledgerWriter` bean is needed, injecting whatever `DataSource` bean already exists (often still declared in XML or a shared infra config). `clearingJob(...)` asks for `ClearingFileReader` and `LedgerWriter` by type; the reader still comes from the XML `id="clearingFileReader"`, the writer from the `@Bean` method. Constructor args do not care which style authored the collaborator. `${clearing.inbox}` in XML still resolves through the Environment when the reader bean is created — placeholders are not "XML-only magic"; they are property resolution against the same Environment the Java side uses.

Runtime during a nightly run after the first slice. Context refresh registers definitions from XML and from `@Bean` methods. If both styles accidentally define the same bean id, you get an override or a conflict depending on settings — a real migration hazard. Instantiation of `ClearingJob` triggers creation of `clearingFileReader` (XML path: property injection of directory and charset) and `ledgerWriter` (Java path: `new JdbcLedgerWriter`). The job runs; file lines become ledger rows. You can move one bean at a time: delete the XML `<bean>` for a collaborator, add a `@Bean`, redeploy, watch the clearing job. Component scanning can join later for *new* services under a controlled base package — another producer of definitions, not a mandate to delete XML overnight.

Failure mode with symptoms ops actually see: two definitions for `clearingFileReader` — one left in XML, one added as `@Bean` with the same name — and `spring.main.allow-bean-definition-overriding` false. Startup fails with `BeanDefinitionOverrideException` naming the id. Or overriding is allowed, the wrong implementation wins, and clearing silently writes with a stub reader that always returns empty files: job "succeeds," ledger stays flat, business thinks the inbox was empty. Another symptom of mixed-style confusion: XML still references `ref="oldLedgerWriter"` after you renamed the Java `@Bean` method to `ledgerWriter` — `NoSuchBeanDefinitionException` at job creation, stack rooted in `AbstractBeanFactory.resolveDependency`.

Trade-offs. XML keeps working systems alive and is explicit about every wire; it loses IDE rename safety and grows hostile past a few hundred beans. Java config wins on navigation, refactoring, and type checking, but method-call semantics inside `@Configuration` classes need care (full vs lite mode — later). Component scanning minimizes ceremony and maximizes "who registered this?" surprises when packages are wide. Coexistence via `@ImportResource` is the pragmatic path for banks; purity is a rewrite fantasy.

Misconception unique to configuration styles: "XML configuration does not support constructor injection or strong typing, so it is unsafe by nature." XML can express constructor args and factory methods; the real costs are tooling, refactor safety, and readability. Java config wins on IDE navigation and compile-time checks — not because XML is incapable of wiring.

Halfway migrated, a cargo multi-module build introduces a new style hazard: component scan base packages so wide that test utilities become production beans. The question shifts from XML versus Java to what scanning actually picks up.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 10 (*Configuration Styles*).
