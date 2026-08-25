# Episode 07 — Methods

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Methods |
| Catalog handbook column | 7 |
| Narration source script | Descriptive instructor narration (4–15 min) |
| Spoken form | Connected explanatory prose with walked-through examples |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

### Opening — a calculation that wants a name

In the previous episodes we learned how to store information in variables, compute with operators, and choose paths with control flow. That is enough to write a working `main` method that does everything in one place.

But let's start with a problem.

Suppose our application needs to calculate the total price of an order. We could place all of the calculation directly inside `main()`. That might work for one calculation, but what happens when we need the same calculation in several places — checkout, invoice preview, and a refund path?

Instead of copying the same logic repeatedly, we can give that behavior a name and place it inside a **method**.

A method is simply a named piece of behavior. You give it inputs, it does work, and it can return a result. That sounds small. It is one of the most important design tools in Java.

### Why methods exist

Without methods, programs grow by copy and paste. Every duplicated block becomes a place where a bug can be fixed in one spot and forgotten in another. Methods let us say: this behavior has a name, a clear contract, and a single place to improve.

In simple language: a method packages a verb. Variables remember nouns. Methods do work with those nouns.

### Example 1 — the smallest useful method

```java
double calculateTotal(double price, double tax) {
    return price + tax;
}
```

Why is this code here? Because it turns an unnamed expression into a reusable idea.

Walk through it. `double calculateTotal(...)` declares a method that returns a `double`. The name `calculateTotal` tells a reader what the behavior is for. The parameters `price` and `tax` are the inputs. Inside the body, we compute `price + tax` and `return` that value to the caller.

The method does not print anything. It does not talk to a database. It answers one question: given a price and a tax amount, what is the total?

### Calling the method

A method definition by itself does nothing until something calls it.

```java
public class OrderMath {
    static double calculateTotal(double price, double tax) {
        return price + tax;
    }

    public static void main(String[] args) {
        double total = calculateTotal(100.0, 18.0);
        System.out.println(total);
    }
}
```

In `main`, we call `calculateTotal(100.0, 18.0)`. Java binds `100.0` to `price` and `18.0` to `tax`, runs the body, and returns `118.0`. That returned value is stored in `total`, then printed.

Notice the payoff already: if the tax rule changes, we edit one method instead of hunting through every copy of the formula.

### Important detail — Java is pass-by-value

This is a common misunderstanding, so we will face it directly.

For primitives, the method receives a copy of the value. Changing the parameter inside the method does not change the caller's variable.

```java
static void tryChange(int n) {
    n = 99;
}

public static void main(String[] args) {
    int x = 1;
    tryChange(x);
    System.out.println(x);   // still 1
}
```

For object references, the method still receives a copy — a copy of the reference. That means the method can mutate the same object the caller sees, but it cannot make the caller's variable point to a different object by reassigning the parameter.

If someone asks in an interview, "Is Java pass-by-reference?" the precise answer is: no. Java is pass-by-value. For objects, the value being copied is the reference.

### Example 2 — a more practical checkout fragment

Let's evolve the example toward something you might see in a small shop application.

```java
static double calculateTotal(double price, double taxRate) {
    if (price < 0 || taxRate < 0) {
        throw new IllegalArgumentException("price and taxRate must be non-negative");
    }
    return price + (price * taxRate);
}

static void printReceipt(String item, double price, double taxRate) {
    double total = calculateTotal(price, taxRate);
    System.out.println(item + " => " + total);
}
```

Now `calculateTotal` accepts a tax **rate** instead of a precomputed tax amount. It also guards against invalid input. `printReceipt` uses the calculation and focuses on presentation. Each method has one job. That separation makes testing and reuse easier.

### Example 3 — a common mistake: doing too much in one method

What if we skip method design and put everything in `main`?

```java
public static void main(String[] args) {
    double price = 100.0;
    double taxRate = 0.18;
    double total = price + (price * taxRate);
    System.out.println("Shirt => " + total);
    // later, same formula again for another item...
}
```

This works for a demo. Then requirements grow. Discount rules appear. Receipt formatting changes. Refunds need the same math. The formula gets copied, then copied with a tiny difference, then nobody is sure which copy is correct.

The method is not ceremony. It is how we keep behavior coherent as the program grows.

### Overloading — same name, different parameter lists

Java allows multiple methods with the same name if their parameter lists differ. That is overloading.

```java
static double calculateTotal(double price, double taxRate) { /* ... */ }

static double calculateTotal(double price, double taxRate, double discount) {
    double discounted = price - discount;
    return calculateTotal(discounted, taxRate);
}
```

The compiler chooses which method to call based on the arguments you pass. Overloading is useful when several closely related operations deserve the same verb. It becomes confusing when the overloads secretly do unrelated things.

### Connecting the thread

Methods give behavior a name, a contract, and a place to live. We saw a tiny calculation, a safer practical version, the pass-by-value rule, and the failure mode of endless copy-paste in `main`.

Next we need a way to store many values under one name and access them by position. That is the road into arrays — and later into collections.

That is Episode Eight.

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **7** — *Methods*.
- **How content was used:** Topic spine (reuse, signatures, return values, pass-by-value, overloading). Rewritten as descriptive instructor prose with evolving examples (`calculateTotal` → practical checkout → mistake), matching the course style guide.
- **Runtime note:** Aimed at a **4–15 minute** lesson (soft aim ~10–12).
