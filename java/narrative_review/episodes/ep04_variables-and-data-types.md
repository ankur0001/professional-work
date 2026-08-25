# Episode 04 — Variables and Data Types

| Field | Value |
|---|---|
| Episode | 04 |
| Title | Variables and Data Types |
| Catalog handbook column | 4 |
| Narration source script | Descriptive instructor narration (4–15 min) |
| Spoken form | Connected explanatory prose with walked-through examples |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

### Opening — why programs need memory with meaning

In the previous episode, we looked at how a Java program is structured: packages, classes, and `main`. That gives us a place for code to live. But a program that cannot remember information cannot do useful work.

Before our program can work with information, it needs a way to remember that information. Imagine that we are building a simple application for a school. The application needs to keep track of a student's age. We could simply write the number `20` somewhere in our code, but that number by itself does not tell us much. Is it an age? A mark? A number of subjects?

What we really need is a name that gives meaning to the value. We can call that piece of information `age`. In Java, we do this by creating a **variable**.

### Example 1 — a simple variable

```java
int age = 20;
```

Here, `age` is the name of the variable and `20` is the value we are storing. The word `int` tells Java what kind of value this variable is expected to hold.

This immediately raises another question: why does Java need us to specify the type? Because not every piece of information is a whole number. A student's name is text, a percentage might contain decimal values, and whether a student has passed can be represented as true or false. Java uses **data types** to distinguish these different kinds of values.

So, variables give us a way to **name and remember information**, while data types tell Java **what kind of information that variable represents**.

### Why types exist — what if everything were untyped text?

What if we stored everything as text and hoped for the best?

```java
String ageText = "20";
String marksText = "91.5";
```

You can print those strings. But the moment you try to do arithmetic, sort numerically, or enforce rules like "age cannot be negative," the program has to guess what the text means. Java's type system moves those decisions earlier: the compiler helps catch whole classes of mistakes before the program runs.

That is why types are not bureaucracy. They are a design tool.

### Two families of types: primitives and references

Java splits types into two families. Keep this picture in your head for the rest of the series.

**Primitives** hold values directly. There are eight of them, including `int`, `long`, `double`, `boolean`, and `char`. A primitive variable is never `null`.

**References** point to objects on the heap. `String`, arrays, and the classes you write later are reference types. A reference can be `null`, which means "not pointing at any object right now."

```java
int count = 10;                 // primitive value lives with the variable
String name = "Ada";            // name holds a reference to a String object
boolean ready = true;           // another primitive
double percentage = 91.5;       // decimal numeric primitive
```

Walk through what happens. `count` remembers the integer ten. `name` does not store every character inside the variable slot the way `count` stores ten; it stores a reference to a `String` object. `ready` and `percentage` are again primitive values of different kinds.

If you assign one primitive to another, you copy the value. If you assign one reference to another, you copy the reference — both variables can end up pointing at the same object. That difference will matter enormously when we reach objects, equality, and collections.

### Example 2 — a practical school application fragment

Let's extend the school situation into something closer to real code.

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

Read it as a story. We remember a name as text, an age as a whole number, an average as a decimal value, and a pass/fail flag as a boolean. The expression `averageMarks >= 40.0` produces a boolean result and stores it in `passed`. When the program runs, it prints meaningful labeled output instead of a pile of unexplained numbers.

Notice how the types guide the design. Age should not be a `String` if we want to compare ages numerically. Marks that need a fractional part should not be forced into `int` unless we have a reason. Pass/fail is naturally boolean.

### An important detail — integer division

Here is a misunderstanding that shows up constantly.

```java
int a = 5;
int b = 2;
int result = a / b;   // result is 2, not 2.5
```

Both operands are `int`, so Java performs integer division and truncates toward zero. The fractional part is discarded. If you expected `2.5`, you needed a floating-point type in the computation:

```java
double precise = 5 / 2.0;   // 2.5
```

The code still compiles in the first version. That is what makes the bug sneaky. The type system did exactly what you asked — just not what you meant.

### Example 3 — a common mistake with references and null

```java
String nickname = null;
System.out.println(nickname.length());   // NullPointerException
```

`nickname` is a reference variable. Assigning `null` means it currently points to no object. Asking for `.length()` requires an actual `String` object. The result is a `NullPointerException` at runtime.

Primitives protect you from this particular failure: an `int` cannot be `null`. That does not make primitives "better" in every situation. It means each family has different rules, and you must know which family you are using.

### Local type inference with `var`

Modern Java allows `var` for local variables when the right-hand side makes the type obvious.

```java
var total = 10 * 19.99;   // inferred as double
```

This is still static typing. The compiler figures out the type and then enforces it. `var` is not a way to turn Java into a dynamically typed language. It is a way to reduce repetition when the type is already clear from the initializer.

### Connecting back and looking ahead

Let's connect this to where we have been. Episode Three gave us program structure. Variables and types give that structure something meaningful to remember and compute with. Names give meaning. Types constrain behavior. Primitives and references explain how values and objects are handled differently in memory.

Next we need to ask: once we have values, how do we combine them, compare them, and make decisions with them? That is where operators enter — and where a single character like `=` versus `==` can change the meaning of a whole program.

That is Episode Five.

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **4** — *Variables and Data Types*.
- **How content was used:** Teaching spine (variables name values; types distinguish kinds of information; primitives vs references; common pitfalls). Narration rewritten as descriptive instructor prose with evolving examples, matching the course style guide — not short definition beats.
- **Runtime note:** Aimed at a **4–15 minute** lesson (soft aim ~10–12).
