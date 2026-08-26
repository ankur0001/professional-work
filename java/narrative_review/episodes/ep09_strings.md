# Episode 09 — Strings

| Field | Value |
|---|---|
| Episode | 09 |
| Title | Strings |
| Catalog handbook column | 9 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Arrays gave us a way to hold many values by position. That helps for scores and samples. Most applications, though, spend at least as much energy on text: a customer name, a log line, an order id, a JSON body. If arrays are shelves for numbers, strings are the language the rest of the system speaks — and language has rules.

Text feels simple until you try to change it, compare it, or move it across a network boundary. So start from a small action that looks harmless. You have a greeting and you want to add emphasis.

```java
String a = "hi";
String b = a + "!";
```

`a` still refers to `"hi"`. `b` refers to a new string `"hi!"`. Nothing edited the original characters in place. In Java, `String` is immutable. Concatenation does not mutate; it creates another object. That design buys safer sharing, simpler reasoning about aliases, and reliable behavior when strings are used as map keys — at the cost of allocating when you keep building new text.

Why bake immutability into the type everyone uses? Because text crosses trust boundaries constantly — path names, class names, passwords in older APIs, cache keys. If any caller could silently change the characters underneath a shared reference, security and hashing would become nightmares. Immutability is not purity theater. It is a trade: more objects sometimes, fewer alias surprises often. Once you accept that trade, a lot of "why can't I change this string in place?" frustration turns into a design feature.

Immutability raises a practical question the first time you build a result in a loop: if every `+` can mean a new object, what do you do when you append hundreds of pieces?

Use `StringBuilder` for repeated appends.

```java
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 100; i++) {
    sb.append(i);
}
String result = sb.toString();
```

The builder holds a mutable buffer. Each `append` changes that buffer instead of inventing a brand-new `String` for every step. At the end, `toString()` gives you an immutable string to share. Building with `+` inside a tight loop is attractive because it looks short. The cost shows up as needless allocation and slower code when the loop is hot.

A single `+` in ordinary code is fine — `"Hello, " + name` is readable and clear. The rule of thumb is about repetition under load, not about fear of every plus sign. If a profiler never sees the loop, clarity wins; if the loop is hot, the builder earns its keep.

Comparison is the next place strings surprise people — and it connects straight back to operators and references.

```java
String x = new String("ada");
String y = new String("ada");
System.out.println(x == y);       // false — identity
System.out.println(x.equals(y));  // true  — content
```

`==` asks whether two references point at the same object. `equals` asks whether the character content matches. Literal pooling can make `==` look correct in a tiny demo and then fail when the same letters arrive from a file, a scanner, or a constructor. When you mean content, call `equals`. When you mean identity, keep `==` and know why. Null-safe comparison also matters: `Objects.equals(a, b)` or putting the literal first in `"ada".equals(x)` avoids calling equals on a null reference.

What about longer text — SQL, HTML snippets, sample payloads — where quote-escaped one-liners become unreadable?

Text blocks give you multiline string literals without drowning in `\n` noise.

```java
String query = """
        SELECT id, name
        FROM students
        WHERE passed = true
        """;
```

The content can span lines. Indentation rules strip a shared indent so the string is not polluted by how far you indented the code. Use text blocks when the text itself is multiline. Keep ordinary quotes for short values. Mixing styles randomly in one class makes reviews harder than the feature deserves.

One more boundary problem appears the moment strings leave the comfortable world of Java characters and meet bytes — files, sockets, HTTP bodies. Encoding mistakes are silent until a name with an accent turns into garbage or a checksum stops matching.

```java
byte[] bytes = name.getBytes(java.nio.charset.StandardCharsets.UTF_8);
String again = new String(bytes, java.nio.charset.StandardCharsets.UTF_8);
```

Always be explicit at the boundary. "The platform default charset" is not a team agreement; it is a future incident. You do not need the full I/O chapter yet. You only need the habit: text and bytes are different, and the mapping between them has a name.

What if we ignore these rules? A loop that builds CSV with `+`, a login check that uses `==`, a file reader that assumes the default charset — each one works in a demo and fails under slightly wider reality. Strings look simple because the type is everywhere. The discipline exists because the type is everywhere.

So reconnect the chain. Arrays handled positional values. Strings handle text with an immutability rule that reshapes how you concatenate. `StringBuilder` absorbs repeated appends. `equals` compares content; `==` compares identity. Text blocks serve multiline literals. Charset discipline protects the edges of the system.

Once text, numbers, and methods are comfortable, another modeling pressure appears. A student is not only a name string and an age int living as loose locals in `main`. The data and the rules that protect it want to travel together as one idea — create a student, keep the id valid, refuse impossible states.

That pressure opens Episode Ten: object-oriented programming.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 9 (*Strings*).

Narration technique: text-everywhere situation → immutability and concatenation → StringBuilder → equals vs == → text blocks → charset boundaries → next natural problem (bundling data + behavior / OOP). Continuity-checked transitions.
