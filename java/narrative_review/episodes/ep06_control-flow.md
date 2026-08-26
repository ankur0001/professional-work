# Episode 06 — Control Flow

| Field | Value |
|---|---|
| Episode | 06 |
| Title | Control Flow |
| Catalog handbook column | 6 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Operators can tell you that a score is high enough, that a name is non-null, that a counter has not reached its limit. Those answers are still just values. A program that only computes and never chooses is a calculator stuck on one path.

Picture a registration desk. You can compute age from a birth year. That still does not enroll anyone. You need a fork: if age is at least eighteen, continue; otherwise refuse. Then you need a loop: for each applicant in today's list, repeat the check. Control is what turns facts into actions.

So the next natural question is: how does Java take a boolean — or a set of cases — and send the program down different routes?

That is control flow. It is how programs make decisions and how they repeat work. It is also how nesting turns into vines nobody wants to read.

Start with the choice you already feel after Episode Five: if this, then that.

```java
if (averageMarks >= 40.0) {
    System.out.println("passed");
} else {
    System.out.println("failed");
}
```

The condition is an expression that yields a boolean. One branch runs. The other does not. When the decision has several labeled outcomes instead of a true/false fork, modern Java prefers switch expressions that return a value and push you toward covering the cases.

```java
String grade = switch (score / 10) {
    case 10, 9 -> "A";
    case 8 -> "B";
    case 7 -> "C";
    default -> "needs review";
};
```

A switch expression is not just new syntax for old `switch` statements. It encourages exhaustiveness and makes the result a value you can store. Old fall-through statement switches still exist, and forgetting a `break` is still a classic bug. Prefer the form that matches the job: expression when you want a result, statement when you are performing actions.

Choosing once is not enough. Often the same kind of decision must happen for every item — every student, every retry attempt, every page of results. That pressure brings loops: `for`, `while`, and the enhanced-for when you simply walk each element.

```java
for (int i = 0; i < n; i++) {
    if (i % 2 == 0) continue;
    System.out.println(i);
}
```

This loop visits indexes from zero up to, but not including, `n`. When `i` is even, `continue` skips the rest of that iteration. When `i` is odd, it prints. `break` would leave the loop entirely. `while` fits when you do not know the trip count in advance. Enhanced-for fits when you already have a collection and only need each element. Index `for` still wins when the position itself matters. Labeled `break` and `continue` exist for nested loops; use them sparingly — if you need a label to explain the control, the structure may be asking for a method instead.

As programs grow, another control-flow pain appears: you receive an `Object` or a general type, check what it really is, cast, then use it. Pattern matching reduces those casts by binding the narrowed type in the same test.

```java
if (value instanceof String s) {
    System.out.println(s.toUpperCase());
}
```

If `value` is a `String`, `s` is already that string inside the block. Older code would write a separate cast that can drift out of sync with the check. Pattern matching collapses them on purpose.

Now look at the design failure that control flow tempts: the giant nested if pyramid.

```java
if (user != null) {
    if (user.isActive()) {
        if (order != null) {
            if (order.total() > 0) {
                // finally do the work
            }
        }
    }
}
```

Each condition feels reasonable. Together they bury the real work. The healthier move is often to extract methods — early returns for guard clauses, named helpers for each policy — so each block has one job.

```java
boolean canCheckout(User user, Order order) {
    if (user == null || !user.isActive()) return false;
    if (order == null || order.total() <= 0) return false;
    return true;
}
```

Now the nested pyramid becomes a flat checklist. Control flow syntax cannot save a design that refuses to name its decisions — but naming the decision often shrinks the syntax you need.

Operators produced the booleans and comparisons we needed. Control flow uses those results to choose branches, return values from switches, repeat with loops, and narrow types with pattern matching. The skill is not collecting keywords. It is keeping the path readable as the rules multiply.

Once `main` can decide and loop, another trap appears. The same decision logic — calculate a total, validate an order, format a line — gets copied into every place that needs it. Behavior wants a name.

That need is what methods exist to answer.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 6 (*Control Flow*).

Narration technique: computed-values-need-routes situation → if/else and switch expressions → loops → break/continue → pattern matching → nesting failure → extract methods → next natural problem (named behavior). Continuity-checked transitions.
