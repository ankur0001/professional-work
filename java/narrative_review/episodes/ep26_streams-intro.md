# Episode 26 — Streams Intro

| Field | Value |
|---|---|
| Episode | 26 |
| Title | Streams Intro |
| Catalog handbook column | 26 |
| Narration source script | `make_episode_26.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Sorting orders a collection. Streams transform how you process one.
2. Instead of nested loops everywhere — declare a pipeline.
3. Source, intermediate operations, terminal operation.
4. Lazy until it needs to run. Expressive when the problem fits.
5. Today — the mental model that makes Streams useful.
6. Data as a pipeline — not a pile of index variables.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Six.
2. Streams introduction — pipelines over data.

### Scene `idea` (renderer: `idea`)

1. A Stream is not a new collection type.
2. It is a sequence of elements supporting aggregate operations.
3. You build a pipeline — then a terminal operation triggers computation.
4. Streams are single-use. Consume once.
5. They can come from collections, arrays, generators, or I/O wrappers.
6. Think recipe first — result second.

### Scene `ops` (renderer: `ops`)

1. Operations split into two families.
2. Intermediate — filter, map, flatMap, sorted, distinct — return a stream.
3. Terminal — collect, reduce, forEach, count, anyMatch — produce a result or side effect.
4. Without a terminal operation, nothing useful happens.
5. Keep intermediate steps free of surprising mutation.
6. Readable pipelines beat clever one-liners.

### Scene `lazy` (renderer: `lazy`)

1. Laziness is the key performance idea.
2. Intermediate operations record what to do — they do not run yet.
3. A terminal operation pulls data through the pipeline.
4. anyMatch can stop early. limit can bound work.
5. That is why filter then findFirst can skip unused elements.
6. Use laziness — do not fight it with eager side effects mid-pipeline.

### Scene `collect` (renderer: `collect`)

1. collect is how most pipelines finish.
2. Collectors.toList and toSet materialize results.
3. toMap builds maps carefully — watch duplicate keys.
4. groupingBy clusters elements by a classifier.
5. joining builds strings without manual StringBuilder noise.
6. Choose a collector that matches the shape you need next.

### Scene `when` (renderer: `when`)

1. When Streams shine.
2. Transform and filter chains that would be noisy loops.
3. Pipelines that read like the business rule.
4. Optional parallelism later — after you measure.
5. When not — heavy mutable accumulation that is clearer as a for-loop.
6. Clarity first. Streams are a tool, not a purity contest.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — reusing a stream after it was consumed.
3. Two — sneaking side effects into map instead of keeping transformations pure.
4. Three — sprinkling parallel without evidence it helps.
5. Also — giant pipelines nobody can debug at a breakpoint.
6. Good stream code is still boringly clear.

### Scene `interview` (renderer: `interview`)

1. Interview question — what is a Stream, and why does laziness matter?
2. A pipeline over elements with intermediate and terminal operations.
3. Laziness delays work until a terminal operation — enabling short-circuiting.
4. Mention collect as the common way to materialize results.
5. Contrast with collections — streams do not store elements themselves.
6. That answer shows conceptual understanding.

### Scene `teaser` (renderer: `teaser`)

1. Pipelines are in place. Next — collectors with real shape.
2. Episode Twenty-Seven — Stream Collectors.
3. Grouping, partitioning, and downstream collectors.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **26** — *Streams Intro*.
- **Series catalog:** Episode 26 ↔ handbook lesson 26 — *Streams Intro*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Sorting orders a collection. Streams transform how you process one._
- **`title`** — starts from: _Episode Twenty-Six._
- **`idea`** — starts from: _A Stream is not a new collection type._
- **`ops`** — starts from: _Operations split into two families._
- **`lazy`** — starts from: _Laziness is the key performance idea._
- **`collect`** — starts from: _collect is how most pipelines finish._
- **`when`** — starts from: _When Streams shine._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — what is a Stream, and why does laziness matter?_
- **`teaser`** — starts from: _Pipelines are in place. Next — collectors with real shape._
