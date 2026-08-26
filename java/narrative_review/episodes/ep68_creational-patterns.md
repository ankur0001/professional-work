# Episode 68 — Creational Patterns

| Field | Value |
|---|---|
| Episode | 68 |
| Title | Creational Patterns |
| Catalog handbook column | 68 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Sixty-Seven left us with a rule: name a pattern when a problem recurs. Creation is one of those recurring problems. Objects do not only "get constructed." They need validation, defaults, shared instances, or alternate implementations. Creational patterns manage how objects come to life. In modern Java services, dependency injection containers often own lifecycle — which means some classical factory and singleton moves migrate into the container. The ideas do not vanish. Their addresses change.

Start with the singleton everyone meets too early:

```java
public final class App {
  public static final App INSTANCE = new App();
  private App() {}
}
```

This is a simple eager singleton: one instance, private constructor, global access. It is clear. It is also a magnet for misuse. Singleton as a global mutable bag — a place to stash whatever state anyone wants — recreates global variables with better branding. Double-checked locking myths still circulate for lazy singletons; modern Java has safer idioms, enums-as-singleton, or simply letting a container manage scope. The interview trap is debating locking trivia while missing the design smell: do you need a global at all?

Factory methods appear when construction deserves a name. `Order.createFromCart(cart)` can encapsulate invariants better than a public constructor with eight parameters. Factories also hide concrete classes behind interfaces — useful when tests need fakes and production needs a real gateway. But a factory that only wraps `new` without policy is ceremony. Use factories when creation policy exists: caching, subtype selection, validation, or environment-specific wiring.

Builders earn their keep when telescoping constructors appear — `new Foo(a)`, `new Foo(a,b)`, `new Foo(a,b,c,d,e)` — and call sites become unreadable. A builder keeps optional fields explicit at the call site:

```java
Report report = Report.builder()
    .title("Q4")
    .includeCharts(true)
    .build();
```

That readability is the point. Builder versus telescoping constructors is not aesthetics alone; it is about whether the next teammate can see which arguments are which without counting commas. Prototype — cloning instances — shows up more rarely in Java application code; prefer clear copy constructors or factories unless you truly need clone-style duplication.

Now the modern twist. In Spring and similar containers, beans have scopes and lifecycle callbacks. The container may be your factory. Constructor injection, which we will deepen soon, makes dependencies honest instead of reaching for `App.INSTANCE`. That does not abolish creational thinking. It relocates it: you still decide what is singleton-scoped, what is request-scoped, what should be built per call, and what should be assembled by a builder before registration.

Walk a failure mode. A team makes a "service locator" singleton that hands out dependencies anywhere. Tests become hard because anything can pull anything. Circular creation appears. Hidden static dependencies multiply. The creational pattern that would have helped was not a fancier singleton — it was explicit construction or DI with constructor injection. Creational patterns are about controlling birth so the rest of the design stays honest.

If asked builder versus telescoping constructors, say: builder keeps call sites readable when many optional fields exist. If asked about singletons, admit caveats: global mutable state, testing pain, and the fact that containers often own the one-instance story now.

Make the builder story more tactile. An email message needs from, to, subject, optional cc, optional bcc, optional attachments, optional headers. Telescoping constructors force nulls and argument-order bugs. A builder makes the call site self-describing and can enforce invariants in `build()` — for example, requiring at least one recipient. That is creational policy, not mere sugar.

Factory methods also shine at boundary types. `Money.of(amount, currency)` can reject invalid combinations; `UserId.from(string)` can encapsulate parsing. These look small, but they concentrate rules that would otherwise scatter across constructors and static helpers. Prototype stays rare because Java cloning is awkward and most domains prefer explicit copy operations you can read.

Containers change the singleton conversation in enterprise apps. A Spring bean defaulting to singleton scope is not the same social object as a mutable `App.INSTANCE` bag. The container can still give you one instance, but dependencies remain injected and testable. Prefer that model for application services. Keep true singletons for rare infrastructure needs — and even then, ask whether an enum singleton or a holder is clearer than clever lazy locking.

Double-checked locking myths persist in interviews. You do not need to perform the myth; you need to say why people reached for it historically, why it was easy to get wrong before memory model clarity, and what you would do now instead. That answer shows judgment.

Finally, connect creation to failure. If construction is dishonest — half-initialized objects, setters required after `new`, optional dependencies actually required — every creational pattern becomes makeup on a broken type. Fix the type's birth certificate first.

One more creational seam shows up in tests. If you cannot construct a domain object with valid defaults in one or two lines, construction policy is too scattered. Builders and factories should make the valid happy path easy and the invalid path loud. When every test needs ten setters before the object is usable, the type was not born honestly — and no container will fully hide that pain.

Also separate "one instance" from "global access." A process may need a single cache manager without every class reaching into a static getter. Injection gives you the single instance without the global lookup. That distinction keeps singleton useful as a scope and dangerous as a lifestyle.

Creation sets the stage for structure: once objects exist, how do we assemble them so behavior can grow without subclass explosions? Episode Sixty-Nine is structural patterns — adapters, decorators, facades, and proxies.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Creational Patterns (Episode 68).

Narration technique: creation as recurring problem → singleton + caveats → factory methods → builder vs telescoping → prototype rarity → containers own lifecycle → failure mode → interview woven → bridge to structural.

Teaching points preserved: singleton caveats; factory methods; builder; prototype rarely; containers may own lifecycle.
