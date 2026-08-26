# Episode 19 — Sealed Classes

| Field | Value |
|---|---|
| Episode | 19 |
| Title | Sealed Classes |
| Catalog handbook column | 19 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Records made transparent data cheap to declare. As soon as those data shapes form a family — circle or rectangle, success or failure, cash or card — a new risk appears.

Suppose we model shapes with an interface and let anyone implement it. Drawing code switches on runtime type, or uses `instanceof` chains, and hopes it covered every case. A new subtype arrives from another package. The switch still compiles. The new shape falls into a default that returns zero area. The bug is quiet until a designer adds a triangle and a dashboard goes blank.

So the question becomes: can a hierarchy say, honestly, "these are the only subtypes that exist"?

Enums already closed a set of constant instances. Here the instances can be whole types — each carrying different fields. That is the leap: from a flat vocabulary to a closed family of shapes.


Sealed classes and interfaces answer that. Sealing closes a hierarchy so switches and readers can be exhaustive. The `permits` clause lists the allowed subtypes.

```java
sealed interface Shape permits Circle, Rect {}
record Circle(double r) implements Shape {}
record Rect(double w, double h) implements Shape {}
```

Read it as a contract. `Shape` is sealed. Only `Circle` and `Rect` may implement it — within the same-module and package rules Java requires for permitted types. Each permitted type is a record here, which pairs cleanly with sealing: the variants are data, the parent is the closed sum of those variants. That models closed domains honestly instead of pretending every hierarchy must stay open forever.

The payoff shows up in switch. Exhaustive switch checking becomes possible because the compiler knows the full set.

```java
double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.r() * c.r();
        case Rect r -> r.w() * r.h();
    };
}
```

No default required when every permitted subtype is handled. Pattern matching binds `c` or `r` so you can read components without a cast. Add `Triangle` to `permits` later, and the incomplete switch becomes a compile error instead of a silent miss. That is the design loop sealing enables: change the domain vocabulary, and the compiler herds the call sites.

What if the domain must stay open? Then do not seal it. Open hierarchies stay unsealed on purpose — plugin types, SPI implementations, frameworks that expect unknown subclasses. Sealing is for closed worlds. Using it on an extension point fights the product. The feature is a truthfulness tool, not a fashion accessory.

Sealed types and records together encourage a style of domain modeling that feels like algebraic data types: a small set of known variants, each carrying its fields, handled exhaustively. You still write ordinary classes when behavior and identity dominate. You reach for sealed + record when the meaning is "exactly these cases."

A common misunderstanding is to seal a type and then keep writing `default` branches that swallow new cases. That throws away the exhaustiveness gift. Another is to permit dozens of unrelated types because "we might need them," which recreates the open mess with extra syntax. Permit what the domain actually allows. Nested permitted types in the same compilation unit can even omit an explicit `permits` list when the compiler can see them — still, clarity often favors saying the list out loud.


The same sealing idea shows up in results, not only shapes.

```java
sealed interface PayResult permits Paid, Declined, Pending {}
record Paid(String txId) implements PayResult {}
record Declined(String reason) implements PayResult {}
record Pending(String pollUrl) implements PayResult {}

String message(PayResult result) {
    return switch (result) {
        case Paid p -> "ok:" + p.txId();
        case Declined d -> "no:" + d.reason();
        case Pending p -> "wait:" + p.pollUrl();
    };
}
```

Payment outcomes are a closed domain. Callers should not invent a fourth unofficial result by subclassing in another jar. Sealing says that out loud. Exhaustive switch makes forgetting `Pending` a compile error. That is honesty in the type system — the same honesty we wanted from enums for flat vocabularies, now for structured variants.

So let's reconnect the chain. Open shape hierarchies hid missing cases. Sealing and `permits` closed the set. Records made the variants compact. Exhaustive switches turned domain change into compile-time pressure. Unsealed hierarchies remained the right choice for true extension points.

Once types and packages multiply across a large codebase, another boundary question appears above the package level: which parts of the JDK and which parts of our own system are allowed to see each other at all? Packages alone proved too weak for that.

Think of sealing as the sibling of enums at a larger scale. Enums close a set of constant instances. Sealed types close a set of subtypes that may themselves carry data. Both exist so the compiler can help you stay honest when the domain is finite. When the domain is intentionally infinite — third-party plugins, customer-provided extensions — leave the hierarchy open and document the SPI. The language supports both truths; your job is to pick the true one.

When you combine sealed types with modules, permitted subtypes typically need to live in the same module (and often the same package for accessibility). That constraint is intentional: a closed hierarchy should not be quietly extended from across a jar boundary. If you need cross-module variants, redesign — perhaps a sealed interface in an API module with permitted types that are themselves exported carefully — or admit the hierarchy is open.

That larger encapsulation story is Episode Twenty — Modules and JPMS.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 19 (*Sealed Classes*).

Narration technique: open-hierarchy miss → sealed/permits as answer → records as variants → exhaustive switch → keep open when needed → next natural problem (strong encapsulation / modules). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- permits lists allowed subtypes.
- Enables exhaustive switch checking.
- Pairs well with records.
- Models closed domains honestly.
- Open hierarchies stay unsealed on purpose.
