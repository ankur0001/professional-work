# Episode 53 — Heap and Stack

| Field | Value |
|---|---|
| Episode | 53 |
| Title | Heap and Stack |
| Catalog handbook column | 53 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Bytecode runs inside a model of memory. If you only remember "objects on the heap," you already have a useful half-truth. The other half — the stack — explains recursion limits, local variables, and why a crash dump's stack trace is not a heap dump.

The stack is per-call bookkeeping. The heap is where objects live (generally). Mixing those stories is how people misread incidents.

```java
void f() {
    int x = 1;           // stack local in the frame
    User u = new User(); // object on the heap; reference in the frame
}
```

When `f` is invoked, the JVM creates a stack frame for that call on the current thread's stack. The frame holds locals — including `x` and the reference `u` — plus bookkeeping for return. `new User()` allocates an object on the heap. The local variable does not contain the whole object; it contains a reference pointing at the heap object. When `f` returns, the frame is discarded. If nothing else references that `User`, the object becomes eligible for garbage collection later. The reference died with the frame; the object's fate depends on reachability.

Frames hold locals and return info. Deep recursion creates many frames and can throw `StackOverflowError`. Huge or many objects can exhaust the heap and throw `OutOfMemoryError`. Those errors sound similar in a chat message and mean different missing resources. Confusing heap dumps with stack traces is a classic ops mix-up: one shows objects and retention; the other shows who called whom when something blew up. You often need both, but they answer different questions.

Escape analysis may elide allocations. The JIT sometimes proves an object never leaves a method and can allocate it in a way that avoids a full heap object — or scale it into registers and stack-like storage. That is why "every `new` always hits the heap forever" is too strong. You need enough humility to know optimizations can change allocation stories after warmup.

```java
void printSum(int a, int b) {
    Integer boxed = Integer.valueOf(a + b); // may allocate
    System.out.println(boxed);
}
```

Whether `boxed` becomes a real heap object in steady state depends on escape and JIT decisions. Microbenchmarks that ignore warmup lie about these effects.

GC cares about heap reachability from GC roots — including references in stack frames, static fields, and JNI handles. An object is collectible when no GC root can reach it. Stack frames are temporary roots for their locals. That is why a long-lived thread stuck in a method can pin objects through locals, and why finishing the method can suddenly make a large graph collectible.

What if we ignore native and stack limits while staring only at `-Xmx`? We miss `StackOverflowError`, thread stack sizing, and native memory. Heap is central, not total.

Thread stacks have size limits configured by the runtime. Many threads mean many stacks — a footprint cost separate from the heap. Virtual threads change the economics of stack usage for blocking workloads, but the conceptual split remains: frame state versus heap objects. When you read a stack overflow, look at recursion depth and huge frames. When you read a heap OOM, look at retention charts.

A heap dump answers "what objects dominate and who retains them?" A stack trace answers "what was this thread doing?" An incident that shows both — a thread stuck holding a large structure in locals while others allocate — teaches why the two views belong together.

Picture a recursive XML parser that dies with `StackOverflowError` on a hostile deep document. The heap may be fine. Raising heap size does nothing. Bounding depth or switching to an explicit stack structure does. The stack/heap split decides the fix family before you touch a single flag.

Picture the opposite: a cache growing without eviction until `OutOfMemoryError: Java heap space`. Stack traces show random request threads; the heap dump shows the cache. Different tool, different truth.

Hold a practical checklist: frames for locals and control; heap for objects; SO vs OOM as different resources; heap dumps vs stack traces as different questions; escape analysis as a reason to measure before declaring allocation fate. Prefer the right dump for the question. If the question is retention, dump the heap. If the question is "who called what," read the stack.

The next question is the reclaim story itself: how and when unused objects go away, and what your allocation rate does to that pace.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Lesson 53 (*Heap and Stack*).

Narration technique: memory-model situation → frame vs heap → SO vs OOM → escape foreshadow → GC roots → next natural problem (GC).
