# Episode 05 — Operators

| Field | Value |
|---|---|
| Episode | 05 |
| Title | Operators |
| Catalog handbook column | 5 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

In the previous episode we learned how to remember values with types. A student can have an age, a name, a percentage, a pass flag. That solves storage. It does not yet solve work.

Suppose the gradebook already holds `marks` and `passingScore`. We need to know whether the student passed, compute a weighted total, maybe bump a counter. We are no longer asking "what is this value?" We are asking "what do we do with these values together?"

That is where operators arrive. An operator is a compact way to combine, compare, or transform values. The danger is not that operators are hard to spell. The danger is that a single character can change the meaning of a whole expression — and the code can still compile.

Before lists of symbols, learn the rules that actually decide outcomes: precedence and associativity. Precedence answers which operator binds first. Associativity answers how equal-precedence operators group when they sit side by side. Memorizing every trivia table is less useful than knowing when to add parentheses because the default reading is not the reading you meant.

```java
int total = 10 + 2 * 5;      // 20, not 60
boolean inRange = x >= 0 && x < 100;
```

`10 + 2 * 5` is twenty because multiplication binds tighter than addition. If you wanted sixty, you needed parentheses. `x >= 0 && x < 100` is a common range check; the comparisons happen, then `&&` combines the booleans. Parentheses are how you document intent for the next reader, including future you.

Assignment versus equality is another one-character fork. `=` stores. `==` compares. Mixing them in a condition is rarer in modern Java than in C — but the mental mix-up still shows up when people read code aloud and say "equals" for both.

Once arithmetic and comparison feel familiar, side effects show up — especially `++` and `--`.

```java
int x = 5;
int y = x++ + ++x;
```

Walk it carefully. `x++` yields the current value of `x`, then increments. `++x` increments first, then yields the new value. Starting at five, the left side contributes five and leaves `x` at six; the right side bumps `x` to seven and contributes seven; `y` becomes twelve. The expression is legal. It is also a terrible place to hide business logic. Prefer clarity over clever increments.

Another operator trap looks quieter: boolean operators that short-circuit versus ones that do not.

`&&` stops early. If the left side is false, the right side never runs. `&` on booleans evaluates both sides. That difference matters when the right side has a cost — or a crash.

```java
String name = null;
boolean bad = (name != null) & name.length() > 0;   // NPE
boolean ok  = (name != null) && name.length() > 0;  // safe
```

With `&`, both sides run, so `name.length()` executes even when `name` is null. With `&&`, the null check protects the second call. The same short-circuit idea applies to `||`: if the left side is already true, the right side is skipped.

Then comes the comparison question that follows from Episode Four's primitive-versus-reference split: when you write `==`, what are you comparing?

For primitives, `==` compares values. For objects, `==` compares identity — whether two references point at the same object. Content equality usually means `equals`.

```java
String a = new String("hi");
String b = new String("hi");
System.out.println(a == b);        // false — different objects
System.out.println(a.equals(b));   // true  — same characters
```

If you accidentally use `==` for string content, you may get true in a demo because of interning, then false in production when the strings were built differently. Prefer `equals` when you mean content. Save `==` for identity, null checks, and enums where identity is the point.

You can recite an operator table and still ship a bug the first time precedence, short-circuiting, and `==` collide in one condition. The durable skill is slower: read an expression the way the compiler does, then rewrite it until a human can too.

(Bitwise operators — masks and packed flags — exist for another job entirely. You will meet them when a problem actually needs bits. Today, do not confuse them with boolean `&&` and `||`.)

Variables gave us named values. Operators let us compute and decide with those values. But once you can produce a boolean, a new pressure appears. Knowing that `passed` is true is not enough. The program must take different paths — print a pass message, retry a download, loop through every student. Computation alone does not choose a route.

That pressure is what control flow exists to answer.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 5 (*Operators*).

Narration technique: stored-values-need-work situation → operators as answer → precedence → increment side effects → short-circuit → == vs equals → bitwise deferred → next natural problem (choosing paths). Continuity-checked transitions.
