# Episode 20 — Starter Dependencies

| Field | Value |
|---|---|
| Episode | 20 |
| Title | Starter Dependencies |
| Phase | Phase 2 — Spring Boot |
| Catalog handbook lesson | 20 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

New hire opens a PR titled "add web endpoint for station status." The `pom.xml` diff lists `spring-web`, `spring-webmvc`, `hibernate-validator`, `jackson-databind`, `tomcat-embed-core`, each with a hand-picked version. Two of those versions disagree with the Boot BOM already imported. CI fails on `NoSuchMethodError` deep in Jackson or Spring MVC — not in the new controller. Reviewer comment: "Delete all of that. Use `spring-boot-starter-web`." The bike-share API does not need a custom dependency graph for "hello HTTP."

Starters are dependency descriptors, not runtime containers. `spring-boot-starter-web` pulls a tested set of jars compatible with your Boot version — Spring MVC, embedded Tomcat, Jackson, validation API — so auto-configuration conditions become true *together*. The Boot dependency-management BOM (via `spring-boot-dependencies` or the parent POM) aligns versions. You choose features; Boot chooses compatible coordinates. That separation is the whole product pitch of starters.

```xml
<!-- before: dependency hell -->
<dependency>
  <groupId>org.springframework</groupId>
  <artifactId>spring-webmvc</artifactId>
  <version>6.1.2</version>
</dependency>
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
  <version>2.15.0</version>
</dependency>
<!-- ...and twelve more... -->

<!-- after -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

Walk the before/after. Hand versions look precise and are usually wrong relative to the Boot release train: Boot 3.x expects a specific Spring Framework line and a Jackson line tested against it. Mixing "latest Jackson" with "Boot's Spring" produces method mismatches at runtime — compile may still pass if your code does not call the missing method. The starter dependency omits `<version>` when the parent BOM manages it; Maven/Gradle resolves a coherent graph. Transitive jars appear in `mvn dependency:tree` under the starter — that tree *is* the classpath signal auto-config reads.

Runtime effect is indirect but real. With `spring-boot-starter-web` on the classpath, Boot's servlet web auto-configuration sees Tomcat and `DispatcherServlet` classes, starts an embedded server, registers MVC infrastructure beans, and configures HTTP message converters including Jackson if present. Without Jackson on the classpath, JSON `@RestController` methods fail at runtime when writing responses. Without version alignment, you might get a server that starts and explodes on the first JSON payload — symptom: `NoSuchMethodError` or `ClassNotFoundException` in converter setup, HTTP 500 on `/api/stations/{id}` while `/actuator/health` still looks fine. Starters keep classpath signaling intentional: add `starter-data-jpa` and you invite DataSource and JPA auto-config; remove `starter-web` and the embedded server should disappear.

Common starters sketch a vocabulary: `spring-boot-starter-web`, `data-jpa`, `security`, `actuator`, `test`. Each is a menu item for a feature slice. `spring-boot-starter-test` brings JUnit, Mockito, AssertJ, and Spring Test — use it in test scope so production images stay lean. When you need only JDBC without JPA, prefer `starter-jdbc` over dragging Hibernate via `starter-data-jpa`.

Failure mode: new hire "fixes" a missing class by adding a second, differently versioned copy of a jar already on the tree. Symptom: duplicate classes on the classpath, non-deterministic which wins, subtle bugs in one environment. Maven's dependency mediation picked one version; an explicit wrong version forced another. Another failure: adding `starter-webflux` beside `starter-web` "to try reactive" — dual stacks, confused web-application-type deduction, larger image, surprising thread models.

Trade-offs. Starters trade fine-grained control for curated coherence — perfect for services; occasionally heavy if you only wanted one transitive and got fifteen. Excluding a transitive (`<exclusions>`) is valid when you replace embedded Tomcat with Jetty via `spring-boot-starter-jetty`, but each exclusion is a promise you understand the auto-config conditions you just changed. Pinning versions manually fights the BOM and reintroduces the PR that started this lesson.

After the new hire switches to `spring-boot-starter-web`, run `mvn dependency:tree | head` in review and look for a single Jackson and a single Spring MVC line managed by the Boot BOM. That tree is the artifact you are actually shipping. If a transitive from a random SDK pulls an older `jackson-databind`, resolve it with Boot's dependency management or an explicit BOM-aligned override — not by deleting the starter. Starters and the BOM are one system: the starter selects features; the BOM selects versions.

Misconception unique to starters: "A starter contains the auto-configuration Java code for that feature." Auto-configuration mostly lives in `spring-boot-autoconfigure`. Starters primarily bring dependencies (and sometimes transitive config). Removing a starter removes jars; excluding an auto-config class is a different lever.

The POM is clean. Controllers still fail to map because the main application class sits in `com.bikeshare` while controllers live in `com.bikeshare.api.web`, and someone set a custom scan base that missed them. `@SpringBootApplication` is three annotations fused — and the scan-base mistake hides in that fusion.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 20 (*Starter Dependencies*).
