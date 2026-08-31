# Episode 17 — Reflection

| Field | Value |
|---|---|
| Episode | 17 |
| Title | Reflection |
| Catalog handbook column | 17 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Annotations gave us metadata. Frameworks still need a way to discover that metadata — and the shapes of classes — while the program is running. Ordinary application code does not need that superpower every day. Frameworks do.

The temptation for beginners is to treat reflection as cleverness: look up a method by name, call it, feel powerful. The cost shows up months later when renames break production and nobody's IDE could see the string. Learn the mechanism so you can read framework code — then keep it out of your domain layer.

Imagine you are writing a tiny serializer. You do not want a handwritten method for every domain type. You want to ask an object: what fields do you have, what are their names, what values are inside? That question is reflection: inspect classes, methods, and fields at runtime, then optionally invoke or read them.

```java
Class<?> c = String.class;
var m = c.getMethod("length");
int n = (int) m.invoke("hi");
```

Walk the example slowly. `String.class` is a `Class` object — a runtime handle on the type. `getMethod("length")` looks up a public method by name and signature. `invoke("hi")` calls that method on the instance `"hi"` and returns the result. Nothing in this snippet names `length` as a normal Java call. The call path is data-driven. That is exactly how many frameworks wire controllers, inject dependencies, and map JSON: discover, then invoke.

So when is reflection justified? Frameworks, tools, serializers, debuggers — places where the set of types is not known when the library was compiled. In day-to-day domain code, prefer a direct call. Reflection is slower and more brittle than `"hi".length()`. Names become strings. Refactors break silently until runtime. The mechanism is powerful; casual use wrecks readability and performance.

Modules tighten the story further. The module system can restrict deep reflective access to internal packages. Code that once called `setAccessible(true)` on private fields may now fail unless the module `opens` that package. When a library breaks on a newer JDK with illegal reflective access errors, you are meeting this episode in production.

Because of cost and brittleness, prefer interfaces or codegen when possible. If you control both sides, a clear interface beats scanning private fields. If you need speed at scale, annotation processors and generated code often outperform repeated reflective lookup. When reflection is unavoidable, cache the `Method` and `Field` handles — looking them up on every request pays the search cost again and again.

What if we use reflection for ordinary business logic?

```java
Object result = order.getClass()
    .getMethod("total")
    .invoke(order);
```

It works until the method is renamed, overloaded, or moved. The compiler cannot protect you. That is the wrong trade for a total that could have been `order.total()`. Keep reflection at the edges — frameworks and tools — and keep domain code boring and direct.

Stretch the idea one step toward a framework-shaped helper: read a runtime annotation and call the method.

```java
for (var method : HelloController.class.getDeclaredMethods()) {
    Route route = method.getAnnotation(Route.class);
    if (route != null) {
        Object result = method.invoke(controller);
        System.out.println(route.path() + " => " + result);
    }
}
```

Here reflection and annotations cooperate. The controller methods stay ordinary Java. The routing table is discovered, not handwritten for every new endpoint. Discovery at the edge; direct calls in the domain.

If you remember only one design rule from this episode, make it this: reflection is for discovering what you could not know at compile time. If you already know the type, call it directly. If you need many types to share a behavior, give them an interface. If you need speed with discovery, generate the code once.

After living in that reflective, framework-heavy world, another fatigue appears: so many classes exist only to carry a few immutable fields, yet we still write constructors, accessors, `equals`, `hashCode`, and `toString` by hand. Is there a tighter way to model plain data?

That pressure opens records.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 17 (*Reflection*).

Narration technique: framework discovery need → reflection as answer → Class/Method/invoke walkthrough → when justified → cost/brittleness → modules → prefer interfaces/codegen → next natural problem (data carriers / records). Continuity-checked transitions.
