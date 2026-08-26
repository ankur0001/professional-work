# Episode 59 — Escape Analysis

| Field | Value |
|---|---|
| Episode | 59 |
| Title | Escape Analysis |
| Catalog handbook column | 59 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

We have been talking about heaps, collectors, and dumps as if every `new` in source code becomes a heap object that GC must eventually judge. That mental model is useful — and incomplete. After the JIT warms up, the runtime may prove that some objects never escape the method that created them. If nothing outside needs to see that object as an object, the JIT can optimize it away. That analysis is called escape analysis, and it is one reason microbenchmarks lie and why "I allocated less in source" does not always match profiles.

Here is a tiny example that forces the question:

```java
Point p = new Point(1, 2);
return p.x() + p.y(); // may not need a real heap object
```

In source, you clearly constructed a `Point`. In a hot method, after inlining and escape analysis, the JIT may scalar-replace that object: keep `1` and `2` in registers or stack slots, never allocate a real heap `Point`, and still return the sum. From the programmer's view there was an object. From the machine's view there may only have been values. If you open an allocation profile and wonder where `Point` went, the answer might be "it never became a heap citizen on this path."

What does "escape" mean here? If the object is returned to an unknown caller, stored in a field, placed into a collection that outlives the method, published to another thread, or otherwise made reachable outside the analyzing scope, it escapes. If it stays local and the JIT can see all uses, it may not escape. Non-escaping objects enable scalar replacement — breaking an object into its constituent fields. And sometimes more: if you synchronize on an object that the JIT proves is thread-local and never escapes, lock elision becomes possible. The lock was protecting you from contention that cannot happen. The source still shows `synchronized`; the optimized native code may not pay for a real monitor. That is not a license to sprinkle synchronized blocks randomly. It is an explanation of why some synchronized local objects do not show up as contended locks in profiles.

This is exciting in interviews and dangerous in code reviews. The wrong reaction is to rewrite clear code into contortions because you imagine every `new` is expensive. Readability still wins for code that is not on a proven hot path. The JIT may already be removing the allocation you are about to make uglier. Another wrong reaction is to trust a tiny microbenchmark that "proves" allocations vanished — or did not — without JMH and without a warmup story that matches production. Escape analysis depends on inlining and profile-guided decisions. A cold microbench can miss the optimization. A poorly written one can fool you into celebrating nothing, or into panicking about allocations that disappear in the real service.

So when do you care? When allocation profiles under real load show pressure, and you are deciding whether a particular allocation site is real heap traffic. When you see synchronized blocks on obviously local objects and wonder whether contention is imaginary. When someone claims "Java always allocates this" as a reason to rewrite an API into primitive soup before measuring. Escape analysis is the mechanism that makes those claims incomplete. It does not make measurement optional; it makes naive reading of source allocation counts incomplete.

Walk the reasoning with the `Point` example again, with variations. If `Point` is a simple carrier and `p` never leaves the method, scalar replacement may apply. If you store `p` into a list that outlives the method, it escapes — heap allocation is required. If you return `p` itself, it escapes. If you pass `p` into a method the JIT cannot inline or analyze fully, escape may be assumed conservatively. The keyword is not "never allocate." The keyword is "allocate when the object must be visible as an object." Ignoring when objects truly escape is how people invent conspiracy theories about the JIT "not working."

Measure with real workloads. JFR allocation samples and async-profiler allocation mode show what survived into the heap, not what your eyes saw in source. That pairing — source intent versus runtime evidence — is the mature way to talk about escape analysis. Rewriting clear code for imaginary allocations, and trusting microbenchmarks without JMH, are the twin failure modes of this topic.

If asked what escape analysis is, say: the JIT analyzes whether an object escapes a method or thread; if it does not, optimizations like scalar replacement and sometimes lock elision become legal. Then add the humility clause: do not micro-optimize assuming every `new` escapes, and do not rewrite clear code for imaginary allocations.

Today's lesson connects the JIT back to the heap: not every object you construct becomes collector work. Next we leave the "objects on the heap" frame for a moment. Processes die with free heap space when native memory, metaspace, or container limits are the real budget — and that is Episode Sixty.

Connect this back to GC pressure conversations. A developer points at a line that constructs a temporary object inside a hot loop and declares victory after deleting it. Sometimes allocation profiles improve. Sometimes nothing changes because the object never escaped and never hit the heap after warmup. Sometimes something gets worse because the "optimization" blocked inlining or made the code harder for the JIT to see through. Escape analysis does not forbid caring about allocations. It forbids caring about them without profiles from the warmed path.

Connect this back to GC pressure conversations. A developer points at a line that constructs a temporary object inside a hot loop and declares victory after deleting it. Sometimes allocation profiles improve. Sometimes nothing changes because the object never escaped and never hit the heap after warmup. Sometimes something gets worse because the "optimization" blocked inlining or made the code harder for the JIT to see through. Escape analysis does not forbid caring about allocations. It forbids caring about them without profiles from the warmed path.

Lock elision deserves one more grounded picture. You write a helper that synchronizes on a freshly created local lock object "to be safe." No other thread can see that object. After JIT optimization, the monitor may disappear. The code review conversation should still ask why the lock exists — clarity for readers matters — but the performance conversation should not assume contention that the runtime proved impossible.

Lock elision deserves one more grounded picture. You write a helper that synchronizes on a freshly created local lock object "to be safe." No other thread can see that object. After JIT optimization, the monitor may disappear. The code review conversation should still ask why the lock exists — clarity for readers matters — but the performance conversation should not assume contention that the runtime proved impossible.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Escape Analysis (Episode 59).

Narration technique: every-new-is-heap assumption → Point example → escape definition → scalar replacement + lock elision → anti-patterns → when to care → variations → measure → interview woven → bridge to metaspace/native.

Teaching points preserved: escape analysis / scalar replacement; lock elision; don't micro-opt every new; readability; measure real workloads.
