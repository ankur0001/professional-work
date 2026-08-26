# Episode 72 — IoC and Dependency Injection

| Field | Value |
|---|---|
| Episode | 72 |
| Title | IoC and Dependency Injection |
| Catalog handbook column | 72 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Seventy-One said Spring wires beans so your code can depend on interfaces. Today we make that wiring honest. IoC inverts construction — your class no longer news up its collaborators. Dependency injection is how the inverted control delivers those collaborators. The style you choose changes testability, clarity, and failure modes.

Here is the shape you want in new code:

```java
@Service
class OrderService {
  private final OrderRepo repo;
  OrderService(OrderRepo repo) { this.repo = repo; }
}
```

Constructor injection preferred. Required dependencies are explicit, `final`, and impossible to forget if you construct the object yourself in a unit test. `new OrderService(fakeRepo)` is a complete story. No Spring container required for that unit test. That is why testability skyrockets when constructors tell the truth.

Contrast service locator: code asks a global registry for dependencies when it feels like it. Dependencies become invisible in the signature. Hidden static dependencies create the same fog. Field injection — `@Autowired` on fields — looks tidy and makes testing and immutability harder; avoid field injection in new code unless you have a constrained reason. Setters can work for optional dependencies; required ones belong in the constructor.

IoC versus service locator is worth saying aloud. Both can avoid `new` inside business logic. IoC with injection pushes dependencies inward from the outside. Service locator pulls them from a deep hole in the middle of a method. Pulling hides graph shape. Pushing reveals it.

Scopes matter once the container owns lifecycle. A singleton-scoped bean is one shared instance — fine for stateless services, dangerous if you stash request state in fields. Request or session scopes exist for web concerns. Mixing scopes carelessly — injecting a narrower-scoped bean into a singleton without care — creates subtle bugs. Circular dependencies are a design smell; frameworks may work around them, but the honest move is to break the cycle in the domain model.

Walk the failure modes. Field injection everywhere until tests need reflection hacks. Hidden static gateways that bypass the container and freeze concrete types. Circular dependencies ignored until startup fails in a different environment. Each failure is a construction honesty problem.

Why constructor injection? Required dependencies are explicit, final, and easy to unit test. Keep that sentence ready. Then add: prefer interfaces at boundaries, let the container provide implementations, and keep business logic free of lookup calls.

Make the unit-test story loud. With constructor injection, a pure unit test creates the service with a fake repository and asserts a domain rule — no Spring test slice required. That speed changes how often people run tests. Field injection quietly destroys that path: you need reflection or a container to populate private fields. The annotation looked shorter. The feedback loop got longer.

Circular dependencies often mean two types each need the other to exist. Sometimes the real fix is a third type that owns the interaction. Sometimes it is an event. Sometimes it is splitting a god service. Framework workarounds that inject proxies to break cycles can boot the app and still leave a confused domain. Treat the cycle as a design alarm.

Scopes bite when a singleton service stores request-specific state in an instance field. Under concurrent requests, users see each other's data. The DI style did not cause that alone — mutability plus scope did — but injection makes it easy to share one instance widely. Prefer stateless services; pass request data as method arguments.

IoC also clarifies boundaries for future microservices. A service that depends on an interface can later be wired to a local impl or a remote adapter. Dishonest static dependencies freeze you in place.

Constructor injection preferred remains the headline. Support it with: explicit required deps, immutability, easy fakes, clearer graphs, fewer hidden nulls after construction.

Compare three constructors aloud. No-args plus setters: the object exists before it is ready. Field injection: the object looks ready in source but is not constructible in tests. Constructor with required deps: the object cannot exist unfinished. That progression is the teaching point. Frameworks that encourage unfinished objects make illegal states representable; constructor injection fights that.

Service locator versus IoC also shows up in legacy migrations. You may find getBean calls mid-method. Treat them as debt. Replace with injection at the boundary when you can. Each lookup you remove makes the graph more visible and the test suite more honest.

When someone asks why constructor injection, answer with explicit required dependencies, final fields, and easy unit tests — then mention scopes and circular dependencies as the next maturity topics so the conversation does not stop at the annotation.

Put the preference hierarchy in one spoken checklist. Required collaborators: constructor parameters, final fields. Optional collaborators: optional parameters or setters with defaults. Cross-cutting infrastructure: prefer forms that keep business classes unaware. Lookups mid-method: debt. Field injection in new code: avoid. If a classmate asks for a rule of thumb, that checklist is enough to start reviewing pull requests with taste.

Circular dependencies deserve an example. OrderService needs InventoryService; InventoryService needs OrderService to reserve stock for an order id. A better model might pass a reservation request value object or raise a domain event. The container might boot with a workaround; the domain remains confused. Prefer fixing the conversation between types.

Once wiring is clear, teams still drown in configuration for HTTP servers, JSON, DataSource, and logging. Spring Boot exists to make the happy path executable with opinions and auto-configuration — Episode Seventy-Three.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — IoC and Dependency Injection (Episode 72).

Narration technique: honest wiring need → constructor injection example → vs locator/field injection → scopes → failure modes → interview woven → bridge to Boot.

Teaching points preserved: constructor injection preferred; IoC vs service locator; testability; avoid field injection; scopes matter.
