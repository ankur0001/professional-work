# Episode 11 — Component Scanning

| Field | Value |
|---|---|
| Episode | 11 |
| Title | Component Scanning |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 11 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

The cargo routing service passes every unit test on a laptop and fails contract tests in the pipeline with a bizarre bean: `FakeGpsClock` from `com.cargo.testsupport`. Production logs show the clock advancing in 15-minute jumps designed for demos. Someone set `@ComponentScan("com.cargo")` on the Boot application in `cargo-app`, and the `cargo-test-support` JAR — depended on as `test` scope in the library module but somehow compile-scoped in the app — sat on the runtime classpath with `@Component` classes under `com.cargo.testsupport`. Scanning did exactly what it was told. The package boundary did not.

Component scanning walks packages looking for stereotype annotations — `@Component`, `@Service`, `@Repository`, `@Controller`, and meta-annotated types — and registers bean definitions for each hit. It is convenience, not magic. Convenience without package discipline becomes a production classpath mine: anything annotated and reachable under the scan base becomes a candidate singleton.

```java
@SpringBootApplication
@ComponentScan(
    basePackages = "com.cargo.routing",
    excludeFilters = @ComponentScan.Filter(
        type = FilterType.REGEX,
        pattern = "com\\.cargo\\.testsupport\\..*"
    )
)
public class CargoRoutingApp {
    public static void main(String[] args) {
        SpringApplication.run(CargoRoutingApp.class, args);
    }
}
```

Walk that fix. `@SpringBootApplication` already includes a `@ComponentScan` defaulted to the main class package. The explicit `@ComponentScan` replaces that default with `basePackages = "com.cargo.routing"` — only that tree and its subpackages are candidates. `excludeFilters` with a REGEX pattern is belt-and-suspenders if a testsupport class somehow still shares the prefix; filter types also include ANNOTATION, ASSIGNABLE_TYPE, and ASPECTJ. Better still in many apps: put the application class in `com.cargo.routing` and rely on the default scan of that package and below — never `com.cargo` if sibling modules share the prefix. Keep test helpers in `src/test` or in a JAR that production never depends on; scope mistakes are half of this outage class.

Runtime of a scan during context refresh. `ClassPathBeanDefinitionScanner` (or Boot's equivalent path) obtains candidate resource paths under the base packages. For each `.class` resource it reads *metadata* via a metadata reader — often without fully initializing the class — and checks for stereotype annotations and include/exclude filters. Hits become `BeanDefinition` entries. Default bean name is the short class name decapitalized (`fakeGpsClock`), unless `@Component("explicit")` overrides. Instantiation happens later when the bean is needed or when non-lazy singletons are pre-instantiated at end of refresh. That timing is why `FakeGpsClock` can become a real singleton before any HTTP request: the scan already decided it was a bean, and something depended on `Clock` or `GpsClock` by type — or the fake was simply created as an eager singleton and started ticking in a `@PostConstruct`.

Failure mode symptoms in the cargo outage: contract tests assert arrival ETAs against wall-clock windows and fail intermittently; production metrics show routes recalculated on a 15-minute grid; `beans` actuator (if exposed) lists `fakeGpsClock`; debug logging of `ClassPathBeanDefinitionScanner` shows `com.cargo.testsupport.FakeGpsClock` as a candidate. Another related symptom: duplicate type matches — both `SystemGpsClock` and `FakeGpsClock` implement `GpsClock`, startup fails with `NoUniqueBeanDefinitionException`, or `@Primary` on the wrong one silently wins.

Trade-offs. Wide scans (`com.company`) onboard new `@Service` classes with zero registration code and maximize accidental inclusion of demos, fakes, and abandoned packages. Narrow scans and explicit `@Bean` methods cost a line of registration but make the graph auditable. Filters help, but filters that exist because the classpath is dirty are treating the symptom; fixing Maven/Gradle scopes and package layout treats the cause. Scanning also interacts with multi-module builds: a dependency's `@Component` classes are visible if that dependency is on the runtime classpath — "it's only a library" is not isolation.

Misconception unique to scanning: "`@SpringBootApplication` only scans the package of the main class, so deep package trees are always safe." It scans that package *and all subpackages*. If you place main in `com.cargo` to "see everything," you opted into everything under `com.cargo`, including modules you forgot existed.

`FakeGpsClock` is gone from prod. The next fight is subtler: the same app declares two `DataSource` beans — OLTP and reporting — and developers disagree whether `@Autowired`, `@Resource`, or `@Inject` will pick the right one when a field is named `reportingDataSource`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 11 (*Component Scanning*).
