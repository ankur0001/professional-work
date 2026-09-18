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

Lifecycle hooks only help if Spring knows which classes are beans and how they connect. Teams have argued for years about the best way to write that knowledge down.

Walk into a codebase from 2008 and you may find a thousand-line `applicationContext.xml` where every service is a `<bean>` element. Walk into a 2016 service and you find `@Component` on every class plus a few XML leftovers. Walk into a modern library integration and you find `@Configuration` classes with `@Bean` methods wrapping third-party types. Same container underneath. Three dialects for declaring intent. Mixing them without a policy produces dual sources of truth: a bean defined in XML and again in Java, or a scan that silently duplicates an XML id.

What goes wrong is not that XML is evil or annotations are magic. What goes wrong is unclear authorship — nobody knows where to look, reviews miss wiring, and refactors break the silent second definition. The engineer asks: how should we express bean definitions so the team can read and change them safely?

Spring supports three primary configuration styles. XML configuration declares beans in documents the container loads. Annotation-driven configuration puts stereotypes like `@Component`, `@Service`, and `@Repository` on classes and relies on discovery. Java-based configuration uses `@Configuration` classes with `@Bean` factory methods — type-safe, refactorable in the IDE, and excellent for objects you do not own. Modern Spring applications lean on Java config plus annotations; XML remains for legacy islands and some externalized wiring.

```java
// Java config style — explicit, refactor-friendly
@Configuration
public class NotificationConfig {

    @Bean
    NotificationClient notificationClient(Environment env) {
        return new SendGridClient(env.getRequiredProperty("sendgrid.api-key"));
    }

    @Bean
    OrderNotifier orderNotifier(NotificationClient client) {
        return new OrderNotifier(client);
    }
}

// Equivalent idea in annotation style elsewhere:
// @Service class OrderNotifier { ... }
// discovered by component scanning instead of an @Bean method
```

When this `NotificationConfig` is registered with an `AnnotationConfigApplicationContext`, Spring turns each `@Bean` method into a bean definition, invokes the methods at the right time, and injects `notificationClient` into `orderNotifier`. Rename the method in the IDE and the bean name updates with you. Compare that to hunting string ids in XML. For `SendGridClient` — a type you do not control — `@Bean` is the natural style because you cannot put `@Component` on a third-party class without wrapping it.

Style choice is contextual. Prefer stereotypes and scanning for your own application services. Prefer `@Bean` methods for infrastructure and external types. Keep XML only when migrating or when a legacy module still speaks it. You can combine styles in one context, but pick a default and document exceptions.

A misconception here is "annotations replaced the need to understand configuration." Annotations are one authoring style that still produces bean definitions. Another is copying every bean into both XML and Java "to be sure," which creates conflicts and duplicate definitions.

Annotation style only scales if Spring can find the annotated classes. That discovery mechanism — component scanning — is the next piece. Without it, `@Service` is just a comment the compiler ignores.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 10 (*Configuration Styles*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
