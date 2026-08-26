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

Records exist for that job. A record is a compact declaration of immutable state. The compiler supplies the canonical constructor, accessors, `equals`, `hashCode`, and `toString` based on the components. Records are for immutable data carriers — less boilerplate, clearer models.

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

Walk this carefully. `record Point(int x, int y)` declares the state up front. The body shows a compact constructor: no parameter list repeated, validation before the fields are assigned. Invalid coordinates fail fast. Accessors are `x()` and `y()`, not `getX()` by default. Two points with the same coordinates compare equal because `equals` and `hashCode` are derived from the components. Logging a point prints something readable without a handwritten `toString`.

Canonical and compact constructors matter once validation appears. The canonical constructor takes every component. The compact form lets you validate or normalize without relisting assignments. Stuffing huge validation logic awkwardly into a record is a smell — if construction needs a multi-step workflow, you may want a factory or a fuller class. Records keep construction honest; they are not a dumping ground for every rule in the domain.

Records also pair naturally with sealed types and pattern matching, which we will deepen next episode. A closed set of record subtypes makes a switch over shapes feel like reading a specification. For now, notice the fit: transparent data plus a closed hierarchy is how many modern APIs model messages and results.

What records are not: a replacement for every class. Record versus class? Records model transparent immutable data; classes model richer encapsulated behavior. Entities with identity, mutable lifecycle, inheritance of behavior, or complex encapsulation still want ordinary classes. Using records for mutable entities casually fights the model — record fields are final; the immutability is shallow. A record can hold a mutable list reference, and the list can still change. Forgetting that they are final and only shallow-immutable by default causes subtle bugs when people assume "record means deep freeze."

Serialization and frameworks also feel the change. Many libraries understand records well now, but assumptions about JavaBean getters or mutable setters may not apply. Prefer records at boundaries where transparent data is the point: DTOs, value objects, coordinates, and message payloads.

What if we skip records and keep writing boilerplate carriers?

```java
final class Point {
    private final int x;
    private final int y;
    // constructor, getters, equals, hashCode, toString...
}
```

It works. It also drifts. Someone updates a field and forgets `equals`. Someone adds logging and skips `toString`. The record is not fashion. It is how Java makes the data-carrier intent explicit and keeps the mechanical contract in sync with the state declaration.


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

`Money` validates in a compact constructor. `PriceQuote` nests records without inventing getter ceremony. Logging prints meaningful text. Equality compares by value. If `Money` later needs rounding policies, tax rules, and mutable ledgers, promote it to a class — records are not a ban on classes, they are a better default for pure carriers.

So let's reconnect the chain. Boilerplate carriers created fatigue. Records answered with auto `equals` / `hashCode` / `toString` / accessors. Compact constructors handled validation. Sealed types and pattern matching hinted at the larger design. Ordinary classes remained for richer behavior. Shallow immutability and framework assumptions kept us honest.

Once data carriers are easy, another design question sharpens: sometimes a type should have only a known set of subtypes — not an open inheritance free-for-all. How do we say that in the language?

Teams adopting records often ask whether every DTO should convert overnight. Prefer opportunistic adoption: new carriers start as records; old classes convert when you touch them for a real reason — a bug in equals, a painful constructor, a serialization mismatch. The goal is clearer models, not a rewrite festival. Each record you add should make a boundary easier to read, not just shorter to type.

One more boundary case: serialization. A record's state is its components. That clarity helps many serializers, but it also means you should not hide derived fields as if they were part of the persisted shape. If a value is computed, compute it in a method; if it is part of the data, declare it as a component. Records reward honesty about what the data is.

That is Episode Nineteen — Sealed Classes.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 18 (*Records*).

Narration technique: boilerplate data-carrier problem → record as answer → compact constructor walkthrough → not every class → sealed/pattern pairing hint → shallow immutability → next natural problem (closed hierarchies / sealed). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Auto equals/hashCode/toString/accessors.
- Canonical and compact constructors.
- Great with sealed types and pattern matching.
- Not a replacement for every class.
- Implications for serialization and frameworks.
