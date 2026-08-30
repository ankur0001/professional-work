# Episode 18 — Records

| Field | Value |
|---|---|
| Episode | 18 |
| Title | Records |
| Catalog handbook column | 18 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Reflection showed how frameworks dig into types. A lot of those types are not rich behavior engines. They are data carriers: a point with x and y, an order id with a total, a message with a timestamp. For years Java made us write the same ceremony for each one.

Suppose we need an immutable point. The classic class grows a constructor, getters, `equals`, `hashCode`, and `toString`. Miss one and sets, maps, or logs misbehave. Two points with equal coordinates fail as map keys because `equals` was forgotten. The natural question is: if the class is only transparent data, why are we handwriting the mechanical parts?

Records exist for that job. A record is a compact declaration of immutable state. The compiler supplies the canonical constructor, accessors, `equals`, `hashCode`, and `toString` based on the components.

```java
record Point(int x, int y) {
    public Point {
        if (x < 0 || y < 0) {
            throw new IllegalArgumentException("coordinates must be non-negative");
        }
    }
}

Point originish = new Point(0, 0);
System.out.println(originish.x() + "," + originish.y());
```

Walk this carefully. `record Point(int x, int y)` declares the state up front. The body shows a compact constructor: no parameter list repeated, validation before the fields are assigned. Accessors are `x()` and `y()`, not `getX()` by default. Two points with the same coordinates compare equal because `equals` and `hashCode` are derived from the components.

Canonical and compact constructors matter once validation appears. The canonical constructor takes every component. The compact form lets you validate or normalize without relisting assignments. If construction needs a multi-step workflow, you may want a factory or a fuller class. Records keep construction honest; they are not a dumping ground for every rule in the domain.

What records are not: a replacement for every class. Records model transparent immutable data; classes model richer encapsulated behavior. Entities with identity, mutable lifecycle, or complex encapsulation still want ordinary classes. Record fields are final; the immutability is shallow. A record can hold a mutable list reference, and the list can still change. Forgetting that causes subtle bugs when people assume "record means deep freeze."

Prefer records at boundaries where transparent data is the point: DTOs, value objects, coordinates, and message payloads.

What if we skip records and keep writing boilerplate carriers?

```java
final class Point {
    private final int x;
    private final int y;
    // constructor, getters, equals, hashCode, toString...
}
```

It works. It also drifts. Someone updates a field and forgets `equals`. Someone adds logging and skips `toString`. The record makes the data-carrier intent explicit and keeps the mechanical contract in sync with the state declaration.

Place a record at an API boundary where transparent data is the whole point.

```java
record Money(long cents, String currency) {
    public Money {
        if (cents < 0) throw new IllegalArgumentException("cents");
        if (currency == null || currency.isBlank()) {
            throw new IllegalArgumentException("currency");
        }
    }
}

record PriceQuote(String sku, Money amount) {}
```

`Money` validates in a compact constructor. `PriceQuote` nests records without inventing getter ceremony. If `Money` later needs rounding policies and mutable ledgers, promote it to a class — records are not a ban on classes, they are a better default for pure carriers.

Boilerplate carriers created fatigue. Records answered with auto `equals` / `hashCode` / `toString` / accessors. Compact constructors handled validation. Ordinary classes remained for richer behavior.

Once data carriers are easy, another design question sharpens: sometimes a type should have only a known set of subtypes — not an open inheritance free-for-all. How do we say that in the language?

That is the pressure that brings sealed classes.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 18 (*Records*).

Narration technique: boilerplate data-carrier problem → record as answer → compact constructor walkthrough → not every class → sealed/pattern pairing hint → shallow immutability → next natural problem (closed hierarchies / sealed). Continuity-checked transitions.
