# Episode 72 — IoC and Dependency Injection

**Cut:** v1 (original)

## Transcript (from captions)

Episode Seventy-One introduced Spring as a platform around an IoC container. Inversion of Control flips who constructs collaborators — the framework does. Dependency Injection is the main technique Spring uses to achieve IoC.

Get this wrong — mysterious nulls, circular dependencies, and untestable code. Get this right — clear graphs, easy mocks, and predictable startup. Today — IoC versus DI, injection styles, bean scopes, and wiring pitfalls.

Episode Seventy-Two. IoC and Dependency Injection. IoC is the principle — DI is the mechanism. Inversion of Control — your code does not new up the whole object graph. Dependency Injection — dependencies are provided from outside the class.

Spring's ApplicationContext is the injector and lifecycle manager. Factories, service locators, and events are other IoC styles — DI is the default. Say IoC for the idea — DI for how Spring usually implements it.

Three injection styles you will see in Spring code. Constructor injection — required dependencies as final fields — preferred. Setter injection — optional dependencies or reconfiguration after create.

Field injection with Autowired — short, but harder to test and reason about. Constructor injection makes invariants obvious — object is complete after new. Modern Spring and Boot samples default to constructor injection for a reason.

Bean scopes control how many instances the container creates. Singleton — one shared instance per context — the Spring default. Prototype — a new instance every time you ask the container.

Request and session scopes — web-aware, tied to HTTP lifecycle. Wrong scope — shared mutable state across requests is a classic bug. Default to singleton services with immutable or carefully synchronized state.

How Spring finds and wires beans. Component scanning picks up Stereotype annotations — Service, Repository, Controller. Configuration classes with Bean methods define explicit beans.

Qualifiers disambiguate when multiple candidates share a type. Profiles activate environment-specific beans — local, staging, prod. Circular dependencies signal a design smell — break the cycle with redesign.

DI pays off hardest in tests. Unit tests construct the class with mocks — no container required. Slice tests load a thin Spring context — web or data layer only. Full ApplicationContext tests catch wiring mistakes — slower but valuable.

Avoid static singletons and ServiceLocator lookups — they fight DI. If you cannot inject a fake, the design is fighting you. Three common mistakes. One — field injection everywhere — invisible dependencies, awkward tests.

Two — singleton beans holding request-specific mutable state. Three — Autowired on concrete classes with no interface — tight coupling. Also — ignoring constructor failure — missing beans explode at startup for good reason.

Fail fast at context refresh — never with a NullPointerException in production. Interview question — why prefer constructor injection? Required dependencies are explicit and can be final.

The object is fully initialized after construction — no half-ready beans. Unit tests pass mocks without Spring or reflection hacks. Circular dependencies surface earlier — design problems become visible.

Spring and the community treat constructor injection as the default style. Wiring is clear — next is how projects start fast. Episode Seventy-Three — Spring Boot Basics. Starters, auto-configuration, configuration properties, and the executable jar.

See you there.
