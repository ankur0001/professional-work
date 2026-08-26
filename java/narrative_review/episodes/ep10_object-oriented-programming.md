# Episode 10 — Object-Oriented Programming

| Field | Value |
|---|---|
| Episode | 10 |
| Title | Object-Oriented Programming |
| Catalog handbook column | 10 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We can store values, operate on them, choose paths, name behavior with methods, hold lists in arrays, and work with text. For a while, that is enough — until the same cluster of fields keeps appearing together, and the rules about those fields are scattered across every method that touches them.

Imagine a user id that must never be blank, a balance that must never go negative, an order that must keep its line items consistent. If those values live as public fields floating beside unrelated helpers, any line of code can break the rules. You end up with comments that say "do not set this directly" — which is another way of admitting the language is not helping you.

So a natural question appears: can related data and the behavior that protects it travel as one unit?

That question is what object-oriented programming answers in Java — as a modeling tool, not a religion. You do not need an inheritance diagram for a twenty-line script. You do need a way to stop illegal states from becoming normal. Start with encapsulation: hide the representation, expose a controlled surface, protect invariants.

```java
class User {
    private final String id;

    User(String id) {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("id required");
        }
        this.id = id;
    }

    String id() {
        return id;
    }
}
```

The field is private. Construction validates. Callers can read the id through a method, but they cannot assign `user.id = ""` from outside. Encapsulation is not a checkbox labeled "I used a class." It is a boundary that keeps illegal states harder to create.

Contrast that with the scattered version everyone writes first: a string `id` in `main`, a helper that assumes it is non-blank, another helper that forgets to check. The rules exist only as hope. An object gathers the noun and the verbs that protect it.

Once you have objects, reuse becomes the next temptation. Inheritance looks like the fastest reuse: a subclass "is a" kind of parent and picks up its fields and methods. The cost is coupling. Changes in the parent ripple through every child. Deep inheritance trees feel clever on a whiteboard and brittle in a year-old codebase. Composition — "has a" collaborator you call — often evolves more safely.

```java
class OrderService {
    private final Pricing pricing;

    OrderService(Pricing pricing) {
        this.pricing = pricing;
    }

    double total(Cart cart) {
        return pricing.price(cart);
    }
}
```

`OrderService` is not a subclass of `Pricing`. It holds a `Pricing` and uses it. You can swap pricing strategies without rewriting the service's type hierarchy. Prefer inheritance when you truly have a stable subtype relationship and polymorphism needs a shared type. Prefer composition when you mainly wanted reuse. A deep tree that exists only to share three utility methods is usually a composition opportunity wearing an inheritance costume.

Polymorphism is the payoff that makes abstractions worth depending on. Callers program to a general type; runtime chooses the specific behavior. Without that, every new channel forces edits through every `welcome` call site — the same duplication methods already taught us to hate, now at the type level.

```java
interface Notifier {
    void send(String message);
}

class EmailNotifier implements Notifier {
    public void send(String message) { /* email */ }
}

class SmsNotifier implements Notifier {
    public void send(String message) { /* sms */ }
}

void welcome(Notifier notifier) {
    notifier.send("Welcome");
}
```

`welcome` does not care which notifier arrived. It depends on the abstraction. New channels can appear without rewriting every caller. That is polymorphism earning its keep.

Two words collide for beginners: overriding and overloading. Overloading is same name, different parameter lists, resolved at compile time — we met that with methods. Overriding is a subclass replacing a superclass method with the same signature, resolved at runtime for instance methods. If you "override" with a different parameter list, you actually overloaded — and the parent method still runs when callers use the parent type. Mixing the terms in an interview usually means mixing the mechanisms in code.

Finally, once objects live in sets and maps, identity and equality stop being philosophy. `equals` and `hashCode` are part of the object contract. If two objects are equal, their hash codes must match. Break that pair and collections misbehave in ways that look like ghost bugs.

```java
// If you override equals, override hashCode in tandem.
// Equal users must hash equally or HashSet/HashMap will surprise you.
```

You will deepen this when collections take center stage. For now, treat equality as part of the type's meaning, not an afterthought you paste from a generator without reading. If two `User` objects with the same id should be interchangeable in a `HashSet`, the type must say so consistently.

What if we skip the modeling discipline? Public fields everywhere, god classes that know every feature, inheritance used as a junk drawer — the program still runs until change arrives. Then every feature touches everything, and invariants live only in tribal memory. OOP did not fail. Design refused to use the tools for their purpose.

So reconnect the chain. Scattered data needed a boundary; encapsulation provided one. Reuse needed a safer default than deep trees; composition often wins. Callers needed stability; polymorphism provided abstractions. Overriding and overloading needed clear separation. Equality needed a contract. OOP is how Java lets you model those pressures — not a requirement to turn every script into a framework.

As soon as classes have insides and outsides, a sharper question appears: who is allowed to see the private field, call the helper, or extend the hook? Without language-level permissions, encapsulation is only a polite agreement.

That vocabulary is Episode Eleven: access modifiers.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 10 (*Object-Oriented Programming*).

Narration technique: scattered-fields situation → encapsulation → inheritance vs composition → polymorphism → overriding vs overloading → equals/hashCode → failure modes → next natural problem (who may touch what). Continuity-checked transitions.
