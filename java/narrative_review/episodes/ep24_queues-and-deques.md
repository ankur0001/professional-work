# Episode 24 — Queues and Deques

| Field | Value |
|---|---|
| Episode | 24 |
| Title | Queues and Deques |
| Catalog handbook column | 24 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Maps excel at lookup. They are awkward as waiting lines. A print spooler, a task buffer, a chat message pipe — these problems care about who arrived first, or who may enter and leave from both ends.

Suppose jobs arrive faster than a worker can finish them. You need a place to hold pending work and take the oldest job next. A list can fake that with `add` at the end and `remove(0)` at the front, but the intent is muddy and the performance story for `ArrayList` removal at zero is poor. The natural question is: what collection means "waiting line"?

Queues shape producer/consumer flow. A classic queue is FIFO — first in, first out. A deque (double-ended queue) allows insertion and removal at both ends. In modern Java, `Deque` is the versatile choice, and `ArrayDeque` is a strong general default for single-threaded use.

```java
Deque<String> q = new ArrayDeque<>();
q.offerLast("a");
String x = q.pollFirst();
```

Walk it. `offerLast("a")` places work at the tail. `pollFirst()` takes from the head and returns `"a"`. The method names advertise ends: last and first. You can also write `offer` and `poll`, which for a deque used as a queue mean the same FIFO story. Queues shape producer/consumer flow — Deque is the modern versatile choice because the same structure can act as queue or stack.

Method pairs matter because exception behavior differs:

```java
Deque<String> q = new ArrayDeque<>();
q.offer("one");          // returns false if it cannot insert (bounded cases)
String a = q.poll();     // returns null if empty
// vs
q.add("two");            // throws if it cannot insert
String b = q.remove();   // throws if empty
```

`offer`/`poll` speak in return values. `add`/`remove` speak in exceptions. Pick the style that matches whether emptiness is normal control flow or a true error. Beginners who call `remove` on an empty queue get surprised by exceptions; `poll` would have returned null and let them branch.

Used as a stack, a deque replaces the legacy `Stack` class:

```java
Deque<String> stack = new ArrayDeque<>();
stack.push("frame-1");
stack.push("frame-2");
String top = stack.pop();   // frame-2
```

Prefer `Deque` over `java.util.Stack`. `Stack` is an old synchronized subclass of `Vector` with a design that modern code avoids. Interviewers still mention it; production code usually reaches for `ArrayDeque`.

A tiny job-buffer story makes the FIFO intent obvious:

```java
Deque<Runnable> jobs = new ArrayDeque<>();
jobs.offerLast(() -> System.out.println("resize image"));
jobs.offerLast(() -> System.out.println("send email"));

while (!jobs.isEmpty()) {
    jobs.pollFirst().run();
}
```

Producers offer last. The consumer polls first. Ordering is the feature. You are not looking up by key; you are draining a line.

When multiple threads produce and consume together, blocking queues appear in the concurrency chapters — structures that wait when empty or full instead of returning immediately. Today, keep the single-threaded mental model clear: `ArrayDeque` for local flow control, and a note that shared pipelines need concurrent variants later.

What if we skip queues and abuse lists?

```java
List<String> jobs = new ArrayList<>();
jobs.add("a");
String next = jobs.remove(0);
```

The code reads like a list accident. Every reader must infer FIFO intent. With a queue or deque, the type itself documents the flow.


Deque's double-ended nature also models undo stacks and work stealing patterns at a small scale.

```java
Deque<String> history = new ArrayDeque<>();
history.push("type A");
history.push("type B");
String undone = history.pop(); // type B
```

Same class as the FIFO queue, different end discipline. That flexibility is why modern Java steers you to `Deque` instead of separate Stack and Queue class hierarchies for local use.

Bounded queues change the `offer` story: when capacity is full, `offer` returns false while `add` throws. In a single-threaded buffer you might never bound an `ArrayDeque`. In concurrent designs you will. Learning the method pairs now means fewer surprises when blocking queues arrive.

Avoid using `LinkedList` as a queue just because it implements `Deque`. `ArrayDeque` almost always outperforms it for stack and queue workloads without needing node allocations per element.


In UI undo/redo, two deques — undo and redo — capture the story without a custom structure. In task scheduling, a single deque as FIFO keeps fairness obvious. When requirements say "priority," you graduate to priority queues later; do not overload a plain deque with manual sorting on each insert. Match structure to rule.

Method naming in your own APIs should mirror `offer`/`poll` if emptiness is normal, and `add`/`remove` if emptiness is exceptional. Consistency between library queues and your wrappers reduces cognitive load.


So let's reconnect the chain. Waiting-line problems outgrew maps and ordinary list usage. Queues gave FIFO language; deques added both ends. `ArrayDeque` became the default. `offer`/`poll` versus `add`/`remove` clarified empty and full handling. Legacy `Stack` was set aside. Blocking queues were deferred to concurrency.

Once collections hold real domain objects, another pressure appears: humans want them sorted — by name, by price, by date — and the rule is rarely only one field. How do we declare comparison policy without baking a single order into the class forever?

Producer and consumer language also clarifies API design: methods named `enqueue`/`dequeue` or accepting a `Queue` parameter tell teammates how to think. If your public API takes a `List` but you only ever treat it as a line, you hid the real contract. Types teach.

Drain patterns show up often: poll until empty, process, repeat. Write that loop with `poll` returning null as the stop condition, not with `size()` checks that race once you add threads later. Habits you form on single-threaded deques should survive contact with concurrency chapters.

That is Episode Twenty-Five — Sorting and Comparators.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 24 (*Queues and Deques*).

Narration technique: waiting-line situation → queue/deque → ArrayDeque default → offer/poll vs add/remove → prefer Deque over Stack → blocking note → next natural problem (ordering policy / comparators). Continuity-checked transitions.

### Teaching points drawn from the topic bank

- FIFO vs double-ended access.
- ArrayDeque is a strong general default.
- offer/poll vs add/remove exception behavior.
- Legacy Stack — prefer Deque.
- Blocking queues appear in concurrency.
