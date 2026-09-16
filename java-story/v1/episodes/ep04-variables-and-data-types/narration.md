# Episode 04 — Variables and Data Types

**Cut:** v1 (original)

## Transcript (from captions)

In Episode Three, we mapped packages and classes. Now — what actually lives inside those fields and methods? Variables name values. Types decide what is valid. Pick the wrong type… and production pays for it — overflow, nulls, money bugs.

Episode Four. Variables and Data Types — primitives, references, and real choices. Java has two families of types. Keep this picture. On the left — primitives. Raw values. Fast. Never null.

On the right — references. They point to objects on the heap. Assignment behaves differently in each family — that is why this split matters. That mental model everything else builds on.

Eight primitives — memorize the common ones first. int for whole numbers. long for bigger IDs and timestamps. boolean for true or false. double for binary floating point. byte, short, char, float exist too — useful, but rarer in day-to-day code.

Primitives hold the value itself — not a pointer. And they cannot be null. That alone prevents a whole class of bugs. Picture memory. int count equals ten — the value sits in the local frame.

Order order equals new Order — the variable holds a reference. The real object lives on the heap. Assignment copies the primitive… or copies the reference — not the whole object. final blocks reassignment of that variable — it does not freeze the object inside.

Production gotcha — money. Never store currency in double. Binary floating point cannot represent many decimals exactly. Prefer long minor units — cents — or a Money value type. Use BigDecimal when you need precise decimal math and rounding rules.

Architects standardize this early — because fixing money types later is expensive. Wrappers look similar — Integer, Long, Boolean. They are objects. They can be null. They cost more memory.

Autoboxing hides conversions — and can hide NullPointerExceptions too. A List of Integer can thrash the heap versus an int array. Prefer primitives in hot paths. Use wrappers when null is a real signal.

Three common mistakes. One — double for money. Rounding bugs wait quietly. Two — ignoring integer overflow on big counters. Three — assuming final means deep immutability. It only blocks reassignment.

Bonus trap — overusing String for every domain idea. Prefer typed values when meaning matters. Interview question — primitive versus wrapper? Answer on screen. Primitive — value, non-null, compact.

Wrapper — object, nullable, overhead, autoboxing risk. Then mention — why avoid double for money. That lands the offer-level detail. You now know how Java stores meaning. Next — operators.

Plus, compare, and, or — and the traps that break equality checks. Episode Five. See you there.
