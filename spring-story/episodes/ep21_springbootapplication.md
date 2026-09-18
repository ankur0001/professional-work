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

Every Boot tutorial starts with one annotation on the main class. Treat it as a composition, not a lucky charm — because when scanning misses a package, that annotation is usually where the story went wrong.

Imagine a service where controllers live under `com.acme.orders.web` and the main class sits in `com.acme.orders`. Everything starts. Move the main class to `com.acme.bootstrap` "to keep startup separate," leave components under `com.acme.orders`, and suddenly mappings vanish. No compile error. Just empty request mappings and a quiet 404. The team blames MVC. The real issue was the default scan root.

The practical question: what does `@SpringBootApplication` actually enable, and where does component scanning begin?

`@SpringBootApplication` is a composed annotation. It layers three jobs. `@SpringBootConfiguration` marks the class as a source of bean definitions — Boot's specialization of `@Configuration`. `@EnableAutoConfiguration` triggers the import of auto-configuration classes we just studied. `@ComponentScan` turns on classpath scanning for `@Component`, `@Service`, `@Repository`, `@Controller`, and the rest — by default from the package of the annotated class downward.

```java
package com.acme.orders;

@SpringBootApplication
public class OrdersApplication {
    public static void main(String[] args) {
        SpringApplication.run(OrdersApplication.class, args);
    }
}
```

Place that class in `com.acme.orders` and scanning covers `com.acme.orders..*`. Controllers, services, and `@Configuration` classes in that tree are candidates. Auto-configuration still imports from Boot's list. Your main method hands the annotated class to `SpringApplication.run`, which uses it as both configuration source and scan anchor.

When the default is wrong, be explicit. Narrow or widen scan bases. Exclude an auto-config class that fights your environment. Keep the composition honest instead of sprinkling duplicate enable annotations.

```java
@SpringBootApplication(
    scanBasePackages = "com.acme.orders",
    exclude = { DataSourceAutoConfiguration.class }
)
public class OrdersApplication { }
```

That form says: scan the orders tree even if this class lives elsewhere, and do not auto-configure a datasource — perhaps tests supply one, or this process is not a DB owner. You can achieve similar effects with `@ComponentScan` and `@EnableAutoConfiguration` written out separately. Prefer the composed form for clarity unless you need a non-default mix.

Runtime behavior is easy to verify. Start the app with debug logging for `org.springframework.context` and watch which packages are scanned. Hit a mapped endpoint. If the handler is missing, check package placement before rewriting controller annotations. Also remember: `@SpringBootApplication` does not replace your domain `@Configuration` classes. It is the root that discovers them and imports Boot's defaults beside them.

A frequent mistake is treating the annotation as "Boot mode on" with no package consequences. Another is stacking `@SpringBootApplication`, `@EnableAutoConfiguration`, and `@ComponentScan` redundantly until nobody knows which attribute wins. A third is putting the main class in a root package so scanning walks the entire classpath including third-party noise — slow startup and surprising bean definitions.

Knowing the entry annotation is half the configuration story. The other half is typed, validated settings for *your* product — not only `spring.*` keys Boot already understands.

That leads to configuration properties: binding your own prefix into a dedicated object.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 21 (*@SpringBootApplication*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
