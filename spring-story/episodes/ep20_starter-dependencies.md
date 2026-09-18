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

Auto-configuration reacts to the classpath. Starters are how teams build that classpath without playing dependency roulette.

Before starters, a "simple" Spring web app meant listing spring-web, spring-webmvc, Jackson, validation, an embedded Tomcat, logging bridges, and hoping every version agreed. One library upgraded early, another lagged, and you spent the morning on `NoSuchMethodError`. The business endpoint was never the hard part — the bill of materials was.

So the engineer question is: can we declare a capability — web, JPA, security — and inherit a tested set of libraries with aligned versions?

Spring Boot starters are that declaration. A starter is a Maven or Gradle dependency that pulls a curated set of transitive libraries. It usually contains little or no code of its own. The value is the graph. `spring-boot-starter-web` brings MVC, an embedded Tomcat by default, Jackson, and validation support. `spring-boot-starter-data-jpa` brings Spring Data JPA, Hibernate, and related pieces. `spring-boot-starter-actuator` brings operational endpoints. Versions are managed by Boot's BOM — the dependency management that pins compatible releases so you typically omit version numbers on starters.

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

With a Boot parent POM or the Boot dependency BOM imported, those two lines replace a fragile hand-picked list. Build the project and inspect the resolved tree: Tomcat, Jackson, Hibernate, and friends appear as transitives. Change Boot's version, and the curated set moves together. That is why onboarding a new service got faster — the "web stack" decision became one coordinate, not twelve.

Runtime connects straight back to auto-configuration. Put `spring-boot-starter-web` on the classpath and web-related auto-config classes see their `@ConditionalOnClass` checks succeed. Leave it off, and those classes stay inactive. Starters do not configure beans by themselves; they supply the jars that make conditions true. Think of starters as the shopping cart and auto-configuration as the kitchen that cooks what you bought.

You can still customize. Exclude Tomcat and add Jetty if you want a different embedded server. Add a database driver beside the JPA starter so datasource auto-config has a driver class. Override a transitive version only when you must — and treat that as a conscious risk, because you stepped outside the BOM's tested combination.

The misunderstanding that wastes time is "starters are frameworks." They are dependency aggregates. Another is adding both `spring-boot-starter-web` and `spring-boot-starter-webflux` "just in case" and then wondering why the app's reactive-versus-servlet story is confused. Choose the stack you mean. A third is pinning random library versions on top of the BOM until the classpath is unique to your laptop.

Once the classpath is coherent and auto-config can fire, you still need one application entry point that turns scanning, configuration, and auto-config import into a single annotation people actually type.

That entry point is `@SpringBootApplication`.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 20 (*Starter Dependencies*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
