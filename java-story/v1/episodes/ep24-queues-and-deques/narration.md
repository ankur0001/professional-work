# Episode 24 — Queues and Deques

**Cut:** v1 (original)

## Transcript (from captions)

Maps associate. Queues sequence work over time. First in, first out — producers and consumers meet in the middle. Deque goes further — both ends open for stacks and queues. ArrayDeque. PriorityQueue. Knowing the failure modes of offer versus add.

Today — waiting lines with explicit rules. Order of arrival — or order of priority. Choose deliberately. Episode Twenty-Four. Queues and Deques — flow structures. Queue models a waiting line.

Insert at the tail. Remove from the head. offer and poll return special values on failure. add and remove throw when the operation cannot proceed. peek inspects without removing — element is the throwing twin.

Pick the style that matches capacity constraints and call-site clarity. Remember the paired APIs. Special-value methods suit bounded buffers and optional work. Exception methods suit invariants — failure should be loud.

Mixing them casually makes empty-queue bugs harder to read. Document which style your module uses. Consistency beats cleverness at the call site. Deque means double-ended queue. Add and remove at head or tail.

That makes Deque a clean stack — push and pop at one end. It also makes a clean queue — offer last, poll first. One interface, two classic structures, fewer legacy types. Prefer Deque over the old Stack class in new code.

ArrayDeque is the usual workhorse. Resizable array — no capacity restriction by default. Faster than Stack for stack operations in typical cases. Often faster than LinkedList as a FIFO queue.

Null elements are not allowed — fail fast on null offer. For single-threaded queues and stacks, start with ArrayDeque. PriorityQueue breaks FIFO on purpose. The next element is the least — by natural order or Comparator.

Under the hood it is a heap — peek is cheap, arbitrary index access is not. Iteration order is not sorted order — do not be fooled. Great for schedulers and best-next algorithms. Wrong when you needed a fair waiting line.

Three common mistakes. One — using java.util.Stack in new code. Two — ignoring whether your queue is bounded when choosing add versus offer. Three — defaulting to LinkedList as a queue without measuring.

Also — treating PriorityQueue iteration as sorted output. Queues are simple. Semantics are the whole game. Interview question — Queue versus Deque, and why ArrayDeque? Queue — FIFO waiting line with paired success and failure APIs.

Deque — both ends, covers stack and queue roles. ArrayDeque — fast general-purpose implementation for single-threaded use. Mention PriorityQueue when ordering is by priority, not arrival.

That answer shows API judgment. Flow structures are clear. Next — how collections decide order. Episode Twenty-Five — Sorting and Comparators. Comparable, Comparator, and stable sort expectations.

See you there.
