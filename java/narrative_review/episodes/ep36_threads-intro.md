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

Imagine a server handling a user request while also refreshing a cache in the background. Or a desktop tool that must stay responsive while a long export runs. If everything stays on one thread, the export freezes the rest of the world. The practical question is not academic: how does Java run an independent path of execution beside the one we are already on?

A thread is that independent path. Shared memory is what makes threads powerful — and dangerous. Multiple threads can see the same objects. Without a coordination story, they can also step on each other in ways that demos never reproduce and production reproduces at 2 a.m.

The everyday unit of work is often a `Runnable` — a task with a `run` method — and a `Thread` that will execute it:

```java
Thread t = new Thread(() -> doWork());
t.start();
t.join();
System.out.println("worker finished");
```

Walk this carefully. We create a `Thread` whose work is the lambda `() -> doWork()`. Calling `start()` asks the JVM to schedule a new thread that will eventually execute that work. Calling `join()` waits until that thread finishes. The calling thread and the worker thread are now two timelines that meet again at `join`. After `join` returns, you know the worker's writes are visible to you in the happens-before sense — a detail that will matter more as we go deeper into memory, but that already explains why `join` is more than "wait for a boolean flag you invent yourself."

The classic beginner trap sits in one method name. `start` schedules. `run` does not start a new thread — it executes the work on the current thread, like a normal method call.

```java
Thread t = new Thread(() -> doWork());
t.run();  // still on the caller's thread — no new timeline
```

If you call `run()` by accident, your program may look multi-threaded in the source and still be single-threaded in behavior. Interviews ask `start` versus `run` because the bug is common and the difference is mechanical once you see it.

Interrupt basics appear as soon as you need cooperative cancellation. You can interrupt a thread to request that it stop waiting or finish early. Well-behaved blocking calls notice the interrupt and throw `InterruptedException` or exit. Code that catches that exception and swallows it without restoring interrupt status becomes hard to shut down cleanly — the signal dies, and higher layers keep waiting. You do not need every interrupt pattern today. You need respect for the signal: treat it as a request, not as noise.

Shared mutation is the deeper issue. If two threads increment the same counter with `count++`, you can lose updates, because that one line is not one atomic action under the hood. If they write a compound structure with no protocol, you can observe half-built state. Creating threads does not create safety. It creates the need for a protocol — mutual exclusion, visibility rules, higher-level concurrent structures — and that protocol is the next stretch of the concurrency story.

Unbounded thread creation hurts for a different reason. Spawning a new OS-backed thread per task feels simple under light load and catastrophic under a spike. Threads cost memory and scheduling time. A burst of work can exhaust the machine before your business logic has a chance to be wrong. Hold that worry; thread pools will address it once we understand the basics of starting, joining, and not lying to ourselves about shared state.

Let's make the shared-memory warning concrete with a tiny mental experiment. Thread A writes `user.name = "Ada"` and then `user.ready = true` without any protocol. Thread B sees `ready` and prints `user.name`. On some machines, some of the time, B prints null or an old name. Threads did not "break Java." They exposed that modern CPUs and compilers reorder and cache aggressively unless your program establishes happens-before edges. Starting a thread is easy. Establishing a memory protocol is the real craft — and it is why the next episodes exist.

What if we avoid shared mutation entirely and only pass immutable messages between threads? That can be an excellent design. It does not remove the need to understand threads; it changes which problems you still have — lifecycle, interruption, bounding concurrency — and which ones you dodge. Either way, `start`, `join`, and interrupt remain the basic verbs of the timeline.

Hold that picture: threads give timelines; shared memory gives both speed and risk. The rest of concurrency is how we keep the speed without drowning in the risk.

A final beginner trap: treating thread priority as a correctness tool. Priorities are hints at best and a source of portability surprises at worst. If your program is only correct when a thread runs "soon enough," you need coordination and timeouts — not a hope that the scheduler favors you. Correctness belongs in protocols; performance tuning comes after the protocol works.

So reconnect the chain. We needed a second path of execution. Threads and `Runnable` provided it. `start` versus `run` separated scheduling from plain calling. `join` and interrupt sketched coordination and cancellation. Shared mutation and unbounded creation showed why "just add threads" is not a strategy — it is the beginning of a design problem.

The moment two threads touch the same mutable data, a new question dominates everything else: how do we take turns safely, and how do we make sure one thread's writes become visible to another?

That is Episode Thirty-Seven: synchronization.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 36 (*Threads Intro*).

Narration technique: dual-work situation → thread as answer → start/join walkthrough → run trap → interrupt → shared mutation → unbounded creation → next natural problem (synchronization).
