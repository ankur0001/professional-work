# Episode 07 — Bean Definition

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Bean Definition |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 7 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

An `ApplicationContext` on refresh does not invent beans from vibes. It reads descriptions — recipes — and materializes objects from them. Those recipes are bean definitions.

Suppose your team needs two `DataSource` beans: one for commands, one for read replicas. Both are the same Java type. If the container only knew "create a DataSource," it could not tell them apart, could not set different JDBC URLs, and could not mark one primary. Or imagine a legacy report generator that must start after the schema-migrator bean finishes. Without metadata for depends-on, startup order becomes race-shaped luck.

When definitions are missing or vague, you get ambiguous injection, wrong property values, or beans that never appear because nothing registered them. The engineer asks: what information does Spring store about a bean before the instance exists?

A `BeanDefinition` is that information. It is not the live object. It is metadata: bean class (or factory method), scope, whether it is lazy, constructor argument values, property values, init and destroy method names, primary flag, depends-on relationships, and role hints. XML `<bean>`, `@Component` stereotypes, and `@Bean` methods all end as bean definitions in a registry. Different authoring styles; one runtime model.

```java
AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();
DefaultListableBeanFactory registry = context.getDefaultListableBeanFactory();

GenericBeanDefinition writerDs = new GenericBeanDefinition();
writerDs.setBeanClass(HikariDataSource.class);
writerDs.setAttribute("role", "writer");
MutablePropertyValues writerProps = new MutablePropertyValues();
writerProps.add("jdbcUrl", "jdbc:postgresql://primary/app");
writerProps.add("username", "app");
writerDs.setPropertyValues(writerProps);
writerDs.setPrimary(true);
registry.registerBeanDefinition("writerDataSource", writerDs);

GenericBeanDefinition readerDs = new GenericBeanDefinition();
readerDs.setBeanClass(HikariDataSource.class);
MutablePropertyValues readerProps = new MutablePropertyValues();
readerProps.add("jdbcUrl", "jdbc:postgresql://replica/app");
readerProps.add("username", "app_ro");
readerDs.setPropertyValues(readerProps);
registry.registerBeanDefinition("readerDataSource", readerDs);

context.refresh();

DataSource primary = context.getBean(DataSource.class); // writer — marked primary
DataSource reader = context.getBean("readerDataSource", DataSource.class);
```

Before `refresh`, the registry holds two definitions and zero pooled connections. During refresh, Spring instantiates from each definition, applies property values, and caches singletons. Type-based lookup for `DataSource` resolves to the primary writer. The reader is still available by name. The definition carried identity and configuration that the class alone could not express.

You rarely register `GenericBeanDefinition` by hand in modern apps — component scanning and `@Bean` methods do it — but understanding definitions explains otherwise mysterious behavior. Why does a `@Bean` method name become the default bean name? Because the definition's id came from the method. Why does `@Lazy` change startup? Because the definition's lazy flag changed. Why do `BeanFactoryPostProcessor`s feel powerful? Because they rewrite definitions before any instance exists.

Do not confuse the definition with the singleton instance. Changing a field on a live bean does not change the recipe. Conversely, editing XML or Java config changes definitions on the next refresh, not the heap objects already created. Another trap: assuming every Java class in the project automatically has a definition. Only what you register — scan, `@Bean`, or XML — becomes a bean.

Definitions answer what to build and with which settings. They also carry a quiet field you will feel the moment shared mutable state appears: scope. How many instances should this definition produce — one for the whole container, one per request, or a fresh object every lookup? That question is bean scopes, and it is waiting as soon as your recipe is more than a class name.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 7 (*Bean Definition*).

Narration technique: situation → problem → question → Spring’s answer → integrated example/code walkthrough → misunderstanding → next natural question. Not a definition dump.
