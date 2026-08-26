# Episode 11 — Access Modifiers

| Field | Value |
|---|---|
| Episode | 11 |
| Title | Access Modifiers |
| Catalog handbook column | 11 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Ten put data and behavior inside classes and drew a boundary with encapsulation. That boundary only works if the language can enforce who may cross it. Otherwise `private` is a comment, and every teammate can reach into the wiring "just for now."

Imagine you finish a `BankAccount` with a careful withdraw method. A colleague adds `account.balance -= 50` from a UI class because the field was left public. Your invariant — never go below zero without a check — evaporates. The bug is not cleverness. It is missing permission language.

So the natural question is: what vocabulary does Java give us for "allowed to touch"?

Access modifiers answer that. They are API design in miniature — rules about visibility for types and members.

Java's everyday ladder has four rungs: `private`, package-private (no modifier), `protected`, and `public`.

```java
public class Api {
    private int secret;
    void pack() { }           // package-private
    protected void hook() { }
    public void open() { }
}
```

Walk each choice as a decision, not a label. `secret` is `private`: only code inside `Api` should see it. `pack` has no modifier: it is package-private, visible to other classes in the same package, hidden from the outside world. `hook` is `protected`: same package, plus subclasses — including subclasses that live in other packages, with cross-package rules that surprise people who thought protected meant "only children." `open` is `public`: part of the advertised surface.

Think of shipping a library jar to another team. Everything you mark `public` becomes a promise. Rename it later and you break callers you do not control. Package-private and private keep room to refactor. That is why "default to the tightest access that works" shows up in reviews: widen on purpose, not by habit.

Encapsulation is a boundary, not a checkbox. Marking a field `private` and then returning the mutable list inside it from a public method still leaks the inside. Access modifiers constrain names. They do not automatically constrain the objects those names hand out.

```java
public class Team {
    private final java.util.List<String> members = new java.util.ArrayList<>();

    public java.util.List<String> members() {
        return members;   // leak — callers can mutate internals
    }
}
```

A safer return might be an unmodifiable view or a defensive copy. The modifier on the field did its job. The method signature undid the boundary. That is why tight access and careful returns travel together. Start narrow. Widen only when a real caller outside the boundary needs the name.

Another quiet leak: a public method that accepts or returns a mutable array the class still keeps. Callers can rewrite slots. The field looked private. The API still handed out the keys.

`protected` deserves an extra beat because it is the most misunderstood middle ground.

```java
// package com.shop.core
public class Account {
    protected void audit(String event) { /* ... */ }
}

// package com.shop.web — subclass in another package
public class WebAccount extends Account {
    void onLogin() {
        audit("login");   // allowed via subclass access
    }
}
```

Subclass access across packages is intentional for frameworks and extension hooks. It is also easy to overuse. If everything interesting is `protected`, you have built an inheritance API whether you meant to or not. People also confuse protected with package-private: package-private never opens the door to a subclass in another package; protected can. Prefer `private` or package-private until a genuine extension point appears.

Modern Java adds another tightening layer: modules. The module system can hide packages from code outside the module even if a type is `public`. Think of modifiers as the first wall and modules as a second wall for larger codebases. You do not need to master `module-info` today. You only need to know that "public" does not always mean "visible to the entire universe forever." Reflection and tests sometimes punch holes on purpose; treat those as deliberate exceptions, not reasons to leave production fields public.

What if we skip the discipline and make everything `public` so demos compile faster? The cost arrives when internals become de facto API. Callers depend on fields you wanted to rename. Tests couple to helpers you wanted to delete. Refactors turn into negotiations. Access that is wider than necessary is debt with compound interest.

Confusing protected with package-private, or leaking mutable internals from public getters, are the same story in different clothes: the modifier on the declaration did not match the boundary you actually needed.

So reconnect the chain. OOP introduced insides and outsides. Access modifiers name who may cross. Private for implementation, package-private for collaborating types in one package, protected for deliberate subclass hooks, public for the supported surface. Boundaries must hold through what methods return. Modules can tighten further. Default tight; widen on purpose.

Once visibility rules exist, another organizational pressure grows with the codebase itself. Class names collide. Folders drift from declarations. Collaborating types need a shared neighborhood so package-private access means something real — not "whatever happens to sit nearby." The project needs geography.

That geography is Episode Twelve: packages.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 11 (*Access Modifiers*).

Narration technique: encapsulation-needs-enforcement situation → four access levels → boundary vs checkbox / leaking internals → protected across packages → modules → public-everywhere failure → next natural problem (packages as geography). Continuity-checked transitions.
