# Episode 03 — Java Program Structure

| Field | Value |
|---|---|
| Episode | 03 |
| Title | Java Program Structure |
| Catalog handbook column | 3 |
| Narration source script | Descriptive instructor narration (4–15 min) |
| Spoken form | Connected explanatory prose with walked-through examples |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

### Opening — start with a problem

In the previous episode, we worked through **JDK, JRE, and JVM**. That gave us a piece of the platform. Today we need the next piece: **Java Program Structure**.

You want to run a program, but Java refuses until the file, class, package, and entry point agree with each other.

If you don't know where main lives or why public classes match filenames, every later lesson feels cursed.

I am not going to rush through slogans. We will introduce the idea in context, explain why it exists, look at Java code, walk through that code, and only then move on.

### Why this exists

In simple language, java program structure is a tool for a recurring design problem. If we ignore that problem, we can still write code for a while — and then the cost shows up as duplication, fragile APIs, runtime surprises, or code that only the original author understands.

### Building the idea step by step

#### Step 1

Now consider this teaching point: A .java file is a compilation unit; one public top-level class must match the filename.

This is usually the first thing you need in your mental model. If this step is fuzzy, the later details will feel like trivia.

Say it back in your own words before we look at code. If you can explain the 'why', the syntax becomes much easier to remember.

#### Step 2

Now consider this teaching point: Packages are namespaces that map to directories.

Notice how this extends the previous step. We are not collecting disconnected facts — we are assembling a mechanism.

Say it back in your own words before we look at code. If you can explain the 'why', the syntax becomes much easier to remember.

#### Step 3

Now consider this teaching point: main(String[] args) is the classic launcher entry point.

Ask yourself: if we skipped this detail, what bug or design smell would become more likely?

Say it back in your own words before we look at code. If you can explain the 'why', the syntax becomes much easier to remember.

#### Step 4

Now consider this teaching point: Imports bring types into scope; classpath/module path finds classes.

Ask yourself: if we skipped this detail, what bug or design smell would become more likely?

Say it back in your own words before we look at code. If you can explain the 'why', the syntax becomes much easier to remember.

#### Step 5

Now consider this teaching point: Structure is not paperwork — it is how the compiler and JVM find your code.

This last point is often where beginners and experienced developers separate. Tutorials mention it. Production work depends on it.

Say it back in your own words before we look at code. If you can explain the 'why', the syntax becomes much easier to remember.

### Example 1 — the smallest useful illustration

Let's start with the smallest example that still teaches the real idea. Read it slowly. Every line is doing work.

```java
package com.example.demo;

public class App {
    public static void main(String[] args) {
        System.out.println("args length = " + args.length);
    }
}
```

Why is this code here? Because an abstract definition is easy to nod at and hard to use. The example forces the idea into a concrete shape.

I'll walk this example like we're pair-programming.

Focus on the idea each line encodes — not memorizing syntax trivia.

Then we'll connect it to the production failure mode.

Look at `package com.example.demo;`.

Ask what would break if this line were missing, mistyped, or replaced with a 'simpler' shortcut. That question turns syntax into understanding.

Look at `public class App {`.

Ask what would break if this line were missing, mistyped, or replaced with a 'simpler' shortcut. That question turns syntax into understanding.

Look at `public static void main(String[] args) {`.

Ask what would break if this line were missing, mistyped, or replaced with a 'simpler' shortcut. That question turns syntax into understanding.

Look at `System.out.println("args length = " + args.length);`.

Ask what would break if this line were missing, mistyped, or replaced with a 'simpler' shortcut. That question turns syntax into understanding.

After this example, you should be able to point to the code and explain what problem each important line is solving.

### Example 2 — make it more realistic

The first example isolates the concept. Real applications rarely stop there. In a practical setting, Java Program Structure usually appears while you are trying to ship a feature under constraints: correctness, readability, and change over time.

So extend the idea: once the basic form works, ask what happens when the input is larger, the call sites multiply, or another teammate must maintain the code next month.

A useful habit is to take the small example and place it inside a tiny scenario — a checkout flow, a student record, a background job, a service boundary — whichever fits the topic. The concept should still be visible, but now it has a reason to exist in a product.

When you rewrite the example in that scenario, keep the same mechanism. Do not invent a new idea. You are proving that the same Java tool still works when the story gets closer to production.

### What if we skip this approach?

Important concepts become memorable when we see the failure mode without them.

For example, consider this common mistake: Public class name does not match filename.

That mistake is attractive because it feels shorter or more familiar. The cost arrives later: a subtle bug, a painful refactor, or an incident that is hard to diagnose.

This is the 'what if?' test. If removing the concept makes dangerous behavior easy, then the concept is earning its place in the language or the standard library.

### Example 3 — a common misunderstanding

**Misunderstanding 1:** Public class name does not match filename.

When you see this in a code review, do not only say 'that is wrong.' Explain the mechanism. Show the safer pattern. Connect it back to the reason the feature exists.

**Misunderstanding 2:** Package declaration does not match folders.

When you see this in a code review, do not only say 'that is wrong.' Explain the mechanism. Show the safer pattern. Connect it back to the reason the feature exists.

**Misunderstanding 3:** Assuming the working directory alone finds classes without classpath.

When you see this in a code review, do not only say 'that is wrong.' Explain the mechanism. Show the safer pattern. Connect it back to the reason the feature exists.

If you can diagnose the misunderstanding, you are no longer memorizing — you are teaching yourself to design.

### Interview-style checkpoint

Question: What must be true about a public top-level class and its file?

Answer in spoken form: Filename must match the public class name exactly (case-sensitive) and end with .java.

Then add one sentence about a trade-off or failure mode. That extra sentence is what makes the answer sound like experience instead of a flashcard.

### Connecting the thread

We came from **JDK, JRE, and JVM**. That set up a need. **Java Program Structure** is one of Java's answers to that need.

You should now be able to say why the idea exists, how a small Java example works, where you would use it, and what people often get wrong.

### Looking ahead

Once this is solid, a new challenge appears. That challenge leads us to **Variables and Data Types**.

We will start there the same way: with a problem, then the reason Java's approach exists, then code we can walk through together.

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary curriculum mapping:** Episode 03 / **Java Program Structure** (see `../reference/EPISODE_CATALOG.md` and handbook TOC notes for any remaps).
- **How content was used:** Handbook/curriculum provided the topic spine and teaching points. Narration was rewritten as **descriptive, example-driven instructor prose** (Introduce → Explain → Illustrate → Code → Walk Through → Question → Extend → Connect), not short disconnected definitions.
- **Runtime note:** Aimed at a **4–15 minute** lesson (soft aim ~10–12).

### Teaching points drawn from the topic bank

- A .java file is a compilation unit; one public top-level class must match the filename.
- Packages are namespaces that map to directories.
- main(String[] args) is the classic launcher entry point.
- Imports bring types into scope; classpath/module path finds classes.
- Structure is not paperwork — it is how the compiler and JVM find your code.
