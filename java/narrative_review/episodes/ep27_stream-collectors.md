# Episode 27 — Stream Collectors

| Field | Value |
|---|---|
| Episode | 27 |
| Title | Stream Collectors |
| Catalog handbook column | 27 |
| Narration source script | `make_episode_27.py` |
| Spoken form | Short documentary beats (Chatterbox / Kokoro render) |

## Full narration (spoken beats)

### Scene `hook` (renderer: `hook`)

1. Streams build pipelines. Collectors decide the shape of the answer.
2. List, Set, Map, string, summary — same stream, different endings.
3. groupingBy and partitioningBy turn flat data into structure.
4. Downstream collectors nest work inside each group.
5. Today — finish pipelines with intent, not afterthoughts.
6. Collect is not dump. Collect is design.

### Scene `title` (renderer: `title`)

1. Episode Twenty-Seven.
2. Stream Collectors — shaping results.

### Scene `basics` (renderer: `basics`)

1. Start with the basics in Collectors.
2. toList and toSet materialize elements.
3. toMap needs a key function, a value function, and often a merge function.
4. Duplicate keys without a merge function throw — loudly.
5. joining builds delimited strings without manual StringBuilder noise.
6. Pick the collector that matches the type you need next.

### Scene `grouping` (renderer: `grouping`)

1. groupingBy is the workhorse for classification.
2. A classifier function produces keys.
3. By default each key maps to a List of matching elements.
4. Orders by region. Users by status. Events by day.
5. You get a Map whose values are groups — ready for reports.
6. Think pivot table — expressed as a pipeline.

### Scene `partition` (renderer: `partition`)

1. partitioningBy is groupingBy for a boolean question.
2. Predicate true goes one side. False the other.
3. The result is Map of Boolean to the grouped values.
4. Active versus inactive. Valid versus invalid. Paid versus unpaid.
5. Two buckets — when two is exactly the model.
6. Do not use it when you really needed many keys.

### Scene `downstream` (renderer: `downstream`)

1. Downstream collectors avoid second passes.
2. groupingBy with counting gives sizes per key.
3. summingInt and averagingDouble summarize in place.
4. mapping then toSet reshapes each group.
5. collectingAndThen applies a finisher — like making the map unmodifiable.
6. Nest the work. Keep the pipeline honest.

### Scene `reduce` (renderer: `reduce`)

1. Beyond grouping — reducing and summarizing.
2. reducing folds with an identity and an operator.
3. summarizingInt returns count, sum, min, max, and average together.
4. teeing runs two collectors and merges their results — Java sixteen and later.
5. Use summaries when dashboards need several stats at once.
6. Collectors are a toolbox — learn the shapes, not every overload by heart.

### Scene `mistakes` (renderer: `mistakes`)

1. Three common mistakes.
2. One — toMap without a merge function when duplicates exist.
3. Two — mutating shared accumulators and hoping parallel collect survives.
4. Three — groupingBy then a manual loop that a downstream collector already covers.
5. Also — assuming toList is always unmodifiable — know your Java version.
6. Clear collectors beat clever post-processing.

### Scene `interview` (renderer: `interview`)

1. Interview question — groupingBy versus partitioningBy?
2. groupingBy — many keys from a classifier function.
3. partitioningBy — boolean predicate, always two sides.
4. Mention downstream collectors for counting or summing inside groups.
5. Give a domain example — orders by region versus paid versus unpaid.
6. That answer shows practical stream fluency.

### Scene `teaser` (renderer: `teaser`)

1. Results have shape. Next — expanding elements inside the pipeline.
2. Episode Twenty-Eight — flatMap and composition.
3. One-to-many transforms without nested collections mess.
4. See you there.

_Total beats: **54** across **10** scenes._

## Source attribution (reference document)

Reference document (user attachment): **`Java_JVM_Handbook_GPT55__1_.html`** — *Java & JVM Handbook — 80 Lessons*.

- **Primary handbook lesson:** Lesson **27** — *Stream Collectors*.
- **Series catalog:** Episode 27 ↔ handbook lesson 27 — *Stream Collectors*.
- **How content was used:** The handbook provided the **topic outline and teaching points**. Spoken lines were **rewritten** into short documentary beats matched to motion-graphics scenes (per user guidance: own narration synced to presentation; handbook as reference, not a script to read aloud).

- Full handbook HTML is **not checked into git** (original upload was ephemeral). Attribution for this episode is by **lesson title / topic** from the recovered TOC and the series catalog.

### Scene ↔ curriculum intent

- **`hook`** — starts from: _Streams build pipelines. Collectors decide the shape of the answer._
- **`title`** — starts from: _Episode Twenty-Seven._
- **`basics`** — starts from: _Start with the basics in Collectors._
- **`grouping`** — starts from: _groupingBy is the workhorse for classification._
- **`partition`** — starts from: _partitioningBy is groupingBy for a boolean question._
- **`downstream`** — starts from: _Downstream collectors avoid second passes._
- **`reduce`** — starts from: _Beyond grouping — reducing and summarizing._
- **`mistakes`** — starts from: _Three common mistakes._
- **`interview`** — starts from: _Interview question — groupingBy versus partitioningBy?_
- **`teaser`** — starts from: _Results have shape. Next — expanding elements inside the pipeline._
