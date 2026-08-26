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

`Status` is now a real type. A method that takes `Status` cannot accidentally receive `"SHIPED"`. The allowed values live in one place. When a teammate reads the code, the domain speaks for itself. Interviewers sometimes ask why enums beat `public static final int`. The short answer is type safety, namespacing, and room for attached behavior — an `int` constant named `PAID` is still just another int that can be confused with a quantity or an http code.

But enums in Java are not only labels. Once you have a named state, behavior often wants to hang off that state. Is this status terminal? Can we refund from here? That pressure turns the enum into a small class with fields and methods.

```java
enum Status {
    NEW, PAID, SHIPPED;

    boolean terminal() {
        return this == SHIPPED;
    }
}
```

Walk through what this buys you. `NEW`, `PAID`, and `SHIPPED` are the only instances of `Status`. `terminal()` answers a domain question without a scattered `if` chain of strings. Call sites write `order.status().terminal()` and stay readable. The method belongs next to the vocabulary it depends on. You can also give constants fields — a display label, a sort rank — as long as you treat that data as part of the fixed vocabulary, not as a mutable global.

Enums also shine with `switch`, because the set of cases is finite. When you switch on a `Status`, every legal value is visible. Modern Java can warn or error when a switch is not exhaustive. That is different from switching on a `String`, where the compiler cannot know which typos you forgot.

```java
String label(Status status) {
    return switch (status) {
        case NEW -> "Awaiting payment";
        case PAID -> "Ready to ship";
        case SHIPPED -> "Done";
    };
}
```

Each case is a real constant, not a quoted guess. If someone later adds `CANCELLED` to the enum, the incomplete switch becomes a compile-time problem instead of a silent default path. That is the habit to build: model states explicitly, then let the compiler herd every place that must react.

What if we skip enums and keep stringly-typed status codes?

```java
void advance(String status) {
    if (status.equals("PAID")) {
        // ship...
    }
}
```

It looks small. Then `"Paid"` sneaks in from a form, or a partner API sends `"paid"`. Equality fails. The order never ships. Or worse, a giant switch grows without exhaustiveness thinking, and one forgotten branch becomes a production incident. Mutable enum fields cause a different surprise: if you stash changing data on an enum constant, every caller shares that mutation. Prefer enums as immutable vocabulary with behavior, not as disguised global variables.

There is one more practical detail once enums become common: collections specialized for them. `EnumSet` and `EnumMap` are fast, compact structures tuned for enum keys and values. If you need a set of flags that are themselves enum constants — say which notification channels are enabled — reach for `EnumSet` before a general `HashSet`. You do not need every collection chapter yet. You only need to know the specialized tools exist when the key type is an enum, and that they exploit the closed, ordinal nature of enum constants.


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

The field is a `Status`, not a `String`. `markPaid` refuses nonsense transitions instead of comparing quoted text. When you later add `CANCELLED`, every place that switches on `status()` becomes a checklist the compiler can help enforce. That is what "model states explicitly" means in a product: the type carries the allowed world, and methods defend the transitions.

So let's reconnect the chain. We started with status strings that compiled and lied. Enums answered with type-safe constants. Fields and methods let vocabulary carry behavior. Switch made exhaustive handling natural. `EnumSet` and `EnumMap` showed specialized collections for the same idea. Skipping enums showed the stringly-typed trap; mutable enum fields showed the shared-mutation trap.

Once constants can be objects, another pressure appears: collections and APIs often want objects, while hot paths still want primitives. How does an `int` sit inside a `List`?

Enums also change how teams talk in reviews. Instead of arguing about string conventions — uppercase or not, British spelling or American — the review asks whether the domain set is complete and whether transitions belong on the enum or on the entity. That shift from formatting debates to domain debates is a quiet productivity win. When you see a `Map<String, String>` of statuses in a legacy module, you now have a concrete refactor target: replace the keys with an enum, move behavior next to the constants, and let switches go exhaustive.

That bridge is Episode Fourteen — Wrappers and Autoboxing.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 13 (*Enums*).

Narration technique: magic-string status problem → enum as answer → behavior on constants → switch exhaustiveness → EnumSet/EnumMap → traps → next natural problem (primitives in object APIs). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Type-safe constants.
- Enums can have fields and methods.
- Great with switch.
- EnumSet/EnumMap are specialized and fast.
- Model states explicitly.
