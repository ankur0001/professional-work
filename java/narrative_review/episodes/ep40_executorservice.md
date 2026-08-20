# Episode 40 — ExecutorService

| Field | Value |
|---|---|
| Episode | 40 |
| Title | ExecutorService |
| Catalog handbook column | 40 |
| Narration source script | Expanded review narration (4–15 min target) |
| Spoken form | Conversational documentary beats + walkthrough code |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Raw Thread per request does not scale — thread creation is expensive, stacks consume megabytes each.
2. Thread pools reuse a fixed set of worker threads for many tasks over time.
3. ExecutorService is the standard abstraction for submitting work in production Java.
4. Submit a Runnable, get back control — the pool handles scheduling and queueing.
5. Shutdown gracefully — in-flight tasks deserve a clean finish, not orphan threads on JVM exit.
6. Today — ExecutorService, thread pools, submission, and lifecycle done properly.

### Scene `title` (renderer: `title`)

1. Episode Forty.
2. ExecutorService and Thread Pools.
3. Factories, pool sizing, submit versus execute, and shutdown discipline.

### Scene `executor` (renderer: `executor`)

1. ExecutorService decouples task submission from thread lifecycle management — separation of concerns.
2. You describe what to run — Runnable or Callable — the executor decides how and when on which thread.
3. Factories in Executors create common pool configurations — don't hand-roll unless you have reason.
4. newFixedThreadPool — bounded thread count, unbounded LinkedBlockingQueue by default — watch queue growth.
5. newCachedThreadPool — grows on demand, reclaims idle threads after sixty seconds — bursty short tasks.
6. Prefer factory methods — they encode sensible defaults — then tune with metrics, not guesses.
7. ThreadPoolExecutor constructor exposes core size, max size, queue, rejection policy — full control when needed.

### Scene `pool` (renderer: `pool`)

1. A thread pool maintains a work queue of tasks and a set of worker threads pulling from it.
2. Workers pull tasks from the queue and execute them — reuse avoids creation overhead per task.
3. Bounded pools cap resource usage — critical for server applications under traffic spikes.
4. Too few threads — tasks wait in queue, latency grows. Too many — context-switch overhead dominates.
5. Size pools based on workload — CPU-bound often near core count; IO-bound higher with blocking factor.
6. Thread pools turn unbounded thread creation into managed concurrency — backpressure becomes possible.
7. Monitor queue depth and active count — metrics tell you when pool is undersized.

### Scene `submit_shutdown` (renderer: `submit_shutdown`)

1. submit takes a Runnable or Callable and returns a Future — result handle for Callable.
2. execute is fire-and-forget void — no Future, exceptions go to UncaughtExceptionHandler or afterExecute.
3. shutdown stops accepting new tasks — existing tasks and queued tasks still run to completion.
4. shutdownNow attempts to cancel pending queued tasks and interrupt running tasks — best-effort stop.
5. awaitTermination waits for the pool to finish — with optional timeout — before JVM exits or next phase.
6. Always shut down executors — leaked pools keep JVM threads alive and prevent clean deploy restarts.
7. Pattern: shutdown, awaitTermination with timeout, shutdownNow if needed, await again — graceful then forceful.

### Scene `types` (renderer: `types`)

1. Common executor types and when each fits.
2. Fixed thread pool — predictable concurrency for steady server workloads — HTTP handlers, batch workers.
3. Cached thread pool — bursty short tasks, grows and shrinks — risk if tasks never terminate, unbounded growth historically.
4. Single-thread executor — sequential execution, ordered results — event loop style, no concurrent mutation.
5. ScheduledThreadPoolExecutor — delayed and periodic tasks — cron replacement in-process.
6. ForkJoinPool — work-stealing for divide-and-conquer — parallel streams use common pool instance.
7. Virtual thread executors since Java twenty-one — different model, huge concurrency — covered later in series.

### Scene `when_pools` (renderer: `when_pools`)

1. When to use thread pools — server request handling with bounded concurrent work.
2. Background processing — logging pipelines, indexing, email notifications off request thread.
3. Batch jobs with many independent units of work — partition and submit, aggregate with Futures later.
4. When not — trivial one-off background task in a CLI tool — maybe one thread is fine.
5. Always size and monitor — blind Executors.newCachedThreadPool in a server has caused outages.
6. Rejection policy matters when queue is full — CallerRunsPolicy backpressure, AbortPolicy throws.
7. Name your threads via custom ThreadFactory — debugging thread dumps without names is pain.

### Scene `code` (renderer: `code`)

1. Fixed pool, submit tasks, graceful shutdown — production-shaped skeleton.

```java
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class ExecutorDemo {
    public static void main(String[] args) throws InterruptedException {
        ExecutorService pool = Executors.newFixedThreadPool(2);

        pool.submit(() -> System.out.println("Task A on " + Thread.currentThread().getName()));
        pool.submit(() -> System.out.println("Task B on " + Thread.currentThread().getName()));

        pool.shutdown();
        if (!pool.awaitTermination(5, TimeUnit.SECONDS)) {
            pool.shutdownNow();
        }
        System.out.println("Pool stopped");
    }
}
```

2. newFixedThreadPool(2) — at most two workers — tasks queue if both busy.
3. submit schedules Runnable — may run on pool-1-thread-1 or pool-1-thread-2.
4. shutdown stops new submissions — already submitted tasks still run.
5. awaitTermination waits up to five seconds for completion — then shutdownNow if stubborn tasks remain.
6. Never leave pool running at main exit in short-lived apps — hooks help in long-running servers too.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — never calling shutdown — threads leak, JVM hangs on exit or redeploy, zombie process.
3. Two — unbounded queue with fixed pool — memory grows forever if producers outpace consumers.
4. Three — submitting blocking IO tasks to a small CPU-bound pool — everything stalls behind one slow call.
5. Also — ignoring RejectedExecutionException when queue and pool are saturated — silent task loss if not handled.
6. Treat the executor as a managed resource — lifecycle matters as much as JDBC connections.

### Scene `interview` (renderer: `interview`)

1. Interview question — why use ExecutorService over raw Thread?
2. Decouples task logic from thread lifecycle — submit work, pool manages threads.
3. Reuses threads — avoids per-task creation overhead and stack memory churn.
4. Provides bounded concurrency — protects system resources under load spikes.
5. Returns Future for Callable results — composition in later episodes with CompletableFuture.
6. Mention shutdown and awaitTermination — shows production hygiene, not demo-code thinking.
7. Contrast fixed versus cached pools — bounded versus elastic — trade-offs not one-size-fits-all.

### Scene `amplify`

1. Let me press on point 1 a bit harder.
2. Fixed/cached/scheduled pools.
3. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
4. If you cannot explain the failure mode, you do not own the feature yet.
5. Let me press on point 2 a bit harder.
6. shutdown vs shutdownNow.
7. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
8. If you cannot explain the failure mode, you do not own the feature yet.
9. Let me press on point 3 a bit harder.
10. Bounded queues and rejection policies.
11. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
12. If you cannot explain the failure mode, you do not own the feature yet.
13. Let me press on point 4 a bit harder.
14. Always have a failure story.
15. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
16. If you cannot explain the failure mode, you do not own the feature yet.
17. Let me press on point 5 a bit harder.
18. Virtual threads change some defaults later.
19. In practice, this shows up when a teammate asks why a change is risky — you answer with the mechanism, not a slogan.
20. If you cannot explain the failure mode, you do not own the feature yet.

### Scene `handbook_spine`

1. How this maps to the reference handbook mindset:
2. The handbook teaches concept, internal working, mistakes, and interview questions.
3. We are doing the same job in spoken form — compressed for video, but not reduced to headlines.
4. So if a section felt familiar, good: that means the curriculum spine is intact.

### Scene `practice`

1. Mini practice before you go.
2. Pause the video and do this without looking:
3. 1) Say out loud what ExecutorService is for in one sentence.
4. 2) Write the example from memory — approximate is fine.
5. 3) Name one mistake from this episode and how you would catch it in review.
6. That three-step drill turns watching into learning.
### Scene `summary` (renderer: `summary`)

1. ExecutorService = submit tasks, pool runs them on reused threads.
2. Fixed pools for servers; cached for bursty short work with caution.
3. shutdown → awaitTermination → shutdownNow is the shutdown dance.
4. Size from workload; monitor queue depth and rejection.
5. Never leak executors — lifecycle is your responsibility.

### Scene `teaser` (renderer: `teaser`)

1. Pools run tasks. What about tasks that return values?
2. Episode Forty-One — Callable and Future.
3. Typed results, blocking get, and CompletableFuture ahead.
4. See you there.

_Total beats: **102** — expanded for ~8–12 minute conversational delivery (4-minute floor, 15-minute ceiling)._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **40** — *ExecutorService*.
- **Series catalog:** Episode 40 ↔ handbook lesson 40 — *ExecutorService*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **expanded** into a conversational 4–15 minute documentary script with a walked-through code example — not a verbatim paste of handbook prose.
- **Runtime note:** Earlier short-cut narration was too thin (~4 min headline beats). This revision deepens explanation, examples, mistakes, and interview answer structure while staying under ~15 minutes.

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — Explicit Locks → ExecutorService bridge
- **`title`** — episode title card
- **`executor`** — ExecutorService abstraction
- **`pool`** — thread pool mechanics
- **`submit_shutdown`** — submit and shutdown lifecycle
- **`types`** — pool types
- **`when_pools`** — when to use pools
- **`code`** — fixed pool walkthrough
- **`mistakes`** — common mistakes
- **`interview`** — ExecutorService vs raw Thread
- **`summary`** — revision
- **`teaser`** — bridge to Callable and Future
