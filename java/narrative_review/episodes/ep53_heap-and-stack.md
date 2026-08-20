# Episode 53 — Heap and Stack

| Field | Value |
|---|---|
| Episode | 53 |
| Title | Heap and Stack |
| Catalog handbook column | 53 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Two decoded bytecode executing on operand stacks inside method frames.
2. But where do those frames and the objects they reference actually live in memory?
3. Each thread owns a stack of frames — locals and operand stacks inside each frame.
4. The heap holds every object your program allocates with new — shared across all threads.
5. Class metadata lives in metaspace — separate from the object heap since Java 8.
6. Today — heap and stack, frames, locals, object layout, and the errors that name each region.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Three.
2. Heap and Stack.
3. We'll map variables to regions, walk object headers, and explain StackOverflowError versus OutOfMemoryError.

### Scene `stack_frames` (renderer: `stack_frames`)

1. Each Java thread has its own call stack — one frame pushed per method invocation.
2. A frame stores local variables, the operand stack, and a reference to the constant pool for this method.
3. When a method is invoked, a new frame is pushed — return pops it and discards locals automatically.
4. StackOverflowError means too many nested calls — usually infinite or runaway recursion.
5. Frames are thread-local — no sharing between threads on the stack — no locks needed for locals.
6. The stack is fast and automatically reclaimed when a method returns — no GC involved.

```java
void recurse(int n) {
    recurse(n + 1);  // StackOverflowError eventually
}
```

7. Default stack size per thread is platform-dependent — -Xss tunes it when deep recursion is intentional.

### Scene `locals_array` (renderer: `locals_array`)

1. Local variable slot zero is always this for instance methods — static methods skip this slot.
2. Parameters occupy the next slots in order — iload and istore bytecode reference slot indices.
3. Wide types long and double consume two consecutive slots — compiler leaves a hole for the second.
4. Operand stack is separate from locals — temporary computation space for bytecode operations.
5. Compiler assigns slot numbers — visible in javap -v LocalVariableTable when debug info present.
6. Locals die with the frame — references on locals stop keeping heap objects alive when frame pops, unless those objects are reachable elsewhere.

### Scene `heap_objects` (renderer: `heap_objects`)

1. Every new keyword allocates an object on the heap — arrays included.
2. All threads share the heap — objects are visible across threads through references.
3. References on the stack, in fields, or in arrays point to heap instances — not the objects themselves on stack.
4. Heap memory is managed by the garbage collector — you never free manually like C++.
5. OutOfMemoryError Java heap space means the heap cannot grow further despite GC attempts.
6. Large object graphs live here — caches, collections, domain models, session state.

```java
String label = "hello";           // reference on stack (local)
StringBuilder buf = new StringBuilder();  // object on heap
buf.append(label);
```

7. label points at interned or heap String — buf points at StringBuilder instance — classic split.

### Scene `object_layout` (renderer: `object_layout`)

1. A heap object starts with a mark word and a klass pointer header — housekeeping and type info.
2. Instance fields follow the header — primitives inline, references are pointer slots.
3. Arrays store length then elements — int arrays pack ints contiguously for cache-friendly access.
4. Object size equals header plus fields plus alignment padding — JVM rounds for alignment.
5. Compressed oops shorten reference fields on 64-bit JVMs with heaps under roughly 32 GB — saves memory bandwidth.
6. Understanding layout helps reason about footprint — why padding makes small objects surprisingly large.

### Scene `metaspace` (renderer: `metaspace`)

1. Class metadata — method tables, constant pools, field layouts, vtables — lives in metaspace.
2. Metaspace replaced PermGen in Java 8 — native memory, not counted in -Xmx heap limit.
3. Grows as classes load — reclaimed when ClassLoader becomes unreachable and GC collects loader.
4. ClassLoader leaks can exhaust metaspace — common in hot-redeploy app servers without restart.
5. MaxMetaspaceSize caps growth — default effectively unlimited on 64-bit until OS says no.
6. Heap holds objects — metaspace holds class definitions — two different OutOfMemoryError stories.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes I want burned into your brain.
2. Mistake one — thinking large objects live on the stack — only references and primitives live in frames, big objects on heap.
3. Mistake two — assuming stack locals are thread-safe globally — safe only if references do not escape to shared structures.
4. Mistake three — ignoring metaspace when leaking ClassLoaders in plugin or hot-reload apps.
5. Also — confusing heap -Xmx with total JVM RSS — native memory, threads, code cache add on top.
6. Know which memory region each piece of data occupies — debugging starts with the right map.

### Scene `interview` (renderer: `interview`)

1. Interview time — say this out loud like someone who has shipped code.
2. Question: Heap versus stack in Java?
3. Answer: Stack — per-thread frames with locals and operand stacks, automatic cleanup on return.
4. Heap — shared object storage, garbage collected when unreachable from GC roots.
5. References on stack or in fields point to objects on heap — not the reverse.
6. Metaspace holds class metadata — separate from heap since Java 8.
7. StackOverflowError versus OutOfMemoryError — different regions, different fixes — name both clearly.

### Scene `teaser` (renderer: `teaser`)

1. Objects on the heap outlive their frames — something must reclaim unreachable graphs.
2. Episode Fifty-Four — Garbage Collection Intro.
3. Roots, mark-sweep, generations, and stop-the-world pauses you feel in latency graphs.
4. See you there.

_Total beats: expanded for ~10–12 minute conversational delivery (well above the 4-minute floor; under the 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **61** — *Heap*.
- **Series catalog mapping:** Episode 53 / catalog column `53` / published title *Heap and Stack*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 61 → episode 53). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with stack versus heap examples — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — memory regions beyond operand stack
- **`title`** — episode title card
- **`stack_frames`** — per-thread call stacks
- **`locals_array`** — locals vs operand stack
- **`heap_objects`** — shared object allocation
- **`object_layout`** — headers, fields, compressed oops
- **`metaspace`** — class metadata region
- **`mistakes`** — stack vs heap confusion, metaspace neglect
- **`interview`** — heap vs stack interview answer
- **`teaser`** — bridge to Garbage Collection
