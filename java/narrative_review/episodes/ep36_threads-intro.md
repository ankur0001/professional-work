# Episode 36 — Threads Intro

| Field | Value |
|---|---|
| Episode | 36 |
| Title | Threads Intro |
| Catalog handbook column | 36 |
| Narration source script | `make_episode_36.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. One CPU core can only do one thing at a time — unless you switch fast enough.
2. Threads let a program do multiple tasks concurrently within one process.
3. Download a file while updating the UI. Process requests while logging metrics.
4. Concurrency is about structure — parallelism is about simultaneous execution.
5. Threads share memory — powerful, but dangerous without coordination.
6. Today — the thread model in Java and how to start your first concurrent task.

### Scene `title` (renderer: `title`)

1. Episode Thirty-Six.
2. Threads Introduction — concurrency in Java.

### Scene `thread` (renderer: `thread`)

1. A Thread is a lightweight unit of execution inside a JVM process.
2. The JVM maps Java threads to OS threads — one-to-one on most platforms.
3. Every Java program starts with a main thread — the one running main.
4. Creating more threads lets work proceed on separate call stacks.
5. Threads share the heap — instance fields are visible across threads.
6. Each thread has its own stack — local variables are thread-confined.

### Scene `runnable` (renderer: `runnable`)

1. Runnable is a functional interface — void run with no arguments.
2. Pass a Runnable to a Thread constructor, then call start.
3. Callable is like Runnable but returns a value and can throw.
4. ExecutorService is the modern way — submit tasks to a thread pool.
5. Prefer Runnable lambdas over subclassing Thread directly.
6. Separate task logic from thread management.

### Scene `lifecycle` (renderer: `lifecycle`)

1. Thread states — NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED.
2. NEW until start is called — then RUNNABLE when eligible to run.
3. BLOCKED waiting for a monitor lock. WAITING until notified.
4. The scheduler decides which RUNNABLE thread runs on which core.
5. You do not control scheduling — design for unpredictability.
6. Understanding states helps you debug stuck and starving threads.

### Scene `starting` (renderer: `starting`)

1. Never call run directly — that executes on the current thread.
2. Call start to launch a new thread that invokes run.
3. join waits for another thread to finish — useful for coordination.
4. sleep pauses the current thread for a duration — does not release locks.
5. yield hints the scheduler to let other threads run — rarely needed.
6. Start threads deliberately — unbounded thread creation exhausts memory.

### Scene `shared` (renderer: `shared`)

1. Threads share the heap — all threads see the same object fields.
2. Local variables live on each thread stack — no sharing by default.
3. Mutable shared state without coordination causes race conditions.
4. Two threads reading and writing the same field — unpredictable results.
5. Visibility matters — changes by one thread may not be seen by another.
6. Shared memory is the reason synchronization exists — next episode.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — calling run instead of start — no new thread created.
3. Two — sharing mutable state without synchronization — race conditions.
4. Three — spawning unlimited threads — one per request does not scale.
5. Also — assuming operations are atomic when they are not — count plus plus.
6. Concurrency bugs are intermittent — design defensively from the start.

### Scene `interview` (renderer: `interview`)

1. Interview question — start versus run on a Thread?
2. start creates a new thread and schedules run on it.
3. run called directly — executes synchronously on the caller thread.
4. Mention Runnable, shared heap, and thread-local stacks.
5. Note race conditions when sharing mutable state.
6. That answer opens the door to synchronization next episode.

### Scene `teaser` (renderer: `teaser`)

1. Threads share memory. Next — making that safe.
2. Episode Thirty-Seven — Synchronization.
3. synchronized, locks, and coordinating access to shared data.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **36** — *Threads Intro*.
- **Series catalog:** Episode 36 ↔ handbook lesson 36 — *Threads Intro*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _One CPU core can only do one thing at a time — unless you switch fast enough._
- **`title`** — starts from: _Episode Thirty-Six._
- **`thread`** — starts from: _A Thread is a lightweight unit of execution inside a JVM process._
- **`runnable`** — starts from: _Runnable is a functional interface — void run with no arguments._
- **`lifecycle`** — starts from: _Thread states — NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, TERMINATED._
- **`starting`** — starts from: _Never call run directly — that executes on the current thread._
- **`shared`** — starts from: _Threads share the heap — all threads see the same object fields._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — start versus run on a Thread?_
- **`teaser`** — starts from: _Threads share memory. Next — making that safe._
