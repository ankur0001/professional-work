# Episode 14 — Wrappers and Autoboxing

| Field | Value |
|---|---|
| Episode | 14 |
| Title | Wrappers and Autoboxing |
| Catalog handbook column | 14 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Enums gave us type-safe vocabulary as objects. Now the language runs into a different friction: Java's collections and many APIs speak in objects, while everyday numbers still want to be primitives.

Imagine a shopping cart that stores item quantities. You reach for a list and try to think in `int` values. Conceptually and historically, a general list holds objects, not raw primitives. So the question becomes unavoidable: how does a primitive participate in an object world?

The answer is wrapper types. `Integer` wraps `int`. `Boolean` wraps `boolean`. `Double` wraps `double`. Each wrapper is a reference type that holds a primitive value and can sit in a collection, return from a generic method, or represent "maybe missing" with `null`. Wrappers let primitives participate in collections — with costs and NPE traps you must respect.

Java then softens the ceremony with autoboxing and unboxing. You can write code that looks like it mixes primitives and wrappers, and the compiler inserts the conversions.

```java
Integer a = 10;          // autobox int → Integer
int b = a;               // unbox Integer → int
List<Integer> list = new ArrayList<>();
list.add(b);             // autobox again when adding
```

Walk the lines like a slow debugger. `10` is an `int` literal; assigning it to `Integer a` boxes it into an object. Reading `a` into `int b` unboxes it. `list.add(b)` boxes again so the list can store an `Integer`. The convenience is real. The danger is that the conversions become invisible, so allocation costs and null failures become invisible too. Autoboxing is convenient and sneaky for exactly that reason.

Here is the failure that every Java developer meets eventually:

```java
Integer score = null;
int value = score;   // NullPointerException
```

Unboxing needs a real object. A null wrapper has nothing to unwrap. The line looks like a simple assignment. At runtime it is a crash. Prefer primitives when absence is not part of the meaning. If absence matters, keep the wrapper — and check it before you unbox. When does unboxing throw? Whenever the wrapper reference is null and a primitive is required.

Autoboxing has another subtle trap around identity. Small `Integer` values are cached. That means this can look "true" by accident:

```java
Integer x = 40;
Integer y = 40;
System.out.println(x == y);      // often true (cache)
Integer p = 400;
Integer q = 400;
System.out.println(p == q);      // often false
```

`==` on wrappers compares references, not numeric value. Inside the cache range, two boxed values may share an instance. Outside it, they usually do not. Use `equals` — or better, compare primitives — when you mean numeric equality. The cache is an optimization, not a contract you should design around. Identity comparisons on Integers are a classic interview and production foot-gun.

Once you see the conversions, performance questions follow. In a tight numeric loop, prefer primitives. Repeated boxing creates objects, pressure on the allocator, and noise in profiles. Wrappers are the right tool at API boundaries and in collections. They are the wrong default inside a hot sum of a million numbers.

```java
int total = 0;
for (int n : values) {
    total += n;   // stay primitive in the hot path
}
```

Using wrappers in tight numeric loops without measuring is how a simple total becomes a surprising GC story. Measure before you optimize — but do not start from the slow default when the meaning is clearly primitive.

What if we ignore wrappers and try to force everything through primitives at collection boundaries? We end up inventing parallel arrays, parallel lists of different lengths, or object bags with manual casts. Wrappers exist so primitives can cross into object APIs cleanly. Autoboxing exists so that crossing does not drown every call site in `Integer.valueOf`. The trade is that convenience can hide null and allocation.


Let's place the bridge inside a tiny cart that tallies quantities.

```java
List<Integer> quantities = new ArrayList<>();
quantities.add(2);      // autobox
quantities.add(5);
int units = 0;
for (Integer q : quantities) {
    units += q;         // unbox each time
}
```

The list cannot store bare `int` values; `Integer` is the ticket in. Each `add` boxes. Each turn of the loop unboxes into the `int` arithmetic. For a handful of line items this is fine. For a million sensor readings in a tight loop, the same pattern becomes a tax — which is why "prefer primitives in hot loops" is not purism, it is measuring where the wrapper stops earning its keep.

So let's reconnect the chain. Collections needed objects; wrappers answered. Autoboxing made the bridge quiet. Null unboxing and `==` on cached Integers showed the traps. Hot loops reminded us to prefer primitives where wrappers add no meaning.

And yet once lists of `Integer` feel natural, another problem shows up: a list that can hold anything forces casts and hides bugs until runtime. How do we tell a collection "these are strings" or "these are orders" and have the compiler enforce it?

One more practical habit: when an API returns `Integer` because the database column is nullable, do not silently assign it to `int` at the boundary. Decide what absence means — zero, a default, an error — and express that decision in code before arithmetic begins. Autoboxing will not make that decision for you. It will only crash later when null finally shows up on a path you forgot to test.

That is Episode Fifteen — Generics.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 14 (*Wrappers and Autoboxing*).

Narration technique: primitives-vs-collections friction → wrappers → autoboxing walkthrough → null unboxing → Integer cache/`==` → prefer primitives in hot loops → next natural problem (typed collections / generics). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- Integer/Boolean/etc. wrap primitives.
- Autoboxing/unboxing is convenient and sneaky.
- Cached small Integer values.
- Prefer primitives in hot loops.
- Null wrappers unbox into NPEs.
