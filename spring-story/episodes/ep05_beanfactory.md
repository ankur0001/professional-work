# Episode 05 — BeanFactory

| Field | Value |
|---|---|
| Episode | 05 |
| Title | BeanFactory |
| Phase | Phase 1 — Spring Fundamentals |
| Catalog handbook lesson | 5 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

```java
public static void main(String[] args) {
    DefaultListableBeanFactory factory = new DefaultListableBeanFactory();
    XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(factory);
    reader.loadBeanDefinitions(new ClassPathResource("freight-rate-beans.xml"));

    RateCalculator calculator = factory.getBean("rateCalculator", RateCalculator.class);
    Money quote = calculator.quote(Lane.of(args[0], args[1]), Weight.kg(args[2]));
    System.out.println(quote);
}
```

That is the entire Spring footprint of a CLI freight-rate calculator ops runs from a laptop on the warehouse floor. No embedded Tomcat. No message source. No `@EventListener`. Just wiring: lane tariffs, fuel surcharges, a calculator. The team embedded Spring only because hand-rolled factories were becoming a second product — every new surcharge rule meant another `if` in a giant `FreightFactory` class, and every unit test had to mock construction order by hand.

`BeanFactory` is that minimal contract. It is the root interface for accessing the Spring container's bean instances. You register bean definitions — class name, id, property values, constructor args — and ask for objects by name or type. `DefaultListableBeanFactory` is the workhorse implementation: it holds the definition registry, resolves dependencies, applies scopes, and caches singletons. Almost everything richer in Spring eventually asks this factory for objects; ApplicationContext does not replace it — it wraps more services around the same core.

Walk the freight CLI line by line. `new DefaultListableBeanFactory()` builds an empty registry and singleton cache — no beans yet, no classpath scanning. `XmlBeanDefinitionReader` is a metadata loader, not the calculator. `loadBeanDefinitions(new ClassPathResource("freight-rate-beans.xml"))` opens the XML from the classpath, parses each `<bean>` element into a `BeanDefinition` object, and registers it under its `id`. At this moment the factory knows *what* could exist; it has not necessarily constructed anything expensive if beans stay lazy. `getBean("rateCalculator", RateCalculator.class)` is the first demand: look up the definition named `rateCalculator`, check the singleton cache, miss, then create. Creation walks constructor arguments: the factory sees refs to `tariffTable` and `fuelSurcharge`, creates those first (loading `tariffs.csv` into memory for the table), injects them into `RateCalculator`, stores the result in the singleton cache, and returns it. `calculator.quote(...)` is ordinary Java — Spring is already out of the path. A second `getBean("rateCalculator")` returns the cached instance. When `main` exits, the JVM dies; there is no graceful context-close ceremony unless you add destroy callbacks yourself.

```xml
<bean id="tariffTable" class="com.freight.TariffTable">
    <constructor-arg value="classpath:tariffs.csv"/>
</bean>
<bean id="fuelSurcharge" class="com.freight.FuelSurchargePolicy"/>
<bean id="rateCalculator" class="com.freight.RateCalculator">
    <constructor-arg ref="tariffTable"/>
    <constructor-arg ref="fuelSurcharge"/>
</bean>
```

Each line of that XML is a `BeanDefinition` field in disguise. `id` is the lookup key. `class` is the implementation to instantiate. The `classpath:tariffs.csv` constructor arg becomes a string (or Resource, depending on conversion) passed into `TariffTable`'s constructor — the factory does not open the CSV until that bean is created. `ref="tariffTable"` is a dependency edge, not a nested object literal; the factory resolves edges by creating or reusing collaborators. Order of `<bean>` elements in the file does not have to match creation order — the dependency graph does.

Failure mode that shows up on the warehouse floor: a typo in a `ref`, or a missing bean id. Symptom at `getBean("rateCalculator")` is `NoSuchBeanDefinitionException` or `UnsatisfiedDependencyException` naming the broken ref — often wrapped so the stack starts in `AbstractBeanFactory`. The CLI prints nothing useful to the quote path; it dies during wiring. Another symptom: `ClassPathResource` cannot find `freight-rate-beans.xml` → `BeanDefinitionStoreException` on `loadBeanDefinitions`, before any quote runs. Those failures are loud and early, which is what you want in a batch tool operators launch by hand.

Trade-offs. A bare `BeanFactory` keeps the process tiny and understandable — ideal for CLIs, custom scopes experiments, and library code that must embed Spring without pulling application services. You pay for that thinness: no built-in i18n message source, no application-event multicaster, no Environment post-processors, no convenient `close()` lifecycle for the whole app unless you wire DisposableBean callbacks yourself. You also own bootstrap — readers, resource locations, when to call `getBean`. ApplicationContext buys those services and a standard refresh lifecycle at the cost of heavier startup and more moving parts.

Misconception unique to BeanFactory: "BeanFactory is obsolete; only ApplicationContext matters." BeanFactory is not obsolete — it is the substrate. ApplicationContext extends it. Tools, custom scopes, and Boot internals still speak factory. Choosing ApplicationContext for an app does not erase the factory; it wraps richer services around the same getBean core.

The warehouse CLI is happy. The pharmacy kiosk team next door is not — they need localized labels on the touchscreen, environment-specific drug catalog URLs, and a way to publish "prescription ready" events to a display board. A bare BeanFactory will wire their services, but it will not give them those application services for free. Something richer has to sit on top of the factory.

## Source attribution

Reference: `Spring_Framework_Handbook.html` — Lesson 5 (*BeanFactory*).
