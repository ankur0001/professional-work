# Episode 04 — Variables and Data Types

| Field | Value |
|---|---|
| Episode | 04 |
| Title | Variables and Data Types |
| Catalog handbook column | 4 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

In the previous episode, we gave a Java program a place to live: packages, classes, and `main`. That solves structure. It does not yet solve a more basic need.

Before our program can work with information, it needs somewhere to keep that information. Let's say we are building a student application and the first thing we need to know about a student is their age. We could simply write `25` in our program, but later we would have no idea what that number represents. Is it the student's age? Their marks? The number of subjects?

We need to give that value a meaningful identity. That is where a variable comes in. A variable allows us to give a name to a piece of information so that our program can remember it and work with it later.

So we might write:

```java
int age = 25;
```

Now the number `25` has meaning because we have associated it with the name `age`. But notice something else: we have also written `int`. Why do we need that?

Because Java needs to know what kind of information we are planning to store. Not every piece of information is a whole number. A student's name is text. A percentage might contain decimal values. Whether a student has passed can be true or false. So the question that follows naturally from naming a value is: what kind of value is this?

That question brings us to data types.

Variables give us a way to name and remember information. Data types tell Java what kind of information that variable represents. Together they turn a bare number into something the program — and the compiler — can reason about.

What if we tried to avoid types and stored everything as text?

```java
String ageText = "25";
String marksText = "91.5";
```

You can print those strings. But the moment you try to add marks, compare ages numerically, or enforce a rule like "age cannot be negative," the program has to guess what the text means. Java's type system moves those decisions earlier. The compiler helps catch whole classes of mistakes before the program runs. Types are not bureaucracy. They are a design tool.

Once you accept that types matter, another distinction appears quickly. Java does not treat every type the same way in memory. Some variables hold values directly. Others hold references to objects.

Primitives hold values directly. Familiar ones are `int`, `long`, `double`, `boolean`, and `char`. A primitive variable is never `null`. References point to objects on the heap — `String`, arrays, and later the classes you write. A reference can be `null`, which means it is not pointing at any object right now.

```java
int count = 10;
String name = "Ada";
boolean ready = true;
double percentage = 91.5;
```

Walk through what is happening. `count` remembers the integer ten as a value. `name` does not store every character inside the variable slot the way `count` stores ten; it stores a reference to a `String` object. `ready` and `percentage` are again primitive values, just of different kinds.

This raises a practical question: when we assign one variable to another, what exactly gets copied?

For primitives, assignment copies the value. For references, assignment copies the reference. Two reference variables can end up pointing at the same object. That single fact will matter enormously when we reach objects, equality, and collections. You do not need those chapters yet — you only need to feel why the family difference is not academic.

Let's put the student story back together in a small program, so the types have a reason to coexist.

```java
public class StudentReport {
    public static void main(String[] args) {
        String studentName = "Ada";
        int age = 20;
        double averageMarks = 91.5;
        boolean passed = averageMarks >= 40.0;

        System.out.println(studentName + " is " + age);
        System.out.println("Average: " + averageMarks);
        System.out.println("Passed: " + passed);
    }
}
```

Read it as one thought. We remember a name as text, an age as a whole number, an average as a decimal, and a pass/fail flag as a boolean. The expression `averageMarks >= 40.0` produces a boolean and stores it in `passed`. When the program runs, it prints labeled meaning instead of unexplained numbers. The types are guiding the design: age should not be a `String` if we want numeric comparison; marks that need a fractional part should not be forced into `int` without a reason; pass/fail is naturally boolean.

Now that the happy path feels clear, we should look at the places this idea bites beginners.

First, integer division:

```java
int a = 5;
int b = 2;
int result = a / b;   // 2, not 2.5
```

Both operands are `int`, so Java performs integer division and discards the fraction. The code compiles. That is what makes the bug sneaky. The type system did what you asked — not what you meant. If you needed `2.5`, a floating-point value had to participate in the computation.

Second, null references:

```java
String nickname = null;
System.out.println(nickname.length());   // NullPointerException
```

`nickname` is a reference. `null` means it currently points to no object. Asking for `.length()` requires an actual `String`. Primitives protect you from this particular failure — an `int` cannot be `null` — but that does not make primitives "always better." It means each family has different rules, and you must know which family you are using.

Modern Java also lets you write `var` for local variables when the initializer makes the type obvious:

```java
var total = 10 * 19.99;   // inferred as double
```

This is still static typing. The compiler figures out the type and then enforces it. `var` is not a door into a dynamically typed Java. It is a way to reduce repetition once the meaning is already clear.

So let's connect the chain. We started with a nameless `25` and asked what it meant. Naming gave us variables. Different kinds of information gave us data types. Memory behavior split types into primitives and references. A small student report showed the types cooperating. Integer division and null showed the failure modes that make the rules worth respecting.

Once we can remember values, the next natural pressure appears: we need to combine them, compare them, and make decisions with them. A single character — `=` versus `==`, `/` between ints versus doubles — can change the meaning of a whole expression.

That pressure is exactly why operators come next — the symbols that combine, compare, and decide.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 4 (*Variables and Data Types*).

Narration technique: situation → nameless value problem → variable as answer → “why `int`?” → data types → what-if untyped text → primitives vs references → student program → failure modes → next natural problem (operators). Continuity-checked transitions.
