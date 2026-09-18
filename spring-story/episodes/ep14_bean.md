# Episode 14 — @Bean

| Field | Value |
|---|---|
| Episode | 14 |
| Title | @Bean |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 14 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

`@Configuration` gives you a place to assemble infrastructure. `@Bean` is the method-level tool that publishes each object into the container.

Take `ObjectMapper`. You do not own Jackson's class. You cannot slap `@Component` on it inside the library. Yet every service wants the same mapper with Java time modules registered and unknown properties ignored. Without `@Bean`, teams hide `new ObjectMapper()` in static holders or build a fresh mapper per call — either shared mutable configuration races or repeated setup cost. Or they subclass just to put a stereotype on a wrapper, which is ceremony without clarity.

The question is simple: how do I register an object Spring did not invent from one of my annotated classes?

`@Bean` on a method tells Spring: invoke this method to produce a bean, manage the result according to the method's scope and lifecycle settings, and expose it for injection by type or name. The default bean name is the method name. Method parameters are injected dependencies. You can set `initMethod`, `destroyMethod`, and `@Scope` on the method. This is the preferred way to bring third-party and infrastructure objects under container control.

```java
@Configuration
public class JacksonConfig {

    @Bean
    ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
        mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        return mapper;
    }

    @Bean(destroyMethod = "close")
    HikariDataSource inventoryDataSource(Environment env) {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl(env.getRequiredProperty("inventory.jdbc-url"));
        ds.setUsername(env.getRequiredProperty("inventory.jdbc-user"));
        ds.setPassword(env.getRequiredProperty("inventory.jdbc-password"));
        return ds;
    }
}
```

At refresh, Spring calls `objectMapper()`, registers the returned instance as a singleton named `objectMapper`, and does the same for `inventoryDataSource`. Every injection point of type `ObjectMapper` receives the same configured mapper unless you define another and disambiguate. On context close, `destroyMethod = "close"` shuts the pool cleanly. For some pooled libraries Spring infers a destroy method you do not want — then you set `destroyMethod = ""` to disable inference. That lifecycle knob is part of why `@Bean` is more than a fancy `new`.

Use `@Bean` when you need to configure before publish, when the type is external, or when one interface has multiple implementations you want to construct explicitly. Prefer `@Component` on your own services when default construction and constructor injection suffice — less config noise.

A `@Bean`-specific misconception is that the annotation belongs on the class you want to expose. It belongs on the factory method that returns the instance. Another is creating a new `@Bean` method for every tiny collaborator that could have been a simple constructor dependency of a single published bean, which scatters assembly without benefit.

`@Bean` methods publish objects for one runtime. Real systems have many runtimes — local, test, staging, production — and not every bean should exist in all of them. Selecting which definitions are active is the job of profiles, and that problem shows up as soon as your local fake payment client must not ship to production.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 14 (*@Bean*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
