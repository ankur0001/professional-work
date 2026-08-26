# Episode 36 — Threads Intro

| Field | Value |
|---|---|
| Episode | 36 |
| Title | Threads Intro |
| Catalog handbook column | 36 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

So far, a Java program has mostly felt like one cook in one kitchen: start at `main`, do the next step, finish. That model breaks the moment you need progress on two fronts at once.

Imagine a server handling a request while also refreshing a cache in the background. Or a UI that must stay responsive while a long export runs. If everything stays on one thread, the export freezes the rest of the world. The practical question is not academic: how does Java run an independent path of execution beside the one we are already on?

A thread is that independent path. Shared memory is what makes threads powerful — and dangerous. Multiple threads can see the same objects. Without a coordination story, they can also step on each other.

The everyday unit of work is often a `Runnable` — a task with a `run` method — and a `Thread` that will execute it:

```java
Thread t = new Thread(() -> doWork());
t.start();
t.join();
```

Walk this carefully. We create a `Thread` whose work is the lambda `() -> doWork()`. Calling `start()` asks the JVM to schedule a new thread that will eventually execute that work. Calling `join()` waits until that thread finishes. The calling thread and the worker thread are now two timelines that meet again at `join`.

The classic beginner trap sits in one method name. `start` schedules. `run` does not start a new thread — it executes the work on the current thread, like a normal method call. If you call `run()` by accident, your program may look multi-threaded in the source and still be single-threaded in behavior.

```java
Thread t = new Thread(() -> doWork());
t.run();  // still on the caller's thread — no new timeline
```

Interrupt basics appear as soon as you need cooperative cancellation. You can interrupt a thread to request that it stop waiting or finish early. Well-behaved blocking calls notice the interrupt and throw or exit. Code that swallows interrupts without restoring status becomes hard to shut down cleanly. You do not need every interrupt pattern today — you need respect for the signal.

Shared mutation is the deeper issue. If two threads increment the same counter with `count++`, you can lose updates, because that one line is not one atomic action under the hood. If they write a compound structure with no protocol, you can observe half-built state. Creating threads does not create safety. It creates the need for a protocol — and that protocol is the next stretch of the concurrency story.

Unbounded thread creation hurts for a different reason. Spawning a new OS-backed thread per task feels simple under light load and catastrophic under a spike. Threads cost memory and scheduling time. A burst of work can exhaust the machine before your business logic has a chance to be wrong. Hold that worry; thread pools will address it once we understand the basics.

So reconnect the chain. We needed a second path of execution. Threads and `Runnable` provided it. `start` versus `run` separated scheduling from plain calling. `join` and interrupt sketched coordination and cancellation. Shared mutation and unbounded creation showed why "just add threads" is not a strategy.

The moment two threads touch the same mutable data, a new question dominates everything else: how do we take turns safely, and how do we make sure one thread's writes become visible to another?

That is Episode Thirty-Seven: synchronization.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 36 (*Threads Intro*).

Narration technique: dual-work situation → thread as answer → start/join walkthrough → run trap → interrupt → shared mutation → unbounded creation → next natural problem (synchronization).
