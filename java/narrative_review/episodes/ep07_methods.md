# Episode 07 — Methods

| Field | Value |
|---|---|
| Episode | 07 |
| Title | Methods |
| Catalog handbook column | 7 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

By now we can store information, compute with it, and choose different paths through a program. That is enough to make `main` do useful work. It is also enough to paint ourselves into a corner.

Suppose our application needs to calculate the total price of an order. We could place the whole calculation directly inside `main()`. For one screen, on one afternoon, that can feel fine. Then checkout needs the same math. The invoice preview needs it. A refund path needs it too. Suddenly the same formula lives in three places.

So a natural question appears: if the behavior is the same, why are we rewriting it by hand?

Instead of copying the logic, we can give that behavior a name and place it inside a method. A method is a named piece of behavior. You give it inputs, it does work, and it can return a result. Variables remember nouns. Methods package verbs.

Here is the smallest version that still teaches the idea:

```java
double calculateTotal(double price, double tax) {
    return price + tax;
}
```

Why show this now? Because an abstract definition of "method" is easy to nod at and hard to use. This example turns an unnamed expression into a reusable idea. `calculateTotal` is the name of the behavior. `price` and `tax` are the inputs. The body computes `price + tax` and `return`s that value. The method does not print. It does not talk to a database. It answers one question: given a price and a tax amount, what is the total?

But a method definition by itself does nothing until something calls it. That raises the next question: how does the program actually use this named behavior?

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

In `main`, we call `calculateTotal(100.0, 18.0)`. Java binds `100.0` to `price` and `18.0` to `tax`, runs the body, and returns `118.0`. That returned value is stored in `total` and then printed. The payoff is already visible: if the tax rule changes, we edit one method instead of hunting through every copy of the formula.

Once calling feels clear, learners usually ask a deeper question — sometimes out loud, sometimes only as confusion later: if I change a parameter inside the method, does the caller's variable change?

For primitives, no. The method receives a copy of the value.

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

`x` remains `1`, because `n` was only a copy. For object references, Java is still pass-by-value — but the value being copied is the reference. So a method can mutate the same object the caller sees, yet it cannot make the caller's variable point somewhere else by reassigning the parameter. If an interview asks whether Java is pass-by-reference, the precise answer is: no. Pass-by-value. For objects, the copied value is the reference.

Now that the mechanism is honest, let's evolve the example toward something closer to a shop.

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

Notice what changed and why. `calculateTotal` now accepts a tax rate instead of a precomputed tax amount, and it refuses invalid input. `printReceipt` uses the calculation and focuses on presentation. Each method has one job. That separation is not style for its own sake — it is how testing and reuse stay possible as requirements grow.

What if we skip methods and keep everything in `main`?

```java
public static void main(String[] args) {
    double price = 100.0;
    double taxRate = 0.18;
    double total = price + (price * taxRate);
    System.out.println("Shirt => " + total);
    // later, the same formula again for another item...
}
```

This works for a demo. Then discounts appear. Receipt formatting changes. Refunds need the same math. The formula gets copied, then copied with a tiny difference, then nobody is sure which copy is correct. The method is not ceremony. It is how behavior stays coherent as the program grows.

There is one more pressure that appears once methods become natural: sometimes several closely related operations deserve the same verb. Java allows overloading — multiple methods with the same name and different parameter lists.

```java
static double calculateTotal(double price, double taxRate) { /* ... */ }

static double calculateTotal(double price, double taxRate, double discount) {
    double discounted = price - discount;
    return calculateTotal(discounted, taxRate);
}
```

The compiler chooses which method to call based on the arguments. Overloading helps when the operations are truly the same idea. It becomes noise when the overloads secretly do unrelated things.

So let's reconnect the chain. We started with duplicated order math and asked why we were rewriting the same behavior. Methods gave that behavior a name and a contract. Calling showed how values move in and results move out. Pass-by-value explained what "inputs" really mean. A more practical checkout fragment showed responsibilities splitting cleanly. Skipping methods showed the maintenance trap. Overloading showed how related forms of the same verb can coexist.

Once we can name behavior, another need becomes obvious: we often need many values under one name, accessible by position — a list of prices, a list of scores, a list of ids. Copying `price1`, `price2`, `price3` into separate variables is the same kind of trap we just escaped with methods.

That is the natural door into Episode Eight: arrays.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 7 (*Methods*).

Narration technique: duplicated-logic situation → “why rewrite?” → method as answer → call site → pass-by-value question → practical evolution → what-if no methods → overloading as related pressure → next natural problem (many values / arrays). Continuity-checked transitions.
