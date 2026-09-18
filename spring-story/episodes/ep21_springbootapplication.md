# Episode 21 — @SpringBootApplication

| Field | Value |
|---|---|
| Episode | 21 |
| Title | @SpringBootApplication |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 21 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Failing test output from the bike-share CI:

```
MockMvc returned 404 for GET /api/stations/42
Bean count for StationController: 0
```

The controller class has `@RestController`. The starter-web is on the classpath. The slice test even looks right. Root cause: `@SpringBootApplication(scanBasePackages = "com.bikeshare.service")` on the main class — written during a "only scan services" cleanup — excludes `com.bikeshare.api.web` where controllers live. Auto-configuration still runs. Component scan does not see the controllers. Fusion hid the knob that was turned.

`@SpringBootApplication` is a composed annotation. It combines `@SpringBootConfiguration` (a `@Configuration` specialization for the application), `@EnableAutoConfiguration`, and `@ComponentScan` with defaults. One annotation on the main class enables Java config of the app itself, Boot auto-config, and scanning of the main class package and subpackages. When you override one attribute, you are not "tweaking Boot" in the abstract — you are changing one of those three meta-annotations' behavior.

```java
package com.bikeshare;

@SpringBootApplication // default scan: com.bikeshare..*
public class BikeShareApi {
    public static void main(String[] args) {
        SpringApplication.run(BikeShareApi.class, args);
    }
}

// package com.bikeshare.api.web — found by default scan
@RestController
@RequestMapping("/api/stations")
public class StationController {
    private final StationDirectory directory;

    public StationController(StationDirectory directory) {
        this.directory = directory;
    }

    @GetMapping("/{id}")
    public StationView get(@PathVariable long id) {
        return StationView.from(directory.require(id));
    }
}
```

Walk the happy path. `BikeShareApi` lives in `com.bikeshare`. Default `@ComponentScan` uses that package as base, so `com.bikeshare.api.web.StationController` is a candidate, becomes a bean, and MVC maps `GET /api/stations/{id}`. `SpringApplication.run(BikeShareApi.class, args)` registers that class as a configuration source: `@SpringBootConfiguration` makes it a configuration class; `@EnableAutoConfiguration` imports auto-config; scan finds the controller and `StationDirectory` under `service` packages. Constructor injection on the controller is ordinary DI once the bean exists.

Runtime of the broken knob. `scanBasePackages = "com.bikeshare.service"` replaces the default base package list. Only types under `com.bikeshare.service` are scanned. Auto-configuration still creates `DispatcherServlet`, handler mappings infrastructure, embedded Tomcat. Zero `StationController` beans → no request handler for `/api/stations/42` → MockMvc 404. Actuator health may still be UP. That split — infrastructure up, application handlers missing — is the characteristic symptom of scan-base mistakes. Putting the main class in a deliberately chosen root package is a structural decision; narrowing scan without moving controllers is how empty handler maps look "healthy" while HTTP dies.

Failure mode variants: main class in `com.bikeshare.Bootstrap` under a deep package while controllers sit in `com.bikeshare.api` — default scan never climbs *up* to siblings. Symptom same 404. Or `@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)` misunderstood as "exclude scanning" — different attribute, different meta-annotation. Or a `@WebMvcTest(StationController.class)` that does not use the right `@Import` / `@ContextConfiguration` and fails for test-slice reasons unrelated to production scan — check whether production `beans` endpoint lists the controller before blaming MockMvc.

Trade-offs. Composition keeps main classes one line and onboarding short; it also hides three mechanisms behind one name, so debugging requires unpacking the composition. Explicit `@ComponentScan` / `@EnableAutoConfiguration` on a `@Configuration` class is more verbose and clearer for unusual layouts (multiple modules, selective auto-config). Prefer moving the main class to the right package over maintaining long `scanBasePackages` arrays that drift as modules grow.

Unpack the composition when debugging the next 404. Open `@SpringBootApplication`'s declaration: you will see `@SpringBootConfiguration`, `@EnableAutoConfiguration`, and `@ComponentScan` as meta-annotations. Attributes like `scanBasePackages`, `exclude`, and `excludeName` are `@AliasFor` mappings onto those meta-annotations — not mysterious Boot-only flags. When CI says bean count zero for a controller, ask which of the three composed behaviors you changed. Auto-config exclusion never removes a `@RestController` from the scan; scan narrowing never disables DataSource auto-config. Separating those mental models turns a fused annotation back into three levers you can reason about.

Misconception unique to `@SpringBootApplication`: "It only enables auto-configuration; scanning is separate and optional." Scanning is included. Disabling or narrowing it without moving controllers is how empty contexts look healthy while HTTP dies.

Controllers map again. Configuration is still a mess of `@Value("${freight.rate.base}")` scattered across constructors in a related rates module. Typed binding — `@ConfigurationProperties` — is the next cleanup that keeps Environment values honest as a group.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 21 (*@SpringBootApplication*).
