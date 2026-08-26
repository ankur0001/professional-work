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

The cast is a confession. You are telling the compiler, "trust me." Runtime is where trust breaks. A list that can hold anything forces casts and hides bugs. So the natural question is: can the collection itself remember what it holds, so the mistake dies at compile time?

That is what generics are for. A type parameter says what belongs inside. Generics move class-cast failures to compile time — if you learn the rules, including wildcards.

```java
List<String> names = new ArrayList<>();
names.add("Ada");
String s = names.get(0);
```

Walk through the win. `List<String>` rejects `names.add(42)` before the program runs. `get` returns `String` without a cast. The type argument is part of the API contract, not a comment. Using raw types throws that safety away and brings the warnings back.

But there is a twist learners must hear early: type parameters erase at runtime. The compiler uses `<String>` for checking, then much of that detail is removed for the JVM's older object model. At runtime you largely see a list of objects with inserted checks. What is type erasure? Generic type arguments are removed at compile time; the runtime sees raw-ish shapes with the checks the compiler inserted. That is why you cannot write `List<int>` — no primitive type arguments — and why wrappers from the previous episode matter for `List<Integer>`. It is also why some reflective tricks and generic array creations feel awkward. Erasure is the compatibility deal Java made.

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

String name = first(List.of("Ada", "Grace"));
```

Here `<T>` is declared on the method. Call sites can pass a `List<String>` or a `List<Order>` and get the matching element type back. You are not forced to bake one type into a helper class. The compiler infers `T` from the argument.

What if we skip generics and live with raw types?

```java
List bag = new ArrayList();
bag.add("Ada");
bag.add(new Order());
```

It feels flexible. Then every read needs a cast, every cast is a possible incident, and unchecked warnings start lighting up. Those warnings are clues, not noise. An unchecked warning means the compiler lost the proof it normally gives you. Ignoring unchecked warnings is how ClassCastExceptions hide until a customer hits the bad path. Suppressing without understanding trades a yellow underline for a production pager.


Let's make the generic contract visible in a small repository-shaped helper.

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

`Box<String>` and `Box<Integer>` share the same bytecode-shaped class after erasure, but at compile time they are different contracts. You cannot `set(42)` on `name`. That is the everyday value of generics: one implementation, many safe uses. When someone hands you a raw `Box`, you have stepped outside that contract — and the unchecked warnings are the compiler saying so.

So let's reconnect the chain. Untyped lists forced casts and late failures. Generics restored compile-time clarity. Erasure explained the runtime shape and the ban on primitive type arguments. PECS guided wildcards for producers and consumers. Generic methods localized type parameters. Raw types and ignored warnings showed the old failure mode.

Now that types can carry parameters, another kind of metadata wants a home: not "what type is this list," but "this method overrides a parent," or "this field is injected," or "this test is disabled." How does Java attach structured notes that tools and frameworks can read?

A useful mental check when you read unfamiliar generic code: ask whether each type parameter is there to protect callers, to protect the implementation, or both. If you cannot answer, the API may be over-parameterized. Generics are a clarity tool. When they make signatures harder to say out loud than the problem they solve, simplify. And when the compiler emits an unchecked warning, treat it like a failing test you have not written yet — understand the hole before you silence it.

Before we leave, notice how wrappers and generics cooperate in real APIs: `List<Integer>`, `Map<String, Double>`, `Optional<Boolean>`. The type parameter needs a reference type, so the previous episode's wrappers are not trivia — they are how primitives enter generic APIs. Erasure does not make that pairing optional; it makes it mandatory.

That is Episode Sixteen — Annotations.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 15 (*Generics*).

Narration technique: raw-list cast failure → generics as answer → erasure → PECS → generic methods → unchecked warnings → next natural problem (metadata / annotations). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Type parameters erase at runtime.
- PECS: producer extends, consumer super.
- Generic methods.
- No primitive type arguments.
- Unchecked warnings are clues, not noise.
