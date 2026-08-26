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

The practical situation that makes Spring necessary is the same pain Episode Sixty-Eight named: construction sprawl. Without a container, every service builds its dependencies by hand, or reaches into static locators, or news up concrete classes deep inside methods. Tests suffer. Swapping a real mailer for a fake means editing production construction paths. Enterprises adopt Spring because large codebases need consistent wiring, lifecycle, and extension points — not because annotations are fashionable.

Hold the IoC container mindset firmly. IoC means inversion of control over construction: instead of your class creating its dependencies, something outside provides them. In Spring, that something is the `ApplicationContext`. Objects the container manages are beans. You describe what beans exist and how they relate; the container instantiates, injects, and manages lifecycle.

Walk a mental first day. You open a service class. It declares a constructor taking a repository interface. You do not see `new JdbcOrderRepository` inside. Somewhere else — configuration class, component scan, Boot auto-config — a bean implementing that interface is defined. At runtime the context creates the repository, creates the service, injects the repository, and hands you a ready graph. Your service's job stays business logic. Construction policy lives elsewhere.

Convention plus extension points is why teams stay. Defaults get you moving. Interfaces and SPI hooks let you replace parts without forking the framework. That is not magic — it is wiring. Treating Spring as magic is the first misunderstanding. Avoiding understanding DI is the second: people copy `@Autowired` until a circular dependency appears and then declare frameworks evil. Bringing every module for a hello world is the third.

"Not magic — wiring" deserves a debugging ritual. When a bean is missing, read the startup failure: which definition was expected, which condition failed, which auto-config backed out. When two beans compete, understand `@Primary` and qualifiers. When a property is wrong, trace binding. Teams that treat Spring as magic restart until it works. Teams that treat it as wiring read the graph.

Portable abstractions matter at the edges. A `DataSource`, a messaging template, a cache manager — your code can target Spring's abstractions while drivers and brokers swap underneath. That portability is incomplete — dialects leak — but it beats scattering vendor API calls through domain services. Why enterprises adopt Spring becomes clearer with ten teams sharing platform practices: a shared grammar of beans, injection, profiles, and configuration beats each team inventing lifecycle differently.

A healthy first service uses a small slice: Boot for executable shape, web for HTTP, maybe JDBC or JPA, Security when needed. Expanding module count without expanding understanding is how microservices become micro-monoliths of configuration. You do not need every module. You need the container story, then the modules your service actually imports — curiosity driven by a situation, not a checklist.

One last orientation: Spring did not abolish design. If your domain is a mud ball, the container will happily wire a mud ball. IoC makes dependencies explicit; it does not invent bounded contexts. Use the container to reveal the graph, then fix the graph.

What is Spring at heart? A DI-centered programming and configuration model with a large ecosystem around web, data, security, and integration. Say that, then connect it to why your team chose it: testability, consistent structure, and battle-tested integrations.

Curiosity should already be tugging: how exactly should we inject — constructor, setter, field — and why do tests become easier? That is the next episode: IoC and dependency injection in practice.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Spring Framework Intro (Episode 71).

Narration technique: day-one "we use Spring" → ecosystem thesis → construction sprawl → IoC/ApplicationContext/beans → first-day walk → not magic wiring → bridge to DI.

Teaching points preserved: IoC mindset; beans/ApplicationContext; why enterprises adopt; convention+extension; not magic — wiring.
