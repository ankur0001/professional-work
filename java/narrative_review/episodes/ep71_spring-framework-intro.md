# Episode 71 — Spring Framework Intro

| Field | Value |
|---|---|
| Episode | 71 |
| Title | Spring Framework Intro |
| Catalog handbook column | 71 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

You are joining a team that ships a Java backend. On day one someone says, "We use Spring." It sounds like a product name. Then you see annotations, XML legends from older services, starters, Boot, Data, Security, Batch. Spring is not one jar. Spring is an ecosystem centered on dependency injection and portable abstractions — a way to wire applications so your code depends on interfaces and policies, while the container constructs and injects collaborators.

```java
// Spring wires dependencies so your code depends on interfaces
// The container constructs and injects beans
```

The practical situation that makes Spring necessary is the same pain Episode Sixty-Eight named: construction sprawl. Without a container, every service builds its dependencies by hand, or reaches into static locators, or news up concrete classes deep inside methods. Tests suffer. Swapping a real mailer for a fake one means editing production construction paths. Enterprises adopt Spring because large codebases need consistent wiring, lifecycle, and extension points — not because annotations are fashionable.

Hold the IoC container mindset lightly but firmly. IoC means inversion of control over construction: instead of your class creating its dependencies, something outside provides them. In Spring, that something is the `ApplicationContext` — the working heart of the container. Objects the container manages are beans. You describe what beans exist and how they relate; the container instantiates, injects, and manages lifecycle according to configuration and conventions.

Convention plus extension points is why teams stay. Defaults get you moving. Interfaces and SPI hooks let you replace parts without forking the framework. That is not magic — it is wiring. Treating Spring as magic is the first misunderstanding. Avoiding understanding DI is the second: people copy `@Autowired` until a circular dependency appears and then declare frameworks evil. Bringing every module for a hello world is the third: Spring's ecosystem is large; start with what your situation needs.

What is Spring at heart? A DI-centered programming and configuration model with a large ecosystem around web, data, security, integration, and more. Say that, then connect it to why your team chose it: testability, consistent structure, and battle-tested integrations. The ecosystem matters because real applications are not only objects in memory — they talk HTTP, databases, brokers, and identity providers. Spring's portable abstractions aim to keep your code from being married to one vendor's low-level API on day one.

Walk a mental first day. You open a service class. It declares a constructor taking a repository interface. You do not see `new JdbcOrderRepository` inside the service. Somewhere else — configuration class, component scan, Boot auto-config — a bean implementing that interface is defined. At runtime the context creates the repository, creates the service, injects the repository, and hands you a ready graph. Your service's job stays business logic. Construction policy lives elsewhere.

Why enterprises adopt Spring becomes clearer if you picture ten teams sharing platform practices. Without a common wiring model, each team invents constructors, factories, and lifecycle differently. Onboarding costs explode. Spring's container and component model give a shared grammar: beans, injection, profiles, configuration. Ecosystem modules then cover cross-cutting needs without each team writing a one-off security filter chain from scratch — though they still must understand what they enable.

Portable abstractions matter at the edges. A `DataSource`, a messaging template, a cache manager — your code can target Spring's abstractions while drivers and brokers swap underneath with configuration. That portability is incomplete — dialects leak — but it beats scattering vendor API calls through domain services.

"Not magic — wiring" deserves a debugging ritual. When a bean is missing, read the startup failure: which definition was expected, which configuration condition failed, which classpath auto-config backed out. When two beans compete, understand `@Primary` and qualifiers. When a property is wrong, trace binding. Teams that treat Spring as magic restart until it works. Teams that treat it as wiring read the graph.

A healthy first service uses a small slice of the ecosystem: Boot for executable shape, web for HTTP, maybe JDBC or JPA, Security when needed. Expanding module count without expanding understanding is how microservices become micro-monoliths of configuration.

Ask in interviews what Spring is at heart, and answer DI-centered model plus ecosystem. Then give one sentence on why your last team used it: consistency, testability, integrations.

Beans and ApplicationContext become concrete when startup fails. Read the failure: missing bean, two candidates, or an unbound property. The container is showing you the graph it could not build. That graph mindset is the same honesty constructor injection demands inside a single class, scaled to the application.

Convention plus extension points means you can start with component scanning and annotations, then drop to explicit bean methods when wiring needs a human-readable policy. Neither style is morally superior. Clarity in your codebase is. Teams fight annotation-versus-Java-config wars while users wait; pick a house style and optimize for reading the graph.

Spring's size can intimidate. You do not need every module. You need the container story, then the modules your service actually imports. Curiosity about the next module should come from a situation — we need OAuth — not from a checklist.

One last orientation before DI deep dive: Spring did not abolish design. If your domain is a mud ball, the container will happily wire a mud ball. IoC makes dependencies explicit; it does not invent bounded contexts for you. Use the container to reveal the graph, then fix the graph. That attitude prevents "we rewrote in Spring and nothing improved" disappointments.

Curiosity should already be tugging: how exactly should we inject — constructor, setter, field — and why do tests become easier? That is not a side topic. It is the next episode: IoC and dependency injection in practice.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Framework Intro (Episode 71).

Narration technique: day-one "we use Spring" → ecosystem thesis → construction sprawl situation → IoC/ApplicationContext/beans → convention+extension → misconceptions → interview woven → walkthrough → bridge to DI.

Teaching points preserved: IoC mindset; beans/ApplicationContext; why enterprises adopt; convention+extension; not magic — wiring.
