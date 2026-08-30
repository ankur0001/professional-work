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

Constructor injection preferred. Required dependencies are explicit, `final`, and impossible to forget if you construct the object yourself in a unit test. `new OrderService(fakeRepo)` is a complete story — no Spring container required. That is why testability skyrockets when constructors tell the truth. Field injection quietly destroys that path: you need reflection or a container to populate private fields. The annotation looked shorter. The feedback loop got longer. Avoid field injection in new code. Setters can work for optional dependencies; required ones belong in the constructor.

Compare three constructors aloud. No-args plus setters: the object exists before it is ready. Field injection: the object looks ready in source but is not constructible in tests. Constructor with required deps: the object cannot exist unfinished. Frameworks that encourage unfinished objects make illegal states representable; constructor injection fights that.

IoC versus service locator is worth saying aloud. Both can avoid `new` inside business logic. IoC with injection pushes dependencies inward from the outside. Service locator pulls them from a deep hole mid-method. Pulling hides graph shape. Pushing reveals it. In legacy migrations you may find `getBean` calls mid-method — treat them as debt and replace with injection at the boundary when you can.

Scopes matter once the container owns lifecycle. A singleton-scoped bean is one shared instance — fine for stateless services, dangerous if you stash request state in fields. Under concurrent requests, users see each other's data. Prefer stateless services; pass request data as method arguments. Mixing scopes carelessly — injecting a narrower-scoped bean into a singleton without care — creates subtle bugs.

Circular dependencies are a design smell. OrderService needs InventoryService; InventoryService needs OrderService to reserve stock. Frameworks may inject proxies to boot anyway; the domain remains confused. Sometimes the fix is a third type that owns the interaction, sometimes an event, sometimes splitting a god service. Treat the cycle as a design alarm.

Put the preference hierarchy in one spoken checklist. Required collaborators: constructor parameters, final fields. Optional collaborators: optional parameters or setters with defaults. Lookups mid-method: debt. Field injection in new code: avoid. Why constructor injection? Required dependencies are explicit, final, and easy to unit test — then mention scopes and circular dependencies as the next maturity topics.

Once wiring is clear, teams still drown in configuration for HTTP servers, JSON, DataSource, and logging. Spring Boot exists to make the happy path executable with opinions and auto-configuration — but what does that classpath-driven magic actually buy, and what can it hide?

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — IoC and Dependency Injection (Episode 72).

Narration technique: honest wiring need → constructor injection example → vs locator/field injection → scopes → circular deps → checklist → bridge to Boot.

Teaching points preserved: constructor injection preferred; IoC vs service locator; testability; avoid field injection; scopes matter.
