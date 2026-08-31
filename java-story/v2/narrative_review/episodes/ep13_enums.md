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

Suppose we are building an order system. An order can be new, paid, or shipped. The fastest way to encode that is a string field: `"NEW"`, `"PAID"`, `"SHIPPED"`. It compiles. It demos well. Then someone writes `"Payed"`, or `"paid"`, or `"SHIPED"`. The compiler shrugs. The bug arrives in production as a status that matches nothing — a branch never taken, a warehouse never notified.

So a natural question appears: if the set of legal values is known and closed, why are we letting arbitrary text pretend to be a state?

That question is why enums exist. An enum is a type-safe set of named constants. Instead of magic strings or magic ints, you get a vocabulary the compiler understands.

```java
enum Status {
    NEW, PAID, SHIPPED
}
```

`Status` is now a real type. A method that takes `Status` cannot accidentally receive `"SHIPED"`. The allowed values live in one place. Interviewers sometimes ask why enums beat `public static final int`. The short answer is type safety, namespacing, and room for attached behavior — an `int` constant named `PAID` is still just another int that can be confused with a quantity or an HTTP code.

But enums in Java are not only labels. Once you have a named state, behavior often wants to hang off that state. Is this status terminal? Can we refund from here? That pressure turns the enum into a small class with fields and methods.

```java
enum Status {
    NEW, PAID, SHIPPED;

    boolean terminal() {
        return this == SHIPPED;
    }
}
```

`NEW`, `PAID`, and `SHIPPED` are the only instances of `Status`. `terminal()` answers a domain question without a scattered `if` chain of strings. Call sites write `order.status().terminal()` and stay readable. You can also give constants fields — a display label, a sort rank — as long as you treat that data as part of the fixed vocabulary, not as a mutable global.

Enums also shine with `switch`, because the set of cases is finite. Modern Java can warn or error when a switch is not exhaustive.

```java
String label(Status status) {
    return switch (status) {
        case NEW -> "Awaiting payment";
        case PAID -> "Ready to ship";
        case SHIPPED -> "Done";
    };
}
```

Each case is a real constant, not a quoted guess. If someone later adds `CANCELLED` to the enum, the incomplete switch becomes a compile-time problem instead of a silent default path. Model states explicitly, then let the compiler herd every place that must react.

What if we skip enums and keep stringly-typed status codes?

```java
void advance(String status) {
    if (status.equals("PAID")) {
        // ship...
    }
}
```

It looks small. Then `"Paid"` sneaks in from a form, or a partner API sends `"paid"`. Equality fails. The order never ships. Mutable enum fields cause a different surprise: if you stash changing data on an enum constant, every caller shares that mutation. Prefer enums as immutable vocabulary with behavior, not as disguised global variables.

There is one more practical detail once enums become common: collections specialized for them. `EnumSet` and `EnumMap` are fast, compact structures tuned for enum keys and values. If you need a set of flags that are themselves enum constants, reach for `EnumSet` before a general `HashSet`.

Let's put the enum inside a small order story so the vocabulary has somewhere to live.

```java
public class Order {
    private Status status = Status.NEW;

    public void markPaid() {
        if (status != Status.NEW) {
            throw new IllegalStateException("already past NEW");
        }
        status = Status.PAID;
    }

    public Status status() {
        return status;
    }
}
```

The field is a `Status`, not a `String`. `markPaid` refuses nonsense transitions instead of comparing quoted text. When you later add `CANCELLED`, every place that switches on `status()` becomes a checklist the compiler can help enforce.

We started with status strings that compiled and lied. Enums answered with type-safe constants. Fields and methods let vocabulary carry behavior. Switch made exhaustive handling natural.

Once constants can be objects, another pressure appears: collections and APIs often want objects, while hot paths still want primitives. How does an `int` sit inside a `List`?

That bridge is wrappers and autoboxing.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 13 (*Enums*).

Narration technique: magic-string status problem → enum as answer → behavior on constants → switch exhaustiveness → EnumSet/EnumMap → traps → next natural problem (primitives in object APIs). Continuity-checked transitions.
