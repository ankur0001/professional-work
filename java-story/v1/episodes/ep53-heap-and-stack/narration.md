# Episode 53 — Heap and Stack

**Cut:** v1 (original)

## Transcript (from captions)

Episode Fifty-Two decoded bytecode on the operand stack. But where do method frames and objects actually live in memory? Each thread owns a stack of frames — locals and operand stacks inside.

The heap holds every object your program allocates with new. Class metadata lives in metaspace — separate from the object heap. Today — heap and stack, frames, locals, and object layout.

Episode Fifty-Three. Heap and Stack. Each Java thread has its own call stack — one frame per active method. A frame stores local variables, the operand stack, and a reference to the constant pool.

When a method is invoked, a new frame is pushed — return pops it. StackOverflowError means too many nested calls — usually infinite recursion. Frames are thread-local — no sharing between threads on the stack.

The stack is fast and automatically reclaimed when a method returns. Local variable slot zero is always this for instance methods. Parameters occupy the next slots — iload and istore reference them.

Wide types like long and double consume two consecutive slots. The operand stack is separate from locals — temporary computation space. Compiler assigns slot numbers — visible in javap with -v.

Locals die with the frame — no manual cleanup needed. Every new keyword allocates an object on the heap. All threads share the heap — objects are visible across threads. References on the stack or in other objects point to heap instances.

Heap memory is managed by the garbage collector — not freed manually. OutOfMemoryError means the heap cannot grow further. Large object graphs live here — caches, collections, domain models.

A heap object starts with a mark word and a klass pointer header. Instance fields follow the header — primitives inline, references are pointers. Arrays store length then elements — int arrays pack ints contiguously.

Object size depends on header plus fields plus alignment padding. Compressed oops shorten reference fields on 64-bit JVMs with less than 32 GB heap. Understanding layout helps reason about memory footprint and cache behavior.

Class metadata — method tables, constant pools, field layouts — lives in metaspace. Metaspace replaced PermGen in Java 8 — native memory, not part of the heap. Grows as classes load — reclaimed when ClassLoader is collected.

ClassLoader leaks can exhaust metaspace — a common production issue. Flag MaxMetaspaceSize caps growth — default is effectively unlimited. Heap holds objects — metaspace holds class definitions.

Three common mistakes. One — storing large objects on the stack — only references live on the stack. Two — assuming stack variables are thread-safe — only if not escaped. Three — ignoring metaspace when leaking ClassLoaders in hot-reload apps.

Also — confusing heap size with total JVM memory footprint. Know which memory region each piece of data occupies. Interview question — heap versus stack in Java? Stack — per-thread frames with locals and operand stacks — automatic cleanup.

Heap — shared object storage — garbage collected. References on stack point to objects on heap. Metaspace holds class metadata — separate from heap since Java 8. StackOverflowError versus OutOfMemoryError — different regions, different causes.

Objects on the heap outlive their frames — something must reclaim them. Episode Fifty-Four — Garbage Collection Intro. Roots, mark-sweep, generations, and stop-the-world pauses. See you there.
