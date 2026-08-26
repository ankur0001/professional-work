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
names.add(42);                     // compiles with raw types
String s = (String) names.get(1);  // ClassCastException at runtime
```

The cast is a confession. You are telling the compiler, "trust me." Runtime is where trust breaks. So the natural question is: can the collection itself remember what it holds, so the mistake dies at compile time?

That is what generics are for. A type parameter says what belongs inside. Generics move class-cast failures to compile time — if you learn the rules, including wildcards.

```java
List<String> names = new ArrayList<>();
names.add("Ada");
String s = names.get(0);
```

`List<String>` rejects `names.add(42)` before the program runs. `get` returns `String` without a cast. The type argument is part of the API contract, not a comment. Using raw types throws that safety away.

But there is a twist learners must hear early: type parameters erase at runtime. The compiler uses `<String>` for checking, then much of that detail is removed for the JVM's older object model. At runtime you largely see a list of objects with inserted checks. That is why you cannot write `List<int>` — no primitive type arguments — and why wrappers from the previous episode matter for `List<Integer>`. Erasure is the compatibility deal Java made.

Once you write APIs that accept or return collections of related types, wildcards appear. The mnemonic is PECS: producer extends, consumer super.

```java
void copyAll(List<? extends Number> source, List<? super Number> dest) {
    for (Number n : source) {
        dest.add(n);
    }
}
```

If a list produces values for you to read, `? extends Number` is safe — every element is some kind of `Number`. If a list consumes values you want to put in, `? super Number` is safe — it can accept a `Number`. Wrong wildcard bounds are not a style debate; they are a symptom of mixing "I need to read" with "I need to write."

Generic methods solve a related need: sometimes the type parameter belongs to the method, not the class.

```java
static <T> T first(List<T> items) {
    return items.get(0);
}

String name = first(List.of("Ada", "Grace"));
```

Here `<T>` is declared on the method. Call sites can pass a `List<String>` or a `List<Order>` and get the matching element type back. The compiler infers `T` from the argument.

What if we skip generics and live with raw types?

```java
List bag = new ArrayList();
bag.add("Ada");
bag.add(new Order());
```

It feels flexible. Then every read needs a cast, and unchecked warnings start lighting up. Those warnings are clues, not noise. An unchecked warning means the compiler lost the proof it normally gives you. Ignoring them is how ClassCastExceptions hide until a customer hits the bad path.

Let's make the generic contract visible in a small helper.

```java
class Box<T> {
    private T value;
    void set(T value) { this.value = value; }
    T get() { return value; }
}

Box<String> name = new Box<>();
name.set("Ada");
String s = name.get();
```

`Box<String>` and `Box<Integer>` share the same bytecode-shaped class after erasure, but at compile time they are different contracts. You cannot `set(42)` on `name`. That is the everyday value of generics: one implementation, many safe uses.

Untyped lists forced casts and late failures. Generics restored compile-time clarity. Erasure explained the runtime shape and the ban on primitive type arguments. PECS guided wildcards. Generic methods localized type parameters.

Notice how wrappers and generics cooperate in real APIs: `List<Integer>`, `Map<String, Double>`. The type parameter needs a reference type, so the previous episode's wrappers are how primitives enter generic APIs.

Now that types can carry parameters, another kind of metadata wants a home: not "what type is this list," but "this method overrides a parent," or "this field is injected," or "this test is disabled." How does Java attach structured notes that tools and frameworks can read?

That is the doorway into annotations.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 15 (*Generics*).

Narration technique: raw-list cast failure → generics as answer → erasure → PECS → generic methods → unchecked warnings → next natural problem (metadata / annotations). Continuity-checked transitions.
