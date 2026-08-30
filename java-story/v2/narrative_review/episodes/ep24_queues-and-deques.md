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

Walk it. `offerLast("a")` places work at the tail. `pollFirst()` takes from the head and returns `"a"`. The method names advertise ends: last and first. Queues shape producer/consumer flow — Deque is the modern versatile choice because the same structure can act as queue or stack.

Method pairs matter because exception behavior differs:

```java
Deque<String> q = new ArrayDeque<>();
q.offer("one");          // returns false if it cannot insert (bounded cases)
String a = q.poll();     // returns null if empty
// vs
q.add("two");            // throws if it cannot insert
String b = q.remove();   // throws if empty
```

`offer`/`poll` speak in return values. `add`/`remove` speak in exceptions. Pick the style that matches whether emptiness is normal control flow or a true error.

Used as a stack, a deque replaces the legacy `Stack` class:

```java
Deque<String> stack = new ArrayDeque<>();
stack.push("frame-1");
stack.push("frame-2");
String top = stack.pop();   // frame-2
```

Prefer `Deque` over `java.util.Stack`. `Stack` is an old synchronized subclass of `Vector` with a design that modern code avoids.

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

When multiple threads produce and consume together, blocking queues appear in the concurrency chapters — structures that wait when empty or full instead of returning immediately. Today, keep the single-threaded mental model clear: `ArrayDeque` for local flow control.

What if we skip queues and abuse lists?

```java
List<String> jobs = new ArrayList<>();
jobs.add("a");
String next = jobs.remove(0);
```

The code reads like a list accident. Every reader must infer FIFO intent. With a queue or deque, the type itself documents the flow.

Deque's double-ended nature also models undo stacks. Same class as the FIFO queue, different end discipline. Avoid using `LinkedList` as a queue just because it implements `Deque` — `ArrayDeque` almost always outperforms it for stack and queue workloads.

Waiting-line problems outgrew maps and ordinary list usage. Queues gave FIFO language; deques added both ends. `ArrayDeque` became the default. `offer`/`poll` versus `add`/`remove` clarified empty and full handling. Legacy `Stack` was set aside.

Once collections hold real domain objects, another pressure appears: humans want them sorted — by name, by price, by date — and the rule is rarely only one field. How do we declare comparison policy without baking a single order into the class forever?

That is the pressure that brings sorting and comparators.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 24 (*Queues and Deques*).

Narration technique: waiting-line situation → queue/deque → ArrayDeque default → offer/poll vs add/remove → prefer Deque over Stack → blocking note → next natural problem (ordering policy / comparators). Continuity-checked transitions.
