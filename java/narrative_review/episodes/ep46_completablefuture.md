# Episode 46 — CompletableFuture

| Field | Value |
|---|---|
| Episode | 46 |
| Title | CompletableFuture |
| Catalog handbook column | 46 |
| Narration source script | `make_episode_46.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Episode Forty-One introduced CompletableFuture — supplyAsync and a quick chain.
2. Production async code needs richer composition and solid error handling.
3. thenApply transforms a result synchronously on the completion thread.
4. thenCompose flattens nested futures — the async equivalent of flatMap.
5. allOf waits for every future — anyOf for the first to complete.
6. Today — deep dive into composing and recovering CompletableFuture pipelines.

### Scene `title` (renderer: `title`)

1. Episode Forty-Six.
2. CompletableFuture Deep Dive.

### Scene `then_apply` (renderer: `then_apply`)

1. thenApply maps the result when the previous stage completes.
2. Runs on the same executor as the completing thread by default.
3. thenApplyAsync runs the mapping function on a specified executor.
4. Use for pure transformations — parse JSON, format strings, map values.
5. Returns a new CompletableFuture of the transformed type.
6. Chain multiple thenApply calls — each waits for the prior stage.

### Scene `then_compose` (renderer: `then_compose`)

1. thenCompose chains when the next step itself returns a CompletableFuture.
2. Flattens CompletableFuture of CompletableFuture into a single future.
3. Without compose you nest futures — blocking get inside thenApply.
4. thenComposeAsync runs the composing function on an executor.
5. Essential for dependent async calls — fetch then save then notify.
6. Think flatMap for futures — compose, do not nest.

### Scene `all_of` (renderer: `all_of`)

1. allOf accepts an array or collection of CompletableFuture instances.
2. Returns CompletableFuture of Void — completion means all inputs finished.
3. Join individual futures after allOf completes to collect results.
4. anyOf completes when any one input future completes.
5. Use allOf for parallel fan-out — aggregate when every branch is done.
6. anyOf for racing alternatives — first successful or fastest response wins.

### Scene `exception_handling` (renderer: `exception_handling`)

1. exceptionally recovers from failure — returns a fallback value.
2. handle receives both result and exception — unified success and failure path.
3. whenComplete is a side-effect hook — does not transform the result.
4. completeExceptionally manually fails a future you created.
5. orTimeout and completeOnTimeout add deadline semantics in Java 9+.
6. Never swallow exceptions — log in whenComplete, recover in handle.

### Scene `when_compose` (renderer: `when_compose`)

1. When to use each combinator.
2. thenApply — synchronous transform of a completed value.
3. thenCompose — next step is itself async — dependent chain.
4. allOf — parallel independent work — wait for all.
5. exceptionally or handle — explicit failure recovery.
6. Avoid blocking get in callbacks — keep the pipeline non-blocking.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — thenApply when the lambda returns a Future — use thenCompose.
3. Two — ignoring exceptions — pipeline fails silently downstream.
4. Three — blocking get inside thenApply — stalls the executor.
5. Also — allOf without collecting individual results — Void only signals done.
6. Compose async work — do not turn CompletableFuture back into blocking code.

### Scene `interview` (renderer: `interview`)

1. Interview question — thenApply versus thenCompose?
2. thenApply — function returns a plain value — map the result.
3. thenCompose — function returns CompletableFuture — flatten nested futures.
4. thenApply nests CompletableFuture of CompletableFuture — compose flattens.
5. allOf waits for all — anyOf for first completion.
6. handle and exceptionally for unified error handling in pipelines.

### Scene `teaser` (renderer: `teaser`)

1. CompletableFuture defaults to ForkJoinPool.commonPool.
2. Episode Forty-Seven — ForkJoinPool and Work-Stealing.
3. Parallel decomposition, recursive tasks, and the common pool.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **46** — *CompletableFuture*.
- **Series catalog:** Episode 46 ↔ handbook lesson 46 — *CompletableFuture*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Episode Forty-One introduced CompletableFuture — supplyAsync and a quick chain._
- **`title`** — starts from: _Episode Forty-Six._
- **`then_apply`** — starts from: _thenApply maps the result when the previous stage completes._
- **`then_compose`** — starts from: _thenCompose chains when the next step itself returns a CompletableFuture._
- **`all_of`** — starts from: _allOf accepts an array or collection of CompletableFuture instances._
- **`exception_handling`** — starts from: _exceptionally recovers from failure — returns a fallback value._
- **`when_compose`** — starts from: _When to use each combinator._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — thenApply versus thenCompose?_
- **`teaser`** — starts from: _CompletableFuture defaults to ForkJoinPool.commonPool._
