# Episode 68 — Creational Patterns

| Field | Value |
|---|---|
| Episode | 68 |
| Title | Creational Patterns |
| Catalog handbook column | 68 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Sixty-Seven left us with a rule: name a pattern when a problem recurs. Creation is one of those problems. Objects need validation, defaults, shared instances, or alternate implementations. Creational patterns manage how objects come to life. In modern Java services, DI containers often own lifecycle — classical factory and singleton moves migrate into the container. The ideas do not vanish. Their addresses change.

Start with the singleton everyone meets too early:

```java
public final class App {
  public static final App INSTANCE = new App();
  private App() {}
}
```

A simple eager singleton: one instance, private constructor, global access. Clear — and a magnet for misuse. Singleton as a global mutable bag recreates global variables with better branding. Double-checked locking myths still circulate for lazy singletons; modern Java has safer idioms, enums-as-singleton, or simply letting a container manage scope. The interview trap is debating locking trivia while missing the design smell: do you need a global at all?

Separate "one instance" from "global access." A process may need a single cache manager without every class reaching into a static getter. Injection gives you the single instance without the global lookup. A Spring bean defaulting to singleton scope is not the same social object as a mutable `App.INSTANCE` bag — dependencies remain injected and testable. Prefer that model for application services.

Factory methods appear when construction deserves a name. `Order.createFromCart(cart)` encapsulates invariants better than a public constructor with eight parameters. Factories also hide concrete classes behind interfaces — useful when tests need fakes. A factory that only wraps `new` without policy is ceremony. Use factories when creation policy exists: caching, subtype selection, validation, or environment-specific wiring. Boundary types shine here: `Money.of(amount, currency)` rejects invalid combinations; `UserId.from(string)` encapsulates parsing.

Builders earn their keep when telescoping constructors appear and call sites become unreadable:

```java
Report report = Report.builder()
    .title("Q4")
    .includeCharts(true)
    .build();
```

An email message needs from, to, subject, optional cc, bcc, attachments, headers. Telescoping constructors force nulls and argument-order bugs. A builder makes the call site self-describing and can enforce invariants in `build()` — requiring at least one recipient. That is creational policy, not mere sugar. Prototype — cloning — shows up rarely in Java application code; prefer clear copy constructors or factories unless you truly need clone-style duplication.

In Spring and similar containers, beans have scopes and lifecycle callbacks. The container may be your factory. Constructor injection makes dependencies honest instead of reaching for `App.INSTANCE`. You still decide what is singleton-scoped, what is request-scoped, what should be built per call, and what a builder should assemble before registration.

Walk a failure mode. A team makes a "service locator" singleton that hands out dependencies anywhere. Tests become hard. Circular creation appears. The creational pattern that would have helped was not a fancier singleton — it was explicit construction or DI with constructor injection. If construction is dishonest — half-initialized objects, setters required after `new` — every creational pattern becomes makeup on a broken type. Fix the type's birth certificate first. In tests: if you cannot construct a valid domain object in one or two lines, construction policy is too scattered.

If asked builder versus telescoping constructors, say: builder keeps call sites readable when many optional fields exist. If asked about singletons, admit caveats: global mutable state, testing pain, and that containers often own the one-instance story now. On double-checked locking: say why people reached for it historically, why it was easy to get wrong, and what you would do now instead.

Creation sets the stage for structure: once objects exist, how do we assemble them so behavior can grow without subclass explosions? Episode Sixty-Nine is structural patterns — adapters, decorators, facades, and proxies.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Creational Patterns (Episode 68).

Narration technique: creation as recurring problem → singleton + caveats → factory methods → builder vs telescoping → containers own lifecycle → failure mode → bridge to structural.

Teaching points preserved: singleton caveats; factory methods; builder; prototype rarely; containers may own lifecycle.
