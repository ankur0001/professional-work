# Episode 63 — Object Layout

| Field | Value |
|---|---|
| Episode | 63 |
| Title | Object Layout |
| Catalog handbook column | 63 |
| Spoken form | Continuous spoken lesson (narrative chain of thought) |
| Runtime target | **4–15 minutes** (aim ~10–12) |

## Full narration

Suppose a teammate says, "This class only has a byte field, so each instance is basically one byte." Then they multiply by ten million instances, glance at the heap, and wonder why reality refused the arithmetic. Episode Sixty-Two taught us to measure. Object layout is one reason measurements surprise people who estimate memory by field sizes alone.

Every object pays for a header. On HotSpot, that header carries identity and metadata the runtime needs — mark-related information, class pointer information, and related machinery that varies with JVM version and configuration. You do not need every bit field to learn the lesson: a "tiny" object is never only its fields.

```java
// a 'tiny' object still pays for header + padding
class Tiny { byte b; }
```

`Tiny` looks like one byte of payload. Alignment and padding round the instance size up to the platform's object alignment — commonly eight bytes on many configurations. One byte of business data can sit inside a much larger footprint. Create millions of `Tiny` instances and you have paid for millions of headers and padding gaps. Arrays add their own story: array headers include length, then elements, still subject to alignment. A `byte[]` is not simply "length bytes" in retained-size accounting. Empty arrays are not free either — thousands of empty collections "just in case" pay header taxes repeatedly. Sometimes a shared empty singleton or null meaning empty is denser — with care for mutability.

References complicate the arithmetic further. A field of type `String` is not "the string's characters inside your object." It is a reference — a pointer-sized slot, often compressed — plus whatever the `String` itself costs elsewhere. Ignoring reference costs is how people underestimate graphs of wrappers, tree nodes, and DTOs. Compressed oops use narrower references on heaps in a certain size range, trading a little decode work for denser memory. On many heaps, references cost less than a full 64-bit pointer — which is also why whiteboard "pointer is eight bytes" estimates can be wrong either way. When you need precision, measure.

Field order can matter for packing. The JVM lays out fields with alignment rules; reordering source fields can change padding gaps. This is real — and a footgun for premature obsession. Algorithms, data-structure choice, and retention policy usually dominate before field packing saves you. Use layout knowledge to interpret heap numbers and to decide when many tiny objects should become denser representations — arrays of primitives, fewer wrappers, flyweight-style sharing — not as an excuse to rearrange fields while an unbounded cache still grows.

Bring `Tiny` into a product decision. A telemetry pipeline boxes every metric sample into a small object with a few fields and a reference to a name string. Ten million samples later, headers and references dominate. The fix might be a columnar structure — parallel arrays of primitives and a dictionary for names — not a field reorder on the small class. Layout knowledge showed why the heap exploded; data representation fixed it.

So why is a tiny object bigger than expected? Headers, alignment, and references add overhead. Say that in an interview. Then say what you would do next: measure retained sizes with a heap dump or instrumentation, ask whether the design needs millions of tiny objects at all, and only then worry about packing. Estimating by field sizes only, ignoring reference costs, and layout-obsessing before algorithms are the three mistakes this episode exists to prevent.

Object layout makes the heap's accounting honest. But pauses are not only about how big objects are. Sometimes latency appears when the JVM needs all threads to reach a safe state before a VM operation. Those rendezvous points are safepoints — and Episode Sixty-Four explains why time-to-safepoint can show up as mysterious latency even when "GC was slow" is not the whole story.

## Source attribution

Reference: `Java_JVM_Handbook_GPT55__1_.html` — Object Layout (Episode 63).

Narration technique: tiny-object myth → header + Tiny example → alignment/arrays → reference costs + compressed oops → field order vs premature obsession → telemetry product decision → interview woven → bridge to safepoints.

Teaching points preserved: object header; alignment/padding; compressed oops; array headers; field order packing.
