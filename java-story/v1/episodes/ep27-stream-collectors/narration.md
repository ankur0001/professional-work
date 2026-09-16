# Episode 27 — Stream Collectors

**Cut:** v1 (original)

## Transcript (from captions)

Streams build pipelines. Collectors decide the shape of the answer. List, Set, Map, string, summary — same stream, different endings. groupingBy and partitioningBy turn flat data into structure.

Downstream collectors nest work inside each group. Today — finish pipelines with intent, not afterthoughts. Collect is not dump. Collect is design. Episode Twenty-Seven. Stream Collectors — shaping results.

Start with the basics in Collectors. toList and toSet materialize elements. toMap needs a key function, a value function, and often a merge function. Duplicate keys without a merge function throw — loudly.

joining builds delimited strings without manual StringBuilder noise. Pick the collector that matches the type you need next. groupingBy is the workhorse for classification. A classifier function produces keys.

By default each key maps to a List of matching elements. Orders by region. Users by status. Events by day. You get a Map whose values are groups — ready for reports. Think pivot table — expressed as a pipeline.

partitioningBy is groupingBy for a boolean question. Predicate true goes one side. False the other. The result is Map of Boolean to the grouped values. Active versus inactive. Valid versus invalid. Paid versus unpaid.

Two buckets — when two is exactly the model. Do not use it when you really needed many keys. Downstream collectors avoid second passes. groupingBy with counting gives sizes per key.

summingInt and averagingDouble summarize in place. mapping then toSet reshapes each group. collectingAndThen applies a finisher — like making the map unmodifiable. Nest the work. Keep the pipeline honest.

Beyond grouping — reducing and summarizing. reducing folds with an identity and an operator. summarizingInt returns count, sum, min, max, and average together. teeing runs two collectors and merges their results — Java sixteen and later.

Use summaries when dashboards need several stats at once. Collectors are a toolbox — learn the shapes, not every overload by heart. Three common mistakes. One — toMap without a merge function when duplicates exist.

Two — mutating shared accumulators and hoping parallel collect survives. Three — groupingBy then a manual loop that a downstream collector already covers. Also — assuming toList is always unmodifiable — know your Java version.

Clear collectors beat clever post-processing. Interview question — groupingBy versus partitioningBy? groupingBy — many keys from a classifier function. partitioningBy — boolean predicate, always two sides.

Mention downstream collectors for counting or summing inside groups. Give a domain example — orders by region versus paid versus unpaid. That answer shows practical stream fluency. Results have shape. Next — expanding elements inside the pipeline.

Episode Twenty-Eight — flatMap and composition. One-to-many transforms without nested collections mess. See you there.
