# Episode 24 — Queues and Deques

| Field | Value |
|---|---|
| Episode | 24 |
| Title | Queues and Deques |
| Catalog handbook column | 24 |
| Narration source script | `make_episode_24.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Maps associate. Queues sequence work over time.
2. First in, first out — producers and consumers meet in the middle.
3. Deque goes further — both ends open for stacks and queues.
4. ArrayDeque. PriorityQueue. Knowing the failure modes of offer versus add.
5. Today — waiting lines with explicit rules.
6. Order of arrival — or order of priority. Choose deliberately.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Four.
2. Queues and Deques — flow structures.

### Scene `queue` (renderer: `queue`)

1. Queue models a waiting line.
2. Insert at the tail. Remove from the head.
3. offer and poll return special values on failure.
4. add and remove throw when the operation cannot proceed.
5. peek inspects without removing — element is the throwing twin.
6. Pick the style that matches capacity constraints and call-site clarity.

### Scene `exception` (renderer: `exception`)

1. Remember the paired APIs.
2. Special-value methods suit bounded buffers and optional work.
3. Exception methods suit invariants — failure should be loud.
4. Mixing them casually makes empty-queue bugs harder to read.
5. Document which style your module uses.
6. Consistency beats cleverness at the call site.

### Scene `deque` (renderer: `deque`)

1. Deque means double-ended queue.
2. Add and remove at head or tail.
3. That makes Deque a clean stack — push and pop at one end.
4. It also makes a clean queue — offer last, poll first.
5. One interface, two classic structures, fewer legacy types.
6. Prefer Deque over the old Stack class in new code.

### Scene `arraydeque` (renderer: `arraydeque`)

1. ArrayDeque is the usual workhorse.
2. Resizable array — no capacity restriction by default.
3. Faster than Stack for stack operations in typical cases.
4. Often faster than LinkedList as a FIFO queue.
5. Null elements are not allowed — fail fast on null offer.
6. For single-threaded queues and stacks, start with ArrayDeque.

### Scene `priority` (renderer: `priority`)

1. PriorityQueue breaks FIFO on purpose.
2. The next element is the least — by natural order or Comparator.
3. Under the hood it is a heap — peek is cheap, arbitrary index access is not.
4. Iteration order is not sorted order — do not be fooled.
5. Great for schedulers and best-next algorithms.
6. Wrong when you needed a fair waiting line.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using java.util.Stack in new code.
3. Two — ignoring whether your queue is bounded when choosing add versus offer.
4. Three — defaulting to LinkedList as a queue without measuring.
5. Also — treating PriorityQueue iteration as sorted output.
6. Queues are simple. Semantics are the whole game.

### Scene `interview` (renderer: `interview`)

1. Interview question — Queue versus Deque, and why ArrayDeque?
2. Queue — FIFO waiting line with paired success and failure APIs.
3. Deque — both ends, covers stack and queue roles.
4. ArrayDeque — fast general-purpose implementation for single-threaded use.
5. Mention PriorityQueue when ordering is by priority, not arrival.
6. That answer shows API judgment.

### Scene `teaser` (renderer: `teaser`)

1. Flow structures are clear. Next — how collections decide order.
2. Episode Twenty-Five — Sorting and Comparators.
3. Comparable, Comparator, and stable sort expectations.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **24** — *Queue & Deque*.
- **Series catalog mapping:** Episode 24 / catalog column `24` / published title *Queues and Deques*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Maps associate. Queues sequence work over time._
- **`title`** — starts from: _Episode Twenty-Four._
- **`queue`** — starts from: _Queue models a waiting line._
- **`exception`** — starts from: _Remember the paired APIs._
- **`deque`** — starts from: _Deque means double-ended queue._
- **`arraydeque`** — starts from: _ArrayDeque is the usual workhorse._
- **`priority`** — starts from: _PriorityQueue breaks FIFO on purpose._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — Queue versus Deque, and why ArrayDeque?_
- **`teaser`** — starts from: _Flow structures are clear. Next — how collections decide order._
