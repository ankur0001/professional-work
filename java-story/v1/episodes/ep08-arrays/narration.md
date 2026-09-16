# Episode 08 — Arrays

**Cut:** v1 (original)

## Transcript (from captions)

Methods package behavior. Arrays package many values. An array is fixed-size, indexed, and homogeneous — same type in every slot. Arrays are objects in Java, with special syntax and fast indexed access.

They underpin collections, buffers, and performance-sensitive code. Get the mental model right — index, length, bounds. Episode Eight. Arrays — fixed size, indexed access, and off-by-one traps.

Declaration looks like this. int scores equals new int of five. Length is five. Valid indices are zero through four. Remember — zero-based indexing. The last index is length minus one.

Once created, the length never grows. Fixed size means fixed size. If you need growth — that is a list conversation, coming soon. Access is by index. scores bracket zero equals ninety. Read and write in constant time.

Ask for scores bracket five — ArrayIndexOutOfBoundsException. Off-by-one bugs love loops that use less-than-or-equal when they should use less-than. Practice saying length minus one out loud until it sticks.

Multidimensional arrays are arrays of arrays. int bracket bracket grid — rows that each hold a row array. Rows can even have different lengths — jagged arrays. Do not assume one flat contiguous block the way C sometimes does.

When you need a true matrix library — use a library. Arrays stay simple. When do you choose arrays versus ArrayList? Arrays — fixed size, simple, very fast indexed access. ArrayList — grows, richer API, clearer for most application code.

Prefer collections when intent is a growing list of domain objects. Prefer arrays for tight buffers, primitives, and interoperability. Choose the structure that matches how the size changes.

Three common mistakes. One — off-by-one indexing in loops. Two — exposing an internal array from a getter — callers can mutate your guts. Three — returning huge arrays from APIs when a stream or page would do.

Also — using Object arrays when a typed collection communicates intent better. Interview question — are arrays objects in Java? Yes — they live on the heap and have a length field. But they have special syntax — brackets — and covariant quirks to know later.

Length for arrays. Size for lists. Do not mix the words. Zero-based indexing is non-negotiable. Many values, fixed slots. Next — text. Episode Nine — Strings. Immutability, equals, and careful construction.

See you there.
