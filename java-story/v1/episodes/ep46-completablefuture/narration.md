# Episode 46 — CompletableFuture

**Cut:** v1 (original)

## Transcript (from captions)

Episode Forty-One introduced CompletableFuture — supplyAsync and a quick chain. Production async code needs richer composition and solid error handling. thenApply transforms a result synchronously on the completion thread.

thenCompose flattens nested futures — the async equivalent of flatMap. allOf waits for every future — anyOf for the first to complete. Today — deep dive into composing and recovering CompletableFuture pipelines.

Episode Forty-Six. CompletableFuture Deep Dive. thenApply maps the result when the previous stage completes. Runs on the same executor as the completing thread by default. thenApplyAsync runs the mapping function on a specified executor.

Use for pure transformations — parse JSON, format strings, map values. Returns a new CompletableFuture of the transformed type. Chain multiple thenApply calls — each waits for the prior stage.

thenCompose chains when the next step itself returns a CompletableFuture. Flattens CompletableFuture of CompletableFuture into a single future. Without compose you nest futures — blocking get inside thenApply.

thenComposeAsync runs the composing function on an executor. Essential for dependent async calls — fetch then save then notify. Think flatMap for futures — compose, do not nest. allOf accepts an array or collection of CompletableFuture instances.

Returns CompletableFuture of Void — completion means all inputs finished. Join individual futures after allOf completes to collect results. anyOf completes when any one input future completes.

Use allOf for parallel fan-out — aggregate when every branch is done. anyOf for racing alternatives — first successful or fastest response wins. exceptionally recovers from failure — returns a fallback value.

handle receives both result and exception — unified success and failure path. whenComplete is a side-effect hook — does not transform the result. completeExceptionally manually fails a future you created.

orTimeout and completeOnTimeout add deadline semantics in Java 9+. Never swallow exceptions — log in whenComplete, recover in handle. When to use each combinator. thenApply — synchronous transform of a completed value.

thenCompose — next step is itself async — dependent chain. allOf — parallel independent work — wait for all. exceptionally or handle — explicit failure recovery. Avoid blocking get in callbacks — keep the pipeline non-blocking.

Three common mistakes. One — thenApply when the lambda returns a Future — use thenCompose. Two — ignoring exceptions — pipeline fails silently downstream. Three — blocking get inside thenApply — stalls the executor.

Also — allOf without collecting individual results — Void only signals done. Compose async work — do not turn CompletableFuture back into blocking code. Interview question — thenApply versus thenCompose?

thenApply — function returns a plain value — map the result. thenCompose — function returns CompletableFuture — flatten nested futures. thenApply nests CompletableFuture of CompletableFuture — compose flattens.

allOf waits for all — anyOf for first completion. handle and exceptionally for unified error handling in pipelines. CompletableFuture defaults to ForkJoinPool.commonPool. Episode Forty-Seven — ForkJoinPool and Work-Stealing.

Parallel decomposition, recursive tasks, and the common pool. See you there.
