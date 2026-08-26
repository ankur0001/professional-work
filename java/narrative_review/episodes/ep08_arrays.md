# Episode 08 — Arrays

| Field | Value |
|---|---|
| Episode | 08 |
| Title | Arrays |
| Catalog handbook column | 8 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Episode Seven gave behavior a name. Methods let us calculate a total once and call it from checkout, invoice, and refund. That solves duplicated verbs. It does not solve another kind of duplication that shows up the moment you have more than a few values of the same kind.

Suppose you need three quiz scores. You could write `score1`, `score2`, `score3`. Then a fourth quiz appears. Then you need to average them, sort them, or pass them into a method that should not grow a new parameter every semester. Separate variables do not scale. You need many values under one name, reachable by position.

That need is an array. An array is a fixed-length sequence of elements of one type. You create it with a length, and that length does not grow later. Indexes start at zero. The last valid index is `length - 1`. Those three facts — fixed length, zero-based indexes, typed slots — explain most beginner array bugs before they happen.

```java
int[] scores = {88, 91, 74};
System.out.println(scores.length);   // 3
System.out.println(scores[0]);       // 88
```

`scores` is one variable. Inside it live three ints. `scores.length` is a field, not a method — that detail matters when you later meet `List.size()`. Reading `scores[0]` is the first element. Asking for `scores[3]` throws, because three is past the end. Off-by-one bugs are what happen when zero-based indexing meets a human habit of counting from one.

Try averaging without an array and you feel the pain immediately: `score1 + score2 + score3` does not generalize. With an array you loop.

```java
int sum = 0;
for (int i = 0; i < scores.length; i++) {
    sum += scores[i];
}
double average = sum / (double) scores.length;
```

Notice the cast to `double` — Episode Four's integer-division trap still applies. The array did not invent new arithmetic; it gave the loop a single place to read from.

Once the happy path is clear, helpers save you from hand-rolling common work.

```java
int[] nums = {3, 1, 4};
java.util.Arrays.sort(nums);
System.out.println(java.util.Arrays.toString(nums));
```

`Arrays.sort` rearranges the same array in place. `Arrays.toString` gives a readable print. If you call `System.out.println(nums)` directly, you usually see a type-and-hash style string, not the contents — another beginner surprise that looks like a broken array when the array is fine.

What if the data is not a single line of scores but a grid — seats in a theater, pixels, a small table of daily temperatures by week?

Java models that as arrays of arrays.

```java
int[][] week = {
    {70, 72, 68},
    {75, 71, 73}
};
System.out.println(week[1][0]);   // 75 — second row, first column
```

`week[1]` is the second row. `week[1][0]` is the first value in that row. Rows can even have different lengths — "ragged" arrays — which is powerful and easy to misuse. When you loop a grid, nest carefully: outer loop over rows, inner over `week[r].length`.

Now the design question arrays force: what happens when the number of scores is not known up front, or keeps changing as users add and remove items?

Arrays do not grow. To "add" an element you allocate a larger array and copy. That is fine for fixed tables or buffers with a known capacity. When size changes as a normal part of the feature, prefer a `List`. Arrays remain the fixed-length backbone under many collections, but they are not the default tool for an open-ended shopping cart.

Assuming arrays grow is one of the most common early mistakes. Someone writes `nums[nums.length] = 99` hoping to extend the array and gets an exception instead. The honest move is either a correctly sized array from the start or a `List` that is allowed to grow. Interviewers often ask `array.length` versus `List.size()`: arrays expose a `length` field because size is part of the array object; collections expose `size()` because their size is behavior that can change.

Methods packaged repeated behavior. Arrays package repeated values by position. When the size must change as a product requirement, lists take over.

And yet many programs are not mainly lists of numbers. They are full of text — names, messages, ids, error lines. You can store characters in a `char[]`, but almost nobody wants to manage text that way day to day. Java's `String` type looks friendly until modification and comparison surprise you.

That surprise is where strings begin.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 8 (*Arrays*).

Narration technique: many-values-under-one-name situation → fixed length and zero indexes → Arrays helpers → arrays of arrays → List when size changes → next natural problem (text / strings). Continuity-checked transitions.
