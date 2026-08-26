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

The answer is wrapper types. `Integer` wraps `int`. `Boolean` wraps `boolean`. `Double` wraps `double`. Each wrapper is a reference type that holds a primitive value and can sit in a collection, return from a generic method, or represent "maybe missing" with `null`.

Java then softens the ceremony with autoboxing and unboxing. You can write code that looks like it mixes primitives and wrappers, and the compiler inserts the conversions.

```java
Integer a = 10;          // autobox int → Integer
int b = a;               // unbox Integer → int
List<Integer> list = new ArrayList<>();
list.add(b);             // autobox again when adding
```

Walk the lines like a slow debugger. `10` is an `int` literal; assigning it to `Integer a` boxes it into an object. Reading `a` into `int b` unboxes it. `list.add(b)` boxes again so the list can store an `Integer`. The convenience is real. The danger is that the conversions become invisible, so allocation costs and null failures become invisible too.

Here is the failure that every Java developer meets eventually:

```java
Integer score = null;
int value = score;   // NullPointerException
```

Unboxing needs a real object. A null wrapper has nothing to unwrap. Prefer primitives when absence is not part of the meaning. If absence matters, keep the wrapper — and check it before you unbox.

Autoboxing has another subtle trap around identity. Small `Integer` values are cached:

```java
Integer x = 40;
Integer y = 40;
System.out.println(x == y);      // often true (cache)
Integer p = 400;
Integer q = 400;
System.out.println(p == q);      // often false
```

`==` on wrappers compares references, not numeric value. Inside the cache range, two boxed values may share an instance. Outside it, they usually do not. Use `equals` — or better, compare primitives — when you mean numeric equality. The cache is an optimization, not a contract you should design around.

Once you see the conversions, performance questions follow. In a tight numeric loop, prefer primitives. Repeated boxing creates objects and pressure on the allocator. Wrappers are the right tool at API boundaries and in collections. They are the wrong default inside a hot sum of a million numbers.

```java
int total = 0;
for (int n : values) {
    total += n;   // stay primitive in the hot path
}
```

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

The list cannot store bare `int` values; `Integer` is the ticket in. For a handful of line items this is fine. For a million sensor readings in a tight loop, the same pattern becomes a tax.

Collections needed objects; wrappers answered. Autoboxing made the bridge quiet. Null unboxing and `==` on cached Integers showed the traps. Hot loops reminded us to prefer primitives where wrappers add no meaning.

And yet once lists of `Integer` feel natural, another problem shows up: a list that can hold anything forces casts and hides bugs until runtime. How do we tell a collection "these are strings" or "these are orders" and have the compiler enforce it?

One practical habit: when an API returns `Integer` because the database column is nullable, do not silently assign it to `int` at the boundary. Decide what absence means — zero, a default, an error — and express that decision before arithmetic begins.

That is the pressure that brings generics.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 14 (*Wrappers and Autoboxing*).

Narration technique: primitives-vs-collections friction → wrappers → autoboxing walkthrough → null unboxing → Integer cache/`==` → prefer primitives in hot loops → next natural problem (typed collections / generics). Continuity-checked transitions.
