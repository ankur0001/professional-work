# Episode 28 — flatMap & Composition

**Cut:** v1 (original)

## Transcript (from captions)

Collectors gave results shape. Now expand elements inside the pipeline. One input can become many outputs — without nested loops. flatMap is map plus flatten — the one-to-many transform.

Composition chains small steps into readable pipelines. Today — flatten complexity instead of hiding it in loops. Streams express structure. flatMap expresses expansion. Episode Twenty-Eight.

flatMap and composition — one-to-many pipelines. map transforms one element into one result. flatMap transforms one element into a stream of results. The stream is flattened into the parent pipeline.

List of lists becomes a single flat sequence. Optional values become present elements — absent ones drop away. Think expand, then merge — not nested for-each. Composition means chaining focused operations.

Each step does one job — filter, map, flatMap, collect. Read pipelines top to bottom like a sentence. Extract a method when a chain grows hard to name. Good composition favors clarity over cleverness.

Small steps compose into big behavior. Without flatMap, nested structures invite nested loops. Orders with line items. Departments with employees. A map gives you a stream of collections — still nested.

flatMap unwraps each inner collection into the outer flow. One pipeline replaces index juggling. Flatten at the right level — not too early, not too late. One-to-many shows up everywhere in real domains.

Split a sentence into words. Parse CSV fields. Expand a user into their roles or permissions. flatMap with Arrays.stream or Collection.stream is idiomatic. Choose flatMap when the natural result is many, not one.

If you only need one, map is simpler. Common patterns worth memorizing. flatMap(Optional::stream) drops empty optionals cleanly. flatMap(Collection::stream) flattens nested collections.

flatMap(s -> s.lines()) splits text into lines. distinct and sorted still apply after flattening. Compose terminal collectors at the end — shape stays last. Three common mistakes. One — using map when flatMap is required — you get Stream of Stream.

Two — flattening too eagerly and losing grouping context. Three — giant flatMap lambdas that should be named methods. Also — forgetting that order is preserved in sequential streams.

Readable steps beat one opaque flatMap block. Interview question — map versus flatMap? map — one input, one output element in the stream. flatMap — one input, zero or more outputs, flattened.

Give examples — words from a line, items from an order. Mention Optional::stream for filtering absent values. That answer shows you understand stream geometry. Pipelines flatten nicely. Next — parallelism with care.

Episode Twenty-Nine — Parallel Streams. When fork-join helps — and when it hurts. See you there.
