# Episode 15 — Generics

| Field | Value |
|---|---|
| Episode | 15 |
| Title | Generics |
| Catalog handbook column | 15 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Wrappers let primitives enter object collections. That solves storage. It does not solve a different kind of lie: a collection that claims to hold "anything."

Picture an old-style list of names:

```java
List names = new ArrayList();
names.add("Ada");
names.add(42);                 // compiles with raw types
String s = (String) names.get(1);  // ClassCastException at runtime
```

The cast is a confession. You are telling the compiler, "trust me." Runtime is where trust breaks. So the natural question is: can the collection itself remember what it holds, so the mistake dies at compile time?

That is what generics are for. A type parameter says what belongs inside.

```java
List<String> names = new ArrayList<>();
names.add("Ada");
String s = names.get(0);
```

Walk through the win. `List<String>` rejects `names.add(42)` before the program runs. `get` returns `String` without a cast. The type argument is part of the API contract, not a comment. Generics move class-cast failures earlier — if you actually use them.

But there is a twist learners must hear early: type parameters erase at runtime. The compiler uses `<String>` for checking, then much of that detail is removed for the JVM's older object model. At runtime you largely see a list of objects with inserted checks. That is why you cannot write `List<int>` — no primitive type arguments — and why wrappers from the previous episode matter for `List<Integer>`. It is also why some reflective tricks and array creations around generics feel awkward. Erasure is the compatibility deal Java made.

Once you write APIs that accept or return collections of related types, wildcards appear. The mnemonic is PECS: producer extends, consumer super.

```java
void copyAll(List<? extends Number> source, List<? super Number> dest) {
    for (Number n : source) {
        dest.add(n);
    }
}
```

If a list produces values for you to read, `? extends Number` is safe — every element is some kind of `Number`. If a list consumes values you want to put in, `? super Number` is safe — it can accept a `Number`. Get the bound wrong and either `add` or `get` becomes confusing. Wrong wildcard bounds are not a style debate; they are a symptom of mixing "I need to read" with "I need to write."

Generic methods solve a related need: sometimes the type parameter belongs to the method, not the class.

```java
static <T> T first(List<T> items) {
    return items.get(0);
}
```

Here `<T>` is declared on the method. Call sites can pass a `List<String>` or a `List<Order>` and get the matching element type back. You are not forced to bake one type into a helper class.

What if we skip generics and live with raw types?

```java
List bag = new ArrayList();
bag.add("Ada");
bag.add(new Order());
```

It feels flexible. Then every read needs a cast, every cast is a possible incident, and unchecked warnings start lighting up. Those warnings are clues, not noise. An unchecked warning means the compiler lost the proof it normally gives you. Suppressing it without understanding is how ClassCastExceptions hide until a customer hits the bad path.

So let's reconnect the chain. Untyped lists forced casts and late failures. Generics restored compile-time clarity. Erasure explained the runtime shape and the ban on primitive type arguments. PECS guided wildcards for producers and consumers. Generic methods localized type parameters. Raw types and ignored warnings showed the old failure mode.

Now that types can carry parameters, another kind of metadata wants a home: not "what type is this list," but "this method overrides a parent," or "this field is injected," or "this test is disabled." How does Java attach structured notes that tools and frameworks can read?

That is Episode Sixteen — Annotations.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 15 (*Generics*).

Narration technique: raw-list cast failure → generics as answer → erasure reality → PECS wildcards → generic methods → unchecked warnings → next natural problem (metadata / annotations). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Type parameters erase at runtime.
- PECS: producer extends, consumer super.
- Generic methods.
- No primitive type arguments.
- Unchecked warnings are clues, not noise.
