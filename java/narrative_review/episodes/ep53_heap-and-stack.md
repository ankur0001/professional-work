# Episode 53 — Heap and Stack

| Field | Value |
|---|---|
| Episode | 53 |
| Title | Heap and Stack |
| Catalog handbook column | 53 |
| Narration source script | `make_episode_53.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Fifty-Two decoded bytecode on the operand stack.
2. But where do method frames and objects actually live in memory?
3. Each thread owns a stack of frames — locals and operand stacks inside.
4. The heap holds every object your program allocates with new.
5. Class metadata lives in metaspace — separate from the object heap.
6. Today — heap and stack, frames, locals, and object layout.

### Scene `title` (renderer: `title`)

1. Episode Fifty-Three.
2. Heap and Stack.

### Scene `stack_frames` (renderer: `stack_frames`)

1. Each Java thread has its own call stack — one frame per active method.
2. A frame stores local variables, the operand stack, and a reference to the constant pool.
3. When a method is invoked, a new frame is pushed — return pops it.
4. StackOverflowError means too many nested calls — usually infinite recursion.
5. Frames are thread-local — no sharing between threads on the stack.
6. The stack is fast and automatically reclaimed when a method returns.

### Scene `locals_array` (renderer: `locals_array`)

1. Local variable slot zero is always this for instance methods.
2. Parameters occupy the next slots — iload and istore reference them.
3. Wide types like long and double consume two consecutive slots.
4. The operand stack is separate from locals — temporary computation space.
5. Compiler assigns slot numbers — visible in javap with -v.
6. Locals die with the frame — no manual cleanup needed.

### Scene `heap_objects` (renderer: `heap_objects`)

1. Every new keyword allocates an object on the heap.
2. All threads share the heap — objects are visible across threads.
3. References on the stack or in other objects point to heap instances.
4. Heap memory is managed by the garbage collector — not freed manually.
5. OutOfMemoryError means the heap cannot grow further.
6. Large object graphs live here — caches, collections, domain models.

### Scene `object_layout` (renderer: `object_layout`)

1. A heap object starts with a mark word and a klass pointer header.
2. Instance fields follow the header — primitives inline, references are pointers.
3. Arrays store length then elements — int arrays pack ints contiguously.
4. Object size depends on header plus fields plus alignment padding.
5. Compressed oops shorten reference fields on 64-bit JVMs with less than 32 GB heap.
6. Understanding layout helps reason about memory footprint and cache behavior.

### Scene `metaspace` (renderer: `metaspace`)

1. Class metadata — method tables, constant pools, field layouts — lives in metaspace.
2. Metaspace replaced PermGen in Java 8 — native memory, not part of the heap.
3. Grows as classes load — reclaimed when ClassLoader is collected.
4. ClassLoader leaks can exhaust metaspace — a common production issue.
5. Flag MaxMetaspaceSize caps growth — default is effectively unlimited.
6. Heap holds objects — metaspace holds class definitions.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — storing large objects on the stack — only references live on the stack.
3. Two — assuming stack variables are thread-safe — only if not escaped.
4. Three — ignoring metaspace when leaking ClassLoaders in hot-reload apps.
5. Also — confusing heap size with total JVM memory footprint.
6. Know which memory region each piece of data occupies.

### Scene `interview` (renderer: `interview`)

1. Interview question — heap versus stack in Java?
2. Stack — per-thread frames with locals and operand stacks — automatic cleanup.
3. Heap — shared object storage — garbage collected.
4. References on stack point to objects on heap.
5. Metaspace holds class metadata — separate from heap since Java 8.
6. StackOverflowError versus OutOfMemoryError — different regions, different causes.

### Scene `teaser` (renderer: `teaser`)

1. Objects on the heap outlive their frames — something must reclaim them.
2. Episode Fifty-Four — Garbage Collection Intro.
3. Roots, mark-sweep, generations, and stop-the-world pauses.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **61** — *Heap*.
- **Series catalog mapping:** Episode 53 / catalog column `53` / published title *Heap and Stack*.
- **Note:** Episode number and handbook lesson number are **not 1:1** here (handbook lesson 61 → episode 53). See `../reference/handbook_toc_recovered.md` for documented divergences.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Fifty-Two decoded bytecode on the operand stack._
- **`title`** — starts from: _Episode Fifty-Three._
- **`stack_frames`** — starts from: _Each Java thread has its own call stack — one frame per active method._
- **`locals_array`** — starts from: _Local variable slot zero is always this for instance methods._
- **`heap_objects`** — starts from: _Every new keyword allocates an object on the heap._
- **`object_layout`** — starts from: _A heap object starts with a mark word and a klass pointer header._
- **`metaspace`** — starts from: _Class metadata — method tables, constant pools, field layouts — lives in metaspace._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — heap versus stack in Java?_
- **`teaser`** — starts from: _Objects on the heap outlive their frames — something must reclaim them._
