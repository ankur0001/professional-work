# Episode 37 — Synchronization

| Field | Value |
|---|---|
| Episode | 37 |
| Title | Synchronization |
| Catalog handbook column | 37 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Threads gave us more than one path of execution. Shared memory made that interesting. Now we hit the problem those paths create the first week you ship them.

Suppose two threads both run `count++` on the same field ten thousand times. You expect twenty thousand. Sometimes you get fewer. The line looks atomic in source. At the machine level it is a read, a modify, and a write — and another thread can interleave between those steps. Even when you "get lucky" on counts in a short test, you can still have visibility problems: one thread wrote a value, another never sees the new value when its logic expected to. Races are not only lost updates. They are also stale reads.

So the natural question is: how do we make a critical section exclusive, and make writes visible to the next thread that enters?

`synchronized` is Java's built-in answer for many cases. It buys mutual exclusion and visibility for threads that synchronize on the same lock. Keep the sections small. The lock should protect shared state, not become a global pause button for unrelated work.

```java
private int count;

synchronized void incr() {
    count++;
}

synchronized int get() {
    return count;
}
```

Walk the idea. Before a thread enters `incr`, it must acquire the intrinsic lock associated with the instance (for a non-static synchronized method). Only one thread holds that lock at a time for this object's synchronized methods. When the method exits, the lock is released, and the memory effects become visible to other threads that later acquire the same monitor. Mutual exclusion prevents the torn increment. The happens-before relationship from releasing and later acquiring the same monitor makes the write visible to `get`.

That second part is easy to under-teach. People memorize "synchronized means one at a time" and forget "synchronized also defines when memory becomes visible." Without that, you get designs that lock on write and read unlocked fields the rest of the time, then wonder why production sees stale state that "should be impossible."

Lock on the shared state you mean to protect — typically a private final lock object, or the object that owns the invariant — not on a random string literal or a publicly accessible instance that strangers can contend on.

```java
private final Object lock = new Object();
private int count;

void incr() {
    synchronized (lock) {
        count++;
    }
}
```

Synchronizing on `this` for a public API can be careless if callers might also synchronize on your instance and create unintended coupling. A private lock keeps ownership inside your class.

Deadlocks appear when multiple locks enter the chat. Thread One takes lock A then waits for B. Thread Two takes B then waits for A. Both wait forever. Nested locks without a global ordering are how that story starts. You will get a full deadlock episode later; today you only need the fear that makes you keep critical sections small and lock sets simple.

Prefer higher-level concurrency utilities when they fit — executors, concurrent collections, atomics, synchronizers. `synchronized` is foundational, not mandatory for every problem. Using it everywhere can serialize a program that only needed a concurrent map or an atomic counter.

Common mistakes follow from stretching the tool. Synchronizing on `this` for public types without thinking about external locking. Huge synchronized methods that hold the lock while doing I/O or calling alien code. Nested locks grabbed in different orders on different paths. Each mistake turns a safety tool into a scalability or liveness problem.

A useful way to choose the size of a critical section is to ask what invariant you are protecting. If the invariant is "count matches the number of accepted jobs," then only the few lines that update both structures need the lock. If you lock the entire request — including network calls — you have serialized the internet behind one monitor. Correctness may hold. Throughput will not. Synchronization is a scalpel. Using it like a blanket is how systems become mysteriously single-threaded under load while still looking concurrent in a thread dump.

What if two different locks protect two related fields, and a reader needs a consistent snapshot of both? Then synchronizing each field separately is not enough. You need one lock for the combined invariant, or an atomic structure that publishes both values together. Lock identity follows the invariant, not the field list in your IDE.

If you remember only one practice from today, make critical sections small and lock sets obvious. Most synchronization disasters are large sections and fuzzy ownership wearing a correct keyword.

Static synchronized methods lock on the `Class` object. That is useful when the shared state is truly static, and painful when unrelated static methods contend on the same class lock by accident. Same rule as before: the lock identity must match the shared state identity. If two static fields are unrelated, do not make them wait on each other just because both methods say `synchronized`.

So reconnect the chain. Racing increments showed why shared mutation needs a protocol. `synchronized` provided mutual exclusion and visibility through intrinsic locks. Small sections and clear lock identity kept the protocol sane. Deadlock risk and higher-level utilities reminded us not to stop thinking once the keyword appears.

Sometimes you do not need a full critical section — you only need to publish a flag or a reference so other threads reliably see that a write happened. That narrower need is where `volatile` and happens-before edges deserve their own careful episode.

Episode Thirty-Eight is that episode.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 37 (*Synchronization*).

Narration technique: lost-update situation → synchronized as mutex+visibility → walkthrough → lock identity → deadlock foreshadow → higher-level utils → mistakes → next natural problem (volatile).
