# Episode 28 — flatMap & Composition

| Field | Value |
|---|---|
| Episode | 28 |
| Title | flatMap & Composition |
| Catalog handbook column | 28 |
| Narration source script | `make_episode_28.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Collectors gave results shape. Now expand elements inside the pipeline.
2. One input can become many outputs — without nested loops.
3. flatMap is map plus flatten — the one-to-many transform.
4. Composition chains small steps into readable pipelines.
5. Today — flatten complexity instead of hiding it in loops.
6. Streams express structure. flatMap expresses expansion.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Eight.
2. flatMap and composition — one-to-many pipelines.

### Scene `flatmap` (renderer: `flatmap`)

1. map transforms one element into one result.
2. flatMap transforms one element into a stream of results.
3. The stream is flattened into the parent pipeline.
4. List of lists becomes a single flat sequence.
5. Optional values become present elements — absent ones drop away.
6. Think expand, then merge — not nested for-each.

### Scene `composition` (renderer: `composition`)

1. Composition means chaining focused operations.
2. Each step does one job — filter, map, flatMap, collect.
3. Read pipelines top to bottom like a sentence.
4. Extract a method when a chain grows hard to name.
5. Good composition favors clarity over cleverness.
6. Small steps compose into big behavior.

### Scene `nested` (renderer: `nested`)

1. Without flatMap, nested structures invite nested loops.
2. Orders with line items. Departments with employees.
3. A map gives you a stream of collections — still nested.
4. flatMap unwraps each inner collection into the outer flow.
5. One pipeline replaces index juggling.
6. Flatten at the right level — not too early, not too late.

### Scene `onetomany` (renderer: `onetomany`)

1. One-to-many shows up everywhere in real domains.
2. Split a sentence into words. Parse CSV fields.
3. Expand a user into their roles or permissions.
4. flatMap with Arrays.stream or Collection.stream is idiomatic.
5. Choose flatMap when the natural result is many, not one.
6. If you only need one, map is simpler.

### Scene `patterns` (renderer: `patterns`)

1. Common patterns worth memorizing.
2. flatMap(Optional::stream) drops empty optionals cleanly.
3. flatMap(Collection::stream) flattens nested collections.
4. flatMap(s -> s.lines()) splits text into lines.
5. distinct and sorted still apply after flattening.
6. Compose terminal collectors at the end — shape stays last.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — using map when flatMap is required — you get Stream of Stream.
3. Two — flattening too eagerly and losing grouping context.
4. Three — giant flatMap lambdas that should be named methods.
5. Also — forgetting that order is preserved in sequential streams.
6. Readable steps beat one opaque flatMap block.

### Scene `interview` (renderer: `interview`)

1. Interview question — map versus flatMap?
2. map — one input, one output element in the stream.
3. flatMap — one input, zero or more outputs, flattened.
4. Give examples — words from a line, items from an order.
5. Mention Optional::stream for filtering absent values.
6. That answer shows you understand stream geometry.

### Scene `teaser` (renderer: `teaser`)

1. Pipelines flatten nicely. Next — parallelism with care.
2. Episode Twenty-Nine — Parallel Streams.
3. When fork-join helps — and when it hurts.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **28** — *flatMap & Composition*.
- **Series catalog:** Episode 28 ↔ handbook lesson 28 — *flatMap & Composition*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Collectors gave results shape. Now expand elements inside the pipeline._
- **`title`** — starts from: _Episode Twenty-Eight._
- **`flatmap`** — starts from: _map transforms one element into one result._
- **`composition`** — starts from: _Composition means chaining focused operations._
- **`nested`** — starts from: _Without flatMap, nested structures invite nested loops._
- **`onetomany`** — starts from: _One-to-many shows up everywhere in real domains._
- **`patterns`** — starts from: _Common patterns worth memorizing._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — map versus flatMap?_
- **`teaser`** — starts from: _Pipelines flatten nicely. Next — parallelism with care._
