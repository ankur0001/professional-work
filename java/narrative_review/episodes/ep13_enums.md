# Episode 13 — Enums

| Field | Value |
|---|---|
| Episode | 13 |
| Title | Enums |
| Catalog handbook column | 13 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Packages gave our types a home. That does not yet solve a quieter mess that shows up the moment a domain has a fixed vocabulary.

Suppose we are building an order system. An order can be new, paid, or shipped. The fastest way to encode that is a string field: `"NEW"`, `"PAID"`, `"SHIPPED"`. It compiles. It demos well. Then someone writes `"Payed"`, or `"paid"`, or `"SHIPED"`. The compiler shrugs. The bug arrives in production as a status that matches nothing.

So a natural question appears: if the set of legal values is known and closed, why are we letting arbitrary text pretend to be a state?

That question is why enums exist. An enum is a type-safe set of named constants. Instead of magic strings or magic ints, you get a vocabulary the compiler understands.

```java
enum Status {
    NEW, PAID, SHIPPED
}
```

`Status` is now a real type. A method that takes `Status` cannot accidentally receive `"SHIPED"`. The allowed values live in one place. When a teammate reads the code, the domain speaks for itself.

But enums in Java are not only labels. Once you have a named state, behavior often wants to hang off that state. Is this status terminal? Can we refund from here? That pressure turns the enum into a small class with fields and methods.

```java
enum Status {
    NEW, PAID, SHIPPED;

    boolean terminal() {
        return this == SHIPPED;
    }
}
```

Walk through what this buys you. `NEW`, `PAID`, and `SHIPPED` are the only instances. `terminal()` answers a domain question without a scattered `if` chain of strings. Call sites write `order.status().terminal()` and stay readable. The method belongs next to the vocabulary it depends on.

Enums also shine with `switch`, because the set of cases is finite. When you switch on a `Status`, every legal value is visible. Modern Java can even warn or error when a switch is not exhaustive. That is different from switching on a `String`, where the compiler cannot know which typos you forgot.

```java
String label(Status status) {
    return switch (status) {
        case NEW -> "Awaiting payment";
        case PAID -> "Ready to ship";
        case SHIPPED -> "Done";
    };
}
```

Each case is a real constant, not a quoted guess. If someone later adds `CANCELLED` to the enum, the incomplete switch becomes a compile-time problem instead of a silent default path.

What if we skip enums and keep stringly-typed status codes?

```java
void advance(String status) {
    if (status.equals("PAID")) {
        // ship...
    }
}
```

It looks small. Then `"Paid"` sneaks in from a form, or a partner API sends `"paid"`. Equality fails. The order never ships. Or worse, a giant switch grows without exhaustiveness thinking, and one forgotten branch becomes a production incident. Enums exist to make those mistakes hard.

There is one more practical detail once enums become common: collections specialized for them. `EnumSet` and `EnumMap` are fast, compact structures tuned for enum keys and values. If you need a set of flags that are themselves enum constants, reach for `EnumSet` before a general `HashSet`. You do not need every collection chapter yet — you only need to know the specialized tools exist when the key type is an enum.

One failure mode still bites people who treat enums like mutable bags: mutable enum fields that change under you. Prefer enums as immutable vocabulary with behavior, not as disguised global variables. Model states explicitly. If a value can be anything, it is not an enum problem. If a value must be one of a closed set, it is.

So let's reconnect the chain. We started with status strings that compiled and lied. Enums answered with type-safe constants. Fields and methods let vocabulary carry behavior. Switch made exhaustive handling natural. `EnumSet` and `EnumMap` showed specialized collections for the same idea. Skipping enums showed the stringly-typed trap.

Once constants can be objects, another pressure appears: collections and APIs often want objects, while hot paths still want primitives. How does an `int` sit inside a `List`?

That bridge is Episode Fourteen — Wrappers and Autoboxing.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 13 (*Enums*).

Narration technique: magic-string status problem → enum as answer → behavior on constants → switch exhaustiveness → EnumSet/EnumMap → mutable-field trap → next natural problem (primitives in object APIs). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Type-safe constants.
- Enums can have fields and methods.
- Great with switch.
- EnumSet/EnumMap are specialized and fast.
- Model states explicitly.
