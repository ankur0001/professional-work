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

Suppose you override `toString` on a domain class. You type carefully… and misspell the method as `tostring`. Without help, Java treats that as a brand-new method. Your override never runs. Logging still shows the useless default. The compiler did not fail you; it simply never knew you meant to override.

So the question appears: can we declare intent so the compiler verifies it?

Annotations are structured metadata attached to declarations. Compilers, build tools, and frameworks listen to them. Think of an annotation as a structured sticky note: humans can read it, but more importantly, programs can read it without parsing comments.

```java
@Override
public String toString() {
    return "ok";
}
```

`@Override` is the smallest useful illustration. It does not change runtime behavior by itself. It tells the compiler: this method must match a superclass or interface method. If the signature is wrong, compilation fails. Put `@Override` on every method you believe is an override. Let the compiler argue with you early.

Once you accept that metadata can drive tools, retention becomes the next natural question. How long does the annotation live?

Java defines three retentions. `SOURCE` means the annotation helps during compilation and may disappear afterward. `CLASS` means it is recorded in the class file but not necessarily visible through normal reflection. `RUNTIME` means the annotation remains available while the program runs, so frameworks can read it with reflection. Assuming all annotations exist at runtime is a common misunderstanding; check `@Retention` before you blame the framework.

That runtime case is why annotations feel ubiquitous in modern Java. Dependency injection, web mappings, test runners, and serializers lean on runtime annotations. A method marked for a request path, a field marked for injection, a test marked to ignore — the framework scans, reads the metadata, and wires behavior.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Route {
    String path();
}

public class HelloController {
    @Route(path = "/hello")
    public String hello() {
        return "hi";
    }
}
```

A custom annotation like `@Route` does nothing alone. Custom annotations need processors at build time, or reflection at runtime, to mean anything. Writing `@Route` without a reader is like writing a sticky note and never looking at it.

What if we over-annotate instead of simplifying design?

Teams sometimes decorate every class with a forest of markers while the underlying API stays confused. Annotations do not replace good API design. They amplify a design that already makes sense, and they can obscure one that does not. Prefer a clear method and a clear type. Then add the annotation that tools need.

Now watch how a test runner might use the same idea:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Test { }

public class MathTest {
    @Test
    public void adds() {
        if (1 + 1 != 2) throw new AssertionError();
    }
}
```

A tiny runner would scan `MathTest`, keep methods annotated with `@Test`, and invoke them. Without `@Retention(RUNTIME)`, reflective lookup finds nothing and the suite looks empty for mysterious reasons. The annotation is a signal — the design still has to be worth signaling.

A missed override showed why intent needs verification. `@Override` answered with compiler-checked metadata. Retention explained how long that metadata survives. Frameworks showed why runtime annotations dominate application architecture. Custom annotations revealed they need processors or reflection.

A final check when you invent a custom annotation: name the consumer in the same pull request. If nobody reads it — no processor, no reflective scanner, no compiler plugin — delete it. Dead metadata is worse than no metadata because it teaches the team that annotations are decorative.

And if frameworks read annotations at runtime by inspecting classes and methods, how does that inspection work? What API lets a program look at itself?

That curiosity is reflection.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 16 (*Annotations*).

Narration technique: missed-override situation → annotation as answer → @Override → retention → framework runtime use → custom annotations need consumers → design caution → next natural problem (reflection). Continuity-checked transitions.
