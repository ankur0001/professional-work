# Episode 16 — Annotations

| Field | Value |
|---|---|
| Episode | 16 |
| Title | Annotations |
| Catalog handbook column | 16 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Generics taught the compiler what a collection holds. Sometimes what we need to say is not a type parameter, but a note about intent — a note that another tool should notice.

Suppose you override `toString` on a domain class. You type carefully… and misspell the method as `tostring`. Without help, Java treats that as a brand-new method. Your override never runs. Equality debugging becomes mysterious. The compiler did not fail you; it simply never knew you meant to override.

So the question appears: can we declare intent so the compiler verifies it?

That is the doorway into annotations. Annotations are structured metadata attached to declarations. Compilers, build tools, and frameworks listen to them.

```java
@Override
public String toString() {
    return "ok";
}
```

`@Override` is the smallest useful illustration. It does not change runtime behavior by itself. It tells the compiler: this method must match a superclass or interface method. If the signature is wrong, compilation fails. That is what `@Override` buys you — compile-time proof you actually overrode something. Typos in method names without `@Override` are the classic opposite: silent wrong methods that look fine until behavior diverges.

Once you accept that metadata can drive tools, retention becomes the next natural question. How long does the annotation live?

Java defines three retentions. `SOURCE` means the annotation helps during compilation and may disappear afterward — useful for things only the compiler or an annotation processor needs. `CLASS` means it is recorded in the class file but not necessarily visible through normal reflection. `RUNTIME` means the annotation remains available while the program runs, so frameworks can read it with reflection.

That last case is why annotations feel ubiquitous in modern Java. Dependency injection, web mappings, test runners, and serializers lean on runtime annotations. A method marked for a request path, a field marked for injection, a test marked to ignore — the framework scans, reads the metadata, and wires behavior. The annotation is the hook; the framework is the listener.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Route {
    String path();
}
```

A custom annotation like this does nothing alone. Custom annotations need processors at build time, or reflection at runtime, to mean anything. Writing `@Route` without a reader is like writing a sticky note and never looking at it. The metadata model is powerful precisely because something else consumes it.

What if we over-annotate instead of simplifying design?

Teams sometimes decorate every class with a forest of markers while the underlying API stays confused. Annotations do not replace good API design. They amplify a design that already makes sense, and they can obscure one that does not. Prefer a clear method and a clear type. Then add the annotation that tools need — not the annotation that makes the file look "framework native."

Another misunderstanding: assuming every annotation exists at runtime. If retention is `SOURCE` or `CLASS`, reflective lookup may find nothing. When a framework "ignores" your annotation, check retention and target before rewriting the business logic.

So let's reconnect the chain. A missed override showed why intent needs verification. `@Override` answered with compiler-checked metadata. Retention explained how long that metadata survives. Frameworks showed why runtime annotations dominate application architecture. Custom annotations revealed they need processors or reflection. Over-annotating reminded us that metadata is not architecture.

And if frameworks read annotations at runtime by inspecting classes and methods, how does that inspection work? What API lets a program look at itself?

That curiosity is Episode Seventeen — Reflection.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 16 (*Annotations*).

Narration technique: missed-override situation → annotation as answer → @Override walkthrough → retention policies → framework runtime use → custom annotations need consumers → design caution → next natural problem (reflection). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- @Override catches signature mistakes.
- Retention: SOURCE/CLASS/RUNTIME.
- Frameworks use runtime annotations heavily.
- Custom annotations need processors or reflection.
- Annotations don't replace good API design.
