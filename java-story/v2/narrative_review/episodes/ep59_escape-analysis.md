# Episode 59 — Escape Analysis

| Field | Value |
|---|---|
| Episode | 59 |
| Title | Escape Analysis |
| Catalog handbook column | 59 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We have been talking about heaps, collectors, and dumps as if every `new` in source becomes a heap object GC must eventually judge. That model is useful — and incomplete. After the JIT warms up, the runtime may prove that some objects never escape the method that created them. If nothing outside needs to see that object as an object, the JIT can optimize it away. That is escape analysis — one reason microbenchmarks lie, and why "I allocated less in source" does not always match profiles.

Here is a tiny example that forces the question:

```java
Point p = new Point(1, 2);
return p.x() + p.y(); // may not need a real heap object
```

In source, you clearly constructed a `Point`. In a hot method, after inlining and escape analysis, the JIT may scalar-replace it: keep `1` and `2` in registers or stack slots, never allocate a heap `Point`, and still return the sum. From the programmer's view there was an object. From the machine's view there may only have been values. If an allocation profile wonders where `Point` went, it may never have become a heap citizen on this path.

What does "escape" mean? If the object is returned to an unknown caller, stored in a field, placed into a collection that outlives the method, published to another thread, or otherwise made reachable outside the analyzing scope, it escapes. If it stays local and the JIT can see all uses, it may not. Non-escaping objects enable scalar replacement — breaking an object into its fields. Sometimes more: if you synchronize on an object the JIT proves is thread-local and never escapes, lock elision becomes possible. The source still shows `synchronized`; optimized native code may not pay for a real monitor. That is not a license to sprinkle synchronized blocks randomly. It explains why some synchronized local objects do not show up as contended locks.

Walk the `Point` variations. Local carrier that never leaves the method — scalar replacement may apply. Store `p` into a list that outlives the method — it escapes. Return `p` — it escapes. Pass `p` into a method the JIT cannot inline or analyze fully — escape may be assumed conservatively. The keyword is not "never allocate." It is "allocate when the object must be visible as an object."

This is exciting in interviews and dangerous in reviews. Do not rewrite clear code into contortions because you imagine every `new` is expensive. Readability still wins off the proven hot path; the JIT may already remove the allocation you are about to uglify. Do not trust a tiny microbenchmark without JMH and a warmup story that matches production. Escape analysis depends on inlining and profiles. A cold microbench can miss the optimization or panic about allocations that disappear in the real service.

Connect this to GC pressure conversations. A developer deletes a temporary object in a hot loop and declares victory. Sometimes profiles improve. Sometimes nothing changes because the object never escaped after warmup. Sometimes things get worse because the "optimization" blocked inlining. Escape analysis does not forbid caring about allocations. It forbids caring about them without profiles from the warmed path.

Lock elision deserves one grounded picture. You synchronize on a freshly created local lock object "to be safe." No other thread can see it. After JIT optimization, the monitor may disappear. The review should still ask why the lock exists for readers — but the performance conversation should not assume contention the runtime proved impossible.

So when do you care? When allocation profiles under real load show pressure. When synchronized blocks on obviously local objects make you wonder whether contention is imaginary. When someone claims "Java always allocates this" as a reason to rewrite an API into primitive soup before measuring. Measure with real workloads: JFR allocation samples and async-profiler show what survived into the heap, not what your eyes saw in source.

If asked what escape analysis is, say: the JIT analyzes whether an object escapes a method or thread; if it does not, optimizations like scalar replacement and sometimes lock elision become legal. Then add humility: do not micro-optimize assuming every `new` escapes, and do not rewrite clear code for imaginary allocations.

Today's lesson connects the JIT back to the heap: not every object you construct becomes collector work. Next we leave the "objects on the heap" frame. Processes die with free heap space when native memory, metaspace, or container limits are the real budget — and that paradox needs its own explanation.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Escape Analysis (Episode 59).

Narration technique: every-new-is-heap assumption → Point example → escape definition → scalar replacement + lock elision → variations → anti-patterns → GC connection → measure → interview woven → bridge to metaspace/native.

Teaching points preserved: escape analysis / scalar replacement; lock elision; don't micro-opt every new; readability; measure real workloads.
